﻿#Copyright (C) 2021 Free Software @noobanon @FakeMasked , Inc.[ https://t.me/noobanon https://t.me/FakeMasked ]
#Everyone is permitted to copy and distribute verbatim copies
#of this license document, but changing it is not allowed.
#The GNGeneral Public License is a free, copyleft license for
#software and other kinds of works.
#PTB13 Updated by @noobanon

import subprocess
import html
import json
import random
import time
import pyowm
import re
from random import randint
from datetime import datetime
from typing import Optional, List
from pythonping import ping as ping3
from typing import Optional, List
from PyLyrics import *
from hurry.filesize import size
#from sylviorus import SYL

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from sexo import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS, BAN_STICKER
from sexo.__main__ import STATS, USER_INFO
from sexo.modules.disable import DisableAbleCommandHandler
from sexo.modules.helper_funcs.extraction import extract_user
from sexo.modules.helper_funcs.filters import CustomFilters
from sexo.modules.rextester.api import Rextester, CompilerError
from sexo.modules.rextester.langs import languages

from sexo.modules.sql.translation import prev_locale

from sexo.modules.translations.strings import tld

from requests import get

BOT_STRINGS = (
    "ｷﾀﾜァ*･゜ﾟ･*:.｡..｡.:*･゜(n‘∀‘)ηﾟ･*:.｡. .｡.:*･゜ﾟ･* !!!!! oh my god i'm a Bot!!!",
)    

RAPE_STRINGS = (
     "Rape Done Drink The Cum",
     "The user has been successfully raped",
     "Dekho Bhaiyya esa hai! Izzat bachailo apni warna Gaand maar lenge tumhari",
     "Relax your Rear, ders nothing to fear,The Rape train is finally here",
     "Dont Rape Too much Bsdk.",
     "Rape coming... Raped! haha :p",
     "Lodu Andha hai kya Yaha tera rape ho raha hai aur tu abhi tak yahi gaand mara raha hai lulz",
)    
    
    
def bot(update, context):
    update.effective_message.reply_text(random.choice(BOT_STRINGS))
    

def pubg(update, context):
    # reply to correct message
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text("PUBG Chutiyo ka Game! Be lyk moi Use Tik-Tok and become Chakka")
    
    

def rape(update, context):
    # reply to correct message
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(RAPE_STRINGS)) 



def runs(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(random.choice(tld(chat.id, "RUNS-K")))



def slap(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user

    temp = random.choice(tld(chat.id, "SLAP_TEMPLATES-K"))
    item = random.choice(tld(chat.id, "ITEMS-K"))
    hit = random.choice(tld(chat.id, "HIT-K"))
    throw = random.choice(tld(chat.id, "THROW-K"))
    itemp = random.choice(tld(chat.id, "ITEMP-K"))
    itemr = random.choice(tld(chat.id, "ITEMR-K"))

    repl = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw, itemp=itemp, itemr=itemr)
    #user1=user1, user2=user2, item=item_ru, hits=hit_ru, throws=throw_ru, itemp=itemp_ru, itemr=itemr_ru

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)
    


def get_id(update, context):
    chat = update.effective_chat
    bot = context.bot
    args = context.args    
    user_id = extract_user(update.effective_message, args)

    if user_id:
        if update.effective_message.reply_to_message and update.effective_message.reply_to_message.forward_from:
            user1 = update.effective_message.reply_to_message.from_user
            user2 = update.effective_message.reply_to_message.forward_from
            update.effective_message.reply_text(tld(chat.id,
                "The original sender, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.").format(
                    escape_markdown(user2.first_name),
                    user2.id,
                    escape_markdown(user1.first_name),
                    user1.id),
                parse_mode=ParseMode.MARKDOWN)
        else:
            user = bot.get_chat(user_id)
            update.effective_message.reply_text(tld(chat.id, "{}'s id is `{}`.").format(escape_markdown(user.first_name), user.id),
                                                parse_mode=ParseMode.MARKDOWN)
    else:
        chat = update.effective_chat  # type: Optional[Chat]
        if chat.type == "private":
            update.effective_message.reply_text(tld(chat.id, "Your id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)

        else:
            update.effective_message.reply_text(tld(chat.id, "This group's id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)



def info(update, context):
    msg = update.effective_message  # type: Optional[Message]
    chat = update.effective_chat
    bot = context.bot
    args = context.args
    user_id = extract_user(update.effective_message, args)
      # type: Optional[Chat]

    if user_id:
        user = bot.get_chat(user_id)

    elif not msg.reply_to_message and not args:
        user = msg.from_user

    elif not msg.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        msg.reply_text(tld(chat.id, "I can't extract a user from this."))
        return

    else:
        return

    text =  tld(chat.id, "<b>User info</b>:")
    text += "\nID: <code>{}</code>".format(user.id)
    text += tld(chat.id, "\nFirst Name: {}").format(html.escape(user.first_name))

    if user.last_name:
        text += tld(chat.id, "\nLast Name: {}").format(html.escape(user.last_name))

    if user.username:
        text += tld(chat.id, "\nUsername: @{}").format(html.escape(user.username))

    text += tld(chat.id, "\nUser link: {}\n").format(mention_html(user.id, "link"))

    if user.id == OWNER_ID:
        text += tld(chat.id, "\n\nAy, This guy is my owner. I would never do anything against him!")
    else:
        if user.id in SUDO_USERS:
            text += tld(chat.id, "\nThis person is one of my sudo users! " \
            "Nearly as powerful as my owner - so watch it.")
        else:
            if user.id in SUPPORT_USERS:
                text += tld(chat.id, "\nThis person is one of my support users! " \
                        "Not quite a sudo user, but can still gban you off the map.")

            if user.id in WHITELIST_USERS:
                text += tld(chat.id, "\nThis person has been whitelisted! " \
                        "That means I'm not allowed to ban/kick them.")
"""
#try:
        sylban = SYL()
        spamer = sylban.get_info(int(user.id))
        if spamer.blacklisted != False:
            text += "\n\n<b>This person is banned on Sylviorus!</b>"
            text += f"\nReason: <pre>{spamer.reason}</pre>"
            text += "\nAppeal at @Sylviorus_Support"
        else:
            pass
    except:
        pass  # don't crash if api is down somehow...
   """ 
    
    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def echo(update, context):
    message = update.effective_message
    bot = context.bot
    args = context.args    
    args = update.effective_message.text.split(None, 1)
    if message.reply_to_message:
        message.reply_to_message.reply_text(args[1])
    else:
        message.reply_text(args[1], quote=False)
    message.delete()

def reply_keyboard_remove(update, context):
    reply_keyboard = []
    reply_keyboard.append([
        ReplyKeyboardRemove(
            remove_keyboard=True
        )
    ])
    reply_markup = ReplyKeyboardRemove(
        remove_keyboard=True
    )
    old_message = context.bot.send_message(
        chat_id=update.message.chat_id,
        text='trying',
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id
    )
    context.bot.delete_message(
        chat_id=update.message.chat_id,
        message_id=old_message.message_id
    )



def markdown_help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(tld(chat.id, "MARKDOWN_HELP-K"), parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(tld(chat.id, "Try forwarding the following message to me, and you'll see!"))
    update.effective_message.reply_text(tld(chat.id, "/save test This is a markdown test. _italics_, *bold*, `code`, "
                                        "[URL](example.com) [button](buttonurl:github.com) "
                                        "[button2](buttonurl://google.com:same)"))

def stats(update, context):
    update.effective_message.reply_text("Current stats:\n" + "\n".join([mod.__stats__() for mod in STATS]))



@run_async
def github(update, context):
    message = update.effective_message
    text = message.text[len('/git '):]
    usr = get(f'https://api.github.com/users/{text}').json()
    if usr.get('login'):
        text = f"*Username:* [{usr['login']}](https://github.com/{usr['login']})"

        whitelist = ['name', 'id', 'type', 'location', 'blog',
                     'bio', 'followers', 'following', 'hireable',
                     'public_gists', 'public_repos', 'email',
                     'company', 'updated_at', 'created_at']

        difnames = {'id': 'Account ID', 'type': 'Account type', 'created_at': 'Account created at',
                    'updated_at': 'Last updated', 'public_repos': 'Public Repos', 'public_gists': 'Public Gists'}

        goaway = [None, 0, 'null', '']

        for x, y in usr.items():
            if x in whitelist:
                if x in difnames:
                    x = difnames[x]
                else:
                    x = x.title()

                if x == 'Account created at' or x == 'Last updated':
                    y = datetime.strptime(y, "%Y-%m-%dT%H:%M:%SZ")

                if y not in goaway:
                    if x == 'Blog':
                        x = "Website"
                        y = f"[Here!]({y})"
                        text += ("\n*{}:* {}".format(x, y))
                    else:
                        text += ("\n*{}:* `{}`".format(x, y))
        reply_text = text
    else:
        reply_text = "User not found. Make sure you entered valid username!"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def repo(update, context):
    message = update.effective_message
    args = context.args
    text = message.text[len('/repo '):]
    usr = get(f'https://api.github.com/users/{text}/repos?per_page=40').json()
    reply_text = "*Repo*\n"
    for i in range(len(usr)):
        reply_text += f"[{usr[i]['name']}]({usr[i]['html_url']})\n"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


LYRICSINFO = "\n[Full Lyrics](http://lyrics.wikia.com/wiki/%s:%s)"


def lyrics(update, context):
    message = update.effective_message
    args = context.args
    text = message.text[len('/lyrics '):]
    song = " ".join(args).split("- ")
    reply_text = f'Looks up for lyrics'
    
    if len(song) == 2:
        while song[1].startswith(" "):
            song[1] = song[1][1:]
        while song[0].startswith(" "):
            song[0] = song[0][1:]
        while song[1].endswith(" "):
            song[1] = song[1][:-1]
        while song[0].endswith(" "):
            song[0] = song[0][:-1]
        try:
            lyrics = "\n".join(PyLyrics.getLyrics(
                song[0], song[1]).split("\n")[:20])
        except ValueError as e:
            return update.effective_message.reply_text("Song %s not found :(" % song[1], failed=True)
        else:
            lyricstext = LYRICSINFO % (song[0].replace(
                " ", "_"), song[1].replace(" ", "_"))
            return update.effective_message.reply_text(lyrics + lyricstext, parse_mode="MARKDOWN")
    else:
        return update.effective_message.reply_text("Invalid syntax! Try Artist - Song name .For example, Luis Fonsi - Despacito", failed=True)


BASE_URL = 'https://del.dog'


def paste(update, context):
    message = update.effective_message
    bot = context.bot

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text("What am I supposed to do with this?!")
        return

    r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))

    if r.status_code == 404:
        update.effective_message.reply_text('Failed to reach dogbin')
        r.raise_for_status()

    res = r.json()

    if r.status_code != 200:
        update.effective_message.reply_text(res['message'])
        r.raise_for_status()

    key = res['key']
    if res['isUrl']:
        reply = f'Shortened URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'{BASE_URL}/{key}'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def get_paste_content(update, context):
    message = update.effective_message
    bot = context.bot
    args = context.args

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text("Please supply a paste key!")
        return

    format_normal = f'{BASE_URL}/'
    format_view = f'{BASE_URL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BASE_URL}/raw/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text('Failed to reach dogbin')
            else:
                update.effective_message.reply_text('Unknown error occured')
        r.raise_for_status()

    update.effective_message.reply_text('```' + escape_markdown(r.text) + '```', parse_mode=ParseMode.MARKDOWN)


def get_paste_stats(update, context):
    message = update.effective_message
    args = context.args

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text("Please supply a paste key!")
        return

    format_normal = f'{BASE_URL}/'
    format_view = f'{BASE_URL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BASE_URL}/documents/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text('Failed to reach dogbin')
            else:
                update.effective_message.reply_text('Unknown error occured')
        r.raise_for_status()

    document = r.json()['document']
    key = document['_id']
    views = document['viewCount']
    reply = f'Stats for **[/{key}]({BASE_URL}/{key})**:\nViews: `{views}`'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def execute(update, context):
    message = update.effective_message
    bot = context.bot
    args = context.args
    text = ' '.join(args)
    regex = re.search('^([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$', text, re.IGNORECASE)

    if not regex:
        available_languages = ', '.join(languages.keys())
        message.reply_text('*The availale languages are:*\n`{}`'.format(available_languages), parse_mode=ParseMode.MARKDOWN)
        return

    language = regex.group(1)
    code = regex.group(2)
    stdin = regex.group(3)

    try:
        regexter = Rextester(language, code, stdin)
    except CompilerError as exc: # Exception on empy code or missing output
        message.reply_text(exc)
        return

    output = ""
    output += "*Language:*\n`{}`".format(language)
    output += "*\n\nSource:*\n`{}`".format(code)

    if regexter.result:
        output += "*\n\nResult:*\n`{}`".format(regexter.result)

    if regexter.warnings:
        output += "\n\n*Warnings:*\n`{}`\n".format(regexter.warnings)

    if regexter.errors:
        output += "\n\n*Errors:*\n'{}`".format(regexter.errors)

    message.reply_text(output, parse_mode=ParseMode.MARKDOWN)


def wiki(update, context):
    kueri = re.split(pattern="wiki", string=update.effective_message.text)
    wikipedia.set_lang("en")
    if len(str(kueri[1])) == 0:
        update.effective_message.reply_text("Enter keywords!")
    else:
        try:
            pertama = update.effective_message.reply_text("🔄 Loading...")
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="🔧 More Info...", url=wikipedia.page(kueri).url)]])
            context.bot.editMessageText(chat_id=update.effective_chat.id, message_id=pertama.message_id, text=wikipedia.summary(kueri, sentences=10), reply_markup=keyboard)
        except wikipedia.PageError as e:
            update.effective_message.reply_text(f"⚠ Error: {e}")
        except BadRequest as et :
            update.effective_message.reply_text(f"⚠ Error: {et}")
            


def shrug(update, context):
    default_msg = "¯\_(ツ)_/¯"
    message = update.effective_message
    if message.reply_to_message:
        message.reply_to_message.reply_text(default_msg)
    else:
        message.reply_text(default_msg)
        
        
def ud(update, context): 
        term = ' '.join(args)
        ud_api = "http://api.urbandictionary.com/v0/define?term=" + term
        ud_reply = json.loads(requests.get(ud_api).content)['list']
        if len(args) == 0:
            update.message.reply_text("USAGE: /ud <Word>")
        elif len(ud_reply) != 0:
            ud = ud_reply[0]
            reply_text = "<b>{0}</b>\n<a href='{1}'>{1}</a>\n<i>By {2}</i>\n\nDefinition: {3}\n\nExample: {4}".format(
                ud['word'], ud['permalink'], ud['author'], ud['definition'], ud['example'])
            update.message.reply_text(reply_text, parse_mode='HTML')
        else:
            update.message.reply_text("Term not found")


       

__help__ = """
 - /id: get the current group id. If used by replying to a message, gets that user's id.
 - /runs: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /info: get information about a user.
 - /gdpr: deletes your information from the bot's database. Private chats only.
 - /markdownhelp: quick summary of how markdown works in telegram - can only be called in private chats.

 - /git: Returns info about a GitHub user or organization.
 - /repo: Return the GitHub user or organization repository list (Limited at 40)
 - /lyrics: Find your favorite songs lyrics!
 - /paste: Create a paste or a shortened url using [dogbin](https://del.dog)
 - /getpaste: Get the content of a paste or shortened url from [dogbin](https://del.dog)
 - /pastestats: Get stats of a paste or shortened url from [dogbin](https://del.dog)
 - /ud: Type the word or expression you want to search. For example /ud Gay
 - /removebotkeyboard: Got a nasty bot keyboard stuck in your group?
 - /exec <language> <code> [/stdin <stdin>]: Execute a code in a specified language. Send an empty command to get the supported languages.
 - /shrug: try and check it out yourself.
 - /bot: try and check it out yourself.
 - /time <place>: gives the local time at the given place.
"""

__mod_name__ = "Misc"

ID_HANDLER = DisableAbleCommandHandler("id", get_id, pass_args=True, admin_ok=True, run_async=True)
#TIME_HANDLER = CommandHandler("time", get_time, pass_args=True, run_async=True)
#PING_HANDLER = DisableAbleCommandHandler("ping", ping, admin_ok=True, run_async=True)
#GOOGLE_HANDLER = DisableAbleCommandHandler("google", google)
LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True, admin_ok=True, run_async=True)


RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, admin_ok=True, run_async=True)
BOT_HANDLER = DisableAbleCommandHandler("bot", bot, admin_ok=True, run_async=True)
RAPE_HANDLER = DisableAbleCommandHandler("rape", rape, admin_ok=True, run_async=True)
SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug, admin_ok=True, run_async=True)
PUBG_HANDLER = DisableAbleCommandHandler("pubg", pubg, admin_ok=True, run_async=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True, admin_ok=True, run_async=True)
INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True, admin_ok=True, run_async=True)
GITHUB_HANDLER = DisableAbleCommandHandler("git", github, admin_ok=True, run_async=True)
REPO_HANDLER = DisableAbleCommandHandler("repo", repo, pass_args=True, admin_ok=True, run_async=True)

ECHO_HANDLER = CommandHandler("echo", echo, filters=CustomFilters.sudo_filter, run_async=True)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help, filters=Filters.private, run_async=True)

STATS_HANDLER = CommandHandler("stats", stats, filters=Filters.user(OWNER_ID))
#GDPR_HANDLER = CommandHandler("gdpr", gdpr, filters=Filters.private)
EXECUTE_HANDLER = CommandHandler("exec", execute, pass_args=True, filters=CustomFilters.sudo_filter)

PASTE_HANDLER = DisableAbleCommandHandler("paste", paste, pass_args=True)
GET_PASTE_HANDLER = DisableAbleCommandHandler("getpaste", get_paste_content, pass_args=True)
PASTE_STATS_HANDLER = DisableAbleCommandHandler("pastestats", get_paste_stats, pass_args=True)


dispatcher.add_handler(PASTE_HANDLER)
#dispatcher.add_handler(TIME_HANDLER)
dispatcher.add_handler(GET_PASTE_HANDLER)
dispatcher.add_handler(PASTE_STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(BOT_HANDLER)
dispatcher.add_handler(PUBG_HANDLER)
dispatcher.add_handler(RAPE_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(CommandHandler('ud', ud, pass_args=True))
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(STATS_HANDLER)
#dispatcher.add_handler(GDPR_HANDLER)
#dispatcher.add_handler(PING_HANDLER)
#dispatcher.add_handler(GOOGLE_HANDLER)
dispatcher.add_handler(GITHUB_HANDLER)
dispatcher.add_handler(LYRICS_HANDLER)
dispatcher.add_handler(REPO_HANDLER)
dispatcher.add_handler(DisableAbleCommandHandler("removebotkeyboard", reply_keyboard_remove))
dispatcher.add_handler(EXECUTE_HANDLER)
