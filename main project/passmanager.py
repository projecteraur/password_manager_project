"""
Модуль управления сохраненными паролями
Содержит функции для работы с файлом паролей, поиска, удаления дубликатов и создания бэкапов
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style


from password_utils import get_password_strength_fast


def password_management_main(password_file: Path, backup_dir: Path):
    """
    Главная функция управления паролями
    
    Args:
        password_file: Путь к файлу с паролями
        backup_dir: Путь к директории для резервных копий
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_password_management_menu()
        
        try:
            choice = input(f"{Fore.CYAN}Выберите пункт меню: {Style.RESET_ALL}").strip()
        except Exception:
            print(f"\n{Fore.YELLOW}❌ Операция отменена{Style.RESET_ALL}")
            return
        
        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            find_password_by_query(password_file)
        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            show_file_directory(password_file)
        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            display_first_n_passwords(password_file)
        elif choice == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            display_last_n_passwords(password_file)
        elif choice == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            display_all_passwords(password_file)
        elif choice == "6":
            os.system('cls' if os.name == 'nt' else 'clear')
            remove_or_replace_duplicates(password_file, backup_dir)
        elif choice == "7":
            os.system('cls' if os.name == 'nt' else 'clear')
            delete_all_passwords(password_file, backup_dir)
        elif choice == "8":
            os.system('cls' if os.name == 'nt' else 'clear')
            create_backup(password_file, backup_dir)
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}❌ Неверный выбор!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def show_password_management_menu():
    """Отображение меню управления паролями"""
    menu = f"""
{Fore.MAGENTA}+------------------------------------+
{Fore.MAGENTA}|{Fore.GREEN}        УПРАВЛЕНИЕ ПАРОЛЯМИ         {Fore.MAGENTA}|
{Fore.MAGENTA}+------------------------------------+
{Fore.MAGENTA}| {Fore.YELLOW}1.{Fore.WHITE} Найти пароль                    {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}2.{Fore.WHITE} Вывести расположение файла      {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}3.{Fore.WHITE} Вывести n первых паролей        {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}4.{Fore.WHITE} Вывести n последних паролей     {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}5.{Fore.WHITE} Вывести все пароли              {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}6.{Fore.WHITE} Удалить/заменить дубликаты      {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}7.{Fore.WHITE} Удалить все пароли              {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}8.{Fore.WHITE} Управление резервными копиями   {Fore.MAGENTA}|
{Fore.MAGENTA}| {Fore.YELLOW}0.{Fore.WHITE} Назад                           {Fore.MAGENTA}|
{Fore.MAGENTA}+------------------------------------+
{Style.RESET_ALL}"""
    print(menu)


def find_password_by_query(password_file: Path):
    """
    Найти пароль по части/заметке/дате (регистронезависимый поиск)
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}🔍 Поиск паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    search_query = input(f"{Fore.YELLOW}Введите запрос для поиска (Enter - назад): {Style.RESET_ALL}").strip()
    
    if not search_query:
        print(f"{Fore.RED}❌ Действие отменено!{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    found_passwords = []
    
    try:
        with open(password_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
                if match:
                    password = match.group(1).strip()
                    note = match.group(2).strip()
                    date_str = match.group(3).strip()
                    
                    search_lower = search_query.lower()
                    
                    if (search_lower in password.lower() or 
                        search_lower in note.lower() or 
                        search_lower in date_str.lower()):
                        
                        found_passwords.append({
                            'password': password,
                            'note': note,
                            'date': date_str,
                            'line': line
                        })
    
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    if found_passwords:
        print(f"\n{Fore.GREEN}✅ Найдено записей: {len(found_passwords)}{Style.RESET_ALL}")
        print()
        
        for i, entry in enumerate(found_passwords, 1):
            
            password_part = f"pass: {entry['password']}"
            note_part = f"note: {entry['note']}"
            date_part = entry['date'][:10] if len(entry['date']) >= 10 else entry['date']
            
            formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_part}"
            print(f"{Fore.CYAN}{i:2d}.{Style.RESET_ALL} {formatted_line}")
    else:
        print(f"\n{Fore.RED}❌ По запросу '{search_query}' ничего не найдено{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def show_file_directory(password_file: Path):
    """
    Показать директорию файла с паролями
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📁 Расположение файла с паролями{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if password_file.exists():
        
        abs_path = password_file.absolute()
        
        directory = abs_path.parent
        
        file_size = password_file.stat().st_size
        
        print(f"{Fore.GREEN}📄 Имя файла: {Style.RESET_ALL}{password_file.name}")
        print(f"{Fore.GREEN}📁 Полный путь: {Style.RESET_ALL}{abs_path}")
        print(f"{Fore.GREEN}📂 Директория: {Style.RESET_ALL}{directory}")
        print(f"{Fore.GREEN}📊 Размер файла: {Style.RESET_ALL}{file_size} байт")
        
        
        try:
            stat_info = password_file.stat()
            created_time = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{Fore.GREEN}🕐 Создан: {Style.RESET_ALL}{created_time}")
            print(f"{Fore.GREEN}✏️ Изменен: {Style.RESET_ALL}{modified_time}")
        except:
            pass
        
        
        print(f"\n{Fore.CYAN}📋 Содержимое директории:{Style.RESET_ALL}")
        try:
            files = list(directory.iterdir())
            for file in sorted(files):
                if file.is_dir():
                    print(f"  {Fore.BLUE}📁 {file.name}{Style.RESET_ALL}")
                else:
                    print(f"  {Fore.WHITE}📄 {file.name}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Ошибка чтения директории: {e}{Style.RESET_ALL}")
            
    else:
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def display_first_n_passwords(password_file: Path):
    """
    Вывести первые n паролей из файла
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📄 Первые N паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        
        while True:
            
            n_str = input(f"{Fore.YELLOW}Введите количество записей для вывода (Enter/0 - отмена): {Style.RESET_ALL}").strip()
            
            
            if not n_str:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            
            if not n_str.isdigit():
                print(f"{Fore.RED}❌ Введите корректное число!{Style.RESET_ALL}")
                continue
            
            n = int(n_str)
            
            
            if n == 0:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            
            if n < 0:
                print(f"{Fore.RED}❌ Число должно быть больше 0!{Style.RESET_ALL}")
                continue
            
            
            break
        
        
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        total_records = len(non_empty_lines)
        
        if total_records == 0:
            print(f"{Fore.RED}❌ Файл с паролями пуст!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        
        if n > total_records:
            print(f"{Fore.YELLOW}⚠️ В файле всего {total_records} записей. Будет выведено {total_records} записей.{Style.RESET_ALL}")
            n = total_records
        
        print(f"\n{Fore.GREEN}📊 Вывод первых {n} записей из {total_records}:{Style.RESET_ALL}")
        print()

        
        for i in range(n):
            line = non_empty_lines[i]
            
            
            match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
            if match:
                password = match.group(1).strip()
                note = match.group(2).strip()
                date_str = match.group(3).strip()
                date_only = date_str[:10] if len(date_str) >= 10 else date_str
                
                
                password_part = f"pass: {password}"
                note_part = f"note: {note}"
                
                formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_only}"
                print(f"{Fore.CYAN}{i+1:2d}.{Style.RESET_ALL} {formatted_line}")
            else:
                
                print(f"{Fore.CYAN}{i+1:2d}.{Style.RESET_ALL} {line}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def display_last_n_passwords(password_file: Path):
    """
    Вывести последние n паролей из файла
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📃 Последние N паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        
        while True:
            
            n_str = input(f"{Fore.YELLOW}Введите количество записей для вывода (Enter/0 - отмена): {Style.RESET_ALL}").strip()
            
            
            if not n_str:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            
            if not n_str.isdigit():
                print(f"{Fore.RED}❌ Введите корректное число!{Style.RESET_ALL}")
                continue
            
            n = int(n_str)
            
            
            if n == 0:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            
            if n < 0:
                print(f"{Fore.RED}❌ Число должно быть больше 0!{Style.RESET_ALL}")
                continue
            
            
            break
        
        
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        total_records = len(non_empty_lines)
        
        if total_records == 0:
            print(f"{Fore.RED}❌ Файл с паролями пуст!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        
        if n > total_records:
            print(f"{Fore.YELLOW}⚠️ В файле всего {total_records} записей. Будет выведено {total_records} записей.{Style.RESET_ALL}")
            n = total_records
        
        print(f"\n{Fore.GREEN}📊 Вывод последних {n} записей из {total_records}:{Style.RESET_ALL}")
        print()

        
        start_index = total_records - n
        
        for i in range(n):
            line_index = start_index + i
            line = non_empty_lines[line_index]
            
            
            match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
            if match:
                password = match.group(1).strip()
                note = match.group(2).strip()
                date_str = match.group(3).strip()
                date_only = date_str[:10] if len(date_str) >= 10 else date_str
                
                
                password_part = f"pass: {password}"
                note_part = f"note: {note}"
                
                formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_only}"
                
                print(f"{Fore.CYAN}{line_index + 1:2d}.{Style.RESET_ALL} {formatted_line}")
            else:
                
                print(f"{Fore.CYAN}{line_index + 1:2d}.{Style.RESET_ALL} {line}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def display_all_passwords(password_file: Path):
    """
    Вывести все пароли из файла с нумерацией
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📋 Все сохраненные пароли{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        
        count = 0
        for line in lines:
            if line.strip():
                count += 1

        
        print(f"{Fore.GREEN}📊 Всего записей: {Style.RESET_ALL}", count)
        print()

        line_number = 1
        for line in lines:
            line = line.strip()
            if line:
                
                match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
                if match:
                    password = match.group(1).strip()
                    note = match.group(2).strip()
                    date_str = match.group(3).strip()
                    date_only = date_str[:10] if len(date_str) >= 10 else date_str
                    
                    
                    password_part = f"pass: {password}"
                    note_part = f"note: {note}"
                    
                    formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_only}"
                    print(f"{Fore.CYAN}{line_number:2d}.{Style.RESET_ALL} {formatted_line}")
                else:
                    
                    print(f"{Fore.CYAN}{line_number:2d}.{Style.RESET_ALL} {line}")
                
                line_number += 1
                
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def create_backup(password_file: Path, backup_dir: Path):
    """
    Создать резервную копию файла с паролями
    
    Args:
        password_file: Путь к файлу с паролями
        backup_dir: Путь к директории для резервных копий
    """
    print(f"\n{Fore.CYAN}💾 Создание резервной копии{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    
    backup_dir.mkdir(exist_ok=True)
    
    try:
        while True:
            
            backup_files = []
            if backup_dir.exists():
                for f in backup_dir.iterdir():
                    if f.is_file():
                        
                        normalized_name = f.name.lower()
                        
                        
                        clean_name = re.sub(r'[0-9_\-\.]', ' ', normalized_name)
                        clean_name = ' '.join(clean_name.split())  
                        
                        
                        keywords = [
                            'backup', 'urpasswordswishi', 'cleanup', 'clean', 
                            'replacement', 'replace', 'before', 'after'
                        ]
                        
                        
                        is_backup_file = any(keyword in clean_name for keyword in keywords)
                        
                        
                        is_backup_file = is_backup_file or any(keyword in normalized_name for keyword in keywords)
                        
                        if is_backup_file:
                            f_size = f.stat().st_size
                            f_time = f.stat().st_ctime
                            backup_files.append({
                                'name': f.name,
                                'path': f,
                                'size': f_size,
                                'time': f_time,
                                'clean_name': clean_name  
                            })
            
            
            backup_files.sort(key=lambda x: x['time'], reverse=True)
            
            
            if backup_files:
                print(f"{Fore.YELLOW}⚠️ У вас есть {len(backup_files)} резервных копий:{Style.RESET_ALL}")
                print()
                
                for i, bf in enumerate(backup_files[:5]):  
                    size_kb = bf['size'] / 1024
                    time_str = datetime.fromtimestamp(bf['time']).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"  {Fore.CYAN}{i+1}.{Style.RESET_ALL} {bf['name']}")
                    print(f"     {Fore.GREEN}Размер: {size_kb:.1f} KB | Создан: {time_str}{Style.RESET_ALL}")
                
                if len(backup_files) > 5:
                    print(f"  {Fore.WHITE}... и еще {len(backup_files) - 5} копий{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}⚠️ У вас нет резервных копий!{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}Что вы хотите сделать?{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}0{Style.RESET_ALL} - Удалить копию")
            print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Создать новую копию")
            
            try:
                action_choice = input(f"\n{Fore.CYAN}Выберите действие (0-1; Enter - отмена): {Style.RESET_ALL}").strip()
                
                if action_choice == "0":
                    
                    if not backup_files:
                        print(f"{Fore.RED}❌ У вас нет резервных копий для удаления!{Style.RESET_ALL}")
                        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"\n{Fore.CYAN}💾 Создание резервной копии{Style.RESET_ALL}")
                        print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
                        continue
                    
                    if len(backup_files) == 1:
                        
                        backup_to_delete = backup_files[0]
                    else:
                        
                        print(f"\n{Fore.CYAN}Какую копию удалить?{Style.RESET_ALL}")
                        for i, bf in enumerate(backup_files[:10]):  
                            size_kb = bf['size'] / 1024
                            time_str = datetime.fromtimestamp(bf['time']).strftime('%Y-%m-%d %H:%M:%S')
                            print(f"  {Fore.YELLOW}{i}{Style.RESET_ALL} - {bf['name']} ({Fore.GREEN}{size_kb:.1f} KB, {time_str}{Style.RESET_ALL})")
                        
                        try:
                            delete_choice = int(input(f"\n{Fore.CYAN}Введите номер копии для удаления (0-{min(9, len(backup_files)-1)}; Enter - отмена): {Style.RESET_ALL}").strip())
                            if 0 <= delete_choice < len(backup_files):
                                backup_to_delete = backup_files[delete_choice]
                            else:
                                print(f"{Fore.RED}❌ Неверный номер копии!{Style.RESET_ALL}")
                                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                                os.system('cls' if os.name == 'nt' else 'clear')
                                print(f"\n{Fore.CYAN}💾 Создание резервной копии{Style.RESET_ALL}")
                                print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
                                continue
                        except (ValueError, IndexError):
                            print(f"{Fore.RED}❌ Действие отменено!{Style.RESET_ALL}")
                            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"\n{Fore.CYAN}💾 Создание резервной копии{Style.RESET_ALL}")
                            print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
                            continue
                    
                    
                    size_kb = backup_to_delete['size'] / 1024
                    print(f"\n{Fore.CYAN}📊 Информация о копии:{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Файл:{Style.RESET_ALL} {backup_to_delete['name']}")
                    print(f"{Fore.GREEN}Размер:{Style.RESET_ALL} {size_kb:.1f} KB")
                    print(f"{Fore.GREEN}Создан:{Style.RESET_ALL} {datetime.fromtimestamp(backup_to_delete['time']).strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"\n{Fore.RED}⚠️ Вы уверены, что хотите удалить копию?{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}0{Style.RESET_ALL} - Нет")
                    print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Да")
                    
                    confirm = input(f"\n{Fore.CYAN}Подтвердите удаление (0-1): {Style.RESET_ALL}").strip()
                    
                    if confirm == "1":
                        backup_to_delete['path'].unlink()
                        print(f"{Fore.GREEN}✅ Копия успешно удалена!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}❌ Удаление отменено{Style.RESET_ALL}")
                    
                    input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                    
                elif action_choice == "1":
                    
                    original_size = password_file.stat().st_size
                    size_kb = original_size / 1024
                    
                    print(f"\n{Fore.CYAN}📊 Информация о создании копии:{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Исходный файл:{Style.RESET_ALL} {password_file.name}")
                    print(f"{Fore.GREEN}Размер исходного файла:{Style.RESET_ALL} {size_kb:.1f} KB")
                    print(f"{Fore.GREEN}Объем новой копии:{Style.RESET_ALL} {size_kb:.1f} KB")
                    
                    print(f"\n{Fore.YELLOW}⚠️ Вы уверены, что хотите создать резервную копию?{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}0{Style.RESET_ALL} - Нет")
                    print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Да")
                    
                    try:
                        confirm = input(f"\n{Fore.CYAN}Подтвердите создание копии (0-1): {Style.RESET_ALL}").strip()
                        
                        if confirm == "1":
                            
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            backup_filename = f"urpasswordswishi_backup_{timestamp}.txt"
                            backup_path = backup_dir / backup_filename
                            
                            
                            shutil.copy2(password_file, backup_path)
                            
                            print(f"\n{Fore.GREEN}✅ Резервная копия создана успешно!{Style.RESET_ALL}")
                            print(f"{Fore.CYAN}📁 Исходный файл: {Style.RESET_ALL}{password_file}")
                            print(f"{Fore.CYAN}💾 Резервная копия: {Style.RESET_ALL}{backup_path}")
                            print(f"{Fore.CYAN}📊 Размер копии: {Style.RESET_ALL}{Fore.GREEN}{size_kb:.1f} KB{Style.RESET_ALL}")
                            
                            
                            backup_files = []
                            for f in backup_dir.iterdir():
                                if f.is_file():
                                    normalized_name = f.name.lower()
                                    clean_name = re.sub(r'[0-9_\-\.]', ' ', normalized_name)
                                    clean_name = ' '.join(clean_name.split())
                                    keywords = ['backup', 'urpasswordswishi', 'cleanup', 'clean', 'replacement', 'replace', 'before', 'after']
                                    is_backup_file = any(keyword in clean_name for keyword in keywords)
                                    is_backup_file = is_backup_file or any(keyword in normalized_name for keyword in keywords)
                                    if is_backup_file:
                                        backup_files.append(f)
                            
                            print(f"{Fore.CYAN}📚 Всего резервных копий: {Style.RESET_ALL}{Fore.GREEN}{len(backup_files)}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}❌ Создание копии отменено{Style.RESET_ALL}")
                            
                    except Exception:
                        print(f"{Fore.YELLOW}❌ Операция отменена{Style.RESET_ALL}")
                    
                    input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            
                else:
                    
                    print(f"{Fore.YELLOW}❌ Операция отменена{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                    return
                
            except Exception:
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{Fore.YELLOW}❌ Операция отменена{Style.RESET_ALL}")
                return
            
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.CYAN}💾 Создание резервной копии{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка при работе с резервными копиями: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def delete_all_passwords(password_file: Path, backup_dir: Path):
    """
    Удалить все пароли из файла
    
    Args:
        password_file: Путь к файлу с паролями
        backup_dir: Путь к директории для резервных копий
    """
    print(f"\n{Fore.CYAN}🗑️ Удаление всех паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        total_records = len(non_empty_lines)
        
        if total_records == 0:
            print(f"{Fore.YELLOW}📭 Файл с паролями уже пуст{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        
        print(f"{Fore.RED}⚠️ ВНИМАНИЕ: Это действие необратимо!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}📊 Статистика файла:{Style.RESET_ALL}")
        print(f"   Всего записей: {total_records}")
        print(f"   Размер файла: {password_file.stat().st_size} байт")
        
        
        print(f"\n{Fore.CYAN}📋 Примеры записей (первые 3):{Style.RESET_ALL}")
        for i in range(min(3, total_records)):
            line = non_empty_lines[i]
            match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
            if match:
                password = match.group(1).strip()
                note = match.group(2).strip()
                date_str = match.group(3).strip()[:10]
                print(f"   {Fore.CYAN}{i+1}.{Style.RESET_ALL} pass: {password} | note: {note} | date: {date_str}")
        
        
        print(f"\n{Fore.CYAN}💾 Создать резервную копию перед удалением?{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Да, создать резервную копию")
        print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Нет, продолжить без резервной копии")
        print(f"{Fore.YELLOW}0{Style.RESET_ALL} - Отмена операции")
        
        backup_choice = input(f"\n{Fore.CYAN}Выберите действие (0-2): {Style.RESET_ALL}").strip()
        
        if backup_choice == "0":
            print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        backup_path = None
        if backup_choice == "1":
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_before_deletion_{timestamp}.txt"
            backup_path = backup_dir / backup_filename
            shutil.copy2(password_file, backup_path)
            print(f"{Fore.GREEN}✅ Создана резервная копия: {backup_filename}{Style.RESET_ALL}")
        
        
        print(f"\n{Fore.RED}🚨 ОПАСНОЕ ДЕЙСТВИЕ!{Style.RESET_ALL}")
        print(f"{Fore.RED}Вы собираетесь удалить ВСЕ {total_records} записей!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Для подтверждения введите '{Fore.RED}УДАЛИТЬ ВСЕ{Fore.CYAN}':{Style.RESET_ALL}")
        
        confirmation = input(f"{Fore.RED}Подтверждение: {Style.RESET_ALL}").strip()
        
        if confirmation != "УДАЛИТЬ ВСЕ":
            print(f"{Fore.YELLOW}❌ Удаление отменено{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        
        with open(password_file, 'w', encoding='utf-8') as f:
            f.write("")  
        
        
        new_size = password_file.stat().st_size
        
        print(f"\n{Fore.GREEN}✅ Все пароли успешно удалены!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Результат:{Style.RESET_ALL}")
        print(f"   Удалено записей: {total_records}")
        print(f"   Новый размер файла: {new_size} байт")
        
        if backup_path:
            print(f"{Fore.CYAN}💾 Резервная копия сохранена: {Style.RESET_ALL}{backup_path}")
        
        print(f"\n{Fore.YELLOW}⚠️ Файл с паролями теперь пуст.{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка при удалении паролей: {e}{Style.RESET_ALL}")
        
        if backup_path and backup_path.exists():
            try:
                shutil.copy2(backup_path, password_file)
                print(f"{Fore.GREEN}✅ Файл восстановлен из резервной копии{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}❌ Не удалось восстановить файл из резервной копии{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def remove_or_replace_duplicates(password_file: Path, backup_dir: Path):
    """
    Удалить или заменить дубликаты паролей
    
    Args:
        password_file: Путь к файлу с паролями
        backup_dir: Путь к директории для резервных копий
    """
    print(f"\n{Fore.CYAN}🔄 Управление дубликатами паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}────────────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        password_entries = []
        for line in lines:
            match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
            if match:
                password_entries.append({
                    'password': match.group(1).strip(),
                    'note': match.group(2).strip(),
                    'date': match.group(3).strip(),
                    'original_line': line
                })
        
        if not password_entries:
            print(f"{Fore.YELLOW}📭 Файл с паролями пуст{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        
        password_count = {}
        for entry in password_entries:
            password = entry['password']
            password_count[password] = password_count.get(password, 0) + 1
        
        duplicates = {pwd: count for pwd, count in password_count.items() if count > 1}
        
        if not duplicates:
            print(f"{Fore.GREEN}✅ Дубликаты не обнаружены{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        
        print(f"{Fore.YELLOW}🔍 Найдено {len(duplicates)} повторяющихся паролей:{Style.RESET_ALL}\n")
        
        for i, (password, count) in enumerate(duplicates.items(), 1):
            entries = [e for e in password_entries if e['password'] == password]
            print(f"{Fore.CYAN}{i}. Пароль: '{password}' ({count} записей){Style.RESET_ALL}")
            for j, entry in enumerate(entries, 1):
                date_short = entry['date'][:10]
                print(f"   {j}. Заметка: '{entry['note']}' | Дата: {date_short}")
            print()
        
        
        print(f"{Fore.CYAN}Выберите действие:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Удалить дубликаты (оставить первую запись)")
        print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Заменить дубликаты (изменить пароли)")
        print(f"{Fore.YELLOW}0{Style.RESET_ALL} - Отмена")
        
        action = input(f"\n{Fore.CYAN}Ваш выбор (0-2): {Style.RESET_ALL}").strip()
        
        if action == "1":
            remove_duplicates(password_file, backup_dir, password_entries, duplicates)
        elif action == "2":
            replace_duplicates(password_file, backup_dir, password_entries, duplicates)
        elif action == "0":
            print(f"{Fore.YELLOW}❌ Операция отменена{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Неверный выбор{Style.RESET_ALL}")
        
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def remove_duplicates(password_file: Path, backup_dir: Path, password_entries: list, duplicates: dict):
    """
    Удалить дубликаты паролей
    
    Args:
        password_file: Путь к файлу с паролями
        backup_dir: Путь к директории для резервных копий
        password_entries: Список всех записей паролей
        duplicates: Словарь дубликатов
    """
    print(f"\n{Fore.CYAN}🗑️ Удаление дубликатов{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}──────────────────────────{Style.RESET_ALL}")
    
    
    entries_to_keep = []
    seen_passwords = set()
    
    for entry in password_entries:
        if entry['password'] not in seen_passwords:
            entries_to_keep.append(entry)
            seen_passwords.add(entry['password'])
    
    entries_to_remove = len(password_entries) - len(entries_to_keep)
    
    if entries_to_remove == 0:
        print(f"{Fore.YELLOW}⚠️ Нечего удалять{Style.RESET_ALL}")
        return
    
    
    print(f"{Fore.YELLOW}📊 Статистика удаления:{Style.RESET_ALL}")
    print(f"   Всего записей: {len(password_entries)}")
    print(f"   Будет удалено: {entries_to_remove}")
    print(f"   Останется: {len(entries_to_keep)}")
    
    
    print(f"\n{Fore.CYAN}💾 Создать резервную копию?{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Да, создать резервную копию")
    print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Нет, продолжить без резервной копии")
    
    backup_choice = input(f"{Fore.CYAN}Выберите (1-2): {Style.RESET_ALL}").strip()
    
    backup_path = None
    if backup_choice == "1":
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_before_cleanup_{timestamp}.txt"
        backup_path = backup_dir / backup_filename
        shutil.copy2(password_file, backup_path)
        print(f"{Fore.GREEN}✅ Создана резервная копия{Style.RESET_ALL}")
    
    
    print(f"\n{Fore.RED}⚠️ Подтвердите удаление{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Удалить дубликаты")
    print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Отмена")
    
    confirm = input(f"{Fore.CYAN}Ваш выбор (1-2): {Style.RESET_ALL}").strip()
    
    if confirm != "1":
        print(f"{Fore.YELLOW}❌ Удаление отменено{Style.RESET_ALL}")
        return
    
    
    try:
        with open(password_file, 'w', encoding='utf-8') as f:
            for entry in entries_to_keep:
                f.write(f"pass: {entry['password']} | note: {entry['note']} | date: {entry['date']}\n")
        
        print(f"\n{Fore.GREEN}✅ Успешно удалено {entries_to_remove} дубликатов{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Осталось записей: {len(entries_to_keep)}{Style.RESET_ALL}")
        
    except Exception as e:
        
        if backup_path and backup_path.exists():
            shutil.copy2(backup_path, password_file)
            print(f"{Fore.RED}❌ Ошибка! Файл восстановлен из резервной копии{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Критическая ошибка! Файл может быть поврежден{Style.RESET_ALL}")


def replace_duplicates(password_file: Path, backup_dir: Path, password_entries: list, duplicates: dict):
    """
    Заменить дубликаты паролей
    
    Args:
        password_file: Путь к файлу с паролями
        backup_dir: Путь к директории для резервных копий
        password_entries: Список всех записей паролей
        duplicates: Словарь дубликатов
    """
    print(f"\n{Fore.CYAN}🔄 Замена дубликатов{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}─────────────────────────{Style.RESET_ALL}")
    
    
    print(f"{Fore.CYAN}💾 Создать резервную копию?{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Да, создать резервную копию")
    print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Нет, продолжить без резервной копии")
    
    backup_choice = input(f"{Fore.CYAN}Выберите (1-2): {Style.RESET_ALL}").strip()
    
    backup_path = None
    if backup_choice == "1":
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_before_replacement_{timestamp}.txt"
        backup_path = backup_dir / backup_filename
        shutil.copy2(password_file, backup_path)
        print(f"{Fore.GREEN}✅ Создана резервная копия{Style.RESET_ALL}")
    
    updated_entries = password_entries.copy()
    replaced_count = 0
    save_and_exit = False
    
    
    for password in duplicates:
        if save_and_exit:
            break
            
        entries = [e for e in updated_entries if e['password'] == password]
        
        if len(entries) <= 1:
            continue
            
        print(f"\n{Fore.CYAN}🔄 Обработка пароля: '{password}'{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Найдено {len(entries)} записей:{Style.RESET_ALL}")
        
        
        for i, entry in enumerate(entries, 1):
            date_short = entry['date'][:10]
            print(f"   {i}. Заметка: '{entry['note']}' | Дата: {date_short}")
        
        
        for i, entry in enumerate(entries):
            if save_and_exit:
                break
                
            print(f"\n{Fore.CYAN}📝 Запись {i+1}/{len(entries)}:{Style.RESET_ALL}")
            print(f"   Заметка: '{entry['note']}'")
            print(f"   Текущий пароль: '{entry['password']}'")
            
            print(f"\n{Fore.CYAN}Действие для этой записи:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Заменить пароль")
            print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Пропустить")
            print(f"{Fore.YELLOW}3{Style.RESET_ALL} - Сохранить изменения и выйти")
            print(f"{Fore.YELLOW}0{Style.RESET_ALL} - Прервать замену (без сохранения)")
            
            choice = input(f"{Fore.CYAN}Выберите (0-3): {Style.RESET_ALL}").strip()
            
            if choice == "0":
                print(f"{Fore.YELLOW}❌ Замена прервана{Style.RESET_ALL}")
                
                if backup_path and backup_path.exists():
                    shutil.copy2(backup_path, password_file)
                    print(f"{Fore.GREEN}✅ Все изменения отменены, файл восстановлен{Style.RESET_ALL}")
                return
            elif choice == "1":
                while True:
                    new_password = input(f"{Fore.YELLOW}Введите новый пароль: {Style.RESET_ALL}").strip()
                    
                    if not new_password:
                        print(f"{Fore.RED}❌ Пароль не может быть пустым{Style.RESET_ALL}")
                        continue
                    
                    
                    strength, color = get_password_strength_fast(new_password)
                    print(f"{color}✓ Надежность пароля: {strength}{Style.RESET_ALL}")
                    
                    
                    if strength == "слабый":
                        print(f"{Fore.RED}⚠️  Этот пароль легко взломать!{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}Что делать с этим паролем?{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Да, использовать этот пароль")
                        print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Нет, ввести другой пароль")
                        
                        use_weak = input(f"{Fore.CYAN}Выберите (1-2): {Style.RESET_ALL}").strip()
                        if use_weak != '1':
                            continue  
                    
                    break  
                
                
                print(f"{Fore.YELLOW}Текущая заметка: '{entry['note']}'{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Изменить заметку?{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Да, изменить заметку")
                print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Нет, оставить текущую")
                
                change_note = input(f"{Fore.CYAN}Выберите (1-2): {Style.RESET_ALL}").strip()
                
                if change_note == "1":
                    new_note = input(f"{Fore.YELLOW}Введите новую заметку: {Style.RESET_ALL}").strip()
                    if new_note:
                        entry['note'] = new_note
                
                
                entry['password'] = new_password
                entry['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                replaced_count += 1
                
                print(f"{Fore.GREEN}✅ Пароль заменен{Style.RESET_ALL}")
            elif choice == "2":
                print(f"{Fore.YELLOW}⚠️ Запись пропущена{Style.RESET_ALL}")
            elif choice == "3":
                save_and_exit = True
                print(f"{Fore.GREEN}💾 Сохранение изменений...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}❌ Неверный выбор{Style.RESET_ALL}")
    
    
    try:
        with open(password_file, 'w', encoding='utf-8') as f:
            for entry in updated_entries:
                f.write(f"pass: {entry['password']} | note: {entry['note']} | date: {entry['date']}\n")
        
        if save_and_exit:
            print(f"\n{Fore.GREEN}✅ Изменения сохранены. Выход из замены дубликатов.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✅ Замена завершена{Style.RESET_ALL}")
            
        print(f"{Fore.CYAN}📊 Заменено паролей: {replaced_count}{Style.RESET_ALL}")
        
    except Exception as e:
        
        if backup_path and backup_path.exists():
            shutil.copy2(backup_path, password_file)
            print(f"{Fore.RED}❌ Ошибка! Файл восстановлен из резервной копии{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Критическая ошибка! Файл может быть поврежден{Style.RESET_ALL}")

def find_password_by_query(password_file: Path):
    """
    Найти пароль по части/заметке/дате (регистронезависимый поиск)
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}🔍 Поиск паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    search_query = input(f"{Fore.YELLOW}Введите запрос для поиска (Enter - назад): {Style.RESET_ALL}").strip()
    
    if not search_query:
        print(f"{Fore.RED}❌ Действие отменено!{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    found_passwords = []
    
    try:
        with open(password_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
                if match:
                    password = match.group(1).strip()
                    note = match.group(2).strip()
                    date_str = match.group(3).strip()
                    
                    search_lower = search_query.lower()
                    
                    if (search_lower in password.lower() or 
                        search_lower in note.lower() or 
                        search_lower in date_str.lower()):
                        
                        found_passwords.append({
                            'password': password,
                            'note': note,
                            'date': date_str,
                            'line': line
                        })
    
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    if found_passwords:
        print(f"\n{Fore.GREEN}✅ Найдено записей: {len(found_passwords)}{Style.RESET_ALL}")
        print()
        
        for i, entry in enumerate(found_passwords, 1):
            password_part = f"pass: {entry['password']}"
            note_part = f"note: {entry['note']}"
            date_part = entry['date'][:10] if len(entry['date']) >= 10 else entry['date']
            
            formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_part}"
            print(f"{Fore.CYAN}{i:2d}.{Style.RESET_ALL} {formatted_line}")
    else:
        print(f"\n{Fore.RED}❌ По запросу '{search_query}' ничего не найдено{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def show_file_directory(password_file: Path):
    """
    Показать директорию файла с паролями
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📁 Расположение файла с паролями{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if password_file.exists():
        abs_path = password_file.absolute()
        directory = abs_path.parent
        file_size = password_file.stat().st_size
        
        print(f"{Fore.GREEN}📄 Имя файла: {Style.RESET_ALL}{password_file.name}")
        print(f"{Fore.GREEN}📁 Полный путь: {Style.RESET_ALL}{abs_path}")
        print(f"{Fore.GREEN}📂 Директория: {Style.RESET_ALL}{directory}")
        print(f"{Fore.GREEN}📊 Размер файла: {Style.RESET_ALL}{file_size} байт")
        
        try:
            stat_info = password_file.stat()
            created_time = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{Fore.GREEN}🕐 Создан: {Style.RESET_ALL}{created_time}")
            print(f"{Fore.GREEN}✏️ Изменен: {Style.RESET_ALL}{modified_time}")
        except:
            pass
        
        print(f"\n{Fore.CYAN}📋 Содержимое директории:{Style.RESET_ALL}")
        try:
            files = list(directory.iterdir())
            for file in sorted(files):
                if file.is_dir():
                    print(f"  {Fore.BLUE}📁 {file.name}{Style.RESET_ALL}")
                else:
                    print(f"  {Fore.WHITE}📄 {file.name}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Ошибка чтения директории: {e}{Style.RESET_ALL}")
            
    else:
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def display_first_n_passwords(password_file: Path):
    """
    Вывести первые n паролей из файла
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📄 Первые N паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        while True:
            n_str = input(f"{Fore.YELLOW}Введите количество записей для вывода (Enter/0 - отмена): {Style.RESET_ALL}").strip()
            
            if not n_str:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            if not n_str.isdigit():
                print(f"{Fore.RED}❌ Введите корректное число!{Style.RESET_ALL}")
                continue
            
            n = int(n_str)
            
            if n == 0:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            if n < 0:
                print(f"{Fore.RED}❌ Число должно быть больше 0!{Style.RESET_ALL}")
                continue
            
            break
        
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        total_records = len(non_empty_lines)
        
        if total_records == 0:
            print(f"{Fore.RED}❌ Файл с паролями пуст!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        if n > total_records:
            print(f"{Fore.YELLOW}⚠️ В файле всего {total_records} записей. Будет выведено {total_records} записей.{Style.RESET_ALL}")
            n = total_records
        
        print(f"\n{Fore.GREEN}📊 Вывод первых {n} записей из {total_records}:{Style.RESET_ALL}")
        print()

        for i in range(n):
            line = non_empty_lines[i]
            
            match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
            if match:
                password = match.group(1).strip()
                note = match.group(2).strip()
                date_str = match.group(3).strip()
                date_only = date_str[:10] if len(date_str) >= 10 else date_str
                
                password_part = f"pass: {password}"
                note_part = f"note: {note}"
                
                formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_only}"
                print(f"{Fore.CYAN}{i+1:2d}.{Style.RESET_ALL} {formatted_line}")
            else:
                print(f"{Fore.CYAN}{i+1:2d}.{Style.RESET_ALL} {line}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def display_last_n_passwords(password_file: Path):
    """
    Вывести последние n паролей из файла
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📃 Последние N паролей{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        while True:
            n_str = input(f"{Fore.YELLOW}Введите количество записей для вывода (Enter/0 - отмена): {Style.RESET_ALL}").strip()
            
            if not n_str:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            if not n_str.isdigit():
                print(f"{Fore.RED}❌ Введите корректное число!{Style.RESET_ALL}")
                continue
            
            n = int(n_str)
            
            if n == 0:
                print(f"{Fore.RED}❌ Операция отменена{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                return
            
            if n < 0:
                print(f"{Fore.RED}❌ Число должно быть больше 0!{Style.RESET_ALL}")
                continue
            
            break
        
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        total_records = len(non_empty_lines)
        
        if total_records == 0:
            print(f"{Fore.RED}❌ Файл с паролями пуст!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
            return
        
        if n > total_records:
            print(f"{Fore.YELLOW}⚠️ В файле всего {total_records} записей. Будет выведено {total_records} записей.{Style.RESET_ALL}")
            n = total_records
        
        print(f"\n{Fore.GREEN}📊 Вывод последних {n} записей из {total_records}:{Style.RESET_ALL}")
        print()

        start_index = total_records - n
        
        for i in range(n):
            line_index = start_index + i
            line = non_empty_lines[line_index]
            
            match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
            if match:
                password = match.group(1).strip()
                note = match.group(2).strip()
                date_str = match.group(3).strip()
                date_only = date_str[:10] if len(date_str) >= 10 else date_str
                
                password_part = f"pass: {password}"
                note_part = f"note: {note}"
                
                formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_only}"
                print(f"{Fore.CYAN}{line_index + 1:2d}.{Style.RESET_ALL} {formatted_line}")
            else:
                print(f"{Fore.CYAN}{line_index + 1:2d}.{Style.RESET_ALL} {line}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")


def display_all_passwords(password_file: Path):
    """
    Вывести все пароли из файла с нумерацией
    
    Args:
        password_file: Путь к файлу с паролями
    """
    print(f"\n{Fore.CYAN}📋 Все сохраненные пароли{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}───────────────────────────────────────{Style.RESET_ALL}")
    
    if not password_file.exists():
        print(f"{Fore.RED}❌ Файл с паролями не найден{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        return
    
    try:
        with open(password_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        count = 0
        for line in lines:
            if line.strip():
                count += 1

        print(f"{Fore.GREEN}📊 Всего записей: {Style.RESET_ALL}", count)
        print()

        line_number = 1
        for line in lines:
            line = line.strip()
            if line:
                match = re.match(r'pass:\s*([^|]+)\s*\|\s*note:\s*([^|]+)\s*\|\s*date:\s*(.+)', line)
                if match:
                    password = match.group(1).strip()
                    note = match.group(2).strip()
                    date_str = match.group(3).strip()
                    date_only = date_str[:10] if len(date_str) >= 10 else date_str
                    
                    password_part = f"pass: {password}"
                    note_part = f"note: {note}"
                    
                    formatted_line = f"{password_part} {Fore.GREEN}|{Style.RESET_ALL} {note_part} {Fore.GREEN}|{Style.RESET_ALL} date: {date_only}"
                    print(f"{Fore.CYAN}{line_number:2d}.{Style.RESET_ALL} {formatted_line}")
                else:
                    print(f"{Fore.CYAN}{line_number:2d}.{Style.RESET_ALL} {line}")
                
                line_number += 1
                
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка чтения файла: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")

