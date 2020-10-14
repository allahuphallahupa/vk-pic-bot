import requests
import vk_api
import json
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

class VkBot:
    def __init__(self, token):
        self.token = token
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()  #api
        print('auth successful')

    def send_message(self, msg, user_id, attachment=None):
        """
        Отправляет сообщение
        :param msg: текст сообщения
        :param user_id: id пользователя
        :param attachment: фото в формате <type><owner_id>_<media_id>
        :return: None
        """
        self.vk.messages.send(user_id=user_id, message=msg, random_id = get_random_id(), attachment=attachment)
        print('Отправлено для ' + str(user_id) + ': ' + msg)

    def get_upload_server_url(self):
        """
        Получает url сервера на который нужно загружать картинку
        :return: url
        """
        return self.vk.photos.getMessagesUploadServer()['upload_url']

    @staticmethod
    def upload_img_to_server(url, path):
        """
        Загружает картинку на сервер
        :param url: url сервера, полученный в функции get_upload_server_url
        :param path: путь к файлу фотографии, которую нуэно загрузить
        :return: словарь с параметрами server, photo, hash
        """
        return requests.post(url, files={'file':open(path, 'rb')}).json()

    def save_messages_photo(self, photo, server, hsh):
        """

        :param photo: параметр полученный в функции upload_img_to_server
        :param server: параметр полученный в функции upload_img_to_server
        :param hsh: параметр полученный в функции upload_img_to_server
        :return: словарь с owner_id и id, которые требуются для  отправки фото в сообщении
        """
        return self.vk.photos.saveMessagesPhoto(photo=photo, server=server, hash=hsh)

    def get_message(self):
        """
        Получает сообщение с свервера
        :return: Сообщение
        """
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text:
                print('Получено в ' + str(event.datetime) + ' от ' + str(event.user_id) + ': ' + event.text)
                message = {'text': event.text, 'id': event.user_id }
                return message