import requests
import string
import random
import logging
import re

username = input("Введите логин, под которым будете регистрироваться: ")
email = input("Введите почту (можно любую): ")
password = input(
    "Введите пароль (минимум 6 символов, только буквы, цифры и спец. символы): "
)
referral_code = input("Реферальный код (можно не указывать): ")

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
            "email": email,
            "password": password,
            "confirm_password": password,
            "referral_code": referral_code,
            "captcha": captcha_text,
        }

        response_login = requests.post(
            "https://oxware.ru/register.php",
            headers=headers,
            cookies=cookies,
            data=data,
        )

        messages = [
            "Аккаунт успешно создан! Теперь вы можете войти.",
            "Пользователь с таким именем или email уже существует",
            "Имя пользователя должно быть от 3 до 20 символов",
            "Пароль должен содержать минимум 6 символов",
            "Имя пользователя может содержать только буквы, цифры и нижнее подчеркивание",
            "Неверный формат email",
            "Неверный формат реферального кода",
        ]

        for message in messages:
            if message in response_login.text:
                logging.info(message)
                break
        else:
            logging.info(
                "Успешно обошли капчу, правильное написание почты, правильный PHPSESSID и бесграничное кол-во символов в пароле!"
            )
    except KeyboardInterrupt:
        pass
