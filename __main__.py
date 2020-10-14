import requests
import logging
import settings
import os
from vk_bot import VkBot
from parser_ import Parser


messages = {
    'start':'Что хочешь увидеть?',
    'accepted':'К вашим услугам',
    'denied':'А это?',
    'photo_sent':'Пойдет?',
    'wrong':'Ты где-то что-то перепутал, походу',
    'out_of_photos':'Видимо ни чем тебе помочь не смогу'
}

aliases = {
    'yes': ["да", "Да"],
    'no': ["Нет", "нет"]
}


def get_attachment(bot, query, image_number):
    parser = Parser(query)
    html = parser.get_html()
    # print("Страничка получена")
    img_url_list = parser.get_img_urls(html)
    # print("Список из url фотографий получен")
    img_bytes = parser.get_img_from_url(img_url_list, image_number)
    # print("Фотография в байтах получена")
    file_path = parser.create_img(img_bytes)
    # print("Путь к фотографии: " + file_path)
    url = bot.get_upload_server_url()
    # print("Адрес сервера для загрузки фотографий получен")
    server, photo, hash_ = bot.upload_img_to_server(url, file_path).values()
    response = bot.save_messages_photo(photo, server, hash_)
    # print('Фотография загружена на сервер вк')
    attachment = 'photo' + str(response[0]['owner_id']) + '_' + str(response[0]['id'])
    return attachment

def main():
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(name)s %(levelname)s:%(message)s', filename='log.log')
    logging.log(logging.DEBUG, 'started with token: {}'.format(os.getenv('TOKEN')))
    bot = VkBot(os.getenv('TOKEN'))
    while True:
        try:
            msg = bot.get_message()
            text, user_id = msg['text'], msg['id']
            query = text
            picture_accepted = False
            img_num = 0
            message = messages['photo_sent']
            while picture_accepted is False:
                attachment = get_attachment(bot, query, img_num)
                bot.send_message(message, user_id, attachment)
                text = bot.get_message()['text']
                while text not in aliases['no'] and text not in aliases['yes']:
                    bot.send_message(messages['wrong'], user_id)
                    text = bot.get_message()['text']
                else:
                    if text in aliases['yes']:
                        bot.send_message(messages['accepted'], user_id)
                        picture_accepted = True
                    else:
                        img_num+=1
                        message = messages['denied']
        except LookupError:
            bot.send_message(messages['out_of_photos'], user_id)
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    main()