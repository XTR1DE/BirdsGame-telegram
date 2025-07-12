import telebot
from telebot import types
import DataBase
import BirdsData
import time
import Codes
import asyncio
import threading
import os
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row(types.KeyboardButton("Играть"))
    keyboard.row(types.KeyboardButton("Баланс"))
    keyboard.row(types.KeyboardButton("F.A.Q"), types.KeyboardButton("Друзья"))
    keyboard.row(types.KeyboardButton("Привязать кошелек"))
    return keyboard


def chat_send(message):
    print(f"{message.from_user.first_name} - {message.text}")
    if len(message.text) > 80:
        bot.send_message(message.chat.id, "<b>Данный текст слишком длинный</b>", parse_mode="html", reply_markup=keyboard)
        return

    if message.text == "Играть" or message.text == "/start":
        bot.send_message(message.chat.id, "<b>'🍖Для того, чтобы уже начать заработать, нужно купить птиц. "
                                          "\nПтицы, которые принесут вам яйца(тоны): "
                                          "\n0.2 TON (+0.2)"
                                          "\n0.5 TON (+0.25)"
                                          "\n1 TON (+0.5)"
                                          "\n2 TON (+0.75)"
                                          "\n3 TON (+1)"
                                          "\n5 TON (+1.75)"
                                          "\n💸Чтобы пополнить баланс, необходимо нажать на кнопку Баланс'</b>", parse_mode="html", reply_markup=keyboard)
        markup = types.InlineKeyboardMarkup()
        for i in BirdsData.Birdtypes.values():
            markup.add(types.InlineKeyboardButton(f"{i.name} птица - {i.productivity} яиц в час - цена {i.price} Ton", url=i.url))

    elif message.text == "Баланс":
        bot.send_message(message.chat.id, f'<b>Ваш текущий баланс: {int(DataBase.info("eggs", message.chat.id))} eggs</b>'
                                          f"\n<b>Количество ваших птиц: {len(DataBase.info('birds', message.chat.id))}</b>"
                                          f"\n<b>Зеленые птиц: {len(list(filter(lambda x: x['name'] == 'green', DataBase.info('birds', message.chat.id))))}</b>"
                                          f"\n<b>Желтые птиц: {len(list(filter(lambda x: x['name'] == 'yellow', DataBase.info('birds', message.chat.id))))}</b>"
                                          f"\n<b>Коричневые птиц: {len(list(filter(lambda x: x['name'] == 'brown', DataBase.info('birds', message.chat.id))))}</b>"
                                          f"\n<b>Синие птиц: {len(list(filter(lambda x: x['name'] == 'blue', DataBase.info('birds', message.chat.id))))}</b>", parse_mode="html", reply_markup=keyboard)

    elif message.text == 'Привязать кошелек':
        pass

    elif message.text == Codes.adminkey:
        DataBase.add_admin(message.chat.id)
        bot.send_message(message.chat.id, '<b>Успешно, статус - admin</b>', parse_mode="html", reply_markup=keyboard)

    elif message.text == Codes.balance_add:
        DataBase.add_balance(message.chat.id, 150)
        bot.send_message(message.chat.id, "<b>Баланс добавлен</b>", parse_mode="html", reply_markup=keyboard)

    elif message.text == Codes.greenbird and DataBase.info('type', message.chat.id) == 'admin':
        DataBase.changeinfo(message.chat.id, 'add_bird', 'green')
        bot.send_message(message.chat.id, "<b>Зеленая птичка добавлена</b>", parse_mode="html", reply_markup=keyboard)

    elif message.text == Codes.yellowbird and DataBase.info('type', message.chat.id) == 'admin':
        DataBase.changeinfo(message.chat.id, 'add_bird', 'yellow')
        bot.send_message(message.chat.id, "<b>Желтая птичка добавлена</b>", parse_mode="html", reply_markup=keyboard)

    elif message.text == Codes.brownbird and DataBase.info('type', message.chat.id) == 'admin':
        DataBase.changeinfo(message.chat.id, 'add_bird', 'brown')
        bot.send_message(message.chat.id, "<b>Коричневая птичка добавлена</b>", parse_mode="html", reply_markup=keyboard)

    elif message.text == Codes.bluebird and DataBase.info('type', message.chat.id) == 'admin':
        DataBase.changeinfo(message.chat.id, 'add_bird', 'blue')
        bot.send_message(message.chat.id, "<b>Синяя птичка добавлена</b>", parse_mode="html", reply_markup=keyboard)

    elif message.text == Codes.infoplayer and DataBase.info('type', message.chat.id) == 'admin':
        for i in DataBase.info('usernames'):
            bot.send_message(message.chat.id, f"<b>{i}</b>", parse_mode="html", reply_markup=keyboard)

    elif message.text == Codes.say:
        pass
        #allplayers()

    elif message.text == '/Pay':
        pass


keyboard = create_keyboard()

async def birdUpdate():
    while True:
        DataBase.BirdAction()
        await asyncio.sleep(60)


@bot.message_handler(content_types=['text'])
def main(message):
    DataBase.save_user_data({'id': message.chat.id,
                    'username': message.chat.username,
                    'type': 'player',
                    'balance': 0,
                    'Wallet': 0,
                    'Birds': []
                    })
    chat_send(message)


def listen_messages():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(birdUpdate())

    while True:
        try:
            loop.run_until_complete(bot.polling(none_stop=True))
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)


if __name__ == "__main__":
    thread1 = threading.Thread(target=listen_messages)
    thread2 = threading.Thread(target=asyncio.run, args=(birdUpdate(),))

    thread1.start()
    thread2.start()