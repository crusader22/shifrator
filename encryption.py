import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import pyAesCrypt
import os
from random import choice

# класс под дешифровку
op = ''
password_str = ''
flag = 0  # флаг шифровки/дешифровки


class Decryptor:
    def decryption(file, password):
        buffer_size = 512 * 1024
        pyAesCrypt.decryptFile(
            str(file),
            str(os.path.splitext(file)[0]),
            password,
            buffer_size
        )
        print(f"Файл {str(os.path.splitext(file))} расшифрован")
        os.remove(file)

    # функция которая позволяет забуриться вглубь директории
    def walking_by_dirs(dir, password):
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                try:
                    Decryptor.decryption(path, password)
                except Exception as ex:
                    print(ex)
            else:
                Decryptor.walking_by_dirs(path, password)


class Encriptor:
    def encryption(file, password):
        buffer_size = 512 * 1024
        pyAesCrypt.encryptFile(
            str(file),
            str(file) + ".crp",
            password,
            buffer_size
        )
        print(f"Файл {str(os.path.splitext(file))} зашифрован")
        os.remove(file)

    def walking_by_dirs(dir, password):
        for name in os.listdir(dir):
            path = os.path.join(dir, name)

            if os.path.isfile(path):
                try:
                    Encriptor.encryption(path, password)
                except Exception as ex:
                    print(ex)
            else:
                Encriptor.walking_by_dirs(path, password)


def open_dir():
    print('Открытие файла')
    global op
    op = fd.askdirectory()
    print(op)


def decrypt():
    entry.pack_forget()
    btn5.pack_forget()
    btn3.pack_forget()
    if op != "":
        entry.place(x=21, y=321)
        btn5.place(x=21, y=421)
    else:
        print("Неверно задана директория")


def encrypt():
    entry.pack_forget()
    btn5.pack_forget()
    btn3.pack_forget()
    if op != "":
        entry.place(x=21, y=321)
        btn3.place(x=21, y=421)
    else:
        print("Неверно задана директория")


def get_entry_enc():
    print(f"Шифровать: {op}, с паролем {entry.get()}")

    Encriptor.walking_by_dirs(f'{op}', entry.get())

    entry.delete(0, tk.END)
    entry.place_forget()
    btn3.place_forget()


def get_entry_dec():
    print(f"Раcшифровать: {op} c паролем {entry.get()}")

    Decryptor.walking_by_dirs(f"{op}", entry.get())

    entry.delete(0, tk.END)
    entry.place_forget()
    btn5.place_forget()


# _____________________


# Текcтовые шифровки:
# вспомогательные функции для фибонначи(
N = 30
fib = [0 for i in range(N)]


def largestFiboLessOrEqual(n):
    fib[0] = 1
    fib[1] = 2
    i = 2
    while fib[i - 1] <= n:
        fib[i] = fib[i - 1] + fib[i - 2]
        i += 1
    return (i - 2)


def fibonacciEncoding(n):
    index = largestFiboLessOrEqual(n)
    codeword = ['a' for i in range(index + 2)]
    i = index
    while (n):
        codeword[i] = '1'
        n = n - fib[i]
        i = i - 1
        while (i >= 0 and fib[i] > n):
            codeword[i] = '0'
            i = i - 1
    codeword[index + 1] = '1'
    return "".join(codeword)


# )

alf = '1234567890 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгджеёжзийклмнопрстуфхцчшщъыьэюя\n!,.;' + '"()?[]-_+=*^%$#@~`№%:/\|'


def Fi_shifr(n):
    password = alf
    code = {}
    for i in range(len(password)):
        code[password[i]] = fibonacciEncoding(i + 1)
    message = ''
    for i in n:
        message += code.get(i)
    print("Your encoded mes:\n", message, sep='')
    return message


def Fi_password_shifr(n):
    a = []
    for i in n:
        a.append(str(n.count(i)) + i)
    b = sorted(set(a), reverse=1)
    password = ''
    for i in b:
        password += i[-1]
    code = {}
    for i in range(len(password)):
        code[password[i]] = fibonacciEncoding(i + 1)
    message = ''
    try:
        for i in n:
            message += code.get(i)
        return [message, password]
    except TypeError as e:
        mb.showerror("Ошибка", "Неверно введеные данные")
        print(e)
        return False


def deFi_shifr(message, password=alf):
    a = message.split('11')
    itog = ''
    decode = {}
    for i in range(len(password)):
        decode[fibonacciEncoding(i + 1)] = password[i]
    try:
        for i in a[:-1]:
            itog += decode.get(i + '11')
        return itog
    except TypeError:
        mb.showerror("Ошибка", "Неверно введеные данные")
        return False


def Caesar_shifr(message, n):
    message = message.upper()
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyr_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    res = ''
    try:
        n = int(n)
        for i in message:
            if i in alphabet:
                res += alphabet[(alphabet.index(i) + n) % 26]
            elif i in cyr_alphabet:
                res += cyr_alphabet[(cyr_alphabet.index(i) + n) % 33]
            else:
                res += i
        return res
    except ValueError:
        mb.showerror("Ошибка", "Введите числовой пароль!")
        return ''


def deCaesar_shifr(message, n):
    message = message.upper()
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyr_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    res = ''
    try:
        n = int(n)
        for i in message:
            if i in alphabet:
                res += alphabet[(alphabet.index(i) - n) % 26]
            elif i in cyr_alphabet:
                res += cyr_alphabet[(cyr_alphabet.index(i) - n) % 33]
            else:
                res += i
        return res
    except ValueError:
        mb.showerror("Ошибка", "Введите числовой пароль!")
        return ''


def Affine_shifr(message, n):
    message = message.upper()
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyr_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    res = ''
    try:
        a, b = map(int, n.split())
        for i in message:
            if i in alphabet:
                res += alphabet[(alphabet.index(i) * a + b) % 26]
            elif i in cyr_alphabet:
                res += cyr_alphabet[(cyr_alphabet.index(i) * a + b) % 33]
            else:
                res += i
        return res
    except ValueError:
        mb.showerror("Ошибка", "Введите пароль в формате два числа через пробел (5 7)!")
        return ''


# вспомогательная функция для аффиной
def modReverse(a, b):
    r, s, t = [min(a, b), max(a, b)], [1, 0], [0, 1]
    while r[-1] != 1:
        q = r[-2] // r[-1]
        r.append(r[-2] - q * r[-1])
        s.append(s[-2] - q * s[-1])
        t.append(t[-2] - q * t[-1])
    return (s[-1] % r[1])


def deAffine_shifr(message, n):
    message = message.upper()
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyr_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    res = ''
    try:
        a, b = map(int, n.split())
        for i in message:
            if i in alphabet:
                res += alphabet[modReverse(a, 26) * (alphabet.index(i) - b) % 26]
            elif i in cyr_alphabet:
                res += cyr_alphabet[modReverse(a, 33) * (cyr_alphabet.index(i) - b) % 33]
            else:
                res += i
        return res
    except ValueError:
        mb.showerror("Ошибка", "Введите пароль в формате два числа через пробел (5 7)!")
        return ''


def Vernam_shifr(message):
    message = message.replace('\n', '')
    alfvernam = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    if not (set(message).issubset(set(alfvernam))):
        return False
    res = ''
    key = generate_key(message)
    for i in range(len(message)):
        res += alfvernam[(alfvernam.index(message[i]) ^ alfvernam.index(key[i]))]
    return [res, key]


# Вспомогательная функция для Вернама
def generate_key(message):
    length = len(message)
    alfvernam = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    key = ''.join(choice(alfvernam) for i in range(length))
    return key


def deVernam_shifr(res, key):
    res = res.replace('\n', '')
    key = key.replace('\n', '')
    alfvernam = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    if len(res) != len(key):
        return False
    if not (set(res).issubset(set(alfvernam))):
        return False
    message = ''
    for i in range(len(res)):
        message += alfvernam[(alfvernam.index(res[i]) ^ alfvernam.index(key[i]))]
    return message


# Функции нажатий на кнопки:

def Fi():  # шифровка фиббоначи (остальные кнопки отличатся будут только в строке (1) и соответственно алгоритмом шифровки)
    out_text.delete(1.0, tk.END)
    s = in_text.get(1.0, tk.END)
    s = Fi_shifr(s)  # строка (1)
    out_text.insert(1.0, s)


def deFi():  # расшифровка фиббоначи (остальные кнопки отличатся будут только в строке (1) и соответственно алгоритмом шифровки)
    in_text.delete(1.0, tk.END)
    s = out_text.get(1.0, tk.END)
    s = deFi_shifr(s)  # строка (1)
    in_text.insert(1.0, s)


def Fi_password():  # шифровка фиббоначи (с паролем)
    out_text.delete(1.0, tk.END)
    key_text.delete(1.0, tk.END)
    s = in_text.get(1.0, tk.END)
    s = Fi_password_shifr(s)  # строка (1)
    out_text.insert(1.0, s[0])
    key_text.insert(1.0, s[1])


def deFi_password():  # расшифровка фиббоначи (с паролем)
    in_text.delete(1.0, tk.END)
    s = out_text.get(1.0, tk.END)
    a = key_text.get(1.0, tk.END)
    s = deFi_shifr(s, a)  # строка (1)
    if s:
        in_text.insert(1.0, s)


def Caesar():  # шифровка Цезаря
    out_text.delete(1.0, tk.END)
    s = in_text.get(1.0, tk.END)
    a = key_text.get(1.0, tk.END)
    s = Caesar_shifr(s, a)  # строка (1)
    out_text.insert(1.0, s)


def deCaesar():  # расшифровка Цезаря
    in_text.delete(1.0, tk.END)
    s = out_text.get(1.0, tk.END)
    a = key_text.get(1.0, tk.END)
    s = deCaesar_shifr(s, a)  # строка (1)
    in_text.insert(1.0, s)


def Affine():  # Аффиная шифровка
    out_text.delete(1.0, tk.END)
    s = in_text.get(1.0, tk.END)
    a = key_text.get(1.0, tk.END)
    s = Affine_shifr(s, a)  # строка (1)
    out_text.insert(1.0, s)


def deAffine():  # Аффиная расшифровка
    in_text.delete(1.0, tk.END)
    s = out_text.get(1.0, tk.END)
    a = key_text.get(1.0, tk.END)
    s = deAffine_shifr(s, a)  # строка (1)
    in_text.insert(1.0, s)


def Vernam():  # шифровка Вернама
    out_text.delete(1.0, tk.END)
    key_text.delete(1.0, tk.END)
    s = in_text.get(1.0, tk.END)
    s = Vernam_shifr(s)  # строка (1)
    if s:
        out_text.insert(1.0, s[0])
        key_text.insert(1.0, s[1])
    else:
        mb.showerror("Ошибка", "Используйте только числа и буквы!")


def deVernam():  # расшифровка Вернама
    in_text.delete(1.0, tk.END)
    s = out_text.get(1.0, tk.END)
    a = key_text.get(1.0, tk.END)
    s = deVernam_shifr(s, a)  # строка (1)
    if s:
        in_text.insert(1.0, s)
    else:
        mb.showerror("Ошибка",
                     "Используйте только числа и буквы, и проверьте, совпадают ли длины пароля и зашифрованного сообщения")


win = tk.Tk()
win.geometry(f"800x500+100+200")
win.title("Шифратор2000")
entry = tk.Entry(win, width=24)
btn1 = tk.Button(win, text="Открыть директорию", command=open_dir, height=4, width=20)
btn2 = tk.Button(win, text="Зашифровать", command=encrypt, height=4, width=20)
btn3 = tk.Button(text='Передать', height=4, width=20, command=get_entry_enc)
btn4 = tk.Button(text="Расшифровать", height=4, width=20, command=decrypt)
btn5 = tk.Button(text='Передать', height=4, width=20, command=get_entry_dec)
btn1.place(x=21, y=21)
btn2.place(x=21, y=121)
btn4.place(x=21, y=221)

in_text = tk.Text(width=45, height=10)  # поле под шифруемый текст
in_text.place(x=196, y=21)

out_text = tk.Text(width=45, height=10)  # поле под расшифруемый текст
out_text.place(x=196, y=320)

key_text = tk.Text(width=45, height=2)  # поле под пароль
key_text.place(x=196, y=230)

# тут делать кнопки под шифры #
tk.Button(text="Шифровка Фиббоначи",
          command=Fi, width=30).place(x=570, y=20)
tk.Button(text="Шифровка Фиббоначи (с паролем)",
          command=Fi_password, width=30).place(x=570, y=42)
tk.Button(text="Шифровка Цезаря",
          command=Caesar, width=30).place(x=570, y=64)
tk.Button(text="Аффиная шифровка",
          command=Affine, width=30).place(x=570, y=88)

tk.Button(text="Шифровка Вернама",
          command=Vernam, width=30).place(x=570, y=110)

# тут делать кнопки под расшифры #
tk.Button(text="Расшифровка Фиббоначи",
          command=deFi, width=30).place(x=570, y=320)
tk.Button(text="Расшифровка Фиббоначи(с паролем)",
          command=deFi_password, width=30).place(x=570, y=342)
tk.Button(text="Расшифровка Цезаря",
          command=deCaesar, width=30).place(x=570, y=364)
tk.Button(text="Аффиная расшифровка",
          command=deAffine, width=30).place(x=570, y=388)
tk.Button(text="Расшифровка Вернама",
          command=deVernam, width=30).place(x=570, y=410)

# Надписи
tk.Label(text="Исходный текст:").place(x=196, y=0)
tk.Label(text="Ключ:").place(x=196, y=209)
tk.Label(text="Зашифрованный текст:").place(x=196, y=299)
tk.Label(text="Работа с файлами:").place(x=0, y=0)

win.mainloop()

# n = -1
# while n != 3:
#    print("1.Шифровать")
#    print("2.Расшифровать")
#    print("3.Выход")
#    n = int(input())
#    if n == 1:
#        password = input("Введите пароль для шифрования: ")
#        Encriptor.walking_by_dirs("F:\crpTest1", password)
#    elif n == 2:
#        password = input("Введите пароль для расшифрования: ")
#        Decryptor.walking_by_dirs("F:\crpTest1", password)
