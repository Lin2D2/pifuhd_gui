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
            try:
                if img.size[0] > img.size[1]:
                    baseheight = height_wanted
                    wpercent = (baseheight / float(img.size[0]))
                    wsize = int((float(img.size[1]) * float(wpercent)))
                    img = img.resize((baseheight, wsize), Image.ADAPTIVE)
                else:
                    basewidth = width_wanted
                    wpercent = (basewidth / float(img.size[1]))
                    hsize = int((float(img.size[0]) * float(wpercent)))
                    img = img.resize((hsize, basewidth), Image.ADAPTIVE)

                width, height = img.size
                print(f'resized {os.path.basename(pngfile)} to {width}x{height}')
                img.save(os.path.join(image_path,f'''tmp/converted/{os.path.basename(pngfile)
                                      .replace(".png", "").replace(".jpg", "")}-converted-{width}x{height}.png'''))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    converte("/home/space/Documents/pifuhd_gui/Input")
