from telegram.ext import Updater, CommandHandler
from config.auth import token
import json
import requests
import subprocess
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('CasetaMagentaBot')

def start(bot, update):
    logger.info('He recibido un comando start')
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hi Master, I'm here to server you!! "
    )

def status(bot, update):
    logger.info('He recibido un comando Status')
    r = requests.get('http://192.168.88.200:4040/api/tunnels', json={"key": "value"})
    if r.status_code == 200:
        response = r.json()
        botAnswer = response['tunnels'][0]['public_url']
        logger.info(botAnswer)
    elif r.status_code == 404:
        loger.error('Not Found.')
        botAnswer = "No se puede consultar el estatus del puerto"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=botAnswer
    )

def up(bot, update):
    logger.info('He recibido un comando UP')
    p = subprocess.Popen("sudo service ngrok start", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    logger.info("Command output : ", output)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Encendiedo servicio de VPN y forwardeo de puerto "
    )

def down(bot, update):
    logger.info('He recibido un comando DOWN')
    p = subprocess.Popen("sudo service ngrok stop", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    logger.info("Command output : ", output)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Apagando servicio de VPN y forwarding"
    )

if __name__ == '__main__':

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('ping', start))
    dispatcher.add_handler(CommandHandler('statusport', status))
    dispatcher.add_handler(CommandHandler('up', up))
    dispatcher.add_handler(CommandHandler('down', down))

    updater.start_polling()
    updater.idle()


