import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

SELECTING_ACTION, CHANGING_GREETING, CHANGING_SPAM = range(3)

reply_keyboard_admin = [["Change greeting", "Spam"]]
reply_keyboard_greeting = [["/Change_text", "/Change_photo"], ["/Show_greeting", "/Done"]]
reply_keyboard_spam = [["/Show_saved", "/Spam!", "/Done"], ["/Change_text", "/Change_photo"]]

async def admin(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) in config.admins:
        text = ("Admin settings\nsend /cancel to abort")
        markup = ReplyKeyboardMarkup(reply_keyboard_admin, one_time_keyboard=True)
        await update.message.reply_text(text=text, reply_markup=markup)
        return SELECTING_ACTION
    else:
        pass

async def change_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(reply_keyboard_greeting, one_time_keyboard=False)
    await update.message.reply_text(text="Greeting settings", reply_markup=markup)
    return CHANGING_GREETING

async def change_greeting_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config.greeting_text = update.message.text
    await update.message.reply_text("Greeting text updated", reply_markup=ReplyKeyboardMarkup(reply_keyboard_admin,
                                                                                              one_time_keyboard=True))
    return SELECTING_ACTION

async def show_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(config.spam_text, reply_markup=ReplyKeyboardMarkup(reply_keyboard_admin,
                                                                                       one_time_keyboard=True))
    return SELECTING_ACTION

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Spam settings", reply_markup=ReplyKeyboardMarkup(reply_keyboard_spam,
                                                                                           one_time_keyboard=False))
    return CHANGING_SPAM

async def show_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=config.greeting_text, reply_markup=ReplyKeyboardMarkup(reply_keyboard_admin,
                                                                                                one_time_keyboard=True))
    return SELECTING_ACTION

async def change_spam_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config.spam_text = update.message.text
    await update.message.reply_text("Spam text updated", reply_markup=ReplyKeyboardMarkup(reply_keyboard_spam,
                                                                                          one_time_keyboard=True))
    return CHANGING_SPAM

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END

#async def spam_all(update: Update, context: ContextTypes.DEFAULT_TYPE):

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("admin", admin)],
    states={
        SELECTING_ACTION: [
            MessageHandler(filters.Regex("^(Change greeting)$"), change_greeting),
            MessageHandler(filters.Regex("^(Spam)$"), spam),
        ],
        CHANGING_GREETING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, change_greeting_text),
            MessageHandler(filters.Regex("^(/Show_greeting)$"), show_greeting),
        ],
        CHANGING_SPAM: [
            MessageHandler(filters.Regex("^(/Show_saved)"), show_spam),
            MessageHandler(filters.TEXT & ~filters.COMMAND, change_spam_text),
        ]
    },
    fallbacks=[MessageHandler(filters.Regex("^(/Done)$"), done)],
    name="admin",
    persistent=False,
)
