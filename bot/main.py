import vk
import requests
import json
from time import sleep
from random import randint
from datetime import datetime
from database import Database

database = Database()

token = 'e80e5de9b7623bc4158531cd3d14f8f569d8b551f5b1e1521bcb6c5ba4e52d309221095b952b347158059'
session = vk.AuthSession(access_token=token)
vk_api = vk.API(session, v='5.103')


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
                    "payload": json.dumps(payload),
                    "label": label
        },
        "color": color
    }

keyboard_activated = {
    'one_time': False,
    "buttons": [
        [get_button("Добавить интересы", "primary")],
        [get_button("Отключить рассылку", "positive")]
    ]
}

keyboard = {
    'one_time': True,
    "buttons": [
        [get_button("Начать", "primary")],
    ]
}

keyboard_choose = {
    'one_time': False,
    "buttons": [
        [get_button("Добавить информатика", "primary")],
        [get_button("Добавить математика", "primary")],
        [get_button("Добавить физика", "primary")],
        [get_button("Добавить английский язык", "primary")],
        [get_button("Добавить русский язык", "primary")],
        [get_button("Добавить право", "primary")],
        [get_button("Готово", "positive")],
    ]
}

interests = ["информатика", "математика", "физика", "английский язык", "русский язык", "право"]

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard_activated = json.dumps(keyboard_activated, ensure_ascii=False).encode('utf-8')
keyboard_activated = str(keyboard_activated.decode('utf-8'))


keyboard_choose = json.dumps(keyboard_choose, ensure_ascii=False).encode('utf-8')
keyboard_choose = str(keyboard_choose.decode('utf-8'))


def get_messages(vk_api):

    return vk_api.messages.getConversations(offset=0, filter='unread')


def send_message(vk_api, user_id, type, message):
    global keyboard_activated
    global keyboard
    global keyboard_choose

    if type == 'conf':
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message='Рассылка активирована!\nЧтобы отключить рассылку, нажмите на кнопку "Отключить рассылку"', keyboard=keyboard_activated)

    elif type == "understand_false":
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message='Команда не распознана')
    elif type == "on_error":
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message=message)
    elif type == "off":
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message="Жаль, что вы отписались(\nЕсли захотите снова присоединиться, отправьте мне слово 'Активация' или нажмите на кнопку 'Начать' !", keyboard=keyboard)
    elif type == "keyboard_activated":
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message="Доброго времени суток!", keyboard=keyboard_activated)
    elif type == "keyboard":
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message="Доброго времени суток!", keyboard=keyboard)
    elif type == "done":
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message="Принято", keyboard=keyboard_activated)
    elif type == "interests":
        vk_api.messages.send(user_id=user_id, peer_id=user_id, random_id=randint(-1000000, 100000000),
                             message="Выберите свои интересы с помощью кнопок", keyboard=keyboard_choose)



def get_username(vk_api, user_id):
    response = vk_api.users.get(user_ids=user_id)[0]
    return response['first_name'], response['last_name']


def activate(vk_api, messages_info):
    for i in range(messages_info['count']):

        last_message = messages_info['items'][i]['last_message']
        user_id = last_message['from_id']
        text = last_message['text']
        first_name = get_username(vk_api, user_id)[0]
        last_name = get_username(vk_api, user_id)[1]

        global database

        user = {
            'name': first_name,
            'last_name': last_name,
            'id': user_id,
            "interests": []
        }



        if database.check_in_users(user) != None:
            send_message(vk_api, user_id, 'keyboard_activated', None)
        else:
            send_message(vk_api, user_id, 'keyboard', None)



        if ("активация" in text.lower()) or ("начать" in text.lower()):
            if database.check_in_users(user) == None:
                database.add_user(user)
                send_message(vk_api, user_id, 'conf', None)
            else:
                send_message(vk_api, user_id, 'on_error',
                             "Ваш аккаунт уже был активирован!")
        elif "отключить" in text.lower():
            send_message(vk_api, user_id, 'keyboard', None)
            if database.check_in_users(user) == None:
                send_message(vk_api, user_id, 'on_error',
                             "Вашего аккаунта нет в нашей базе!")
            else:
                if database.delete_user(user):
                    send_message(vk_api, user_id, 'off', None)
                else:
                    send_message(vk_api, user_id, 'on_error',
                                 "Произошла ошибка! Напиши разработчику <a href='https://vk.com/gppetr'>Пётр Говорухин</a>")
        elif "интересы" in text.lower():
            if "добавить интересы" in text.lower():
                send_message(vk_api, user_id, 'interests', None)
        if text.lower().replace('добавить ', '') in interests:
            user['interests'].append(text.lower().replace('добавить ', ''))
            print(user['interests'])
            send_message(vk_api, user_id, 'done', "Принято")
        if "готово" in text.lower():
            send_message(vk_api, user_id, 'done', "Принято")




        else:
            send_message(vk_api, user_id, "understand_false", None)


while True:
    messages_info = get_messages(vk_api)
    activate(vk_api, messages_info)
    sleep(2.5)
