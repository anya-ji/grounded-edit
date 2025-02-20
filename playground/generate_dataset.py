'''
Input: initial code {c'}, render {r'}, target render {r}
PROMPT1: edit descriptions {[d0,d1,...]}: what's one thing i need to do to change from {r_0} to {r}?
for each edit description {d}:
    PROMPT2: code edit diff {ed}: what's the code change to do this?
Output: add to dataset
    - c', d, ed
    - (for testing viz) edit(c', ed), render(c')
'''

import argparse
import os 
import subprocess
from models import *
import logging
import datetime

def logger_setup():
    timestamp = datetime.datetime.now().strftime("%m%d_%H%M")
    log_filename = f"./logs/log_{timestamp}.log"
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(log_filename, mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger

def save_text(current_iter_folder, file_name, text):
    with open(os.path.join(current_iter_folder, file_name), "w") as f:
        f.write(text)

def main():
    logger = logger_setup()
    compare_instruction_file = 'prompt/compare_instruction.txt'
    edit_instruction_file = 'prompt/edit_instruction.txt'
    # Read the instruction template
    with open(compare_instruction_file, "r") as f:
        compare_instruction = f.read()
    with open(edit_instruction_file, "r") as f:
        edit_instruction_template = f.read()
    # Each example in data
    folders = sorted(os.listdir(args.data_dir))
    total = len(folders)
    for idx, folder in enumerate(folders):
        if args.test:
            if idx!=args.test-1: # only test the specified example
                continue
        if args.start_idx:
            if idx<args.start_idx-1: # start from an example index
                continue
        logger.info(f'---{folder} ({idx+1}/{total})---')
        print(f'{folder} ({idx+1}/{total})')
        example_root = os.path.join(args.data_dir, folder)
        init_render_path = os.path.join(example_root, "init/render.png")

        if not os.path.exists(init_render_path): # skip over no init render examples
            continue
        
        # PROMPT 1: NL description of change
        target_image_path = os.path.join(example_root, "target/render.png")
        result = generate_edit_description(args.model, compare_instruction, target_image_path, init_render_path)

        result_folder = os.path.join(example_root, args.model)
        os.makedirs(result_folder, exist_ok=True)
        
        save_text(result_folder, "full_edit_description.txt", result)
        edit_descs = parse_edit_description(args.model, result)
        logger.info(f"Generated {len(edit_descs)} suggestions")
        
        # Loop over each edit description
        for desc_idx, edit_description in enumerate(edit_descs):
            current_edit_folder =  os.path.join(result_folder, f"edit_{desc_idx}")
            os.makedirs(current_edit_folder, exist_ok=True)
            save_text(current_edit_folder, "edit_description.txt", edit_description)

            # Add the code to instruction
            init_code_path = os.path.join(example_root, "init/code.py")
            with open(init_code_path, "r") as f:
                code = f.read()
            edit_instruction = edit_instruction_template.replace('[CODE]', code)

            # PROMPT 2: Generate code edit
            tries_left = 2
            while tries_left > 0:
                logger.info(f'Code edit generation for edit {desc_idx}: {tries_left} retries left')
                edit_instruction = edit_instruction.replace('[DESCRIPTION]', edit_description)
                result = generate_code_edit(args.model, edit_instruction, init_render_path)
                code_edit = parse_code(args.model, result)
                save_text(current_edit_folder, "code.py", code_edit)

                # Save diff file
                with open(os.path.join(current_edit_folder, "diff.patch"), 'w') as f:
                    result = subprocess.Popen([
                        "diff", "-u", init_code_path,
                        os.path.join(current_edit_folder, "code.py")
                    ], stdout=f, text=True).communicate()

                # Render the generated code
                try:
                    subprocess.run(["python", "code.py"], capture_output=True, text=True, check=True, cwd=current_edit_folder)
                    pptx_path = os.path.join(current_edit_folder, 'render.pptx')
                    subprocess.run(["unoconv", "-f", "png", pptx_path])
                    break
                except subprocess.CalledProcessError as e:
                    error_msg = f"Failed to execute code for edit {desc_idx}: " + e.stderr
                    if tries_left == 1:
                        save_text(current_edit_folder, "code_error.txt", error_msg)
                tries_left -= 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate training data')
    parser.add_argument("--data_dir", type=str, required=True, help="Path to data directory.")
    parser.add_argument("--model", type=str, required=True, help="Model to use. Options: llava-ov, gpt-4o.")
    parser.add_argument("--start_idx", type=int, required=False, help="Start from an index (used when generation is preempted).")
    parser.add_argument("--test", type=int, required=False, help="Test a specific example.")
    
    args = parser.parse_args()

    main()