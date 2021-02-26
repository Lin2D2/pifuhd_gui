import glob
import json
import os

import cv2
import numpy as np
import pygame
import shutil

from resize_images import converte


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


class PrepareImage:
    def __init__(self, dir_path, input_path):
        self.dir_path = dir_path
        self.input_path = input_path

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

        # Render ress
        self.render_resolution = [128, 256, 512, 1024]
        self.render_resolution_index = 0

        # lock
        self.screen_clock = pygame.time.Clock()
        self.tick_rate = 15

        self.SW = self.screen.get_width()
        self.SH = self.screen.get_height()
        self.background_color = self.color_black

        self.image_index = 0
        self.images = []
        self.image_paths = []

        self.margin = 10

        # buttons / TextFields
        self.confirm_button_dimension = (self.SW / 8, self.SH / 18)
        self.confirm_button_location = (int(self.SW / 2 - self.confirm_button_dimension[0] / 2),
                                        int(self.SH - self.confirm_button_dimension[1] - self.margin))
        self.confirm_button = Button(self.color_white, self.confirm_button_location[0], self.confirm_button_location[1],
                                     self.confirm_button_dimension[0], self.confirm_button_dimension[1], self.SW / 21.6, "confirm")

        self.subt_button_dimension = (self.SW / 12, self.SH / 18)
        self.subt_button_location = (
            int(self.SW / 2 - self.subt_button_dimension[0] - self.confirm_button_dimension[0] / 2 - self.margin),
            int(self.SH - self.subt_button_dimension[1] - self.margin))
        self.subt_button = Button(self.color_red, self.subt_button_location[0],
                                  self.subt_button_location[1],
                                  self.subt_button_dimension[0], self.subt_button_dimension[1],
                                  self.SW / 21.6, "-")

        self.add_button_dimension = (self.SW / 12, self.SH / 18)
        self.add_button_location = (
            int(self.SW / 2 + self.confirm_button_dimension[0] / 2 + self.margin),
            int(self.SH - self.add_button_dimension[1] - self.margin))
        self.add_button = Button(self.color_green, self.add_button_location[0], self.add_button_location[1],
                                 self.add_button_dimension[0], self.add_button_dimension[1], self.SW / 21.6, "+")

        self.render_res_dimension = (self.SW / 6, self.SH / 18)
        self.render_res_location = (int(self.SW - self.render_res_dimension[0] - self.margin),
                                    int(self.SH - self.render_res_dimension[1] - self.margin))
        self.render_res_button = Button(self.darkslate_gray, self.render_res_location[0], self.render_res_location[1],
                                        self.render_res_dimension[0], self.render_res_dimension[1], self.SW / 21.6, "")

        self.center_text_dimension = (self.SW / 6, self.SH / 18)
        self.center_text_location = (int(self.SW / 2 - self.center_text_dimension[0] / 2),
                                     int(self.SH / 2 - self.center_text_dimension[1] / 2))
        self.center_text_button = Button(self.color_yellow, self.center_text_location[0], self.center_text_location[1],
                                         self.center_text_dimension[0], self.center_text_dimension[1], self.SW / 21.6,
                                         "Loading..")

        # start screen
        self.screen.fill(self.background_color)
        self.center_text_button.draw(self.screen)
        pygame.display.update()

        # setup up
        converte(os.path.join(dir_path, input_path))

        self.run_opempose("tmp/converted", self.render_resolution[self.render_resolution_index])
        self.images, self.image_paths = self.read_draw_keypoints("tmp/converted")

        self.draw_update()
        try:
            self.loop()
        except pygame.error as error:
            print(f'error: {error}')

    def read_draw_keypoints(self, path):
        image_list = []
        for filename in glob.glob(os.path.join(self.dir_path, os.path.join(self.input_path, path)) + '/*.png'):
            image_list.append(filename)
        image_result = []
        for imgage in image_list:
            img = cv2.imread(imgage, cv2.IMREAD_COLOR)
            with open(f'{imgage.replace(".png", "")}_keypoints.json') as file:
                data = json.load(file)
                people = data["people"]

            for peopl in people:
                img = draw_image(img, peopl)
            image_result.append(img)
        return image_result, image_list

    def run_opempose(self, path, ress):
        path = os.path.join(self.dir_path, os.path.join(self.input_path, path))
        os.system(f'openpose --image_dir {path} --write_json {path} --net_resolution "{ress}x{ress}" --render_pose 0 --display 0')

    def move_file(self, origin, target_folder):
        target = os.path.join(self.dir_path, os.path.join(self.input_path, target_folder))
        try:
            shutil.move(origin, target)
            shutil.move(f'{origin.replace(".png", "")}_keypoints.json', target)
        except shutil.Error:
            # TODO stuck in loop if programm crashes and the image is duplicated
            pass

    def increment(self):
        if self.image_index < len(self.images) - 1:
            self.image_index = self.image_index + 1
            self.draw_update()
        else:
            # TODO not quit
            if len(os.listdir(os.path.join(self.dir_path, os.path.join(self.input_path, 'tmp/ress_down')))) == 0:
                if len(os.listdir(os.path.join(self.dir_path, os.path.join(self.input_path, 'tmp/ress_up')))) == 0:
                    print("Done")
                    pygame.quit()
                    pygame.quit()
                else:
                    print("ress up")
                    self.image_index = 0
                    self.screen.fill(self.background_color)
                    self.center_text_button.draw(self.screen)
                    pygame.display.update()
                    self.render_resolution_index = self.render_resolution_index + 1
                    self.run_opempose("tmp/ress_up", self.render_resolution[self.render_resolution_index])
                    for filename in glob.glob(os.path.join(
                            self.dir_path, os.path.join(self.input_path, "tmp/ress_up")) + '/*.png'):
                        self.move_file(filename, "tmp/converted")
                    self.images, self.image_paths = self.read_draw_keypoints("tmp/converted")
                    self.draw_update()
            else:
                print("ress down")
                self.image_index = 0
                self.screen.fill(self.background_color)
                self.center_text_button.draw(self.screen)
                pygame.display.update()
                self.render_resolution_index = self.render_resolution_index - 1
                self.run_opempose("tmp/ress_down", self.render_resolution[self.render_resolution_index])
                for filename in glob.glob(os.path.join(self.dir_path, os.path.join(self.input_path, "tmp/ress_down")) + '/*.png'):
                    self.move_file(filename, "tmp/converted")
                self.images, self.image_paths = self.read_draw_keypoints("tmp/converted")
                self.draw_update()

    def confirm(self):
        self.move_file(self.image_paths[self.image_index], "tmp/render_ready")
        self.increment()

    def add(self):
        if self.render_resolution_index < len(self.render_resolution) - 1:
            self.move_file(self.image_paths[self.image_index], "tmp/ress_up")
            self.increment()

    def subtract(self):
        if self.render_resolution_index > 0:
            self.move_file(self.image_paths[self.image_index], "tmp/ress_down")
            self.increment()

    def set_button_locations_dimensions(self):
        self.confirm_button_dimension = (self.SW / 8, self.SH / 18)
        self.confirm_button_location = (int(self.SW / 2 - self.confirm_button_dimension[0] / 2),
                                        int(self.SH - self.confirm_button_dimension[1] - self.margin))
        self.confirm_button = Button(self.color_white, self.confirm_button_location[0], self.confirm_button_location[1],
                                     self.confirm_button_dimension[0], self.confirm_button_dimension[1], self.SW / 21.6,
                                     "confirm")
        self.subt_button_dimension = (self.SW / 12, self.SH / 18)
        self.subt_button_location = (
            int(self.SW / 2 - self.subt_button_dimension[0] - self.confirm_button_dimension[0] / 2 - self.margin),
            int(self.SH - self.subt_button_dimension[1] - self.margin))
        self.subt_button = Button(self.color_green, self.subt_button_location[0],
                                  self.subt_button_location[1],
                                  self.subt_button_dimension[0], self.subt_button_dimension[1],
                                  self.SW / 21.6, "-")
        self.add_button_dimension = (self.SW / 12, self.SH / 18)
        self.add_button_location = (
            int(self.SW / 2 + self.confirm_button_dimension[0] / 2 + self.margin),
            int(self.SH - self.add_button_dimension[1] - self.margin))
        self.add_button = Button(self.color_green, self.add_button_location[0], self.add_button_location[1],
                                 self.add_button_dimension[0], self.add_button_dimension[1], self.SW / 21.6, "+")
        self.render_res_dimension = (self.SW / 6, self.SH / 18)
        self.render_res_location = (int(self.SW - self.render_res_dimension[0] - self.margin),
                                    int(self.SH - self.render_res_dimension[1] - self.margin))
        self.render_res_button = Button(self.darkslate_gray, self.render_res_location[0], self.render_res_location[1],
                                        self.render_res_dimension[0], self.render_res_dimension[1], self.SW / 21.6, self.render_res_button.text)
        self.center_text_dimension = (self.SW / 6, self.SH / 18)
        self.center_text_location = (int(self.SW / 2 - self.center_text_dimension[0] / 2),
                                     int(self.SH / 2 - self.center_text_dimension[1] / 2))
        self.center_text_button = Button(self.color_yellow, self.center_text_location[0], self.center_text_location[1],
                                         self.center_text_dimension[0], self.center_text_dimension[1], self.SW / 21.6,
                                         "Loading...")

    def draw_update(self, resize=False):
        img = self.images[self.image_index]
        # fill screen
        self.screen.fill(self.background_color)
        if resize:
            self.set_button_locations_dimensions()

        self.render_res_button.text = str(self.render_resolution[self.render_resolution_index])

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
        if self.render_resolution_index > 0:
            self.subt_button.draw(self.screen)
        self.confirm_button.draw(self.screen)
        if self.render_resolution_index < len(self.render_resolution) - 1:
            self.add_button.draw(self.screen)
        self.render_res_button.draw(self.screen)

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
                    # confirm button
                    if (self.confirm_button_location[0] <= mouse[0] <= self.confirm_button_location[0] +
                            self.confirm_button_dimension[0]
                            and
                            self.confirm_button_location[1] <= mouse[1] <= self.confirm_button_location[1] +
                            self.confirm_button_dimension[1]):
                        self.confirm()
                    # add button
                    elif (self.add_button_location[0] <= mouse[0] <= self.add_button_location[0] +
                          self.add_button_dimension[0]
                          and
                          self.add_button_location[1] <= mouse[1] <= self.add_button_location[1] +
                          self.add_button_dimension[1]):
                        self.add()
                    # subt button
                    elif (self.subt_button_location[0] <= mouse[0] <= self.subt_button_location[0] +
                          self.subt_button_dimension[0]
                          and
                          self.subt_button_location[1] <= mouse[1] <= self.subt_button_location[1] +
                          self.subt_button_dimension[1]):
                        self.subtract()
                elif event.type == pygame.VIDEORESIZE:
                    self.SW, self.SH = pygame.display.get_window_size()
                    self.draw_update(resize=True)
            # tick
            self.screen_clock.tick(self.tick_rate)


if __name__ == '__main__':
    PrepareImage(os.path.dirname(os.path.realpath(__file__)), "Input")
