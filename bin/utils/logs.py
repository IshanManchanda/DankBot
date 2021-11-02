from datetime import datetime
from inspect import currentframe, getframeinfo

from pytz import timezone
from sys import stdout


def log_debug(message):
    cf = currentframe()
    file = getframeinfo(cf.f_back).filename
    line = cf.f_back.f_lineno
    timestamp = datetime.now(tz=timezone('Asia/Kolkata'))

    stdout.write(f'DEBUG {timestamp} <line {line}, {file}>: {message}\n')


def log_info(message):
    timestamp = datetime.now(tz=timezone('Asia/Kolkata'))
    stdout.write(f'INFO {timestamp}: {message}\n')


def log_warn(message):
    cf = currentframe()
    file = getframeinfo(cf.f_back).filename
    line = cf.f_back.f_lineno
    timestamp = datetime.now(tz=timezone('Asia/Kolkata'))

    stdout.write(f'WARN {timestamp} <line {line}, {file}>: {message}\n')


def log_error(message):
    cf = currentframe()
    file = getframeinfo(cf.f_back).filename
    line = cf.f_back.f_lineno
    timestamp = datetime.now(tz=timezone('Asia/Kolkata'))

    stdout.write(f'ERROR {timestamp} <line {line}, {file}>: {message}\n')


def log_command(update, command):
    log_info(f'{{{command}}} {generate_log_message(update)}')


def log_message(update):
    log_info(generate_log_message(update))


def generate_log_message(update):
    return (
        '(%s[%s]) %s[%s]: %s' % (
            update.message.chat.title,
            update.message.chat.id,
            update.message.from_user.first_name,
            update.message.from_user.id,
            'TEXT' if update.message.text else 'MEDIA'
        )
        if update.message.chat.type != 'private' else
        '%s[%s]: %s' % (
            update.message.from_user.first_name,
            update.message.from_user.id,
            'TEXT' if update.message.text else 'MEDIA'
        )
    )

# REVIEW: Consider adding actions "DankBot is typing" for long actions
#  such as frying, meme generation, etc.
# from functools import wraps
#
#
# def send_action(action):
# 	"""Sends `action` while processing func command."""
#
# 	def decorator(func):
# 		@wraps(func)
# 		def command_func(update, context, *args, **kwargs):
# 			context.bot.send_chat_action(
# 			chat_id=update.effective_message.chat_id, action=action)
# 			return func(update, context, *args, **kwargs)
#
# 		return command_func
#
# 	return decorator
