# OxWare-Bypass-Auth

---

## Русская версия

### Общая информация

Данный репозиторий представляет собой независимое исследование серверной логики сайта, распространяющего программное обеспечение для CS2.

---

### Обнаруженные проблемы

В ходе анализа были выявлены:

- Устаревший программный стек
- Известные CVE с уровнем риска - 7.0 и выше
- CAPTCHA распознаётся автоматически с помощью EasyOCR и OpenCV
- Отсутствие серверной валидации времени заполнения форм
- Возможность использования произвольного OXSESSID
- CSRF-токены извлекаются напрямую из HTML без дополнительной проверки

Это позволяет автоматизировать обход базовых защитных механизмов.

---

### Как работают скрипты

**oxware_bypass_login.py** и **oxware_bypass_register.py** демонстрируют следующий алгоритм:

1. **Инициализация сессии** — создаётся объект `requests.Session()` для сохранения кук между запросами.
2. **Получение CSRF-токена** — выполняется GET-запрос к `login.php` или `register.php`, из HTML извлекается CSRF-токен с помощью регулярного выражения.
3. **Загрузка CAPTCHA** — отправляется GET-запрос на `captcha.php`, изображение сохраняется локально.
4. **Обработка изображения** — с помощью OpenCV изображение увеличивается, переводится в оттенки серого, применяется пороговая бинаризация и инверсия цветов.
5. **Распознавание текста** — обработанное изображение передаётся в EasyOCR, результат очищается от пробелов и приводится к верхнему регистру.
6. **Отправка данных** — формируется POST-запрос с заполненными полями (логин, пароль, email, капча, CSRF-токен).
7. **Анализ ответа** — проверяется наличие ключевых фраз в ответе сервера для определения результата.

---

### Реакция на уязвимости

Была предпринята попытка связаться с администрацией ресурса для информирования о найденных проблемах. Некоторые меры были приняты, однако они не привели к полному устранению уязвимостей — скрипты продолжают успешно работать.

---

### Рекомендация

В качестве дружеской рекомендации - возможно, не стоит поручать проектирование архитектуры и защитных механизмов нейросети без последующего участия специалистов по безопасности.

---

### Правовой статус

Проект не распространяет вредоносное ПО и создан исключительно в исследовательских и образовательных целях. Автор не несёт ответственности за возможное неправомерное использование.

---

## English Version

### Overview

This repository contains independent security research analyzing the backend logic of a website distributing software related to CS2.

---

### Identified Issues

The assessment revealed:

- Outdated software stack
- Public CVEs with severity - 7.0 and higher
- CAPTCHA is automatically recognized using EasyOCR and OpenCV
- Lack of server-side form submission time validation
- Acceptance of arbitrary PHP session identifiers
- CSRF tokens are extracted directly from HTML without additional verification

These weaknesses allow automation of protection bypass.

---

### How Scripts Work

**oxware_bypass_login.py** and **oxware_bypass_register.py** demonstrate the following algorithm:

1. **Session initialization** — a `requests.Session()` object is created to persist cookies between requests.
2. **CSRF token retrieval** — a GET request is sent to `login.php` or `register.php`, CSRF token is extracted from HTML using regex.
3. **CAPTCHA download** — a GET request is sent to `captcha.php`, the image is saved locally.
4. **Image processing** — using OpenCV, the image is resized, converted to grayscale, thresholded, and inverted.
5. **Text recognition** — the processed image is passed to EasyOCR, the result is cleaned and converted to uppercase.
6. **Data submission** — a POST request is formed with filled fields (username, password, email, captcha, CSRF token).
7. **Response analysis** — the server response is checked for specific phrases to determine the outcome.

---

### Response to Vulnerabilities

An attempt was made to contact the site administration regarding the discovered issues. Some measures were taken, but they did not completely eliminate the vulnerabilities — the scripts continue to work successfully.

---

### Recommendation

As a friendly suggestion - it may be wise not to rely solely on a neural network when designing website architecture and security mechanisms.

---

### Legal Notice

This project does not distribute malware and is provided strictly for educational and research purposes. The author assumes no responsibility for misuse.

---

© Security Research Publication
