import threading
import asyncio
from telegram.ext import CommandHandler,Updater,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from ozonparser.tasks import result

class Tgpotok(threading.Thread):

    def __init__(self):
        super(Tgpotok,self).__init__()

    def start_callback(self,update, context):
        keyboard = [
            [
                InlineKeyboardButton("Список товаров", callback_data='3'),
            ],
        ]

    
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Welcome to my awesome bot!",reply_markup=reply_markup)



    def button(self,update: Update, context) -> None:
        query = update.callback_query
        query.answer()
        result.apply_async(args = (update.callback_query.message.chat_id,))
        query.edit_message_text(text=f"Selected option: {query.data}")

    def main(self):
        self.updater = Updater("6464088491:AAEPuZNZiDezsGArG8JIJ8EH7X0ekN2L7_E")
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CallbackQueryHandler(self.button))
        self.dispatcher.add_handler(CommandHandler("start", self.start_callback))
        # Start the bot
        self.updater.start_polling()
        self.updater.idle()

    def run(self):
        self.main()