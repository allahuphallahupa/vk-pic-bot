import requests
import os
from bs4 import BeautifulSoup

class Parser:
    """
    Парсит google и скачивает одну фотографию в папку
    """
    def __init__(self, query):
        self.query = query + 'пнг'
        self.url = 'https://www.google.com/search?q=%s&sxsrf=ALeKk03EdglGgGFfInxcW3aTKgiFbD8YXw:1596023357466&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjQhJmqsvLqAhVKw4sKHedJAR8Q_AUoAXoECBoQAw&biw=2560&bih=1339' % self.query

    def get_html(self):
        """
        Получает страничику в которой лежат нужные фотографии
        :return: html-текст страницы
        :return type: str
        """
        return requests.get(self.url).text

    @staticmethod
    def get_img_urls(html_txt):
        """
        Парсит из полученной html-страницы список url фотографий
        :param html_txt: html-страница которую нужно распарсить
        :return: list
        """
        soup = BeautifulSoup(html_txt, 'html.parser')
        tag_img_list = soup.find_all('img', 't0fcAb')
        img_url_list =  [img['src'] for img in tag_img_list ]
        return img_url_list

    def create_img(self, img_bytes):
        """
        Создает фотографию
        :param img_bytes: фотография в формате multipart/form-data
        :return: Путь к фотографии
        """
        path = os.path.join('pics', 'pic.jpg')
        with open(path, 'wb') as file:
            file.write(img_bytes)
            return file.name

    @staticmethod
    def get_img_from_url(url_list, number):
        """
        Получает фотографии в формате multipart/form-data из списка url
        :param url_list: Список url фотографий, полученный в функции get_img_urls
        :param number: номер по списку фотографии, которую надо
        :return: фотография в формате multipart/form-data
        """
        img_bytes = requests.get(url=url_list[number]).content
        return img_bytes