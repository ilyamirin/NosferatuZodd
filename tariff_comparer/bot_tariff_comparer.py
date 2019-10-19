#!/usr/bin/env python
# coding: utf-8

# In[1]:


from re import match
from math import ceil

from numpy import append
from pandas import read_excel

import telebot


# In[2]:


def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return (arrs)


'''
#for html table generation
import xml.etree.ElementTree as ET
def make_table(data, first_tariff, second_tariff):
    table = ET.Element('table')
    tr_header = ET.SubElement(table, 'tr')
    for i in 'хар-ка', first_tariff, second_tariff:
        ET.SubElement(tr_header, 'th').text = i
    for i in range(1, 8):
        tr_el = ET.SubElement(table, 'tr')
        for j in x['хар-ка\тариф'], x[first_tariff], x[second_tariff]:
            ET.SubElement(tr_el, 'td').text = str(j.loc[i])
    return(ET.tostring(table))
'''


def make_table_text(data, first_tariff, second_tariff):
    text = ''
    for i in 'хар-ка: ', first_tariff + '\t|', second_tariff:
        text += (i + '\t')
    text += ('\n')
    for i in range(1, 8):
        for j in '<b>' + x['хар-ка\тариф'] + '</b>', x[first_tariff] + '\t|', x[second_tariff]:
            text += str(j.loc[i]) + '\t'
        text += ('\n')
    return (text)


# In[3]:


bot = telebot.TeleBot('920441140:AAFb8V75hXzR9oGuN-0aVsqDFxZH8aLI6eo')


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard_bank = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                      one_time_keyboard=True,
                                                      selective=True,
                                                      row_width=2,
                                                      )
    keyboard_bank.add('Привет', 'Пока')
    bot.send_message(message.chat.id,
                     'Я уже работаю, выберите опцию',
                     reply_markup=keyboard_bank,
                     )


@bot.message_handler(content_types=['text'])
def send_text(message):
    if match('прив.*|здравств.*', message.text.lower()):

        count_banks = ceil(len(banks_tariff) / 3)

        keyboard_bank = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                          one_time_keyboard=True,
                                                          selective=True,
                                                          row_width=count_banks,
                                                          )
        banks = split(list(banks_tariff), 3)

        for i in banks:
            keyboard_bank.add(*i)

        bot.send_message(message.chat.id,
                         templates['greet'] + templates['choose_bank'].format('первый'),
                         reply_markup=keyboard_bank,
                         )
        client['condition'] = 'sending_first_bank'

    elif message.text in banks_tariff and client['condition'] == 'sending_first_bank':

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

        bot.send_message(message.chat.id,
                         templates['choose_tariff'].format(message.text),
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

        bot.send_message(message.chat.id,
                         templates['choose_bank'].format('второй'),
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

        bot.send_message(message.chat.id,
                         templates['choose_tariff'].format(message.text),
                         reply_markup=keyboard_tariff)

        client['condition'] = 'sending_second_tariff'

    elif message.text in banks_tariff[client['second_bank']] and client['condition'] == 'sending_second_tariff':
        client['second_tariff'] = message.text
        bot.send_message(message.chat.id,
                         make_table_text(x, client['first_tariff'], client['second_tariff']),
                         parse_mode='HTML', )

    elif message.text.lower() == 'Пока':
        bot.send_message(message.chat.id, templates['bye'])


# In[ ]:


if __name__ == '__main__':
    # little prepr
    x = read_excel('20190901_Рынок пакеты.xlsx')

    cols = list(x.columns)
    for i in range(len(cols)):
        if match('Unnamed:.*', cols[i]):
            cols[i] = prev_col
        prev_col = cols[i]

    # make banks dict with tariffs as values and
    banks_tariff = {i: [] for i in cols[1:]}
    for i, j in zip(cols[1:], x.loc[0][1:]):
        banks_tariff[i].append(j)

    # cut off banks from table
    x.columns = append(['хар-ка\тариф'], x.loc[0][1:])
    x = x[x['хар-ка\тариф'] != 'Тариф']
    x = x.dropna(subset=['хар-ка\тариф'])
    x = x.fillna('-')
    for i in x:
        x[i] = x[i].astype(str)

    templates = {'greet': 'Выберите, пожалуйста, два банка и тарифы в них, я попытаюсь их сравнить.',
                 'choose_bank': 'Выберите, пожалуйста, {} банк',
                 'bye': 'До свидания!',
                 'choose_tariff': 'Выберите, пожалуйста, тариф в {}.',
                 }

    client = {'first_bank': None,
              'second_bank': None,
              'first_tariff': None,
              'second_tariff': None,
              'condition': None}

    bot.polling()

# In[ ]:


# to_file
# open('html.html', 'w').write(make_table(x, 'На старт', 'На старт').decode('utf-8'))

