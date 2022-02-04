import time
import os
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
VK_AUTH_TOKEN = os.getenv('VK_AUTH_TOKEN')

run_flag = None


def start(update, context):
    global run_flag
    run_flag = True
    update.message.reply_text('Hello! Give me the user ID!')

def stop(update, context):
    global run_flag
    run_flag = False
    update.message.reply_text("Okay! I'm going to bed.")


def get_status(user_id):
    params = {
        'user_ids': str(user_id),
        'fields': 'online',
        'v': '5.92',
        'access_token': VK_AUTH_TOKEN
    }
    user = requests.post('https://api.vk.com/method/users.get', params=params)
    user = user.json()['response']
    user_status = user[0]['online']
    return user_status


def reply(update, context):
    user_id = update.message.text
    status = get_status(user_id)
    if status == 1:
        update.message.reply_text(f"User vk.com/{user_id} is online!")
    elif status != (1 and 0):
        update.message.reply_text(f"User vk.com/{user_id} cannot be found!")
    elif status == 0:
        update.message.reply_text(f"User vk.com/{user_id} is offline. I will "
                                  f"let you know, when the status changes.")
        while run_flag:
            status = get_status(user_id)
            if status == 1:
                update.message.reply_text(f"User vk.com/{user_id} is online!")
                break
            time.sleep(5)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()


if __name__ == '__main__':
    main()
