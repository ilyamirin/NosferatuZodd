import telebot
import requests
from aiml_bot import BotClientMod
from math import ceil
from doc_prepr import *
from compare_logic import *

aiml_bot = BotClientMod()
with open('tok', 'r') as tok:
    tlg_bot = telebot.TeleBot(tok.read())
    tlg_bot.compare_flag = False

def get_proxy():
    proxies_provider = 'https://www.proxy-list.download/api/v1/get?type=socks5'
    try:
        proxies = [i for i in requests.get(proxies_provider).text.split()]
        print('Proxies list recieved.')
        for each in proxies:
            yield (each)
    except ConnectionError:
        print('Unable to get proxies list, check your internet connection')

def ConnectionResolve():
    print('Connection troubles, trying to apply proxies...')
    telebot.apihelper.proxy = {'https': 'socks5h://{}'.format(next(get_proxy()))}
    print(telebot.apihelper.proxy)
    run_bot()

def run_bot():
    global client
    client = {'first_bank': None,
              'second_bank': None,
              'first_tariff': None,
              'second_tariff': None,
              'condition': None}
    try:
        tlg_bot.polling(timeout=1000, none_stop=True, interval = 1)
    except requests.exceptions.ConnectionError:
        ConnectionResolve()



@tlg_bot.message_handler(commands=['start'])
def start_message_1(message):
    answer = aiml_bot.get_answer(message.chat.id, 'Привет')
    tlg_bot.send_message(message.chat.id, answer)

@tlg_bot.message_handler(commands=['compare'])
def start_message(message):
    tlg_bot.compare_flag = True
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
    if tlg_bot.compare_flag:
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

            tlg_bot.send_photo(message.chat.id, make_img_from_html(client['first_tariff'], client['first_bank'], client['second_tariff'], client['second_bank']))

            #This is for text message
            '''
            answer = ''
            first_tariff = features_to_dict(client['first_tariff'], client['first_bank'])
            second_tariff = features_to_dict(client['second_tariff'], client['second_bank'])
            compare_results = compare_tariffs(first_tariff, second_tariff)

            flag_bold = True
            for i in compare_results[0]:
                part_of_answer = aiml_bot.get_answer(message.chat.id, 'COMMON FEATURES').format(i,
                                                                                         client['first_tariff'],
                                                                                         client['second_tariff'],
                                                                                         compare_results[0][i])
                if flag_bold:
                    answer += "<b>"+part_of_answer+"</b>"
                    flag_bold = False
                else:
                    answer += part_of_answer
                    flag_bold = True


            for i in compare_results[1]:
                part_of_answer = aiml_bot.get_answer(message.chat.id, 'DIFFERENT FEATURES').format(i,
                                                                                            client['first_tariff'],
                                                                                            client['second_tariff'],
                                                                                            compare_results[1][i][0],
                                                                                            compare_results[1][i][1])
                if flag_bold:
                    answer += "<b>"+part_of_answer+"</b>"
                    flag_bold = False
                else:
                    answer += part_of_answer
                    flag_bold = True

            print("answer: ", answer)
            tlg_bot.send_message(message.chat.id, answer, parse_mode = "html")
            '''
            tlg_bot.compare_flag = False

    else:
        answer = aiml_bot.get_answer(message.chat.id, message.text)
        tlg_bot.send_message(message.chat.id, answer, parse_mode = "html")
        print(answer)

if __name__ == "__main__":
    run_bot()