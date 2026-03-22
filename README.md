# 🔐 Password Strength Checker

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
</p>

---

## 📥 Установка словаря паролей

Для работы программы необходим файл словаря <code style="color: #f39c12;">rockyou_simpl_passw.txt</code>.

### 🤖 Автоматическая загрузка

<details>
<summary><b style="color: #3498db;">🪟 Windows (PowerShell)</b></summary>

```powershell
New-Item -ItemType Directory -Force -Path data; Invoke-WebRequest -Uri "https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_05.txt" -OutFile "data/rockyou_simpl_passw.txt"
