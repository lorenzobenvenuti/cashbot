#!/usr/bin/env python

import logging
import sys

import accesschecker
import config
import telegramwrapper

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class CashBot(object):

    def __init__(self, conf):
        self._app = telegramwrapper.App(
            conf.telegram_token,
            accesschecker.WhitelistChecker(conf.allowed_users)
        )
        self._app.add_command(
            telegramwrapper.Command("in", self.in_command, True)
        )
        self._app.add_command(
            telegramwrapper.Command("out", self.out_command, True)
        )
        self._app.add_command(
            telegramwrapper.Command("cat", self.cat_command, False)
        )
        self._supplier = conf.categories_supplier
        self._outputs = conf.outputs

    def _unpack_args(self, args):
        if len(args) < 2:
            raise ValueError("Command needs at least two arguments")
        if not self._is_number(args[0]):
            raise ValueError("First argument must be a number")
        cats = self._supplier.search(args[1])
        if len(cats) == 0:
            raise ValueError("Invalid category")
        if len(cats) > 1:
            raise ValueError("Too many matches: {}".format(",".join(cats)))
        return args[0], cats[0], ' '.join(args[2:]) if len(args) > 2 else None

    def send(self, bot, update, event, args):
        try:
            amount, category, description = self._unpack_args(args)
            for output in self._outputs:
                if event == 'in':
                    output.on_income(amount, category, description)
                elif event == 'out':
                    output.on_expense(amount, category, description)
            bot.sendMessage(update.message.chat_id, "Done")
        except ValueError as err:
            bot.sendMessage(update.message.chat_id, err.message)
            return

    def _is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def in_command(self, bot, update, args):
        self.send(bot, update, 'in', args)

    def out_command(self, bot, update, args):
        self.send(bot, update, 'out', args)

    def cat_command(self, bot, update):
        bot.sendMessage(
            update.message.chat_id,
            text="\n".join(self._supplier.all())
        )

    def run(self):
        self._app.run()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: cashbot.py config_file")
        sys.exit(1)
    conf = config.YamlConfigFactory(sys.argv[1]).get_config()
    cashbot = CashBot(conf)
    cashbot.run()
