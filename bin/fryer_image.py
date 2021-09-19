from io import BytesIO
from os.path import abspath, split as path_split
from random import shuffle
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from PIL import Image
from time import sleep

from bin.fryer import __colorize, __fry, __get_caption, __increase_contrast, \
	__posterize, __sharpen, __upload_to_imgur
from bin.utils.logs import log_debug, log_error, log_warn

bin_path = path_split(abspath(__file__))[0]


def fry_image(update, url, number_of_cycles, args):
	log_debug('Starting Image Fry')
	number_of_emojis = (
		3 if args['high-fat']
		else 1 if args['low-fat']
		else 0 if args['no-fat']
		else 2
	)
	bulge_probability = (
		0.75 if args['heavy']
		else 0 if args['light']
		else 0.45
	)
	magnitude = (
		4 if args['deep']
		else 1 if args['shallow']
		else 2
	)

	bio = BytesIO()
	name = update.message.from_user.first_name
	bio.name = filename = '%s_%s_%s.png' % (
		update.message.chat_id,
		name,
		update.message.message_id
	)

	filepath = f'{bin_path}/temp/{filename}'
	caption = __get_caption(name, number_of_cycles, args)

	success, img = __get_image(url)
	if not success:
		log_error('Image download failed')
		return
	log_debug('Image successfully downloaded')

	img = __fry(
		img, number_of_cycles, number_of_emojis,
		bulge_probability, not args['no-chilli'], args['vitamin-b']
	)

	log_debug('Frying effects starting')
	fs = [__posterize, __sharpen, __increase_contrast, __colorize]
	for _ in range(number_of_cycles):
		shuffle(fs)
		for f in fs:
			img = f(img, magnitude)
	log_debug('Frying effects applied')

	img.save(bio, 'PNG')
	bio.seek(0)
	update.message.reply_photo(bio, caption=caption, quote=True)

	log_debug('Image saved and replied')

	img.save(filepath, 'PNG')
	__upload_to_imgur(filepath, caption)
	log_debug('Image frying process completed')


def __get_image(url):
	for _ in range(5):
		try:
			return 1, Image.open(BytesIO(urlopen(url).read()))
		except (HTTPError, URLError):
			sleep(1)
		except (OSError, UnboundLocalError):
			log_error('OSError while retrieving image')
			return 0, None
	log_warn('Quitting loop while retrieving image')
	return 0, None
