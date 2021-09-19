"""
Copyright (C) 2020  Ishan Manchanda (@IshanManchanda)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from os import environ

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from bin.handlers import *

if 'TELEGRAM_TOKEN' not in environ:
	load_dotenv()
TOKEN = environ.get('TELEGRAM_TOKEN')


def main():
	updater = Updater(
		TOKEN, workers=32, use_context=True,
		request_kwargs={'read_timeout': 60, 'connect_timeout': 60}
	)

	handlers = [
		CommandHandler('start', start_handler, run_async=True),
		CommandHandler('help', help_handler, run_async=True),
		CommandHandler('changes', changes_handler, run_async=True),
		CommandHandler('cookbook', cookbook_handler, run_async=True),

		MessageHandler(
			Filters.regex('(?i)(^alt:)'),
			alt_handler, run_async=True
		),
		MessageHandler(
			Filters.regex('(?i)(^vaporize:)'),
			vaporize_handler, run_async=True
		),

		MessageHandler(Filters.reply, reply_handler, run_async=True),
		MessageHandler(Filters.text, main_handler, run_async=True),
		MessageHandler(Filters.all, all_handler, run_async=True),
	]

	dispatcher = updater.dispatcher
	dispatcher.add_error_handler(error_handler)
	for handler in handlers:
		dispatcher.add_handler(handler)

	if environ.get('ENVIRONMENT', None) == 'HEROKU':
		print('Starting Webhook')
		updater.start_webhook(
			listen='0.0.0.0',
			port=int(environ.get('PORT')),
			url_path=TOKEN,
			webhook_url="https://dankbot-tg.herokuapp.com/" + TOKEN
		)
		# updater.bot.setWebhook('https://dankbot-tg.herokuapp.com/' + TOKEN)
		updater.idle()
	else:
		print("Starting Polling")
		updater.start_polling()


if __name__ == '__main__':
	main()
