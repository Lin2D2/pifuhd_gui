import glob
import os

from PIL import Image

import pifuhd.apps.modified_simple_test as simple_test


def converte(image_path):
    try:
        os.mkdir(os.path.join(image_path, "converted"))
    except FileExistsError:
        pass
    for pngfile in glob.glob(f'{image_path}/*.png'):
        width = 2048
        height = 2048
        if os.path.basename(pngfile).find("_converted") == -1:
            print(f'resizing {os.path.basename(pngfile)} to {width}x{height}')
            img = Image.open(pngfile)
            try:
                img.thumbnail((width, height), Image.BILINEAR)
                img.save(os.path.join(image_path,
                                      f'converted/{os.path.basename(pngfile).replace(".png", "")}-converted-{width}x{height}.png'))
            except Exception as e:
                print(e)


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = "Input"
    output_path = "Input"
    input_value = input("y for get_rect, s = skip: ")
    if input_value == "y":
        print("convert images")
        converte(input_path)
        print("run openpose")
        os.system(
            f'openpose --image_dir {os.path.join(dir_path, os.path.join(input_path, "converted"))} --write_json {os.path.join(dir_path, os.path.join(input_path, "converted"))} --render_pose 0 --display 0 --net_resolution "512x512"')

    print(f"Done. Enter ress to continue")
    confirmend = False
    while not confirmend:
        _input = input("enter ress: ")
        try:
            render_ress = int(_input)
            confirmend = True
        except Exception as err:
            print(err)
    start = '\033[94m'
    end = '\033[0m'
    print("\n")
    print(f"{start}working on {input_path} with ress: {render_ress}{end}")
    simple_test.run(render_ress, os.path.join(dir_path, os.path.join(input_path, "converted")),
                    os.path.join(dir_path, output_path, "results"))


if __name__ == "__main__":
    try:
        os.mkdir("Input")
    except FileExistsError:
        pass
    try:
        os.mkdir("Output")
    except FileExistsError:
        pass
    main()
