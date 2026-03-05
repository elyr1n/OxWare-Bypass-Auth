import requests
import logging
import easyocr
import cv2
import os
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

    csrf_response = session.get("https://oxware.ru/login.php", headers=headers)
    logging.info("Получаю CSRF-Токен...")

    csrf_token = re.search(
        r'name="csrf" value="([a-z0-9]+)"', csrf_response.text
    ).group(1)
    logging.info(f"CSRF-Токен получен: {csrf_token}")

    data = {
        "csrf": csrf_token,
        "username": username,
        "password": password,
        "captcha": get_captcha_text(),
    }

    response_login = session.post(
        "https://oxware.ru/login.php", headers=headers, data=data
    )

    messages = [
        "Invalid captcha",
        "Invalid username or password",
        "Session expired. Refresh the page and try again.",
    ]

    for message in messages:
        if message in response_login.text:
            logging.info(message)
            break
    else:
        logging.info(
            "Успешно вошли в аккаунт, обходя методы защиты - получение CSRF-Токена, получение капчи с фото!"
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
