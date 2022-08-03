import telegram
import time
import pytesseract
import config
import os
import numpy as np
try:
	from PIL import Image
except ImportError:
	from PIL import Image

intro = open("./messageConfig/intro.txt", "r")


# /setcommands
# lang - query or set your current language
# help - detailed information about the bot

DEFAULT_LANG = 'Eng+bnazanin'

lang_dict = {}

group_photos = {}

available_langs = {'eng' : 'English',
					'per' : 'Persian',
					'Eng+bnazanin':'eng+bnazanin'
					}

def start(update,context):
	context.bot.sendMessage(chat_id=update.message.chat_id,
		text= intro.read(),
		parse_mode=telegram.ParseMode.MARKDOWN,
		disable_web_page_preview=True)

def help(update,context):
	context.bot.sendMessage(chat_id=update.message.chat_id,
		text=help_text,
		parse_mode=telegram.ParseMode.MARKDOWN,
		disable_web_page_preview=True)

def unknown(update,context):
	f = open("./messageConfig/unknown.txt", "r")
	if update.message.chat_id > 0: # user	
		context.bot.sendMessage(chat_id=update.message.chat_id,
			text=f.read())

def message(update,context):
	if not update.message.photo:
		return

	photosize = context.bot.getFile(update.message.photo[-1].file_id)

	if update.message.chat_id > 0: # user	
		_photosize_to_parsed(update, context, photosize)

	else: # group
		group_photos[update.message.chat_id] = photosize


def tesseract(update,context):
	f = open("./messageConfig/tesseract.txt", "r")
	if update.message.chat_id > 0:
		context.bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
	else:
		_photosize_to_parsed(context.bot, update, group_photos[update.message.chat_id])

from io import BytesIO
def Photo(update,context): 
	file = context.bot.get_file(update.message.document.file_id)
	fileName=config.CACHE_DIR+'/photo_'+''.join(str(time.time()).split('.'))+'.png'

	file.download(fileName)

	try:
		language = lang_dict.get(update.message.chat_id, DEFAULT_LANG)
		image_text = pytesseract.image_to_string(Image.open(fileName), lang=language,config="--psm 3 --oem 1")
		if config.CACHE_TEMP:
			os.remove(fileName)

		sanitized_string = image_text
		print(sanitized_string)

		if sanitized_string:
			response_msg =' {} \n'.format(sanitized_string)
		else:
			f = open("./messageConfig/notFound.txt", "r")
			response_msg = f.read()
			## response_msg = 'هیچ چیز پیدا نشد! :( \nParsed in {}'.format(available_langs[language])

		context.bot.sendMessage(chat_id=update.message.chat_id,
						text=response_msg,
					parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as e:
		_something_wrong(update,context,e)


def _photosize_to_parsed(update,context, photosize):
	try:
		filename = config.CACHE_DIR+'/photo_'+''.join(str(time.time()).split('.'))+'.png'

		photosize.download(filename)

		language = lang_dict.get(update.message.chat_id, DEFAULT_LANG)
	
		image_text = pytesseract.image_to_string(Image.open(filename), lang='bnazanin',config="--psm 3 --oem 1")

		if config.CACHE_TEMP:
			os.remove(filename)

		sanitized_string = image_text
		print(sanitized_string)

		if sanitized_string:
			response_msg =' {} \n'.format(sanitized_string)
		else:
			f = open("./messageConfig/notFound.txt", "r")			
			response_msg = f.read()

		context.bot.sendMessage(chat_id=update.message.chat_id,
						text=response_msg,
					parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as e:
		_something_wrong(update, context, e)

def _something_wrong(update,context, e):
	f = open("./messageConfig/cautionError.txt", "r")
	context.bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
	## context.bot.sendMessage(chat_id=update.message.chat_id, text='مشکلی پیش آمده است، لطفا به نکات زیر در مورد فرستادن عکس دقت کنید:\nError type: {}\nError message: {}'.format(type(e), e))
