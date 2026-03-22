# Password Manager
## Установка словаря паролей

Для работы программы необходим файл словаря `rockyou_simpl_passw.txt`.

### Автоматическая загрузка (рекомендуется)

Выполните команду в терминале из корневой папки проекта:

```bash
# Создать папку data, если её нет
mkdir -p data

# Скачать файл по ссылке
curl -L -o data/rockyou_simpl_passw.txt https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_05.txt
