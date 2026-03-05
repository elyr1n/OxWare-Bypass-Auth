import requests
import logging
import easyocr
import cv2
import os
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

session = requests.Session()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://oxware.ru/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


def get_captcha_text():
    response_captcha = session.get("https://oxware.ru/captcha.php", headers=headers)

    if response_captcha.status_code == 200:
        logging.info("Получаю капчу...")

        with open("captcha.png", "wb") as f:
            f.write(response_captcha.content)
    else:
        logging.error(
            f"Не смог получить капчу. Статус код ошибки: {response_captcha.status_code}"
        )
        exit()

    img = cv2.imread("captcha.png")
    img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)
    cv2.imwrite("captcha_text.png", thresh)

    reader = easyocr.Reader(["en"], gpu=False)
    result = reader.readtext("captcha_text.png", detail=0, paragraph=True)
    captcha = "".join(result).replace(" ", "").strip().upper()

    logging.info(f"Получил код капчи: {captcha}")

    os.remove("captcha.png")
    os.remove("captcha_text.png")

    return captcha


def main():
    session.get("https://oxware.ru/", headers=headers)

    csrf_response = session.get("https://oxware.ru/register.php", headers=headers)
    logging.info("Получаю CSRF-Токен...")

    csrf_token = re.search(
        r'name="csrf" value="([a-z0-9]+)"', csrf_response.text
    ).group(1)
    logging.info(f"CSRF-Токен получен: {csrf_token}")

    data = {
        "csrf": csrf_token,
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password,
        "referral_code": referral_code,
        "captcha": get_captcha_text(),
    }

    response_register = session.post(
        "https://oxware.ru/register.php", headers=headers, data=data
    )

    messages = [
        "Аккаунт успешно создан! Теперь вы можете войти.",
        "Пользователь с таким именем или email уже существует",
        "Имя пользователя должно быть от 3 до 20 символов",
        "Пароль должен содержать минимум 6 символов",
        "Имя пользователя может содержать только буквы, цифры и нижнее подчеркивание",
        "Неверный формат email",
        "Неверный формат реферального кода",
        "Неверная капча",
    ]

    for message in messages:
        if message in response_register.text:
            logging.info(message)
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
