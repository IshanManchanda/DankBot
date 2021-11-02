from os import environ, remove
from os.path import abspath, isfile, join as path_join, split as path_split

from PIL import Image, ImageEnhance, ImageOps
from numba import njit
from numpy import arcsin, arctan, array, copy, pi, sin, sqrt, square, sum
from numpy.random import normal, random
from pyimgur import Imgur
from time import sleep

from bin.cv import find_chars, find_eyes
from bin.utils.logs import log_debug, log_error, log_warn

bin_path = path_split(abspath(__file__))[0]


def __fry(
        img, number_of_cycles, number_of_emojis,
        bulge_probability, laser, vitamin_b
):
    log_debug('__fry starting')
    if laser:
        log_debug('Finding eye coordinates')
        coords = find_eyes(img)
        if coords:
            log_debug('Eye coordinates found')
            img = __add_lasers(img, coords)
            log_debug('Laser eyes added')
        else:
            log_debug('No eye coordinates found')

    if vitamin_b:
        log_debug('Finding char coordinates')
        coords = find_chars(img)
        if coords:
            log_debug('Char coordinates found')
            img = __add_b(img, coords, number_of_emojis / 20)
            log_debug('"B"s added')
        else:
            log_debug('No char coordinates found')

    log_debug('Adding emojis')
    img = __add_emojis(img, number_of_cycles * number_of_emojis)
    log_debug('emojis added')

    log_debug('Adding bulges')
    img = __add_bulges_helper(img, number_of_cycles, bulge_probability)
    log_debug('Bulges added, __fry completed')
    return img


def __posterize(img, p):
    return ImageOps.posterize(
        img,
        4 if p == 4 else 6 if p == 1 else 5
    )


def __sharpen(img, p):
    return ImageEnhance.Sharpness(img).enhance(
        (img.width * img.height * p / 3200) ** 0.4
    )


def __increase_contrast(img, p):
    return ImageEnhance.Contrast(img).enhance(normal(1.8, 0.8) * p / 2)


def __colorize(img, p):
    return ImageEnhance.Color(img).enhance(normal(2.5, 1) * p / 2)


def __add_lasers(img, coords):
    if not coords:
        return img
    tmp = img.copy()

    laser = Image.open(path_join(bin_path, 'resources/frying/laser1.png'))
    for coord in coords:
        tmp.paste(
            laser, (
                int(coord[0] - laser.size[0] / 2),
                int(coord[1] - laser.size[1] / 2)
            ), laser
        )

    return tmp


def __add_b(img, coords, c):
    tmp = img.copy()

    b = Image.open(path_join(bin_path, 'resources/frying/b.png'))
    for coord in coords:
        if random(1)[0] < c:
            resized = b.copy()
            resized.thumbnail((coord[2], coord[3]), Image.ANTIALIAS)
            tmp.paste(resized, (int(coord[0]), int(coord[1])), resized)

    return tmp


def __add_emojis(img, m):
    emojis = ['100', 'fire', 'hmmm', 'laugh', 'ok', ]
    tmp = img.copy()

    for e in emojis:
        emoji = Image.open(path_join(bin_path, 'resources/frying/%s.png' % e))
        for _ in range(int(random(1)[0] * m)):
            coord = random(2) * array([img.width, img.height])
            size = int((img.width / 10) * (random(1)[0] + 1)) + 1
            theta = random(1)[0] * 360

            resized = emoji.copy()
            resized = resized.rotate(theta)
            resized.thumbnail((size, size), Image.ANTIALIAS)
            tmp.paste(resized, (int(coord[0]), int(coord[1])), resized)

    return tmp


def __add_bulges_helper(img, number_of_cycles, bulge_probability):
    w, h = img.width - 1, img.height - 1
    if w * h > 9000000:
        return img

    img_data = array(img)
    for _ in range(number_of_cycles):
        if random(1)[0] > bulge_probability:
            continue

        # (img, coords, radius, flatness, h, ior)
        img_data = __add_bulges(
            img_data, array([w, h]),
            array([
                int(w * random(1)),
                int(h * random(1))
            ]),
            int(((img.width + img.height) / 10) * (random(1)[0] + 1)),
            1 + random(3)[0],
            6 + random(2)[0],
            1.2 + random(2)[0]
        )
        log_debug('Bulge generated')

    return Image.fromarray(img_data)


@njit(fastmath=True)
def __add_bulges(img_data, size, coords, radius, flatness, h, ior):
    """
    Creates a bulge like distortion to the image

    :param img_data: Image as a numpy array
    :type img_data: numpy.array
    :param coords: Numpy Array with Coordinates of Centre of Bulge
    :type coords: numpy.array
    :param radius: Radius of Bulge
    :type radius: int
    :param flatness: Flatness: 1 for Spherical, > 1 for Flat.
    :type flatness: int
    :param h: Height of Bulge
    :type h: int
    :param ior: Index of Refraction of Bulge Material
    :type ior: float
    :return: The Bulged Image
    :rtype: PIL.Image
    """

    # Determine range of pixels to be checked (square enclosing bulge)
    x_min = int(coords[0] - radius)
    if x_min < 0:
        x_min = 0
    x_max = int(coords[0] + radius)
    if x_max > size[0]:
        x_max = size[0]
    y_min = int(coords[1] - radius)
    if y_min < 0:
        y_min = 0
    y_max = int(coords[1] + radius)
    if y_max > size[1]:
        y_max = size[1]

    # Array for holding bulged image
    bulged = copy(img_data)
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            ray = array([x, y])

            # Find the magnitude of displacement
            # in the xy plane between the ray and focus
            s = sqrt(sum(square(ray - coords)))

            # If the ray is in the centre of the bulge or beyond the radius,
            # it doesn't need to be modified
            if not 0 < s < radius:
                continue

            # Slope of the bulge relative to xy plane at (x, y) of the ray
            m = -s / (flatness * sqrt(radius ** 2 - s ** 2))

            # Find the angle between the ray and the normal of the bulge
            theta = pi / 2 + arctan(1 / m)

            # Find the magnitude of the angle between
            # the XY plane and refracted ray using Snell's Law

            # s >= 0 -> m <= 0 -> arctan(-1/m) > 0,
            # but ray is below xy plane so we want a negative angle
            # arctan(-1/m) is therefore negated
            phi = abs(arctan(1 / m) - arcsin(sin(theta) / ior))

            # Find length the ray travels in xy plane before hitting z=0
            k = (h + (sqrt(radius ** 2 - s ** 2) / flatness)) / sin(phi)

            # Find intersection point
            normalized = (coords - ray) / sqrt(sum(square(coords - ray)))
            intersect = ray + normalized * k

            # Assign pixel the colour of pixel at intersection
            if 0 < intersect[0] < size[0] and 0 < intersect[1] < size[1]:
                bulged[y][x] = img_data[int(intersect[1])][int(intersect[0])]
            else:
                # No light reaching the pixel
                bulged[y][x] = [0, 0, 0]

    return bulged


def __upload_to_imgur(path, caption):
    log_debug('__upload started')
    if not isfile(path):
        log_warn('File to be uploaded not found')
        return

    # TODO: Convert to GIF and upload.
    if path[-3:] == 'mp4':
        remove(path)
        log_warn('Skipping mp4 upload')
        return

    log_debug('Authorizing imgur client')
    im = Imgur(
        environ.get('IMGUR_CLIENT_ID'),
        environ.get('IMGUR_CLIENT_KEY'),
        environ.get('IMGUR_ACCESS_TOKEN'),
        environ.get('IMGUR_REFRESH_TOKEN')
    )

    for _ in range(5):
        try:
            im.upload_image(
                path=abspath(path),
                title=caption,
                album=environ.get('IMGUR_ALBUM')
            )
            log_debug('Image successfully uploaded')
            break
        except Exception:
            log_warn('Upload failed, refreshing token')
            im.refresh_access_token()
            sleep(10)
            continue
    else:
        log_error('Upload failed, proceeding')

    log_debug('Deleting file')
    remove(path)
    return


def __get_caption(name, number_of_cycles, args):
    caption = 'Requested by %s, %d Cycle(s) of%sfrying. %s, %s' % (
        name,
        number_of_cycles,
        ' Deep ' if args['deep'] else ' Shallow ' if args['shallow'] else ' ',
        (
            'High-fat' if args['high-fat']
            else 'Low-fat' if args['low-fat']
            else 'No-fat' if args['no-fat']
            else 'Normal-fat'
        ),
        (
            'Heavy' if args['heavy']
            else 'Light' if args['light']
            else 'Classic'
        )
    )
    if args['no-chilli']:
        if args['vitamin-b']:
            return f'{caption}, with added Vitamin-B and no Chilli.'

        return f'{caption}, without Chilli.'

    if args['vitamin-b']:
        return f'{caption}, with added Vitamin-B.'
    return f'{caption}.'
