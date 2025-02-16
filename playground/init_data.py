'''
Initialize training set with:
/target
    /render.png: target render
/media: parsed images from slides
/init
    /code.py: base code
    /render.png: render of base code
'''

import os
import shutil
import re
import subprocess

def copy_folders():
    # copy over target and media
    source_base = "../SlidesAgent/slidesbench/examples"
    destination_base = "./data"

    for example_name in os.listdir(source_base):
        example_path = os.path.join(source_base, example_name)
        if os.path.isdir(example_path):
            for example_slide in os.listdir(example_path):
                slide_path = os.path.join(example_path, example_slide)
                if os.path.isdir(slide_path):
                    new_dir = os.path.join(destination_base, f"{example_name}_{example_slide}")
                    media_source = os.path.join(slide_path, "media")
                    slide_source = os.path.join(slide_path, "slide.png")
                    media_dest = os.path.join(new_dir, "media")
                    slide_dest = os.path.join(new_dir, "target", "render.png")

                    os.makedirs(media_dest, exist_ok=True)
                    os.makedirs(os.path.dirname(slide_dest), exist_ok=True)

                    # Copy media folder
                    if os.path.exists(media_source):
                        shutil.copytree(media_source, media_dest, dirs_exist_ok=True)

                    # Copy slide.png file
                    if os.path.exists(slide_source):
                        shutil.copy(slide_source, slide_dest)

def generate_init_code():
    # generate initial code and copy to /init
    base_dir = "../SlidesAgent/generate"
    os.chdir(base_dir)
    destination_base = "../../playground/data"
    examples_dir = "./examples"

    example_names = os.listdir("../slidesbench/examples")
    print(example_names)
    
    for example_name in example_names:
        example_path = os.path.join(examples_dir, example_name)
        os.makedirs(example_path, exist_ok=True)
        cmd = ["python", "create_slide_deck.py", "--slide_deck", example_name, "--setting", "sufficient"]
        subprocess.run(cmd, check=True)
        for example_slide in os.listdir(example_path):
            slide_path = os.path.join(example_path, example_slide)
            new_dir = os.path.join(destination_base, f"{example_name}_{example_slide}", "init")
            os.makedirs(new_dir, exist_ok=True)
            code_source = os.path.join(slide_path, "gpt_4o.py")
            render_source = os.path.join(slide_path, "gpt_4o.png")
            code_dest = os.path.join(new_dir, "code.py")
            render_dest = os.path.join(new_dir, "render.png")

            with open(code_source, "r", encoding="utf-8") as file:
                content = file.read()

            # Replace image paths
            pattern = r'"../slidesbench/examples/(?P<example_name>[^/]+)/(?P<example_slide>[^/]+)/media/(?P<media_name>[^"]+)\.jpg"'
            replacement = r'"../../media/\g<media_name>.jpg"'
            content = re.sub(pattern, replacement, content)

            # Replace presentation save path
            content = re.sub(
                r'presentation\.save\(\s*".*?"\s*\)',
                r'presentation.save("render.pptx")',
                content
            )

            with open(code_dest, "w", encoding="utf-8") as file:
                file.write(content)
            if os.path.exists(render_source):
                shutil.copy(render_source, render_dest)

if __name__ == "__main__":
    # copy_folders()
    generate_init_code()