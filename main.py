import argparse
import os
from PIL import Image

def parse_size(size_str):
    try:
        width, height = map(int, size_str.lower().split('x'))
        return width, height
    except ValueError:
        raise argparse.ArgumentTypeError("Size must be in the format 'WxH', for example '32x32'.")

def split_image(image_path, output_dir, width, height):
    img = Image.open(image_path)
    img_width, img_height = img.size

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = 0
    for top in range(0, img_height, height):
        for left in range(0, img_width, width):
            right = min(left + width, img_width)
            bottom = min(top + height, img_height)
            box = (left, top, right, bottom)
            cropped_img = img.crop(box)
            cropped_img.save(os.path.join(output_dir, f"img_{count}.png"))
            count += 1

    print(f"Cutting complete. {count} images have been saved in the folder '{output_dir}'.")

def main():
    parser = argparse.ArgumentParser(description="Cut images within a stylesheet image into pieces of a specified size.")
    parser.add_argument("size", type=parse_size, help="Cut size in the format 'WxH', e.g., '32x32'.")
    parser.add_argument("image", type=str, help="Path to the image to be cut.")
    parser.add_argument("output_dir", type=str, help="Output folder to save the cut images.")

    args = parser.parse_args()
    width, height = args.size
    split_image(args.image, args.output_dir, width, height)

if __name__ == "__main__":
    main()
