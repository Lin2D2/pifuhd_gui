import os

import pifuhd.apps.modified_simple_test as simple_test


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = "Input"
    output_path = "Output"
    input_value = input("y for get_rect, s = skip: ")
    if input_value == "y":
        print("prepare images")
        # TODO run prepare_images here

        # print("run openpose")
        # os.system(
        #     f'openpose --image_dir {os.path.join(dir_path, os.path.join(input_path, "tmp/converted"))} --write_json {os.path.join(dir_path, os.path.join(input_path, "tmp/converted"))} --render_pose 0 --display 0 --net_resolution "512x512"')

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


if __name__ == "__main__":
    try:
        os.mkdir("Input")
    except FileExistsError:
        pass
    try:
        os.mkdir("/Input/tmp")
    except FileExistsError:
        pass
    try:
        os.mkdir("/Input/tmp/converted")
    except FileExistsError:
        pass
    try:
        os.mkdir("/Input/tmp/render_ready")
    except FileExistsError:
        pass
    try:
        os.mkdir("/Input/tmp/ress_down")
    except FileExistsError:
        pass
    try:
        os.mkdir("/Input/tmp/ress_up")
    except FileExistsError:
        pass
    try:
        os.mkdir("Output")
    except FileExistsError:
        pass
    main()
