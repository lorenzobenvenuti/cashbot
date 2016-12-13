from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    RegexHandler
)
import logging

logger = logging.getLogger(__name__)


class Command(object):

    def __init__(self, name, function, pass_args):
        self._name = name
        self._function = function
        self._pass_args = pass_args

    @property
    def name(self):
        return self._name

    @property
    def function(self):
        return self._function

    @property
    def pass_args(self):
        return self._pass_args


class App(object):

    def __init__(self, token, access_checker, bootstrap_retries=-1):
        self._token = token
        self._access_checker = access_checker
        self._bootstrap_retries = bootstrap_retries
        self._commands = []

    def _secure_function(self, f):
        def inner(*args, **kwargs):
            bot = args[0]
            update = args[1]
            if not self._access_checker.is_allowed(update.message.from_user):
                logger.warn('Unauthorized user access {}'.format(
                    update.message.from_user
                ))
                bot.sendMessage(
                    update.message.chat_id,
                    text="You are not allowed to use this bot"
                )
            else:
                try:
                    f(*args, **kwargs)
                except BaseException as error:
                    logger.exception(
                        'Update "%s" caused error "%s"' % (update, error))
                    bot.sendMessage(
                        update.message.chat_id,
                        text="An error occurred: {}".format(str(error))
                    )
        return inner

    def _unknown_command(self, bot, update):
        bot.sendMessage(update.message.chat_id, text="Invalid command")

    def _message(self, bot, update):
        bot.sendMessage(update.message.chat_id, text="Please send a command")

    def _error(self, bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))

    def add_command(self, command):
        self._commands.append(command)

    def run(self):
        updater = Updater(self._token)
        dispatcher = updater.dispatcher
        for command in self._commands:
            dispatcher.add_handler(CommandHandler(
                command.name,
                self._secure_function(command.function),
                pass_args=command.pass_args
            ))
        dispatcher.add_handler(MessageHandler(
            [Filters.text],
            self._secure_function(self._message)
        ))
        dispatcher.add_handler(RegexHandler(
            '/.*',
            self._secure_function(self._unknown_command)
        ))
        dispatcher.add_error_handler(self._error)
        updater.start_polling(bootstrap_retries=self._bootstrap_retries)
        updater.idle()
