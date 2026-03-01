# Oxware-Bypass-Auth

---

## Русская версия

### Общая информация

Данный репозиторий представляет собой независимое исследование серверной логики сайта, распространяющего программное обеспечение для CS2.

Публикация выполнена после отсутствия реакции на попытки уведомления о проблемах безопасности.

---

### Обнаруженные проблемы

В ходе анализа были выявлены:

- Устаревший программный стек
- Известные CVE с уровнем риска - 7.0 и выше
- Некорректная реализация CAPTCHA (текст доступен напрямую в SVG)
- Отсутствие достаточной серверной валидации
- Возможность использования произвольного PHPSESSID
- Логические ошибки в механизмах аутентификации и регистрации

Это позволяет автоматизировать обход базовых защитных механизмов.

---

### Содержимое репозитория

Proof-of-Concept скрипты:

- oxware_bypass_login.py
- oxware_bypass_register.py

Они демонстрируют получение CAPTCHA, извлечение кода из SVG и обход логики проверки при определённых условиях.

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

The research was published after disclosure attempts received no response.

---

### Identified Issues

The assessment revealed:

- Outdated software stack
- Public CVEs with severity - 7.0 and higher
- Insecure CAPTCHA implementation (plaintext embedded in SVG)
- Insufficient server-side validation
- Acceptance of arbitrary PHP session identifiers
- Logical flaws in authentication and registration workflows

These weaknesses allow automation of protection bypass.

---

### Repository Contents

Proof-of-Concept scripts:

- oxware_bypass_login.py
- oxware_bypass_register.py

They demonstrate CAPTCHA retrieval, SVG parsing and authentication logic bypass under certain conditions.

---

### Recommendation

As a friendly suggestion - it may be wise not to rely solely on a neural network when designing website architecture and security mechanisms.

---

### Legal Notice

This project does not distribute malware and is provided strictly for educational and research purposes. The author assumes no responsibility for misuse.

---

© Security Research Publication

