# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ℹ Password Manager Guide

## ⬇ Установка и запуск программы
1. Скачайте архив с проектом и разархивируйте его.
2. Откройте папку проекта в терминале.
3. Выполните установку базы данных паролей (см. ниже).
4. Запустите файл `main.py`.

## Установка словаря паролей

Для работы программы необходим файл словаря `rockyou_simpl_passw.txt`

## ⚙ Автоматическая загрузка

Выполните команду в терминале из корневой папки проекта:

```bash
mkdir -p data

wget -O data/rockyou_simpl_passw.txt https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_05.txt
```

## ✋ Ручная загрузка

1. Скачайте фаил по ссылке ниже:
- https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_05.txt

3. Переименуйте скачанный фаил в `rockyou_simpl_passw.txt`

4. Переместите данный фаил в папку `main project/data/`

