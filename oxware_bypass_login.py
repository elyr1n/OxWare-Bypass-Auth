import requests
import string
import random
import logging
import re

username = input("Введите логин: ")
password = input("Введите пароль: ")

logging.addLevelName(logging.INFO, "\033[92mINFO\033[0m")
logging.addLevelName(logging.ERROR, "\033[91mERROR\033[0m")
logging.basicConfig(
    level=logging.INFO,
    format="[\033[90m%(asctime)s\033[0m] | [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
)

cookies = {
    "PHPSESSID": "".join(random.choices(string.ascii_letters + string.digits, k=32))
}
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "referer": "https://oxware.ru/",
}

if __name__ == "__main__":
    try:
        response_captcha = requests.get(
            "https://oxware.ru/captcha.php", headers=headers, cookies=cookies
        )

        if response_captcha.status_code == 200:
            logging.info("Получаю капчу...")
        else:
            logging.error(
                f"Не смог получить капчу. Статус код ошибки: {response_captcha.status_code}"
            )
            exit()

        captcha = re.findall(r"<text[^>]*>(.*?)</text>", response_captcha.text)
        captcha_text = "".join(captcha)

        logging.info(f"Получил код капчи: {captcha_text}")

        data = {
            "username": username,
            "password": password,
            "captcha": captcha_text,
        }

        response_login = requests.post(
            "https://oxware.ru/login.php", headers=headers, cookies=cookies, data=data
        )

        messages = [
            "Неверные данные для входа",
            "Неверная капча",
        ]

        for message in messages:
            if message in response_login.text:
                logging.info(message)
                break
        else:
            logging.info(
                "Успешно обошли капчу, правильный PHPSESSID и вошли в аккаунт!"
            )
    except KeyboardInterrupt:
        pass
