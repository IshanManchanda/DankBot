from io import BytesIO
from os.path import abspath, join as path_join, split as path_split
from random import randint

from PIL import Image, ImageDraw, ImageFont

from bin.utils.files import Files
from bin.utils.logs import log_command, log_error

bin_path = path_split(abspath(__file__))[0]
font_path = path_join(bin_path, 'resources/fonts/raleway.ttf')
font = ImageFont.truetype(font_path, 32)


def drake(update, top_text, bottom_text):
    meme_format = ('drake', 'drake', 'robbie', 'babushka')[randint(0, 3)]
    img_path = path_join(bin_path, 'resources/drake/', f'{meme_format}.png')

    bio = BytesIO()
    img = Image.open(img_path)
    draw_obj = ImageDraw.Draw(img)

    # Manually identified top and bottom y coordinates
    y_top, y_bottom = 129, 387
    if not (
            __draw_text(draw_obj, top_text, y_top) and
            __draw_text(draw_obj, bottom_text, y_bottom)
    ):
        log_error('Drake meme generation failed!')
        update.message.reply_photo(Files.drake, quote=True)
        return

    img.save(bio, 'PNG')
    bio.seek(0)
    update.message.reply_photo(bio, quote=True)
    log_command(update, 'DRAKE')


def __get_lines(text):
    text_width = font.getsize(text)[0]
    # Check if the entire block fits in a single line
    if text_width <= 320:
        return [text]

    text = text.split()
    # Iterate over words in reverse to find the largest block of text
    # that will fit in a single line.
    # After finding that, recurse to find the next line(s).
    for i in range(len(text), -1, -1):
        chosen_prefix = ' '.join(text[:i])
        text_width = font.getsize(chosen_prefix)[0]

        if text_width <= 320:
            remaining_suffix = ' '.join(text[i:])
            return [chosen_prefix] + __get_lines(remaining_suffix)

    # If even a single word doesn't fit, we give up and raise a ValueError
    # REVIEW: Ideally should keep trying with smaller fonts
    #  until we reach a practical readability limit?
    raise ValueError


def __draw_text(draw_obj, text, y_coordinate):
    text = text.strip()
    text_width, text_height = font.getsize(text)
    color = (255, 255, 255)

    # Check if text width within limit
    if text_width <= 320:
        x_center = 480 - (text_width / 2)
        y_center = y_coordinate - (text_height / 2)
        draw_obj.text((x_center, y_center), text, color, font=font)
        return True

    # Else try multi-line
    try:
        lines = __get_lines(text)
    # Value error thrown if even a single word doesn't fit in a line
    except ValueError:
        return False

    # Get the number of lines and dimensions of each
    num_lines = len(lines)
    dims = [font.getsize(x) for x in lines]
    line_widths, line_heights = [x[0] for x in dims], [x[1] for x in dims]

    # Check if total height greater than acceptable
    total_height = sum(line_heights)
    if total_height > 258:
        return False

    # Compute y-coordinate for line 1
    y_center = y_coordinate - (total_height / 2)
    for i in range(num_lines):
        x_center = 480 - (line_widths[i] / 2)
        draw_obj.text((x_center, y_center), lines[i], color, font=font)
        # Increment next y-coordinate by current line's height
        y_center += line_heights[i]

    return True
