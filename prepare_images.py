import glob
import json
import os

import cv2
import numpy as np
import pygame

from resize_images import converte


def run_opempose(di_path, in_path, ress):
    print("running openpose")
    path = os.path.join(di_path, os.path.join(in_path, "converted"))
    print(path)
    os.system(f'openpose --image_dir {path} --write_json {path} --net_resolution "{ress}x{ress}" --render_pose 0 --display 0')
    print("done running openpose")


def draw_image(img, peopl):
    points_raw_raw = peopl["pose_keypoints_2d"]
    points_raw = np.array(points_raw_raw).reshape(-1, 3)
    points = [tuple([int(e[0]), int(e[1])]) for e in points_raw]

    line_thickness = 10

    # head
    # left eye
    if points[0] != (0, 0) and points[15] != (0, 0):
        cv2.line(img, points[0], points[15], (153, 48, 175), line_thickness)
    # left ear
    try:
        if points[15] != (0, 0) and points[17] != (0, 0):
            cv2.line(img, points[15], points[17], (155, 34, 72), line_thickness)
    except IndexError:
        pass
    # right eye
    if points[0] != (0, 0) and points[16] != (0, 0):
        cv2.line(img, points[0], points[16], (116, 45, 179), line_thickness)
    # right ear
    try:
        if points[16] != (0, 0) and points[18] != (0, 0):
            cv2.line(img, points[16], points[18], (172, 45, 131), line_thickness)
    except IndexError:
        pass

    # body
    # spine
    if points[0] != (0, 0) and points[1] != (0, 0):
        cv2.line(img, points[0], points[1], (167, 34, 30), line_thickness)
    if points[1] != (0, 0) and points[8] != (0, 0):
        cv2.line(img, points[1], points[8], (167, 34, 30), line_thickness)
    # right shoulder
    if points[1] != (0, 0) and points[2] != (0, 0):
        cv2.line(img, points[1], points[2], (193, 132, 34), line_thickness)
    # right arm
    if points[2] != (0, 0) and points[3] != (0, 0):
        cv2.line(img, points[2], points[3], (200, 188, 46), line_thickness)
    if points[3] != (0, 0) and points[4] != (0, 0):
        cv2.line(img, points[3], points[4], (112, 145, 17), line_thickness)
    # left shoulder
    if points[1] != (0, 0) and points[5] != (0, 0):
        cv2.line(img, points[1], points[5], (66, 143, 21), line_thickness)
    # left arm
    if points[5] != (0, 0) and points[6] != (0, 0):
        cv2.line(img, points[5], points[6], (26, 143, 20), line_thickness)
    if points[6] != (0, 0) and points[7] != (0, 0):
        cv2.line(img, points[6], points[7], (23, 145, 69), line_thickness)
    # right hip
    if points[8] != (0, 0) and points[9] != (0, 0):
        cv2.line(img, points[8], points[9], (22, 151, 120), line_thickness)
    # right leg
    if points[9] != (0, 0) and points[10] != (0, 0):
        cv2.line(img, points[9], points[10], (31, 161, 161), line_thickness)
    if points[10] != (0, 0) and points[11] != (0, 0):
        cv2.line(img, points[10], points[11], (31, 161, 161), line_thickness)
    # left hip
    if points[8] != (0, 0) and points[12] != (0, 0):
        cv2.line(img, points[8], points[12], (22, 78, 167), line_thickness)
    # left leg
    if points[12] != (0, 0) and points[13] != (0, 0):
        cv2.line(img, points[12], points[13], (9, 30, 152), line_thickness)
    if points[13] != (0, 0) and points[14] != (0, 0):
        cv2.line(img, points[13], points[14], (9, 30, 152), line_thickness)
    try:
        # right foot
        if points[11] != (0, 0) and points[22] != (0, 0):
            cv2.line(img, points[11], points[22], (31, 161, 161), line_thickness)
        if points[11] != (0, 0) and points[23] != (0, 0):
            cv2.line(img, points[11], points[23], (31, 161, 161), line_thickness)
        if points[11] != (0, 0) and points[24] != (0, 0):
            cv2.line(img, points[11], points[24], (31, 161, 161), line_thickness)
        # left foot
        if points[14] != (0, 0) and points[19] != (0, 0):
            cv2.line(img, points[14], points[19], (9, 30, 152), line_thickness)
        if points[14] != (0, 0) and points[20] != (0, 0):
            cv2.line(img, points[14], points[20], (9, 30, 152), line_thickness)
        if points[14] != (0, 0) and points[21] != (0, 0):
            cv2.line(img, points[14], points[21], (9, 30, 152), line_thickness)
    except IndexError:
        pass
    return img


class Button:
    def __init__(self, color, x, y, width, height, fontsize, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fontsize = fontsize
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont("Corbel", int(self.fontsize))
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (int(self.width / 2 - text.get_width() / 2)),
                self.y + (int(self.height / 2 - text.get_height() / 2))))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class Window:
    def __init__(self, images):
        pygame.init()
        # screen
        self.screen = pygame.display.set_mode([1280, 720], pygame.RESIZABLE)

        # Color
        self.color_red = pygame.Color("red")
        self.color_white = pygame.Color("white")
        self.color_black = pygame.Color("black")
        self.darkslate_gray = pygame.Color("darkslategray1")
        self.color_green = pygame.Color("green")
        self.color_yellow = pygame.Color("yellow")

        # lock
        self.screen_clock = pygame.time.Clock()
        self.tick_rate = 15

        self.SW = self.screen.get_width()
        self.SH = self.screen.get_height()
        self.background_color = self.color_black
        self.image_path = "./images"

        self.image_index = 0
        self.images = images

        self.margin = 10

        # buttons
        self.next_button_dimension = (self.SW / 12, self.SH / 18)
        self.next_button_location = (int(self.SW / 2 - self.next_button_dimension[0] / 2),
                                     int(self.SH - self.next_button_dimension[1] - self.margin))
        self.next_button = Button(self.color_white, self.next_button_location[0], self.next_button_location[1],
                                  self.next_button_dimension[0], self.next_button_dimension[1], self.SW / 21.6, "next")

        self.subtract_button_dimension = (self.SW / 12, self.SH / 18)
        self.subtract_button_location = (
            int(self.SW / 2 - self.subtract_button_dimension[0] - self.next_button_dimension[0] /
                2 - self.margin), int(self.SH - self.subtract_button_dimension[1] - self.margin))
        self.subtract_button = Button(self.color_red, self.subtract_button_location[0],
                                      self.subtract_button_location[1],
                                      self.subtract_button_dimension[0], self.subtract_button_dimension[1],
                                      self.SW / 21.6, "-")

        self.add_button_dimension = (self.SW / 12, self.SH / 18)
        self.add_button_location = (int(self.SW / 2 - self.add_button_dimension[0] +
                                        self.next_button_dimension[0] / 2 + self.next_button_dimension[0] +
                                        self.margin), int(self.SH - self.add_button_dimension[1] - self.margin))
        self.add_button = Button(self.color_green, self.add_button_location[0], self.add_button_location[1],
                                 self.add_button_dimension[0], self.add_button_dimension[1], self.SW / 21.6, "+")

        self.image_res_dimension = (self.SW / 6, self.SH / 18)
        self.image_res_location = (int(self.SW - self.image_res_dimension[0] - self.margin),
                                   int(self.SH - self.image_res_dimension[1] - self.margin))
        self.image_res = Button(self.darkslate_gray, self.image_res_location[0], self.image_res_location[1],
                                self.image_res_dimension[0], self.image_res_dimension[1], self.SW / 21.6, "")

        self.draw_update()
        try:
            self.loop()
        except pygame.error as error:
            print(f'error: {error}')

    def next(self):
        if self.image_index < len(self.images) - 1:
            self.image_index = self.image_index + 1
            self.draw_update()
        else:
            pygame.quit()

    def add(self):
        pass

    def subtract(self):
        pass

    def set_button_locations_dimensions(self):
        self.next_button_dimension = (self.SW / 12, self.SH / 18)
        self.next_button_location = (int(self.SW / 2 - self.next_button_dimension[0] / 2),
                                     int(self.SH - self.next_button_dimension[1] - self.margin))
        self.next_button = Button(self.color_white, self.next_button_location[0], self.next_button_location[1],
                                  self.next_button_dimension[0], self.next_button_dimension[1], self.SW / 21.6, "next")
        self.subtract_button_dimension = (self.SW / 12, self.SH / 18)
        self.subtract_button_location = (
            int(self.SW / 2 - self.subtract_button_dimension[0] - self.next_button_dimension[0] /
                2 - self.margin), int(self.SH - self.subtract_button_dimension[1] - self.margin))
        self.subtract_button = Button(self.color_red, self.subtract_button_location[0],
                                      self.subtract_button_location[1],
                                      self.subtract_button_dimension[0], self.subtract_button_dimension[1],
                                      self.SW / 21.6, "-")
        self.add_button_dimension = (self.SW / 12, self.SH / 18)
        self.add_button_location = (int(self.SW / 2 - self.add_button_dimension[0] +
                                        self.next_button_dimension[0] / 2 + self.next_button_dimension[0] +
                                        self.margin), int(self.SH - self.add_button_dimension[1] - self.margin))
        self.add_button = Button(self.color_green, self.add_button_location[0], self.add_button_location[1],
                                 self.add_button_dimension[0], self.add_button_dimension[1], self.SW / 21.6, "+")
        self.image_res_dimension = (self.SW / 6, self.SH / 18)
        self.image_res_location = (int(self.SW - self.image_res_dimension[0] - self.margin),
                                   int(self.SH - self.image_res_dimension[1] - self.margin))
        self.image_res = Button(self.darkslate_gray, self.image_res_location[0], self.image_res_location[1],
                                self.image_res_dimension[0], self.image_res_dimension[1], self.SW / 21.6,
                                self.image_res.text)

    def draw_update(self, resize=False):
        img = self.images[self.image_index]
        # fill screen
        self.screen.fill(self.background_color)
        if resize:
            self.set_button_locations_dimensions()

        self.image_res.text = ""

        # draw image
        height, width, channels = img.shape
        image = pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGR")
        if width > height:
            with_fac = self.SW / width
            height_res = with_fac * height
            picture_width = int(self.SW)
            picture_height = int(height_res)
            if picture_height > picture_height > self.SH:
                height_fac = self.SH / height
                width_res = height_fac * width
                height_res = height_fac * height
                picture_width = int(width_res)
                picture_height = int(height_res)
        else:
            height_fac = self.SH / height
            width_res = height_fac * width
            picture_width = int(width_res)
            picture_height = int(self.SH)
        picture = pygame.transform.scale(image, (picture_width, picture_height))
        image_rect = picture.get_rect()
        image_rect.center = (int(self.SW / 2), int(self.SH / 2))

        self.screen.blit(picture, image_rect)
        self.subtract_button.draw(self.screen)
        self.add_button.draw(self.screen)
        self.next_button.draw(self.screen)
        self.image_res.draw(self.screen)

        pygame.display.update()

    def loop(self):
        running = True

        while running:
            # get mouse position
            mouse = pygame.mouse.get_pos()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # next button
                    if (self.next_button_location[0] <= mouse[0] <= self.next_button_location[0] +
                            self.next_button_dimension[0]
                            and
                            self.next_button_location[1] <= mouse[1] <= self.next_button_location[1] +
                            self.next_button_dimension[1]):
                        self.next()

                    # add button
                    elif (self.add_button_location[0] <= mouse[0] <= self.add_button_location[0] +
                          self.add_button_dimension[0]
                          and
                          self.add_button_location[1] <= mouse[1] <= self.add_button_location[1] +
                          self.add_button_dimension[1]):
                        pass
                    # subtract button
                    elif (self.subtract_button_location[0] <= mouse[0] <= self.subtract_button_location[0] +
                          self.subtract_button_dimension[0]
                          and
                          self.subtract_button_location[1] <= mouse[1] <= self.subtract_button_location[1] +
                          self.subtract_button_dimension[1]):
                        pass
                elif event.type == pygame.VIDEORESIZE:
                    self.SW, self.SH = pygame.display.get_window_size()
                    self.draw_update(resize=True)
            # tick
            self.screen_clock.tick(self.tick_rate)


def read_draw_keypoints(image_list):
    image_result = []
    for imgage in image_list:
        img = cv2.imread(imgage, cv2.IMREAD_COLOR)
        with open(f'{imgage.replace(".png", "")}_keypoints.json') as file:
            data = json.load(file)
            people = data["people"]

        for peopl in people:
            img = draw_image(img, peopl)
        image_result.append(img)
    return image_result


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_path = "Input"
    converte(os.path.join(dir_path, input_path))
    run_opempose(dir_path, input_path, 128)  # min ca. 128 / max ca. 1024
    images = []
    for filename in glob.glob(os.path.join(dir_path, os.path.join(input_path, "converted")) + '/*.jpg'):  # assuming jpg
        images.append(filename)
    for filename in glob.glob(os.path.join(dir_path, os.path.join(input_path, "converted")) + '/*.png'):  # assuming png
        images.append(filename)
    result = read_draw_keypoints(images)
    window = Window(result)
