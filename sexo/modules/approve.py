#Copyright (C) 2021 Free Software @noobanon @FakeMasked , Inc.[ https://t.me/noobanon https://t.me/FakeMasked ]
#Everyone is permitted to copy and distribute verbatim copies
#of this license document, but changing it is not allowed.
#The GNGeneral Public License is a free, copyleft license for
#software and other kinds of works.
#PTB13 Updated by @noobanon

from sexo.modules.disable import DisableAbleCommandHandler
from sexo import dispatcher, SUDO_USERS
from sexo.modules.helper_funcs.extraction import extract_user
from telegram.ext import run_async, CallbackQueryHandler
import sexo.modules.sql.approve_sql as sql
from sexo.modules.helper_funcs.chat_status import bot_admin, user_admin, user_can_promote
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update, Bot, Message, Chat, User
from typing import Optional, List


@user_admin
@user_can_promote
def approve(update, context) -> str:
	 message = update.effective_message
	 chat_title = message.chat.title
	 chat = update.effective_chat
	 bot = context.bot
	 args = context.args
	
	 user_id = extract_user(message, args)
	 if not user_id:
	     message.reply_text("I don't know who you're talking about, you're going to need to specify a user!")
	     return ""
	 member = chat.get_member(int(user_id))
	 if member.status == "administrator" or member.status == "creator":
	     message.reply_text(f"User is already admin - locks, blocklists, and antiflood already don't apply to them.")
	     return
	 if sql.is_approved(message.chat_id, user_id):
	     message.reply_text(f"[{member.user['first_name']}](tg://user?id={member.user['id']}) is already approved in {chat_title}", parse_mode=ParseMode.MARKDOWN)
	     return
	 sql.approve(message.chat_id, user_id)
	 message.reply_text(f"[{member.user['first_name']}](tg://user?id={member.user['id']}) has been approved in {chat_title}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood.", parse_mode=ParseMode.MARKDOWN)
     
@user_admin
@user_can_promote
def disapprove(update, context) -> str:
	 message = update.effective_message
	 chat_title = message.chat.title
	 chat = update.effective_chat
	 bot = context.bot
	 args = context.args  
	 
	 user_id = extract_user(message, args)
	 if not user_id:
	     message.reply_text("I don't know who you're talking about, you're going to need to specify a user!")
	     return ""
	 member = chat.get_member(int(user_id))
	 if member.status == "administrator" or member.status == "creator":
	     message.reply_text("This user is an admin, they can't be unapproved.")
	     return
	 if not sql.is_approved(message.chat_id, user_id):
	     message.reply_text(f"{member.user['first_name']} isn't approved yet!")
	     return
	 sql.disapprove(message.chat_id, user_id)
	 message.reply_text(f"{member.user['first_name']} is no longer approved in {chat_title}.")
     

@user_admin
def approved(update, context) -> str:
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    bot = context.bot
    args = context.args
    no_users = False
    msg = "The following users are approved.\n"
    x = sql.list_approved(message.chat_id)
    for i in x:
        try:
            member = chat.get_member(int(i.user_id))
        except:
            pass
        msg += f"- `{i.user_id}`: {member.user['first_name']}\n"
    if msg.endswith("approved.\n"):
      message.reply_text(f"No users are approved in {chat_title}.")
      return
    else:
      message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


@user_admin
def approval(update, context) -> str:
	 message = update.effective_message
	 chat = update.effective_chat
	 bot = context.bot
	 args = context.args
	 user_id = extract_user(message, args)
	 member = chat.get_member(int(user_id))
	 if not user_id:
	     message.reply_text("I don't know who you're talking about, you're going to need to specify a user!")
	     return ""
	 if sql.is_approved(message.chat_id, user_id):
	     message.reply_text(f"{member.user['first_name']} is an approved user. Locks, antiflood, and blocklists won't apply to them.")
	 else:
	     message.reply_text(f"{member.user['first_name']} is not an approved user. They are affected by normal commands.")


@user_admin
def unapproveall(update, context):
    chat = update.effective_chat
    user = update.effective_user
    bot = context.bot
    args = context.args
    member = chat.get_member(user.id)


    if chat.type == "private":
        update.effective_message.reply_text("This command is not specified to be used in my PM.")
        return


    if member.status != "creator" and user.id not in SUDO_USERS:
        update.effective_message.reply_text(
            "Only the chat owner can unapprove all users at once."
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Unapprove all users", callback_data="unapproveall_user"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Cancel", callback_data="unapproveall_cancel"
                    )
                ],
            ]
        )
        update.effective_message.reply_text(
            f"Are you sure you would like to unapprove ALL users in {chat.title}? This action cannot be undone.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )



def unapproveall_btn(update, context):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    bot = context.bot
    member = chat.get_member(query.from_user.id)
    if query.data == "unapproveall_user":
        if member.status == "creator" or query.from_user.id in SUDO_USERS:
            users = []
            approved_users = sql.list_approved(chat.id)
            for i in approved_users:
                users.append(int(i.user_id))
            for user_id in users:
                sql.disapprove(chat.id, user_id)
            message.edit_text("Unapproved all users in chat. All users will now be affected by locks, blocklists, and antiflood.")
            return ""
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")

        if member.status == "member":
            query.answer("You need to be admin to do this.")
    elif query.data == "unapproveall_cancel":
        if member.status == "creator" or query.from_user.id in SUDO_USERS:
            message.edit_text("Removing of all approved users has been cancelled.")
            return ""
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")
        if member.status == "member":
            query.answer("You need to be admin to do this.")
				

__help__  = """
Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.

That's what approvals are for - approve of trustworthy users to allow them to send 

*Admin commands:*
- /approval: Check a user's approval status in this chat.

*Admin commands:*
- /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
- /unapprove: Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
- /approved: List all approved users.

*Owner command:*
- /unapproveall: To unapprove all users in a chat.

*Examples*
 
Here are some examples for Approval module commands.
 
• To approve a user:
‣ `/approve @user`
 
• To unapprove a user:
‣ `/unapprove @user`

• To check all approved users in a chat:
‣ `/approved`

• To unapprove all users at once:
‣ `/unapproveall`
"""

APPROVE_HANDLER = DisableAbleCommandHandler("approve", approve, run_async=True)
DISAPPROVE_HANDLER = DisableAbleCommandHandler(["unapprove", "disapprove"], disapprove, run_async=True)
LIST_APPROVED_HANDLER = DisableAbleCommandHandler("approved", approved, run_async=True)
APPROVAL_HANDLER = DisableAbleCommandHandler("approval", approval, run_async=True)
UNAPPROVEALL_HANDLER = DisableAbleCommandHandler("unapproveall", unapproveall)
UNAPPROVEALL_BTN_HANDLER = CallbackQueryHandler(unapproveall_btn, pattern=r"unapproveall_.*")
				
dispatcher.add_handler(APPROVE_HANDLER)
dispatcher.add_handler(DISAPPROVE_HANDLER)
dispatcher.add_handler(LIST_APPROVED_HANDLER)
dispatcher.add_handler(APPROVAL_HANDLER)
dispatcher.add_handler(UNAPPROVEALL_HANDLER)
dispatcher.add_handler(UNAPPROVEALL_BTN_HANDLER)


__mod_name__ = "Approval"
