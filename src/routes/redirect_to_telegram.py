from flask import request
from flask_cors import cross_origin

import common.log as log
import variables
from telegram_bot.bot import bot

log.configure_logging(variables.REDIRECTION_TO_TELEGRAM_LOGFILE)

cols = {
    'tovar': 'Товар',
    'selected': 'Тип',
    'price': 'Цена',
    'quantity': 'Количество'
}

def handle_order(order_d):
    table = []
    goods = order_d['goods']
    table += ['  '.join([cols[k] for k in cols])]
    template = '  '.join(["{"+k+"}" for k in cols])

    for d in goods:
        table += [template.format(**d)]

    table += ['']
    table += ['Общая цена: ' + str(order_d['total_cost'])]

    text_table = '\n'.join(table)
    return text_table

@cross_origin()
def redirection_to_telegram():
    try:
        content = request.json
        if content is not None:
            text_a = []
            if content.get("name"):
                text_a += ['Имя: ' + content["name"]]
            
            if content.get("phone"):
                text_a += ['Телефон: ' + content["phone"]]
            
            if content.get('address'):
                text_a += ['Адрес: ' + content["address"]]

            if content.get('order'):
                text_a += ['\nЗаказ:\n' + handle_order(content["order"])]
            
            if content.get('desc'):
                text_a += ['\nОписание: ' + content["desc"]]
            if text_a:
                text = '\n'.join(text_a)
                for user_id in variables.USERS_ID_TO_SEND:
                    bot.send_message(chat_id=user_id, text=text)
        else:
            log.logger.info('No JSON in request')
            return 'No JSON in request'
        return 'OK'
    except Exception as e:
        log.logger.exception(e)
        return "Error"
