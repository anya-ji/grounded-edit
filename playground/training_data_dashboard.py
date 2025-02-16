import streamlit as st

import os
import glob

def get_iterations(example_path):
    """Get all iteration directories (iter_0 to iter_x) for an example."""
    iterations = sorted(glob.glob(os.path.join(example_path, 'iter_*')))
    return iterations

def read_text_file(filepath):
    """Read text from a file if it exists."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def display_example(example_path, i, total, model):
    """Display images and text for an example."""
    st.header(f"{i}/{total}: {os.path.basename(example_path)}")
    cols = st.columns(2)
    
    # Target image
    target_image = os.path.join(example_path, "target/render.png")
    if os.path.exists(target_image):
        cols[0].image(target_image, caption="Target", width=500)
    
    # Init image and code
    init_image = os.path.join(example_path, "init/render.png")
    init_code = read_text_file(os.path.join(example_path, "init/code.py"))

    with cols[1].expander("code"):
        st.code(init_code, language='python')
    if os.path.exists(init_image):
        cols[1].image(init_image, caption="Init", width=450)
            
    
    # Iterate over iter_x directories
    iterations = get_iterations(example_path)
    for iter_path in iterations:
        iter_name = os.path.basename(iter_path)
        iter_image = os.path.join(iter_path, f"{model}/render.png")
        iter_error = os.path.join(iter_path, f"{model}/code_error.txt")
       
        iter_desc = read_text_file(os.path.join(iter_path, f"{model}/edit_description.txt"))
        iter_diff = read_text_file(os.path.join(iter_path, f"{model}/diff.patch"))

        with st.expander(iter_name):
            sub_cols = st.columns(1)
            if iter_desc:
                sub_cols[0].write(f"**Edit Description:** {iter_desc}")
            if iter_diff:
                sub_cols[0].code(iter_diff, language='diff')

        if os.path.exists(iter_error):
            error_text = read_text_file(os.path.join(iter_path, f"{model}/code_error.txt"))
            st.code(error_text, language='bash')

        if os.path.exists(iter_image):
            st.image(iter_image, caption=iter_name, width=450)
        

    st.divider()

# Main App
st.set_page_config(layout="wide")
st.title("Data Dashboard")

# Loop through /data directory
# Read paths from file because os.listdir doesn't work for remote deployment
# Run `dashboard/store_paths.py` to store path
# base_dir = "./data"
# examples = sorted([os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
with open('./dashboard/remote_paths.txt', "r") as f:
    examples = [line.strip() for line in f.readlines()]

for i, example in enumerate(examples):
    display_example(example, i+1, len(examples), 'gpt-4o')
