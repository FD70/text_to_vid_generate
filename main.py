import cv2
import numpy
import os
from PIL import Image, ImageDraw, ImageFont

fourcc = cv2.VideoWriter_fourcc(*'XVID')
path_of_out_video = os.path.join(os.getcwd(), "out_vid")
FPS_OUT = 10.0

SAMPLE_TEXT = "ДЕФОРМАЦИЯ"
FRAME = (960, 540)
# FRAME = (1920, 1080)

FONT_SIZE = 48

BACKGROUND_COLOR = '#ffffff'


def take_v_writer(filename):
    # cv2.VideoWriter(filename, fourcc, fps, frameSize)
    return cv2.VideoWriter(os.path.join(path_of_out_video, f"{filename}.avi"), fourcc, FPS_OUT, (FRAME[0], FRAME[1]))


def text_to_vid_generate(input_str):
    image = Image.new('RGB', FRAME, color=(BACKGROUND_COLOR))
    draw = ImageDraw.Draw(image)
    font_enc = ImageFont.truetype("ArialBD.ttf", size=FONT_SIZE, encoding='UTF-8')
    w, h = draw.textsize(input_str, font_enc)

    draw.text(
            ((FRAME[0] - w) // 2, (FRAME[1] - h) // 2),
            input_str,
            font=font_enc,
            fill=(0, 0, 0, 255) # цвет
            )

    vout = take_v_writer(input_str)
    recframe = numpy.array(image)
    for i in range(int(FPS_OUT) * 5):
        vout.write(recframe)
    vout.release()


# FIXME: ПОКА НЕ ГОТОВО, ПОТОМ УБРАТЬ ФИКСМи
def book_to_vid_generate(txt_file_path):
    # image = Image.new('RGB', FRAME, color=(BACKGROUND_COLOR))
    # draw = ImageDraw.Draw(image)
    # font_enc = ImageFont.truetype("ArialBD.ttf", size=FONT_SIZE, encoding='UTF-8')
    # w, h = draw.textsize(input_str, font_enc)
    #
    # draw.text(
    #     ((FRAME[0] - w) // 2, (FRAME[1] - h) // 2),
    #     input_str,
    #     font=font_enc,
    #     fill=(0, 0, 0, 255)  # цвет
    # )
    #
    # vout = take_v_writer(input_str)
    # recframe = numpy.array(image)
    # for i in range(int(FPS_OUT) * 5):
    #     vout.write(recframe)
    # vout.release()
    pass


if __name__ == "__main__":
    with open('input.txt', 'r', encoding="utf-8") as file:
        input_line = file.read().splitlines()

    increment = 0
    for one_line in input_line:
        text_to_vid_generate(one_line)

        increment += 1
        print(increment)
