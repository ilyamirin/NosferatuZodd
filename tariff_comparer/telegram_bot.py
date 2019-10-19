import telebot
from aiml_bot import BotClientMod
from math import ceil
from doc_prepr import *
from compare_logic import *

aiml_bot = BotClientMod()
tlg_bot = telebot.TeleBot('920441140:AAFb8V75hXzR9oGuN-0aVsqDFxZH8aLI6eo')

compare_flag = False

@tlg_bot.message_handler(commands=['compare'])
def start_message(message):
    global compare_flag
    compare_flag = True
    count_banks = ceil(len(banks_tariff) / 3)

    keyboard_bank = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                      one_time_keyboard=True,
                                                      selective=True,
                                                      row_width=count_banks,
                                                      )
    banks = split(list(banks_tariff), 3)
    for i in banks:
        keyboard_bank.add(*i)

    tlg_bot.send_message(message.chat.id,
                     aiml_bot.get_answer(message.chat.id, 'GREET') + aiml_bot.get_answer(message.chat.id, 'CHOOSE BANK').format('первый'),
                     reply_markup=keyboard_bank,
                     )

    client['condition'] = 'sending_first_bank'

@tlg_bot.message_handler(content_types=['text'])
def send_text(message):
    if compare_flag:
        if message.text in banks_tariff and client['condition'] == 'sending_first_bank':

            tariffs = banks_tariff[message.text]
            client['first_bank'] = message.text
            count_tariffs = ceil(len(tariffs) / 3)

            keyboard_tariff = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                one_time_keyboard=True,
                                                                selective=True,
                                                                row_width=count_tariffs,
                                                                )
            tariffs = split(tariffs, 3)
            for i in tariffs:
                keyboard_tariff.add(*i)

            tlg_bot.send_message(message.chat.id,
                             aiml_bot.get_answer(message.chat.id, 'CHOOSE TARIFF').format(message.text),
                             reply_markup=keyboard_tariff)

            client['condition'] = 'sending_first_tariff'

        elif message.text in banks_tariff[client['first_bank']] and client['condition'] == 'sending_first_tariff':

            client['first_tariff'] = message.text
            banks = [i for i in banks_tariff if i != client['first_bank']]
            count_banks = ceil(len(banks) / 3)
            keyboard_bank = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                              one_time_keyboard=True,
                                                              selective=True,
                                                              row_width=count_banks,
                                                              )
            banks = split(list(banks), 3)
            for i in banks:
                keyboard_bank.add(*i)

            tlg_bot.send_message(message.chat.id,
                             aiml_bot.get_answer(message.chat.id, 'CHOOSE BANK').format('второй'),
                             reply_markup=keyboard_bank,
                             )

            client['condition'] = 'sending_second_bank'

        elif message.text in banks_tariff and client['condition'] == 'sending_second_bank':

            tariffs = banks_tariff[message.text]
            client['second_bank'] = message.text
            count_tariffs = ceil(len(tariffs) / 3)

            keyboard_tariff = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                one_time_keyboard=True,
                                                                selective=True,
                                                                row_width=count_tariffs,
                                                                )
            tariffs = split(tariffs, 3)
            for i in tariffs:
                keyboard_tariff.add(*i)

            tlg_bot.send_message(message.chat.id,
                             aiml_bot.get_answer(message.chat.id, 'CHOOSE TARIFF').format(message.text),
                             reply_markup=keyboard_tariff)

            client['condition'] = 'sending_second_tariff'

        elif message.text in banks_tariff[client['second_bank']] and client['condition'] == 'sending_second_tariff':
            client['second_tariff'] = message.text
            answer = ''
            first_tariff = features_to_dict(client['first_tariff'])
            second_tariff = features_to_dict(client['second_tariff'])
            compare_results = compare_tariffs(first_tariff, second_tariff)

            for i in compare_results[0]:
                answer += aiml_bot.get_answer(message.chat.id, 'COMMON FEATURES').format('"'+i+'"', client['first_tariff'], client['second_tariff'], compare_results[0][i])

            for i in compare_results[1]:
                answer += aiml_bot.get_answer(message.chat.id, 'DIFFERENT FEATURES').format('"'+i+'"', client['first_tariff'], client['second_tariff'], compare_results[1][i][0], compare_results[1][i][1])
            tlg_bot.send_message(message.chat.id, answer)
    else:
        answer = aiml_bot.get_answer(message.chat.id, message.text)
        tlg_bot.send_message(message.chat.id, answer)
        print(answer)

if __name__ == '__main__':
    client = {'first_bank': None,
              'second_bank': None,
              'first_tariff': None,
              'second_tariff': None,
              'condition': None}
    tlg_bot.polling()