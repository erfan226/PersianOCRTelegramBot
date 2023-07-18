# PersianOCRTelegramBot

## How to use
1. Install the requirements `pip install -r requirements`
2. Create the config file `touch src/config.py`
2. Add your API token (from Telegram's BotFather) and add to the config file (read below)
3. Install the requirments listed below:
<pre>
sudo apt-get update
sudo apt-get upgrade
sudo apt install tesseract-ocr
sudo apt-get install tesseract-ocr-fas
</pre>
4. Run the bot with `python src/tesseract_bot.py`
## Config file
Place this in your config file:
<pre>
BOT_TOKEN='Your_API_Key'
CACHE_DIR='../cache'
CACHE_TEMP=False
</pre>