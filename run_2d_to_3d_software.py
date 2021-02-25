import sys, getopt, os, glob
from PIL import Image
import subprocess
import software_2d_to_3d.pose_estimation.get_rect as get_rect
import software_2d_to_3d.pifuhd.apps.simple_test as simple_test
from operator import is_not
from functools import partial


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
                img.thumbnail((width,height),Image.BILINEAR)  
                img.save(os.path.join(image_path,f'converted/{os.path.basename(pngfile).replace(".png", "")}-converted-{width}x{height}.png'))
            except Exception as e:
                print(e)
                
def main():
   dir_path = os.path.dirname(os.path.realpath(__file__))
   #paths = [file if os.path.isdir(os.path.join(dir_path, file)) and "batch" in file else None for file in os.listdir(dir_path)]
   #paths = list(filter(partial(is_not, None), paths))
   #paths.sort()
   paths = ["/home/space/Documents/Pictures/final_selection/forth_filter_masked"]
   input_value = input("y for get_rect, s = skip: ")
   if input_value == "y":
      print(paths)
      for path in paths:
         # get_rect.run_get_rect(os.path.join(dir_path, os.path.join(path, "files")))
         print("convert images")
         converte(os.path.join(path, "files"))
         print("run openpose")
         os.system(f'openpose --image_dir {os.path.join(dir_path, os.path.join(path, "files/converted"))} --write_json {os.path.join(dir_path, os.path.join(path, "files/converted"))} --render_pose 0 --display 0 --net_resolution "512x512"')
   
   print(f"Done. Enter ress to continue")
   confirmend = False
   
   while not confirmend:
      _input = input("enter ress: ")
      try:
         render_ress = int(_input)
         confirmend = True
      except Exception as err:
         print(err)
   for path in paths:
      start = '\033[94m'
      end = '\033[0m'
      print("\n")
      print(f"{start}working on {path} with ress: {render_ress}{end}")
      simple_test.run(render_ress, os.path.join(dir_path, os.path.join(path, "files/converted")), os.path.join(dir_path, os.path.join(path, "results")))

if __name__ == "__main__":
   main()
