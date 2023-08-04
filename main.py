import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import codecs
import re
import random


class MyApp:

    # Создание всех виджетов (объектов)
    def __init__(self):
        super().__init__()
        self.list_url = []
        print('AVITO-Parser')
        print('"Добавить - 1", "Сохранить - 2", "Загрузить - 3", "Старт - 4"')
        self.in_text()

    def in_text(self):
        hello_text = input('Что хотите сделать: ')
        if hello_text == '1':
            self.input_url_list()
        if hello_text == '2':
            self.save_url_list()
        if hello_text == '3':
            self.load_url_list()
        if hello_text == '4':
            self.count_url()
        else:
            print("Неверно введённые данные. Повторите запрос.")
            self.in_text()
        print(hello_text)

    def save_url_list(self):
        saved_urls = open('saved_urls.txt', 'w', encoding='utf8')
        saved_urls.write(" ".join(self.list_url))
        saved_urls.close()
        print("Файл сохранён")
        self.in_text()

    def input_url_list(self):
        print('Чтобы добавить url уже к имеющимся, сначала загрузите основной файл.\nВернуться назад - q')
        append_url = input('Введите url: ')
        if append_url != 'q':
            self.list_url.append(append_url)
            print(self.list_url)
            self.input_url_list()
        else:
            self.in_text()

    def convert_list(self):
        # отображение списка в консоли после загрузки в читаемом виде
        str = ''
        for i in self.list_url:
            str += f'{i}\n'
        return str

    def load_url_list(self):
        try:
            loaded_urls = open('saved_urls.txt', 'r', encoding='utf8')
            self.list_url = loaded_urls.read()
            self.list_url = self.list_url.split()
            loaded_urls.close()
            print(self.convert_list())
            print("Файл загружен")
            self.in_text()
        except FileNotFoundError:
            print("Файл не найден")
            pass

    def count_url(self):
        for url in self.list_url:
            self.gen_url = url
            print(url)
            self.parse_url()

    def parse_url(self):
        options = webdriver.ChromeOptions()

        # user-agent
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64; Ubuntu 22.04) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")

        # for ChromeDriver version 114.
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.binary_location = os.getenv('/usr/bin/google-chrome')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')

        service = Service(executable_path='chromedriver')
        browser = webdriver.Chrome(service=service, options=options)

        try:
            print('parsing...')
            browser.get(self.gen_url)

            sec_fl = random.uniform(1, 3)
            sec_round = round(sec_fl, 1)

            time.sleep(sec_round)

            browser.implicitly_wait(0.5)

            n = os.path.join("page.html")

            f = codecs.open(n, "w", "utf−8")
            h = browser.page_source
            f.write(h)

            time.sleep(sec_round)
            browser.quit()
            self.convert_to_txt()
        except Exception as ex:
            print(ex)

    def convert_to_txt(self):
        print('converting...')
        timestr = time.strftime("%Y%m%d-%H%M%S")

        f = open("page.html", "r", encoding='utf8')
        f2 = open(f"parse_{timestr}.txt", "w")
        f3 = open('all.txt', "a")
        for i in re.findall("<p>(.*?)</p>", str(f.read())):
            text2 = i
            text3 = re.sub(r'<br>', '\n', str(text2))
            # text2 = text2.replace("\n<br>\n\n", "\n\n")
            f2.write(text3 + '\n\n')
            f3.write(text3 + '\n\n')

        f.close()
        f2.close()
        f3.close()
        print('DONE!\nnext>>>')

        while self.list_url:
            del self.list_url[0]
            self.count_url()


def main():
    MyApp()


if __name__ == '__main__':
    main()
