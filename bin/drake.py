from io import BytesIO
from os.path import abspath, join as path_join, split as path_split
from random import randint

from PIL import Image, ImageDraw, ImageFont

from bin.utils.files import Files
from bin.utils.logs import log_command, log_error

bin_path = path_split(abspath(__file__))[0]
font_path = path_join(bin_path, 'resources/fonts/raleway.ttf')
font = ImageFont.truetype(font_path, 32)


def drake(update, top, bottom):
    meme_format = ('drake', 'drake', 'robbie', 'babushka')[randint(0, 3)]
    img_path = path_join(bin_path, 'resources/drake/', f'{meme_format}.png')

    bio = BytesIO()
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    # Top, bottom y coordinates
    y1, y2 = 129, 387
    if not (__draw_text(draw, top, y1) and __draw_text(draw, bottom, y2)):
        log_error('Drake meme generation failed!')
        update.message.reply_photo(Files.drake, quote=True)
        return

    img.save(bio, 'PNG')
    bio.seek(0)
    update.message.reply_photo(bio, quote=True)
    log_command(update, 'DRAKE')


def __get_lines(text):
    w = font.getsize(text)[0]
    # Check if the entire block fits in a single line
    if w <= 320:
        return [text]

    text = text.split()
    # Iterate over words in reverse to find the largest block of text
    # that will fit in a single line.
    # After finding that, recurse to find the next line(s).
    for i in range(len(text), -1, -1):
        segment = ' '.join(text[:i])
        w = font.getsize(segment)[0]

        if w <= 320:
            remainder = ' '.join(text[i:])
            return [segment] + __get_lines(remainder)

    # If even a single word doesn't fit, we give up and raise a ValueError
    # TODO: Ideally should keep trying with smaller fonts
    #  until we reach a practical readability limit
    raise ValueError


def __draw_text(draw, t, y):
    # TODO: Make readable, fix param names
    t = t.strip()
    w, h = font.getsize(t)

    if w <= 320:
        draw.text((480 - (w / 2), y - (h / 2)), t, (255, 255, 255), font=font)
        return True

    try:
        lines = __get_lines(t)
    except ValueError:
        return False
    num_lines = len(lines)
    dims = [font.getsize(x) for x in lines]
    ws, hs = [x[0] for x in dims], [x[1] for x in dims]
    total = sum(hs)

    if total > 258:
        return False

    h = y - (total / 2)
    for i in range(num_lines):
        draw.text((480 - (ws[i] / 2), h), lines[i], (255, 255, 255), font=font)
        h += hs[i]

    return True
