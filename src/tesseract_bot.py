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

	updater = ApplicationBuilder().token(config.BOT_TOKEN).build()

	updater.add_handler(MessageHandler(filters.Document.MimeType("image/jpeg"), handler.Photo))
	updater.add_handler(MessageHandler(filters.Document.MimeType("image/png"), handler.Photo))
	updater.add_handler(MessageHandler(filters.Document.MimeType("image/jpg"), handler.Photo))

	start_handler = CommandHandler('start', handler.start)
	updater.add_handler(start_handler)

	help_handler = CommandHandler('help', handler.help)
	updater.add_handler(help_handler)

	tesseract_handler = CommandHandler('tesseract', handler.tesseract)
	updater.add_handler(tesseract_handler)

	# message_handler = MessageHandler(filters._Photo, handler.message)
	message_handler = MessageHandler(filters.Document.MimeType("image/jpeg"), handler.message)
	updater.add_handler(message_handler)

	# unknown_handler = MessageHandler(filters.Command,handler.unknown)
	unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handler.unknown)
	updater.add_handler(unknown_handler)

	updater.run_polling()

if __name__ == '__main__':
	main()
