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

# pytesseract.pytesseract.Y = ( r'/usr/bin/tesseract' )
intro = open("src/messageConfig/intro.txt", "r")

# /setcommands
# lang - query or set your current language
# help - detailed information about the bot

# DEFAULT_LANG = 'Eng+bnazanin'
DEFAULT_LANG = 'fas'

lang_dict = {}

group_photos = {}

available_langs = {'eng' : 'English',
					'fas' : 'Persian',
					'Eng+bnazanin':'eng+bnazanin'
					}

async def start(update, context):
	await context.bot.sendMessage(chat_id=update.message.chat_id,
		text= intro.read())

async def help(update, context):
	await context.bot.sendMessage(chat_id=update.message.chat_id,
		text="help_text")

async def unknown(update, context):
	f = open("messageConfig/unknown.txt", "r")
	if update.message.chat_id > 0: # user	
		await context.bot.sendMessage(chat_id=update.message.chat_id,
			text=f.read())

async def message(update, context):
	if not update.message.photo:
		return

	photosize = await context.bot.getFile(update.message.photo[-1].file_id)

	if update.message.chat_id > 0: # user	
		_photosize_to_parsed(update, context, photosize)

	else: # group
		group_photos[update.message.chat_id] = photosize


async def tesseract(update,context):
	f = open("messageConfig/tesseract.txt", "r")
	if update.message.chat_id > 0:
		await context.bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
	else:
		await _photosize_to_parsed(context.bot, update, group_photos[update.message.chat_id])

from io import BytesIO
async def Photo(update,context): 
	doc = await context.bot.get_file(update.message.document.file_id)
	fileName=config.CACHE_DIR+'/photo_'+''.join(str(time.time()).split('.'))+'.png'
	await doc.download_to_drive(fileName)
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
			f = open("messageConfig/notFound.txt", "r")
			response_msg = f.read()
			## response_msg = 'هیچ چیز پیدا نشد! :( \nParsed in {}'.format(available_langs[language])

		await context.bot.sendMessage(chat_id=update.message.chat_id,
			text=response_msg)
	except Exception as e:
		# await context.bot.sendMessage(chat_id=update.message.chat_id, text=e)
		await _something_wrong(update, context,e)

async def _photosize_to_parsed(update,context, photosize):
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
			f = open("messageConfig/notFound.txt", "r")			
			response_msg = f.read()

		context.bot.sendMessage(chat_id=update.message.chat_id,
						text=response_msg,
					parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as e:
		_something_wrong(update, context, e)

async def _something_wrong(update,context, e):
	f = open("messageConfig/cautionError.txt", "r")
	context.bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
	## context.bot.sendMessage(chat_id=update.message.chat_id, text='مشکلی پیش آمده است، لطفا به نکات زیر در مورد فرستادن عکس دقت کنید:\nError type: {}\nError message: {}'.format(type(e), e))
