from flask_cors import cross_origin
from flask import jsonify
import datetime
import variables

from common.mongo import db, server
today_volume_coll = db.get_collection(variables.MONGO_TODAY_VOLUME_COLL)

import common.log as log
log.configure_logging(variables.TODAY_VOLUME_LOGFILE)

from scripts.volume_generate import volume_generate


@cross_origin()
def today_volume():
    try:
        today = datetime.datetime.today()
        hours = str(datetime.datetime(today.year, today.month, today.day, today.hour, 0, 0).time())

        today_volume = today_volume_coll.find_one()

        if today_volume is None or today.strftime(variables.DATE_FORMAT) != today_volume['day_total']['date']:
            today_volume = volume_generate(today)
        elif variables.LOCAL:
            server.close()

        return jsonify(today_volume[hours])
    except Exception as e:
        log.logger.exception(e)
        return "Error"
