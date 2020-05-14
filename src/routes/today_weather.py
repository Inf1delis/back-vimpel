from flask import jsonify
from flask_cors import cross_origin

from common.extensions import cache
from scripts.yandex_weather import yandex_weather
import variables

import common.log as log
log.configure_logging(variables.TODAY_WEATHER_LOGFILE)


@cross_origin()
@cache.cached(timeout=variables.WEATHER_UPDATE_TIME)
def today_weather():
    try:
        log.logger.info("All OK")
        return jsonify(yandex_weather())
    except Exception as e:
        log.logger.exception(e)
        return "Error"
