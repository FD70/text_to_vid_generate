import cv2
import numpy
import copy
import os
from PIL import Image, ImageDraw, ImageFont

fourcc = cv2.VideoWriter_fourcc(*'XVID')
INPUT_FILE_PATH = 'input.txt'
OUTPUT_FILE_PATH = os.path.join(os.getcwd(), "out_vid")

# OUTPUT_FRAME_SHAPE X, Y
# FRAME = (960, 540)
FRAME = (1920, 1080)
FPS_OUT = 60.0

COLOR_WHITE = '#ffffff'
FONT_SIZE = 48


def get_video_writer(output_filename: str):
    return cv2.VideoWriter(os.path.join(OUTPUT_FILE_PATH, f"{output_filename}.avi"), fourcc, FPS_OUT, (FRAME[0], FRAME[1]))


def text_to_vid_generate(input_str):
    image = Image.new('RGB', FRAME, color=COLOR_WHITE)
    draw = ImageDraw.Draw(image)
    font_enc = ImageFont.truetype("ArialBD.ttf", size=FONT_SIZE, encoding='UTF-8')
    w, h = draw.textsize(input_str, font_enc)

    draw.text(
            ((FRAME[0] - w) // 2, (FRAME[1] - h) // 2),
            input_str,
            font=font_enc,
            fill=(0, 0, 0, 255) # цвет
            )

    vout = get_video_writer(input_str)
    recframe = numpy.array(image)
    # FIXME: поменять "волшебную" зависимость от FPS_OUT, заменить на необхобимое время отрисовки
    for i in range(int(FPS_OUT) * 5):
        vout.write(recframe)
    vout.release()


def book_to_vid_generate(txt_file_path):
    OUTPUT_FILE_NAME = "book_to_vid_generate"
    image_empty = Image.new('RGB', FRAME, color=COLOR_WHITE)
    # draw = ImageDraw.Draw(image)
    font_enc = ImageFont.truetype("ArialBD.ttf", size=FONT_SIZE, encoding='UTF-8')

    vout = get_video_writer(OUTPUT_FILE_NAME)

    with open(txt_file_path, 'r', encoding="utf-8") as _file:
        _file_lines = _file.read().splitlines()

    # FIXME: ADD BUFFER VARIABLE FOR "-"-TYPE SEPARATE SYMBOLS
    for _one_line in _file_lines:
        for _one_word in _one_line.split():
            image = copy.copy(image_empty)
            draw = ImageDraw.Draw(image)

            w, h = draw.textsize(_one_word, font_enc)

            draw.text(
                ((FRAME[0] - w) // 2, (FRAME[1]) // 2),
                _one_word,
                font=font_enc,
                fill=(0, 0, 0, 255)  # TEXT COLOR
            )

            recframe = numpy.array(image)

            # APPEND x FRAMES
            for i in range(6):
                vout.write(recframe)

    vout.release()


if __name__ == "__main__":
    book_to_vid_generate(INPUT_FILE_PATH)

# FIXME: Сделать якори на затраченное на рендер время
# FIXME: Реализовать функццию, которая добавляет "рисует" паузу "-" на заданное в ф-ии время.
