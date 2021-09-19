from telegram import Update
from telegram.ext import CallbackContext

from .drake import drake
from .helpers import helper_b, helper_despacito, helper_fry, helper_generate, \
	helper_gif, helper_image, helper_text
from .utils.logs import log_command, log_error, log_message
from .utils.text import changes, chars, commands, cookbook, vaportext


def error_handler(update: Update, context: CallbackContext):
	log_error(f'Update "{update}" caused error "{context.error}"')


def start_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(f'*This is DankBot!*\n{commands}', quote=True)
	log_command(update, 'START')


def help_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(commands, quote=True)
	log_command(update, 'HELP')


def changes_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(changes, quote=True)
	log_command(update, 'CHANGES')


def cookbook_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(cookbook, quote=True)
	log_command(update, 'COOKBOOK')


def alt_handler(update: Update, context: CallbackContext):
	text = update.message.text[4:].lower()
	result, upper = [update.message.from_user.first_name, ':'], False
	for i in text:
		if i.lower() in chars:
			result.append(i.upper() if upper else i.lower())
			upper = not upper
		else:
			result.append(i)
	if update.message.reply_text("".join(result), quote=True):
		update.message.delete()
	log_command(update, 'ALT')


def vaporize_handler(update: Update, context: CallbackContext):
	text = update.message.text[10:]
	result = [update.message.from_user.first_name, ':']
	for i in text:
		if i in vaportext:
			result.append(vaportext[i])
		else:
			result.append(i)
	if update.message.reply_text("".join(result)):
		update.message.delete()
	log_command(update, 'VAPORIZE')


def reply_handler(update: Update, context: CallbackContext):
	if helper_fry(update, context):
		return

	if helper_generate(update, context):
		return

	main_handler(update, context)


def main_handler(update: Update, context: CallbackContext):
	if not update.message or not update.message.text:
		return

	text_c = update.message.text
	text = text_c.lower()
	words = text.split()

	if ', not ' in text:
		drake(
			update,
			text_c[text.find(', not ') + 6:],
			text_c[:text.find(', not ')]
		)

	elif '🅱️' in text:
		helper_b(update, text)

	elif 'dankbot play despacito' in text or 'alexa play despacito' in text:
		helper_despacito(update, text)

	elif helper_gif(update, text, words):
		return

	elif helper_image(update, text, words):
		return

	elif helper_text(update, text, words):
		return

	else:
		log_message(update)


def all_handler(update: Update, context: CallbackContext):
	if not update.message:
		return

	log_message(update)
	if update.message.chat.id != 623912829:
		return

	update.message.reply_text(
		update.message.animation.file_id if update.message.animation
		else update.message.audio.file_id if update.message.audio
		else update.message.document.file_id if update.message.document
		else update.message.photo[::-1][0].file_id if update.message.photo
		else update.message.video.file_id if update.message.video
		else update.message.video_note.file_id if update.message.video_note
		else update.message.voice.file_id if update.message.voice
		else update.message,
		quote=True
	)
