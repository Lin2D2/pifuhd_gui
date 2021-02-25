import glob
import os.path

from PIL import Image


def converte(image_path):
    try:
        os.mkdir(os.path.join(image_path, "tmp/converted"))
    except FileExistsError:
        pass
    for pngfile in glob.glob(f'{image_path}/*.png') + glob.glob(f'{image_path}/*.jpg'):
        width_wanted = 2048
        height_wanted = 2048
        if os.path.basename(pngfile).find("_converted") == -1:
            print(f'trying resizing {os.path.basename(pngfile)} to {width_wanted}x{height_wanted}')
            img = Image.open(pngfile)
            width, height = img.size
            try:
                if width_wanted > height_wanted:
                    with_fac = width_wanted / width
                    height_res = with_fac * height
                    picture_width = width_wanted
                    picture_height = height_res
                    if picture_height > picture_height > height_wanted:
                        height_fac = height_wanted / height
                        width_res = height_fac * width
                        height_res = height_fac * height
                        picture_width = width_res
                        picture_height = height_res
                else:
                    height_fac = height_wanted / height
                    width_res = height_fac * width
                    picture_width = width_res
                    picture_height = height_wanted

                img.resize((int(picture_width), int(picture_height)), Image.ADAPTIVE)
                width, height = img.size
                print(f'resized {os.path.basename(pngfile)} to {width}x{height}')
                img.save(os.path.join(image_path,f'''tmp/converted/{os.path.basename(pngfile)
                                      .replace(".png", "").replace(".jpg", "")}-converted-{width}x{height}.png'''))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    converte("/home/space/Documents/Pictures/final_selection/forth_filter_masked/files")
