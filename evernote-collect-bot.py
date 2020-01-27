import argparse
import telegram
import evernote
import logging
import time

# setting start up args
parser = argparse.ArgumentParser(
    description='telegram bot for quickly evernote adding')
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument('-et', '--evernote_token',
                    help='evernote token', required=False)
parser.add_argument('-tt', '--telegram_token',
                    help='telegram bot token', required=True)
parser.add_argument('-p', '--proxy',
                    help='set up proxy', required=False)
parser.add_argument('-tuid', '--telegram_user_id', required=False,
                    help='specific user to interact with')
parser.add_argument('-lo', '--listen_only',  action="store_true",
                    help='listen only mode, use this mode and send message to your bot to get your telegram user id')

args = parser.parse_args()

# set up log mode
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# initialize telegram bot
if args.proxy is not None:
    proxy = telegram.utils.request.Request(proxy_url=args.proxy, connect_timeout=30, read_timeout=30)
    telegram_bot = telegram.Bot(token=args.telegram_token, request=proxy)
else:
    telegram_bot = telegram.Bot(token=args.telegram_token)

# check listen only mode
if args.listen_only:
    logging.info('start listen only mode')
    # TODO add KeyboardInterrupt handler
    offset = 0
    while True:
        logging.info('listening telegram bot message...')
        updates = telegram_bot.get_updates(offset=offset)
        for update in updates:
            logging.info(f'recieved message "{update.message.text}" from user {update.message.from_user.username}, id: {update.message.from_user.id}')
            logging.debug(f'update')
            offset = update.update_id + 1
        time.sleep(5) # wait 5 seconds