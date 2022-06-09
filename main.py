import cv2
import numpy
import copy
import time
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
FONT_COLOR = (13, 42, 13) # BGR

FONT_ENC = ImageFont.truetype("ArialBD.ttf", size=FONT_SIZE, encoding='UTF-8')
IMAGE_EMPTY = Image.new('RGB', FRAME, color=COLOR_WHITE)


def get_video_writer(output_filename: str):
    return cv2.VideoWriter(os.path.join(OUTPUT_FILE_PATH, f"{output_filename}.avi"), fourcc, FPS_OUT, (FRAME[0], FRAME[1]))


def pause_generate(video_writer, frames_count: int = 1, symb: str = "-"):
    image = copy.copy(IMAGE_EMPTY)
    draw = ImageDraw.Draw(image)

    w, h = draw.textsize(symb, FONT_ENC)
    draw.text(
        ((FRAME[0] - w) // 2, (FRAME[1] - h) // 2),
        symb,
        font=FONT_ENC,
        fill=FONT_COLOR
    )

    recframe = numpy.array(image)

    for i in range(int(frames_count)):
        video_writer.write(recframe)


def string_to_vid_generate(input_str):
    image = copy.copy(IMAGE_EMPTY)
    draw = ImageDraw.Draw(image)

    w, h = draw.textsize(input_str, FONT_ENC)

    draw.text(
            ((FRAME[0] - w) // 2, (FRAME[1] - h) // 2),
            input_str,
            font=FONT_ENC,
            fill=FONT_COLOR
            )

    vout = get_video_writer(input_str)
    recframe = numpy.array(image)
    # FIXME: поменять "волшебную" зависимость от FPS_OUT, заменить на необхобимое время отрисовки
    # FIXME: добивать default- значение в шапку функции
    for i in range(int(FPS_OUT) * 5):
        vout.write(recframe)
    vout.release()


def book_to_vid_generate(txt_file_path):
    OUTPUT_FILE_NAME = "book_to_vid_generate"

    vout = get_video_writer(OUTPUT_FILE_NAME)

    pause_generate(vout, 60)

    with open(txt_file_path, 'r', encoding="utf-8") as _file:
        _file_lines = _file.read().splitlines()
        _l_counter = 0
        lines_count = len(_file_lines)

    # FIXME: ADD BUFFER VARIABLE FOR "-"-type SEPARATE SYMBOLS
    for _one_line in _file_lines:
        print(f"{lines_count - _l_counter} lines")
        _l_counter += 1

        for _one_word in _one_line.split():
            image = copy.copy(IMAGE_EMPTY)
            draw = ImageDraw.Draw(image)

            w, h = draw.textsize(_one_word, FONT_ENC)

            draw.text(
                ((FRAME[0] - w) // 2, (FRAME[1]) // 2),
                _one_word,
                font=FONT_ENC,
                fill=FONT_COLOR  # TEXT COLOR
            )

            recframe = numpy.array(image)

            # APPEND x FRAMES
            for i in range(6):
                vout.write(recframe)

    vout.release()


if __name__ == "__main__":

    start_time = time.time()

    book_to_vid_generate(INPUT_FILE_PATH)

    print(f"{time.time() - start_time:.2f} - sec's")

# FIXME: Проверка наличия "выходной папки", перед запуском генерации, создавать папку, при отсутствии
