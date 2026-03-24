"""
Общие утилиты для работы с паролями
Содержит класс для проверки паролей и вспомогательные функции
"""

import re
import math
import random
import string
from pathlib import Path
from colorama import Fore, Style


class PasswordCheck:
    """Класс для проверки надежности паролей и работы с базой уязвимых паролей"""
    
    def __init__(self, rockyou_file_path: Path):
        """
        Инициализация класса проверки паролей
        
        Args:
            rockyou_file_path: Путь к файлу с базой уязвимых паролей
        """
        self.rockyou_file_path = rockyou_file_path
        self._rockyou_cache = None
        self._rockyou_loaded = False
    
    def _load_rockyou_cache(self):
        """Загружает базу rockyou в память для быстрого поиска"""
        self._rockyou_loaded = True
        
        if not self.rockyou_file_path.exists():
            self._rockyou_cache = None
            return
        
        try:
            with open(self.rockyou_file_path, 'r', encoding='utf-8', errors='ignore') as filerok:
                self._rockyou_cache = set(line.strip() for line in filerok)
        except Exception:
            self._rockyou_cache = None
    
    def rockupasscheck(self, userpassword: str) -> bool:
        """
        Проверяет пароль на наличие в базе уязвимых паролей
        
        Args:
            userpassword: Проверяемый пароль
            
        Returns:
            True если пароль найден в базе, False если не найден
        """
        if not self._rockyou_loaded:
            self._load_rockyou_cache()
        
        if self._rockyou_cache is None:
            print(f"{Fore.RED}Файл {self.rockyou_file_path} не найден!{Style.RESET_ALL}")
            return False
        
        if userpassword in self._rockyou_cache:
            print(f"{Fore.RED}❌ Этот пароль найден в базе простых паролей!{Style.RESET_ALL}")
            return True
        
        print(f"{Fore.GREEN}✅ Этот пароль не найден в базе простых паролей{Style.RESET_ALL}")
        return False
    
    def rockupasscheck_silent(self, userpassword: str) -> bool:
        """
        Тихая проверка пароля без вывода сообщений
        
        Args:
            userpassword: Проверяемый пароль
            
        Returns:
            True если пароль найден в базе, False если не найден
        """
        if not self._rockyou_loaded:
            self._load_rockyou_cache()
        
        if self._rockyou_cache is None:
            return False
        
        return userpassword in self._rockyou_cache
    
    def coutentropy(self, password: str) -> float:
        """
        Вычисляет энтропию пароля по формуле H = L * log2(N)
        
        Args:
            password: Пароль для расчета энтропии
            
        Returns:
            Значение энтропии в битах
        """
        L = len(password)
        
        lowercase = set('abcdefghijklmnopqrstuvwxyz')
        uppercase = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        digits = set('0123456789')
        special = set('!@#$%^&*()_+-=[]{};:\'",.<>?/|\\')
        
        used_chars = set(password)
        N = 0
        
        if any(c in lowercase for c in used_chars):
            N += 26
        if any(c in uppercase for c in used_chars):
            N += 26
        if any(c in digits for c in used_chars):
            N += 10
        if any(c in special for c in used_chars):
            N += 33
        
        if N == 0:
            return 0
        
        H = L * math.log2(N)
        return H
    
    def evaluateent(self, entropy: float) -> tuple:
        """
        Оценивает уровень энтропии по критериям
        
        Args:
            entropy: Значение энтропии
            
        Returns:
            Кортеж (уровень, цвет, комментарий)
        """
        if entropy < 72:
            return "ненадежный", Fore.RED, "взлом практически мгновенный"
        elif entropy < 75:
            return "средний", Fore.YELLOW, "взлом возможен"
        else:
            return "надежный", Fore.GREEN, "взлом затруднен"
    
    def passsafecheck(self, password: str) -> str:
        """
        Основная проверка надежности пароля
        
        Args:
            password: Пароль для проверки
            
        Returns:
            Статус пароля: "надежный", "средний" или "слабый"
        """
        print(f"\n{Fore.MAGENTA}🔍 ПРОВЕРКА НАДЕЖНОСТИ:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}─" * 40)
        
        # Проверка длины
        length = len(password)
        if length < 8:
            print(f"{Fore.RED}❌ Длина: слишком короткий ({length} симв.){Style.RESET_ALL}")
            return "слабый"
        elif length < 12:
            print(f'{Fore.YELLOW}⚠️  Длина: средняя ({length} симв.) - рекомендуется 12+{Style.RESET_ALL}')
        else:
            print(f"{Fore.GREEN}✅ Длина: отличная ({length} симв.){Style.RESET_ALL}")
        

        entropy = self.coutentropy(password)
        entropy_level, entropy_color, entropy_comment = self.evaluateent(entropy)
        
        print(f"{entropy_color}🔢 Энтропия: {entropy:.2f} бит - {entropy_level.upper()}{Style.RESET_ALL}")
        print(f"{entropy_color}💡 {entropy_comment}{Style.RESET_ALL}")
        

        lower = bool(re.search(r'[a-z]', password))
        upper = bool(re.search(r'[A-Z]', password))
        digit = bool(re.search(r'\d', password))
        specialsimb = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/|\\]', password))

        categories = sum([lower, upper, digit, specialsimb])

        print(f"{Fore.WHITE}Категории символов:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN if lower else Fore.RED}•{Fore.WHITE} Строчные буквы: {'✓' if lower else '✗'}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN if upper else Fore.RED}•{Fore.WHITE} Заглавные буквы: {'✓' if upper else '✗'}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN if digit else Fore.RED}•{Fore.WHITE} Цифры: {'✓' if digit else '✗'}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN if specialsimb else Fore.RED}•{Fore.WHITE} Спецсимволы: {'✓' if specialsimb else '✗'}{Style.RESET_ALL}")
        
        
        if re.search(r'(.)\1{2,}', password):
            print(f"{Fore.YELLOW}⚠️  Обнаружены повторяющиеся символы{Style.RESET_ALL}")
        
        
        if entropy < 72:
            return "слабый"
        elif entropy < 75:
            if categories < 3:
                print(f"{Fore.YELLOW}⚠️  Мало категорий символов ({categories} из 4){Style.RESET_ALL}")
            return "средний"
        else:
            if categories >= 3:
                print(f"{Fore.GREEN}✅ Используются {categories} из 4 категорий символов{Style.RESET_ALL}")
                return "надежный"
            else:
                print(f"{Fore.YELLOW}⚠️  Энтропия высокая, но рекомендуется увеличить разнообразие символов{Style.RESET_ALL}")
                return "средний"


def get_password_strength_fast(password: str) -> tuple:
    """
    Сверхбыстрая проверка надежности пароля без вывода сообщений
    
    Args:
        password: Пароль для проверки
        
    Returns:
        Кортеж (уровень надежности, цвет)
        Уровень: "слабый", "средний" или "надежный"
    """

    length = len(password)
    if length < 8:
        return "слабый", Fore.RED
    

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    categories = sum([has_lower, has_upper, has_digit, has_special])
    
    if categories < 3:
        return "слабый", Fore.RED
    

    char_variety = 0
    if has_lower:
        char_variety += 26
    if has_upper:
        char_variety += 26
    if has_digit:
        char_variety += 10
    if has_special:
        char_variety += 20  
    
    entropy = length * math.log2(char_variety) if char_variety > 0 else 0
    
    if entropy < 72:
        return "слабый", Fore.RED
    elif entropy < 75:
        return "средний", Fore.YELLOW
    else:
        return "надежный", Fore.GREEN


def generate_single_password(length: int = 12) -> str:
    """
    Генерирует один надежный пароль с ограниченным количеством спецсимволов
    
    Args:
        length: Длина пароля (по умолчанию 12)
        
    Returns:
        Сгенерированный пароль
    """
    if length <= 8:
        special_count = 2
    elif length <= 12:
        special_count = random.randint(3, 4)
    elif length <= 16:
        special_count = random.randint(4, 5)
    else:
        special_count = random.randint(5, 6)
    
    remaining_chars = length - special_count
    digit_count = max(1, remaining_chars // 3)
    letter_count = remaining_chars - digit_count
    upper_count = max(1, letter_count // 2)
    lower_count = letter_count - upper_count
    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%&*+-=?"
    
    password_chars = []
    password_chars.append(random.choice(uppercase))
    password_chars.append(random.choice(lowercase))
    password_chars.append(random.choice(digits))
    password_chars.append(random.choice(special_chars))
    
    remaining = length - 4
    if remaining > 0:
        all_chars = lowercase + uppercase + digits + special_chars
        password_chars.extend(random.choice(all_chars) for _ in range(remaining))
    
    random.shuffle(password_chars)
    password = ''.join(password_chars)
    
    return password