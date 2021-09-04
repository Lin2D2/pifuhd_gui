import glob
import os.path
import itertools
import numpy as np
import cv2
import multiprocessing
import multiprocessing.shared_memory


def converte(chunked_image_path, size_wanted=2048):
    images = []
    for image_path in chunked_image_path:
        print(f'trying resizing {os.path.basename(image_path)} to {size_wanted}x{size_wanted}')
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image.shape[1] > image.shape[0]:
            baseheight = size_wanted
            wpercent = (baseheight / float(image.shape[1]))
            wsize = int((float(image.shape[0]) * float(wpercent)))
            image = cv2.resize(image, (baseheight, wsize))
        else:
            basewidth = size_wanted
            wpercent = (basewidth / float(image.shape[0]))
            hsize = int((float(image.shape[1]) * float(wpercent)))
            image = cv2.resize(image, (hsize, basewidth))

        width, height, channel = image.shape
        print(f'resized {os.path.basename(image_path)} to {width}x{height}')
        images.append(image)

    return images


def compare_inner_loop(image_paths, chunk, shm):
    print(f"{os.getpid()}::{image_paths[chunk[0]:chunk[1]]}")
    existing_shm = multiprocessing.shared_memory.SharedMemory(name=shm[0], create=False)
    images_loaded = np.ndarray(shm[1], dtype=shm[2], buffer=existing_shm.buf)
    duplicate = []

    try:
        for chunked_image_index, chunked_image_path in enumerate(image_paths[chunk[0]:chunk[1]]):
            for image_index, image_path in enumerate(image_paths):
                if chunked_image_path != image_path:
                    try:
                        chunked_image = images_loaded[chunk[0]:chunk[1]][chunked_image_index]
                        image = images_loaded[image_index]
                        if chunked_image.shape == image.shape:
                            difference = cv2.subtract(chunked_image, image)
                            sum = np.sum(difference)
                            if np.all((difference == 100)):
                                print("same")
                                print(chunked_image_path)
                                print(image_path)
                                duplicate.append((chunked_image_path, image_path))
                            elif sum <= 100000:
                                print("similar")
                                print(chunked_image_path)
                                print(image_path)
                                duplicate.append((chunked_image_path, image_path))
                            elif sum <= 10000000:
                                print("not far")
                                print(chunked_image_path)
                                print(image_path)
                                duplicate.append((chunked_image_path, image_path))
                            elif sum <= 100000000:
                                print("different?")
                                print(chunked_image_path)
                                print(image_path)
                                # TODO remove?
                                duplicate.append((chunked_image_path, image_path))
                    except IndexError:
                        pass
        return duplicate
    except Exception as err:
        return err


def prepare_images(image_source_path):
    image_paths = glob.glob(f'{image_source_path}/*.png') + glob.glob(f'{image_source_path}/*.jpg')

    try:
        os.mkdir(os.path.join(image_source_path, "tmp/converted"))
    except FileExistsError:
        pass

    cpu_count = multiprocessing.cpu_count()
    chunk_size = len(image_paths) / (cpu_count - 1) + 1

    image_size = int(input("which size should the images be(default: 2048): "))

    with multiprocessing.Pool(processes=cpu_count - 1) as pool:
        results = [pool.apply_async(converte,
                                    (image_paths[int(chunk_size * i):int(chunk_size * (i + 1))],
                                     image_size,
                                     )) for i in range(cpu_count - 1)]
        [res.wait() for res in results]
        images = [res.get() for res in results]
    images = list(itertools.chain.from_iterable(images))
    images = np.array(images)

    shm = multiprocessing.shared_memory.SharedMemory(create=True, size=images.nbytes)
    images_loaded_shared = np.ndarray(images.shape, dtype=images.dtype, buffer=shm.buf)
    images_loaded_shared[:] = images[:]
    del images

    with multiprocessing.Pool(processes=cpu_count - 1) as pool:
        results = [pool.apply_async(compare_inner_loop,
                                    (image_paths,
                                     (int(chunk_size * i), int(chunk_size * (i + 1))),
                                     (shm.name, images_loaded_shared.shape, images_loaded_shared.dtype),)
                                    ) for i in range(cpu_count - 1)]
        [res.wait() for res in results]
        duplicates = [res.get() for res in results]
    duplicates = list(itertools.chain.from_iterable(duplicates))
    duplicate_dict = dict()
    duplicates_filtered = []
    for duplicate in duplicates:
        if duplicate[0] in duplicate_dict:
            duplicate_dict[duplicate[0]].append(duplicate[1])
            duplicates_filtered.append(duplicate[1])
        else:
            found = None
            for key in duplicate_dict.keys():
                if duplicate[0] in duplicate_dict[key]:
                    found = key
            if found:
                duplicate_dict[found].append(duplicate[1])
                duplicates_filtered.append(duplicate[1])
            else:
                duplicate_dict.update({duplicate[0]: [duplicate[1]]})
    # for e in duplicate_dict.keys():
    #     print(f"{e}::{duplicate_dict[e]}")
    del duplicate_dict
    del duplicates
    for image_index, image_path in enumerate(image_paths):
        height, width, channel = images_loaded_shared[image_index].shape
        image_path_dest = os.path.join(
            image_path.replace(os.path.basename(image_path), ""),
            f'''tmp/converted/{os.path.basename(image_path).replace(".png", "").replace(".jpg", "")}-converted-{width}x{height}.png''')
        print(image_path_dest)
        if image_path not in duplicates_filtered:
            cv2.imwrite(image_path_dest, images_loaded_shared[image_index])
    print("done")

    # TODO save images
    shm.close()
    shm.unlink()


# def compare(image_path):
#     with multiprocessing.Pool(processes=cpu_count - 1) as pool:
#         results = [pool.apply_async(compare_inner_loop,
#                                     (images[int(chunk_size * i):int(chunk_size * (i + 1))],
#                                      images,
#                                      shm.name,
#                                      images_loaded_shared.shape,
#                                      images_loaded_shared.dtype,
#                                      range(int(chunk_size * i), int(chunk_size * (i + 1))))) for i in
#                    range(cpu_count - 1)]
#         [res.wait() for res in results]
#         shm.close()
#         shm.unlink()
#         print("results:")
#         duplicate = [res.get() for res in results]
#         duplicate = list(itertools.chain.from_iterable(duplicate))
#         pprint(duplicate)
#         duplicate_filtered = []
#         for e in duplicate:
#             containse = False
#             for el in duplicate:
#                 if e != el and e[0] == el[1] and e[1] == el[0]:
#                     containse = True
#             if not containse:
#                 duplicate_filtered.append(e[1])
#         print("----------")
#         duplicate_filtered = list(dict.fromkeys(duplicate_filtered))
#         pprint(duplicate_filtered)
#         for e in images:
#             if e not in duplicate_filtered:
#                 print(os.path.join(image_path, "filtered"))
#                 filename = e.replace(image_path, "").replace("/", "")
#                 print(filename)
#                 dst = os.path.join(os.path.join(image_path, "filtered"), filename)
#                 print(dst)
#                 copyfile(e, dst)
#         print("done")


if __name__ == '__main__':
    prepare_images("/home/linus/Documents/pifuhd_gui/Input")
