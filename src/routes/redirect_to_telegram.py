from flask import request
from flask_cors import cross_origin

import common.log as log
import variables
from telegram_bot.bot import bot

log.configure_logging(variables.REDIRECTION_TO_TELEGRAM_LOGFILE)


@cross_origin()
def redirection_to_telegram():
    try:
        content = request.json
        print(content)
        if content is not None:
            if content.get("name") is not None and \
                    content.get("phone") is not None:
                text = 'Имя: ' + content["name"] + '\nТелефон: ' + content["phone"] + '\n'
                if content['desc']:
                    text += 'Описание: ' + content["desc"]
                for user_id in variables.USERS_ID_TO_SEND:
                    bot.send_message(chat_id=user_id, text=text)
        else:
            log.logger.info('No JSON in request')
            return 'No JSON in request'
        return 'OK'
    except Exception as e:
        log.logger.exception(e)
        return "Error"
