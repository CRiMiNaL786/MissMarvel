#Copyright (C) 2021 Free Software @noobanon @FakeMasked , Inc.[ https://t.me/noobanon https://t.me/FakeMasked ]
#Everyone is permitted to copy and distribute verbatim copies
#of this license document, but changing it is not allowed.
#The GNGeneral Public License is a free, copyleft license for
#software and other kinds of works.
#PTB13 Updated by @noobanon

from math import ceil
from typing import List, Dict

from telegram import Bot, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import TelegramError

from sexo import dispatcher
from sexo.modules.translations.strings import tld
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler

import sexo.modules.sql.connection_sql as con_sql


def keyboard(update, context):
    user = update.effective_user  # type: Optional[User]
    conn_id = con_sql.get_connected_chat(user.id)
    if conn_id and not conn_id == False:
        btn1 = "/disconnect - Disconnect from chat"
        btn2 = ""
        btn3 = ""
    else:
        if con_sql.get_history(user.id):
            history = con_sql.get_history(user.id)
        try:
            chat_name1 = dispatcher.bot.getChat(history.chat_id1).title
        except:
            chat_name1 = ""

        try:
            chat_name2 = dispatcher.bot.getChat(history.chat_id2).title
        except:
            chat_name2 = ""

        try:
            chat_name3 = dispatcher.bot.getChat(history.chat_id3).title
        except:
            chat_name3 = ""

        if chat_name1:
            btn1 = "/connect {} - {}".format(history.chat_id1, chat_name1)
        else:
            btn1 = "/connect - Connect to the chat"
        if chat_name2:
            btn2 = "/connect {} - {}".format(history.chat_id2, chat_name2)
        else:
            btn2 = ""
        if chat_name3:
            btn3 = "/connect {} - {}".format(history.chat_id3, chat_name3)
        else:
            btn3 = ""

        #TODO: Remove except garbage

    update.effective_message.reply_text("Keyboard Updated",
                                            reply_markup=ReplyKeyboardMarkup([[
                                                KeyboardButton("/help - Bot Help"), 
                                                KeyboardButton("/notes - Notes")],
                                             [KeyboardButton(btn1)], 
                                             [KeyboardButton(btn2)],
                                             [KeyboardButton(btn3)]]))
    

KEYBOARD_HANDLER = CommandHandler(["keyboard"], keyboard, run_async=True)
dispatcher.add_handler(KEYBOARD_HANDLER)
