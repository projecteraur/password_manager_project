# ⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀**Password Manager Guide**

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀![Превью программы](https://github.com/projecteraur/password_manager_project/blob/main/others/preview1.png?raw=true)

## ⬇ Установка и запуск программы
1. **Установите Python:** Если он не установлен, скачайте его с [официального сайта](https://www.python.org/)
2. **Проверьте pip:** Если команды `pip` нет, воспользуйтесь [инструкцией по установке](https://pip.pypa.io/en/stable/installation/)
3. **Подготовьте проект:** Скачайте архив с кодом и разархивируйте его в удобную папку
4. **Установите зависимости:** Откройте терминал в папке проекта и выполните установку библиотек (см. ниже)
5. **Загрузите словарь:** Выполните установку базы паролей (автоматически или вручную см. ниже)
6. **Запуск:** Запустите программу командой: `python main.py`

## 📦 Установка зависимостей

Для работы интерфейса (цветного текста) требуется библиотека `colorama`. Установите её одной командой:
```bash
pip install -r requirements.txt
```

## Установка базы паролей

Для работы программы необходим файл словаря `rockyou_simpl_passw.txt`

## ⚙ Автоматическая загрузка

Выполните команду в терминале из **корневой папки проекта**:

```bash
mkdir -p data

wget -O data/rockyou_simpl_passw.txt https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_05.txt
```

## ✋ Ручная загрузка

1. Скачайте фаил по ссылке: [rockyou_2025_05.txt](https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_05.txt)

3. Переименуйте скачанный фаил в `rockyou_simpl_passw.txt`

4. Переместите этот фаил в папку `main project/data/`

