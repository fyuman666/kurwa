import telebot
import pickle
from telebot import types
import random
import time

bot_token = '6840852496:AAEKM9w7-zKuKZMWhqmLPEboSXV9rGu37uE'

bot = telebot.TeleBot(bot_token)

user_data_file = 'user_data.pkl'

payment_info_dict = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('КАРТА'), types.KeyboardButton('СБП'), types.KeyboardButton('USDT'))
    bot.send_message(message.chat.id, "Для покупки мода на TikTok выбери способ оплаты | оплата автоматически проверяется, если деньги поступили то бот автоматически выдаст ссылку, на приватный чат [наш канал - https://t.me/+EUAIMO009hA1M2Ni]:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['КАРТА', 'СБП', 'USDT'])
def payment_method(message):
    payment_info = ""
    if message.text == 'КАРТА':
        payment_info = "Для оплаты картой отправьте сумму 200 RUB на карту  2200 7302 4322 7721 Время на оплату: 30 минут после успешной оплаты  бот отправит ссылку на приватный чат для вступления."
    elif message.text == 'СБП':
        payment_info = "Для оплаты через СПБ отправьте сумму 200 RUB на счет +79301793564 QIWI BANK Дмитрий Сергеевич. Время на оплату: 30 минут после успешной оплаты бот отправит  ссылку на приватный чат для вступления."
    elif message.text == 'USDT':
        payment_info = "Для оплаты через CryptoBot отправьте сумму 3$ на адрес USDT TRC20 - TCNnXNmHyphB16jcw9E1VVndTzDNkNPYNv. Время на оплату: 15 минут после успешной оплаты вам бот отправит  ссылку на приватный чат для вступления."
    bot.send_message(message.chat.id, payment_info)
    payment_info_dict[message.chat.id] = {'method': message.text, 'paid': False}  

@bot.message_handler(content_types=['photo'])
def payment_screenshot(message):
    if message.chat.id in payment_info_dict:
        if not payment_info_dict[message.chat.id]['paid']:
            bot.forward_message(5727907441, message.chat.id, message.message_id)
            bot.send_message(5727907441, "Пользователь отправил скриншот оплаты. Подтвердите оплату командой /confirm_payment")
        else:
            bot.reply_to(message, "Вы уже подтвердили оплату")

@bot.message_handler(commands=['confirm_payment'])
def confirm_payment(message):
    if message.chat.id == 5727907441:
        user_id = list(payment_info_dict.keys())[0]
        if payment_info_dict[user_id]['paid']:
            bot.send_message(5727907441, "Вы уже подтвердили оплату этого пользователя")
        else:
            payment_info_dict[user_id]['paid'] = True
            bot.send_message(user_id, "Ваша оплата подтверждена. Вот ссылка на группу в Телеграм с файлом: https://t.me/yourgroup")
    else:
        bot.send_message(message.chat.id, "У вас нет прав на подтверждение оплаты")

# Запуск бота
bot.polling()
