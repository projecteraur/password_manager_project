# Password Strength Checker

## <span style="color: #3498db;">Установка словаря паролей</span>

Для работы программы необходим файл словаря `rockyou_simpl_passw.txt`.

### <span style="color: #2ecc71;">Автоматическая загрузка (рекомендуется)</span>

Выполните команду в терминале из корневой папки проекта:

**<span style="color: #e67e22;">Windows (PowerShell):</span>**
```powershell
New-Item -ItemType Directory -Force -Path data; Invoke-WebRequest -Uri "https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_05.txt" -OutFile "data/rockyou_simpl_passw.txt"
