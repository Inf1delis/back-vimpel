from telegram import Bot

import variables

bot = Bot(token=variables.TOKEN)

# import common.log as log
# log.configure_logging(variables.TELEGRAM_BOT_LOGFILE)

# update_id = None

# try:
#     update_id = bot.get_updates()[0].update_id
# except IndexError:
#     update_id = None

#
# def echo(bot):
#     """Echo the message the user sent."""
#     global update_id
#     # Request updates after the last update_id
#     for update in bot.get_updates(offset=update_id, timeout=10):
#         update_id = update.update_id + 1
#
#         if update.message:  # your bot can receive updates without messages
#             # Reply to the message
#             update.message.reply_text(update.message.text)


# def bot_start():
    # while True:
    #     try:
    #         echo(bot)
    #     except NetworkError:
    #         sleep(100)
    #     except Unauthorized:
    #         # The user has removed or blocked the bot.
    #         update_id += 1
    #     except Exception as e:
            # log.logger.exception(e)


# Process(target=bot_start).start()
