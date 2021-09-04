import os
import glob

import pifuhd.apps.modified_simple_test as simple_test
from prepare_images import PrepareImage


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = "Input"
    output_path = "Output"
    input_value = input("y for get_rect, s = skip: ")
    if input_value == "y":
        print("PrepareImage running")
        PrepareImage(dir_path, input_path).start()
        print("PrepareImage done")
        # TODO start rendering here?

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
    simple_test.run(str(render_ress), os.path.join(dir_path, os.path.join(input_path, "tmp/render_ready")),
                    os.path.join(dir_path, output_path), cpu=True)
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
