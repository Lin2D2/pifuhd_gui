import os
import glob

import pygame

import pifuhd.apps.modified_simple_test as simple_test
from prepare_images import Prepare_Image


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = "Input"
    output_path = "Output"
    input_value = input("y for get_rect, s = skip: ")
    if input_value == "y":
        print("prepare images")
        try:
            Prepare_Image(dir_path, input_path)
            pygame.quit()
        except SystemExit:
            pygame.quit()

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
    simple_test.run(render_ress, os.path.join(dir_path, os.path.join(input_path, "tmp/render_ready")),
                    os.path.join(dir_path, output_path))
    for filename in glob.glob(os.path.join(
            dir_path, os.path.join(input_path, "tmp/render_ready")) + '/*.png'):
        os.remove(filename)
        os.remove(f'{filename.replace(".png", "")}_keypoints.json')


if __name__ == "__main__":
    try:
        os.mkdir("Input")
    except FileExistsError:
        pass
    try:
        os.mkdir("Input/tmp")
    except FileExistsError:
        pass
    try:
        os.mkdir("Input/tmp/converted")
    except FileExistsError:
        pass
    try:
        os.mkdir("Input/tmp/render_ready")
    except FileExistsError:
        pass
    try:
        os.mkdir("Input/tmp/ress_down")
    except FileExistsError:
        pass
    try:
        os.mkdir("Input/tmp/ress_up")
    except FileExistsError:
        pass
    try:
        os.mkdir("Output")
    except FileExistsError:
        pass
    main()
