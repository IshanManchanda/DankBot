from io import BytesIO
from os.path import abspath, join as path_join, split as path_split
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont
from time import sleep

bin_path = path_split(abspath(__file__))[0]
font_path = path_join(bin_path, 'resources/fonts/impact.ttf')
s1 = ImageFont.truetype(font_path, 1)


def generate(update, url, top: str, bottom: str):
    top = top.replace('\n', '')
    bottom = bottom.replace('\n', '')
    bio = BytesIO()

    for _ in range(5):
        try:
            img = Image.open(BytesIO(urlopen(url).read()))
            draw = ImageDraw.Draw(img)
            w, h = img.width, img.height
            w900, h20 = 9 * w, h // 5
            st, lt = __calculate_size(top, w900, h20)
            sb, lb = __calculate_size(bottom, w900, h20)
            if (
                    __draw_top(draw, lt, w, h, st)
                    and __draw_bottom(draw, lb, w, h, sb)
            ):
                img.save(bio, 'PNG')
                bio.seek(0)
                update.message.reply_photo(bio, quote=True)
                return
            return
        except (HTTPError, URLError):
            sleep(1)

        except (OSError, UnboundLocalError, IndexError):
            return


def __calculate_size(t, w900, h20):
    t = t.strip()
    w90 = w900 // 10
    n = w900 // (4 * s1.getsize(t)[0])
    fs = list(range(1, n + 1))

    while len(fs) > 1:
        i = len(fs) // 2
        font = ImageFont.truetype(font_path, fs[i])
        lines = __get_lines(t, w90, font)
        dims = [font.getsize(x) for x in lines]
        total = sum([x[1] for x in dims])
        if (len(lines) < 3) and (total < h20):
            fs = fs[i:]
        else:
            fs = fs[:i]

    lines = __get_lines(t, w90, ImageFont.truetype(font_path, fs[0]))
    if fs[0] == 1:
        return 1, lines
    if len(lines) > 2:
        return (
            fs[0] - 1,
            __get_lines(t, w90, ImageFont.truetype(font_path, fs[0] - 1))
        )
    return fs[0], lines


def __draw_top(draw, lines, w, h, f):
    font = ImageFont.truetype(font_path, f)
    num_lines = len(lines)
    dims = [font.getsize(x) for x in lines]

    y = h // 100
    for i in range(num_lines):
        __draw(draw, lines[i], (w - dims[i][0]) // 2, y, font)
        y += dims[i][1]

    return True


def __draw_bottom(draw, lines, w, h, f):
    font = ImageFont.truetype(font_path, f)
    num_lines = len(lines)
    dims = [font.getsize(x) for x in lines]

    y = (h * 99) // 100
    for i in range(num_lines - 1, -1, -1):
        y -= dims[i][1]
        __draw(draw, lines[i], (w - dims[i][0]) // 2, y, font)

    return True


def __draw(draw, t, x, y, font):
    draw.text((x - 2, y), t, (0, 0, 0), font=font)
    draw.text((x + 2, y), t, (0, 0, 0), font=font)
    draw.text((x, y - 2), t, (0, 0, 0), font=font)
    draw.text((x, y + 2), t, (0, 0, 0), font=font)
    draw.text((x, y), t, (255, 255, 255), font=font)


def __get_lines(t, mw, f):
    t.strip()
    w, _ = f.getsize(t)
    if (w <= mw) or (" " not in t):
        return [t]

    t = t.split(" ")
    for i in range(len(t), -1, -1):
        w, _ = f.getsize(" ".join(t[:i]))
        if w <= mw:
            return [" ".join(t[:i])] + __get_lines(" ".join(t[i:]), mw, f)

    return [t]
