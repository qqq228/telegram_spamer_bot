import logging
import config
import adminka
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler,\
    ChatJoinRequestHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.approve_chat_join_request(chat_id=update.effective_chat.id,
                                        user_id=update.effective_user.id)
    await context.bot.send_message(chat_id=update.effective_user.id,
                                   text=config.greeting_text)

if __name__ == '__main__':
    application = ApplicationBuilder().token('YOUR TOKEN').build()

    start_handler = CommandHandler('start', start)
    chat_request_handler = ChatJoinRequestHandler(approve)

    application.add_handler(start_handler)
    application.add_handler(chat_request_handler)
#    application.add_handler(adminka.admin_handler)
#    application.add_handler(adminka.change_spam_text_handler)
    application.add_handler(adminka.conv_handler)

    application.run_polling()