#! /usr/bin/env python3

import logging
import handler
import argparse
import config
import errno
import os
from telegram.ext import Updater
from telegram.ext import MessageHandler, filters
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def resolve_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG,
							format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
	resolve_args()
	os.chdir(os.path.split(os.path.abspath(__file__))[0])

	try:
	    os.mkdir(config.CACHE_DIR)
	except OSError as e:
	    if e.errno != errno.EEXIST:
	        raise e

	app = ApplicationBuilder().token(config.BOT_TOKEN).build()

	app.add_handler(MessageHandler(filters.Document.MimeType("image/jpeg"), handler.Photo))
	app.add_handler(MessageHandler(filters.Document.MimeType("image/png"), handler.Photo))
	app.add_handler(MessageHandler(filters.Document.MimeType("image/jpg"), handler.Photo))

	start_handler = CommandHandler('start', handler.start)
	app.add_handler(start_handler)

	help_handler = CommandHandler('help', handler.help)
	app.add_handler(help_handler)

	tesseract_handler = CommandHandler('tesseract', handler.tesseract)
	app.add_handler(tesseract_handler)

	# message_handler = MessageHandler(filters._Photo, handler.message)
	message_handler = MessageHandler(filters.Document.MimeType("image/jpeg"), handler.message)
	app.add_handler(message_handler)

	# unknown_handler = MessageHandler(filters.Command,handler.unknown)
	unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handler.unknown)
	app.add_handler(unknown_handler)

	app.run_polling()

if __name__ == '__main__':
	main()
