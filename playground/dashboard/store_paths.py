import os

base_dir = "../data"
examples = sorted([os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])

file_path = "./remote_paths.txt"

with open(file_path, "w") as f:
    for example in examples:
        f.write(example.replace('../', '') + "\n")