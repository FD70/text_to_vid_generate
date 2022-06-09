import cv2
import numpy
import copy
import os
from PIL import Image, ImageDraw, ImageFont

fourcc = cv2.VideoWriter_fourcc(*'XVID')
path_of_out_video = os.path.join(os.getcwd(), "out_vid")
FPS_OUT = 60.0

INPUT_FILE_PATH = 'input.txt'
SAMPLE_TEXT = "ДЕФОРМАЦИЯ"
FRAME = (960, 540)
# FRAME = (1920, 1080)

FONT_SIZE = 48

COLOR_WHITE = '#ffffff'


def take_v_writer(filename):
    # cv2.VideoWriter(filename, fourcc, fps, frameSize)
    return cv2.VideoWriter(os.path.join(path_of_out_video, f"{filename}.avi"), fourcc, FPS_OUT, (FRAME[0], FRAME[1]))


def text_to_vid_generate(input_str):
    image = Image.new('RGB', FRAME, color=(COLOR_WHITE))
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
    # FIXME: поменять "волшебную" зависимость от FPS_OUT, заменить на необхобимое время отрисовки
    for i in range(int(FPS_OUT) * 5):
        vout.write(recframe)
    vout.release()


# FIXME: ПОКА НЕ ГОТОВО, ПОТОМ УБРАТЬ ФИКСМи
def book_to_vid_generate(txt_file_path):
    OUTPUT_FILE_NAME = "book_to_vid_generate"
    image_empty = Image.new('RGB', FRAME, color=(COLOR_WHITE))
    # draw = ImageDraw.Draw(image)
    font_enc = ImageFont.truetype("ArialBD.ttf", size=FONT_SIZE, encoding='UTF-8')

    vout = take_v_writer(OUTPUT_FILE_NAME)

    with open(txt_file_path, 'r', encoding="utf-8") as _file:
        _file_lines = _file.read().splitlines()

    # FIXME: REPLACE FILE LINES WITH - WORDS!
    # FIXME: ADD BUFFER VARIABLE FOR "-"-TYPE SEPARATE SYMBOLS
    # FIXME: Вероятно, нужно будет убрать изменения отступа в зависимости от высоты текста, чтобы не скакал
    for _one_line in _file_lines:
        image = copy.copy(image_empty)
        draw = ImageDraw.Draw(image)

        w, h = draw.textsize(_one_line, font_enc)

        draw.text(
            ((FRAME[0] - w) // 2, (FRAME[1] - h) // 2),
            _one_line,
            font=font_enc,
            fill=(0, 0, 0, 255)  # TEXT COLOR
        )

        recframe = numpy.array(image)

        # APPEND 10 FRAMES
        for i in range(6):
            vout.write(recframe)

    vout.release()


if __name__ == "__main__":
    # with open('input.txt', 'r', encoding="utf-8") as file:
    #     input_line = file.read().splitlines()
    #
    # increment = 0
    # for one_line in input_line:
    #     text_to_vid_generate(one_line)
    #
    #     increment += 1
    #     print(increment)
    book_to_vid_generate(INPUT_FILE_PATH)

# FIXME: Сделать якори на затраченное на рендер время
# FIXME: Реализовать функццию, которая добавляет паузу "-" на заданное в ф-ии время.
