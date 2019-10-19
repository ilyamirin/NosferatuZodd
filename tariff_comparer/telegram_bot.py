import telebot
from aiml_bot import BotClientMod

aiml_bot = BotClientMod()
tlg_bot = telebot.TeleBot('920441140:AAFb8V75hXzR9oGuN-0aVsqDFxZH8aLI6eo')

@tlg_bot.message_handler(content_types=['text'])
def send_text(message):
    tlg_bot.send_message(message.chat.id, aiml_bot.get_answer(message.chat.id, message.text))

if __name__ == '__main__':
    tlg_bot.polling()