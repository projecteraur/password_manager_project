"""
Основной модуль программы Password Manager
Точка входа в приложение
"""

import sys
import os
from pathlib import Path
from colorama import Fore, Style, init


init()


sys.path.insert(0, str(Path(__file__).parent))


from password_utils import PasswordCheck, get_password_strength_fast, generate_single_password
from passmanager import password_management_main


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PASSWORDS_FILE = DATA_DIR / "ur_password_project_pass.txt"
ROCKYOU_FILE = DATA_DIR / "rockyou_simpl_passw.txt"
BACKUP_DIR = BASE_DIR / "backups"


def ensure_data_directories():
    """Создает необходимые директории, если они не существуют"""
    DATA_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)


def menushow():
    """Отображение главного меню"""
    menu = f"""
{Fore.MAGENTA}+----------------------------------------+
{Fore.MAGENTA}|            {Fore.GREEN}PASSWORD MANAGER{Fore.MAGENTA}            |
{Fore.MAGENTA}|           {Fore.GREEN}(project_password){Fore.MAGENTA}           |
{Fore.MAGENTA}+----------------------------------------+
{Fore.MAGENTA}| {Fore.YELLOW}1.{Fore.WHITE} Проверить надежность пароля       {Fore.MAGENTA}  |
{Fore.MAGENTA}| {Fore.YELLOW}2.{Fore.WHITE} Создать надежный пароль           {Fore.MAGENTA}  |
{Fore.MAGENTA}| {Fore.YELLOW}3.{Fore.WHITE} Управление сохраненными паролями  {Fore.MAGENTA}  |
{Fore.MAGENTA}| {Fore.YELLOW}4.{Fore.WHITE} Советы по безопасности            {Fore.MAGENTA}  |
{Fore.MAGENTA}| {Fore.YELLOW}5.{Fore.WHITE} Информация о программе            {Fore.MAGENTA}  |
{Fore.MAGENTA}| {Fore.YELLOW}0.{Fore.WHITE} Выход                              {Fore.MAGENTA} |
{Fore.MAGENTA}+----------------------------------------+
{Style.RESET_ALL}"""
    print(menu)


def save_password_to_file(password, note):
    """Сохраняет пароль и подсказку в файл"""
    try:
        from datetime import datetime
        
        file_exists = PASSWORDS_FILE.exists()
        
        with open(PASSWORDS_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"pass: {password}  | note: {note}  | date: {timestamp}\n")
        
        if file_exists:
            print(f"{Fore.GREEN}✅ Пароль успешно добавлен в файл {PASSWORDS_FILE}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✅ Файл {PASSWORDS_FILE} создан и пароль сохранен{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка при сохранении пароля: {e}{Style.RESET_ALL}")


def ask_to_save_password(password):
    """Спрашивает пользователя, хочет ли он сохранить пароль"""
    print(f"\n{Fore.CYAN}💾 СОХРАНЕНИЕ ПАРОЛЯ:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}─" * 40)
    print(f"{Fore.YELLOW}Хотите сохранить этот надежный пароль?{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Enter - Не сохранять{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1 - Сохранить пароль{Style.RESET_ALL}")
    
    choice = input(f"{Fore.CYAN}Ваш выбор: {Style.RESET_ALL}").strip()
    
    if choice == "1":
        note = input(f"{Fore.CYAN}Введите подсказку или домен (например: gmail.com): {Style.RESET_ALL}").strip()
        if not note:
            note = "без подсказки"
        save_password_to_file(password, note)
    else:
        print(f"{Fore.YELLOW}Пароль не сохранен.{Style.RESET_ALL}")


def generate_secure_password():
    """Генерация безопасных паролей"""
    print(f"\n{Fore.MAGENTA}🔐 ГЕНЕРАТОР ПАРОЛЕЙ{Style.RESET_ALL}")
    print(f"{Fore.WHITE}─" * 40)
    
    
    while True:
        length_input = input(f"{Fore.CYAN}Введите длину пароля (по умолчанию 12): {Style.RESET_ALL}").strip()
        
        if not length_input:
            length = 12
            break
        
        try:
            length = int(length_input)
            if length < 12:
                print(f"{Fore.RED}⚠️ Ошибка: длина надежного пароля должна быть не менее 12 символов!{Style.RESET_ALL}")
            elif length > 50:
                print(f"{Fore.RED}⚠️ Ошибка: длина не может превышать 50 символов!{Style.RESET_ALL}")
            else:
                break
        except ValueError:
            print(f"{Fore.RED}⚠️ Ошибка: введите корректное число!{Style.RESET_ALL}")

    
    while True:
        count_input = input(f"{Fore.CYAN}Сколько паролей сгенерировать (по умолчанию 1): {Style.RESET_ALL}").strip()
        
        if not count_input:
            count = 1
            break
        
        try:
            count = int(count_input)
            if count < 1:
                print(f"{Fore.RED}⚠️ Ошибка: количество должно быть не менее 1!{Style.RESET_ALL}")
            elif count > 20:
                print(f"{Fore.RED}⚠️ Ошибка: количество не может превышать 20!{Style.RESET_ALL}")
            else:
                break
        except ValueError:
            print(f"{Fore.RED}⚠️ Ошибка: введите корректное число!{Style.RESET_ALL}")

    
    if count == 1:
        print(f"{Fore.YELLOW}🔄 Начинаю генерацию и автопроверку пароля...{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}🔄 Начинаю генерацию и автопроверку {count} паролей...{Style.RESET_ALL}")

    
    check = PasswordCheck(ROCKYOU_FILE)
    
    
    generated_passwords = []
    for i in range(count):
        password = generate_single_password(length)
        strength, color = get_password_strength_fast(password)
        generated_passwords.append((password, strength, color))
    
    
    print(f"\n{Fore.GREEN}✅ СГЕНЕРИРОВАННЫЕ ПАРОЛИ:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}─" * 40)
    
    for i, (password, strength, color) in enumerate(generated_passwords, 1):
        print(f"{Fore.WHITE}{i}. {password} {color}({strength}){Style.RESET_ALL}")
    
    
    print(f"\n{Fore.CYAN}💾 СОХРАНЕНИЕ ПАРОЛЕЙ:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}─" * 40)
    print(f"{Fore.YELLOW}Хотите сохранить какие-либо пароли?{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Enter - Не сохранять{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1 - Сохранить один пароль{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2 - Сохранить несколько паролей{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3 - Сохранить все пароли{Style.RESET_ALL}")
    
    save_choice = input(f"{Fore.CYAN}Ваш выбор: {Style.RESET_ALL}").strip()
    
    if save_choice == "1":
        
        try:
            pwd_num = int(input(f"{Fore.CYAN}Введите номер пароля для сохранения: {Style.RESET_ALL}").strip())
            if 1 <= pwd_num <= len(generated_passwords):
                password_to_save = generated_passwords[pwd_num - 1][0]
                note = input(f"{Fore.CYAN}Введите подсказку или домен (например: gmail.com): {Style.RESET_ALL}").strip()
                if not note:
                    note = "без подсказки"
                save_password_to_file(password_to_save, note)
            else:
                print(f"{Fore.RED}Неверный номер пароля!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Ошибка: введите корректный номер!{Style.RESET_ALL}")
            
    elif save_choice == "2":
        
        try:
            pwd_nums = input(f"{Fore.CYAN}Введите номера паролей для сохранения через пробел: {Style.RESET_ALL}").strip()
            if pwd_nums:
                nums = [int(num.strip()) for num in pwd_nums.split()]
                valid_nums = [num for num in nums if 1 <= num <= len(generated_passwords)]
                
                if valid_nums:
                    for num in valid_nums:
                        password_to_save = generated_passwords[num - 1][0]
                        print(f"\n{Fore.CYAN}Пароль {num}: {password_to_save}{Style.RESET_ALL}")
                        note = input(f"{Fore.CYAN}Введите подсказку для этого пароля: {Style.RESET_ALL}").strip()
                        if not note:
                            note = "без подсказки"
                        save_password_to_file(password_to_save, note)
                else:
                    print(f"{Fore.RED}Неверные номера паролей!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Не выбрано ни одного пароля для сохранения.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Ошибка: введите корректные номера!{Style.RESET_ALL}")
    
    elif save_choice == "3":
        
        print(f"\n{Fore.CYAN}💾 СОХРАНЕНИЕ ВСЕХ ПАРОЛЕЙ:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}─" * 40)
        print(f"{Fore.YELLOW}Выберите способ сохранения:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1 - Использовать одну подсказку для всех паролей{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2 - Вводить подсказку для каждого пароля отдельно{Style.RESET_ALL}")
        
        method_choice = input(f"{Fore.CYAN}Ваш выбор: {Style.RESET_ALL}").strip()
        
        if method_choice == "1":
            
            common_note = input(f"{Fore.CYAN}Введите общую подсказку для всех паролей: {Style.RESET_ALL}").strip()
            if not common_note:
                common_note = "без подсказки"
            
            for i, (password, strength, color) in enumerate(generated_passwords, 1):
                save_password_to_file(password, common_note)
            
            print(f"{Fore.GREEN}✅ Все {len(generated_passwords)} паролей сохранены с общей подсказкой: '{common_note}'{Style.RESET_ALL}")
            
        elif method_choice == "2":
            
            for i, (password, strength, color) in enumerate(generated_passwords, 1):
                print(f"\n{Fore.CYAN}Пароль {i}: {password}{Style.RESET_ALL}")
                note = input(f"{Fore.CYAN}Введите подсказку для этого пароля: {Style.RESET_ALL}").strip()
                if not note:
                    note = "без подсказки"
                save_password_to_file(password, note)
            
            print(f"{Fore.GREEN}✅ Все {len(generated_passwords)} паролей сохранены с индивидуальными подсказками{Style.RESET_ALL}")
        
        else:
            print(f"{Fore.RED}Неверный выбор!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Пароли не сохранены.{Style.RESET_ALL}")
    
    print(f"{Fore.WHITE}─" * 40)
    input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def passcheck():
    """Проверка надежности пароля"""
    check = PasswordCheck(ROCKYOU_FILE)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"\n{Fore.MAGENTA}🔍 АНАЛИЗ ПАРОЛЯ{Style.RESET_ALL}")
        print(f"{Fore.WHITE}─" * 40)
        
        userpassword = input(f"{Fore.CYAN}Введите пароль (Enter - назад): {Style.RESET_ALL}").strip()
        
        if not userpassword:
            break
        
        print()  
        
        
        if check.rockupasscheck(userpassword):
            print(f"{Fore.RED}❌ Пароль слишком простой!{Style.RESET_ALL}")
            print(f"{Fore.RED}❌ Использование такого пароля крайне небезопасно!{Style.RESET_ALL}")
        else:
            
            status = check.passsafecheck(userpassword)
            
            print(f"{Fore.WHITE}─" * 40)
            print(f"{Fore.CYAN}📊 ИТОГОВАЯ ОЦЕНКА:{Style.RESET_ALL}")
            
            if status == "надежный":
                print(f"{Fore.GREEN}✅ Ваш пароль надежный!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}💪 Взлом такого пароля затруднен{Style.RESET_ALL}")
                
                
                ask_to_save_password(userpassword)
                
            elif status == "средний":
                print(f"{Fore.YELLOW}⚠️  Ваш пароль не совсем надежный!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 Рекомендуем увеличить энтропию до 75+ бит{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Ваш пароль ненадежный!{Style.RESET_ALL}")
                print(f"{Fore.RED}❌ Взлом практически мгновенный - не используйте!{Style.RESET_ALL}")
        
        print(f"{Fore.WHITE}─" * 40)
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def show_security_tips():
    """Показать советы по безопасности"""
    print(f"\n{Fore.CYAN}🔒 СОВЕТЫ ПО БЕЗОПАСНОСТИ ПАРОЛЕЙ{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}────────────────────────────────────────{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Используйте пароли длиной не менее 12 символов")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Комбинируйте заглавные и строчные буквы, цифры и спецсимволы")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Не используйте один пароль для разных сервисов")
    print(f"{Fore.GREEN}4.{Style.RESET_ALL} Регулярно меняйте пароли (раз в 3-6 месяцев)")
    print(f"{Fore.GREEN}5.{Style.RESET_ALL} Используйте менеджер паролей для хранения")
    print(f"{Fore.GREEN}6.{Style.RESET_ALL} Включите двухфакторную аутентификацию где это возможно")
    print(f"{Fore.GREEN}7.{Style.RESET_ALL} Не используйте личную информацию в паролях (даты, имена)")
    print(f"{Fore.GREEN}8.{Style.RESET_ALL} Проверяйте свои пароли на утечки в базах данных")
    print(f"\n{Fore.YELLOW}💡 Помните: надежный пароль - это первый барьер защиты ваших данных!{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}────────────────────────────────────────{Style.RESET_ALL}")
    input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def show_program_info():
    """Показать информацию о программе"""
    print(f"\n{Fore.CYAN}ℹ️ ИНФОРМАЦИЯ О ПРОГРАММЕ{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}────────────────────────────────────────{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Название:{Style.RESET_ALL} Password Manager")
    print(f"{Fore.GREEN}Статус:{Style.RESET_ALL} Итоговый проект учащихся 10 класса")
    print(f"{Fore.GREEN}Разработчики:{Style.RESET_ALL} Панарин К., Курбонова С.")
    print(f"{Fore.GREEN}Назначение:{Style.RESET_ALL} Управление и генерация безопасных паролей")
    print(f"{Fore.MAGENTA}────────────────────────────────────────{Style.RESET_ALL}")
    input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
    
def main():
    """Главная функция программы"""
    
    ensure_data_directories()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        menushow()
        
        try:
            choice = input(f"{Fore.CYAN}Выберите пункт меню: {Style.RESET_ALL}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}Выход из программы...{Style.RESET_ALL}")
            break
        
        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            passcheck()
        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            generate_secure_password()
        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            password_management_main(PASSWORDS_FILE, BACKUP_DIR)
        elif choice == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            show_security_tips()
        elif choice == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            show_program_info()
        elif choice == "0":
            print(f"{Fore.GREEN}See u later! {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Ошибка: выберите верный пункт!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()