'''
Adapted from: https://github.com/mapluisch/LLaVA-CLI-with-multiple-images/blob/main/llava-multi-images.py
'''
import argparse
import requests
from PIL import Image
from io import BytesIO
import os

def load_image(image_file):
    if image_file.startswith('http://') or image_file.startswith('https://'):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_file).convert('RGB')
    return image


def expand_image_range_paths(paths):
    expanded_paths = []
    # check if specified --images is range of imgs
    for path in paths:
        if "{" in path and "}" in path:
            pre, post = path.split("{", 1)
            range_part, post = post.split("}", 1)
            start, end = map(int, range_part.split("-"))

            for i in range(start, end + 1):
                expanded_paths.append(f"{pre}{i}{post}")
        else:
            expanded_paths.append(path)

    return expanded_paths


def parse_resolution(resolution_str):
    # try to parse a string into a resolution tuple for the grid output
    try:
        width, height = map(int, resolution_str.split(','))
        return width, height
    except Exception as e:
        raise argparse.ArgumentTypeError("Resolution must be w,h.") from e


def concatenate_images_vertical(images, dist_images):
    # resize to the smaller image
    min_width = min(img.width for img in images)
    min_height = min(img.height for img in images)
    for img in images:
        img = img.thumbnail((min_width, min_height))

    # calc total height of imgs + dist between them
    total_height = sum(img.height for img in images) + dist_images * (len(images) - 1)

    # create new img with calculated dimensions, black bg
    new_img = Image.new('RGB', (min_width, total_height), (0, 0, 0))

    # init var to track current height pos
    current_height = 0
    for img in images:
        # paste img in new_img at current height
        new_img.paste(img, (0, current_height))
        # update current height for next img
        current_height += img.height + dist_images

    return new_img


def concatenate_images_horizontal(images, dist_images):
    # calc total width of imgs + dist between them
    total_width = sum(img.width for img in images) + dist_images * (len(images) - 1)
    # calc max height from imgs
    height = max(img.height for img in images)

    # create new img with calculated dimensions, black bg
    new_img = Image.new('RGB', (total_width, height), (0, 0, 0))

    # init var to track current width pos
    current_width = 0
    for img in images:
        # paste img in new_img at current width
        new_img.paste(img, (current_width, 0))
        # update current width for next img
        current_width += img.width + dist_images

    return new_img


def concatenate_images(images, strategy, dist_images):
    if strategy == 'vertical':
        return concatenate_images_vertical(images, dist_images)
    elif strategy == 'horizontal':
        return concatenate_images_horizontal(images, dist_images)
    else:
        raise ValueError("Invalid concatenation strategy specified")


def main(args):
    args.images = expand_image_range_paths(args.images)
    images = [load_image(img_file) for img_file in args.images]
    image = concatenate_images(images, args.concat_strategy, args.dist_images) if len(images) > 1 else images[0]

    if args.save_path:
        if not os.path.exists(args.save_path):
            os.makedirs(args.save_path)
        image.save(os.path.join(args.save_path, "merged.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="liuhaotian/llava-v1.6-vicuna-13b")
    parser.add_argument("--load-8bit", action="store_true")
    parser.add_argument("--load-4bit", action="store_true")

    parser.add_argument("--images", type=str, nargs='+', required=True,
                    help="Specify the paths for images to be concatenated. Accepts multiple paths, or range of images in the same location, e.g. img{1-4}.jpg.")

    parser.add_argument("--save-path", type=str, help="Parent directory for saving merged image.")

    parser.add_argument("--concat-strategy", type=str, default="vertical", choices=["vertical", "horizontal"],
                    help="Determines the arrangement strategy for image concatenation. Options: 'vertical', 'horizontal'.")
    
    parser.add_argument("--dist-images", type=int, default=20,
                    help="Sets the spacing (in pixels) between concatenated images.")
    
    args = parser.parse_args()
    main(args)