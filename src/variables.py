TOKEN_PATH = '../bot_token'

with open(TOKEN_PATH, 'r') as f:
    TOKEN = f.readline().strip()

LOCAL = False

TELEGRAM_BOT_LOGFILE = '../logs/telegram_bot.log'

WEATHER_UPDATE_TIME = 15 * 60
TODAY_WEATHER_LOGFILE = '../logs/today_weather.log'
YANDEX_WEATHER_LOGFILE = TODAY_WEATHER_LOGFILE

TODAY_VOLUME_LOGFILE = '../logs/today_volume.log'
VOLUME_GENERATOR_LOGFILE = '../logs/volume_generator.log'

REDIRECTION_TO_TELEGRAM_LOGFILE = '../logs/redirection_to_telegram.log'
USERS_ID_TO_SEND = [197079657, 283754480]

MONGO_TODAY_VOLUME_COLL = 'volume_today'
MONGO_HISTORY_VOLUME_COLL = 'volume_history'

HISTORY_VOLUME_LOGFILE = '../logs/history_volume.log'
DATE_FORMAT = "%d.%m.%y"
