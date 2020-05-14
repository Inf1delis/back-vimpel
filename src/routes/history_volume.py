import datetime

from flask import request, jsonify
from flask_cors import cross_origin

import variables
from common.mongo import db, server

history_volume_coll = db.get_collection(variables.MONGO_HISTORY_VOLUME_COLL)

import common.log as log

log.configure_logging(variables.HISTORY_VOLUME_LOGFILE)

from scripts.volume_generate import volume_generate


@cross_origin()
def history_volume(from_rec=0, to_rec=15):
    try:
        if request.json is not None:
            content = request.json
            from_rec = content.from_rec
            to_rec = content.to_rec

        records = list(history_volume_coll.find({}, {'_id': False}))
        if variables.LOCAL:
            server.close()

        try:
            history = records[from_rec: to_rec]
        except IndexError:
            history = records[from_rec:]
        history = history[::-1]

        if history is not None:
            today = datetime.date.today()
            if today.strftime(variables.DATE_FORMAT) != history[0]['date']:
                volume_generate(today)

        return jsonify(history)
    except Exception as e:
        log.logger.exception(e)
        return "Error"
