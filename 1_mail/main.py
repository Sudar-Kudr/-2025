import tkinter as tk
from tkinter import messagebox
import sys
import re
#import saveFile
import main_find  # 

with open('main_engl_words.txt', 'r', encoding='utf-8') as file:
    english_words = [line.strip() for line in file if line.strip()]


# Глобальная переменная для хранения выбранного языка
_SEL_LANG = None
_RESULT = True

# Библиотека с текстовыми сообщениями на разных языках
messages = {
    'rus': {
        'language_select_title': 'Выбор языка/Lang selection', # пусть
        'language_select_label': 'Выберите язык | Select a Language', # пусть
        'button_rus': 'РУС', # пусть
        'button_us': 'ENG', # пусть будет на всякий случай
        'app_title': 'Project K',
        'password_types': ['Простой', 'Средний', 'Сложный'],
        'ok': 'OK',
        'not_ok': 'Не подойдёт!',
        'rul': 'Правила безопасности пароля:',
        'result': 'Результат проверки:',
        'entry_pass':{
            'введите': 'Введите...',
            'kol-vo': 'Количество символов:'
        },
        'rules': {
            # в процессе понял, что лучше не давать выбор
            # сложности пользователю, а сразу сложный
            'simple': [
                {'title': 'Пароль должен содержать минимум 6 символов.', 
                 'len': 6},
                {'title': 'Пароль должен содержать хотя бы одну заглавную букву.', 
                 'l': 1},
                {'title': 'Пароль должен содержать хотя бы одну цифру.', 
                 'l': 1}
            ],
            'medium': [
                {'title': 'Пароль должен содержать минимум 8 символов.', 
                 'len': 8},
                {'title': 'Пароль должен содержать хотя бы одну заглавную букву.', 
                 'l': 1},
                {'title': 'Пароль должен содержать хотя бы одну цифру.', 
                 'l': 1},
                {'title': 'Пароль должен содержать хотя бы один специальный символ.', 
                 'l': 1}
            ],
            'hard': [
                {'title': 'Пароль должен содержать минимум 12 символов.', 
                 'len': 12},
                {'title': 'Пароль должен содержать хотя бы две заглавной буквы.', 
                 'l': 2},
                {'title': 'Пароль должен содержать хотя бы три цифры.', 
                 'l': 3},
                {'title': 'Пароль должен содержать хотя бы два специальных символа.', 
                 'l': 2},
                {'title': 'Пароль не должен содержать последовательных одинаковых символов.'},
                {'title_warning': 'Вы ввели какойто год. Возможно это ваша дата рождения или иное событие. Не рекомендуется.'}, # покрасится в фиолетовый
                {'title_warning': 'Вы ввели слово из букв. Не рекомендуется.'} # покрасится в фиолетовый
            ]
        }
    },
    'eng': {
        'language_select_title': 'Выбор языка/Lang selection', # пусть
        'language_select_label': 'Выберите язык | Select a Language', # пусть
        'button_rus': 'ruus', # пусть
        'button_us': 'ENG', # пусть будет на всякий случай
        'app_title': 'Project K',
        'password_types': ['Simple', 'Medium', 'Hard'],
        'ok': 'OK',
        'not_ok': 'Not OK',
        'rul': 'Password Security Rules:',
        'result': 'Result of checking:',
        'entry_pass':{
            'введите': 'Enter...',
            'kol-vo': 'Number of symbols:'
        },
        'rules': {
            'simple': [
                {'title': 'The password must contain at least 6 characters.', 
                 'len': 6}
            ],
            'medium': [
                {'title': 'The password must contain at least 8 characters.', 
                 'len': 8}
            ],
            'hard': [
                {'title': 'The password must contain at least 12 characters.', 
                 'len': 12},
                {'title': 'The password must contain at least 2 uppercase letter.', 
                 'l': 2},
                {'title': 'The password must contain at least 3 digit.', 
                 'l': 3},
                {'title': 'The password must contain at least 2 special character.', 
                 'l': 2},
                {'title': 'The password should not contain consecutive identical characters.'},
                {'title_warning': "You have entered a certain year. Maybe it's your date of birth or some other event. Not recommended."}, # покрасится в фиолетовый
                {'title_warning': 'You have entered a letter word. Not recommended.'} # покрасится в фиолетовый
            ]
        }
    }
}

# Функция для отображения окна выбора языка
def show_language_selection():
    def select_language(language):
        global _SEL_LANG
        _SEL_LANG = language
        root.destroy()

    root = tk.Tk()
    root.withdraw()  # Скрываем окно, пока оно не понадобится снова
    root.title(messages['rus']['language_select_title'])
    root.geometry("300x100+500+200") # 500+200 - положение на экране

    label = tk.Label(root, text=messages['rus']['language_select_label'])
    label.pack(pady=10)

    button_rus = tk.Button(root, text=messages['rus']['button_rus'], command=lambda: select_language('rus'))
    button_us = tk.Button(root, text=messages['rus']['button_us'], command=lambda: select_language('eng'))

    button_rus.pack(side='left', padx=20)
    button_us.pack(side='right', padx=20)

    root.deiconify()  # Показываем окно
    root.mainloop()

# Функция для отображения главного окна приложения
def show_main_window():
    # Функция для проверки пароля
    def check_password():
        global _RESULT
        _RESULT = True
        password = entry.get().strip()
        password_type = var.get() # сразу hard
        #print(password, '= entry.get().strip()')

        rules = messages[_SEL_LANG]['rules'][password_type]

        instructions_text.config(state='normal')
        instructions_text.delete(1.0, tk.END)

        # Общая проверка (длина, заглавная и цифра)
        # Проверка длины
        if len(password) >= rules[0]['len']:
            instructions_text.insert(tk.END, f"{rules[0]['title']}\n\n", 'green')
        else:
            instructions_text.insert(tk.END, f"{rules[0]['title']}\n\n", 'red')
            _RESULT = False

        # Счетчики
        upper_count = 0 # для заглавной
        digit_count = 0 # для цифер
        alnum_count = 0 # для спецсимволов
        for char in password:
            if char.isupper():
                upper_count += 1
            if char.isdigit():
                digit_count += 1
            if not char.isalnum():
                alnum_count += 1

        # # Проверка заглавной
        # if any(char.isupper() for char in password):
        #     output_text.insert(tk.END, f"{rules[1]['title']}\n", 'green')
        # else:
        #     output_text.insert(tk.END, f"{rules[1]['title']}\n", 'red')

        # # Проверка цифер
        # if any(char.isdigit() for char in password):
        #     output_text.insert(tk.END, f"{rules[2]['title']}\n", 'green')
        # else:
        #     output_text.insert(tk.END, f"{rules[2]['title']}\n", 'red')
            
        reg = re.compile(r'^[^а-яА-Я]*$')
        if (" " in password) or not (reg.match(password)):
            if _SEL_LANG == "rus":
                instructions_text.insert(tk.END, 'B пароле содержит пробел или русские символы - исправьте', 'red')
            else:
                instructions_text.insert(tk.END, 'The password contains a space or Russian characters - correct it.', 'red')
            _RESULT = False
        elif password_type == 'hard':
            # Проверка заглавной
            if upper_count >= rules[1]['l']:
                instructions_text.insert(tk.END, f"{rules[1]['title']}\n\n", 'green')
            else:
                instructions_text.insert(tk.END, f"{rules[1]['title']}\n\n", 'red')
                _RESULT = False
            # Проверка цифер
            if digit_count >= rules[2]['l']:
                instructions_text.insert(tk.END, f"{rules[2]['title']}\n\n", 'green')
            else:
                instructions_text.insert(tk.END, f"{rules[2]['title']}\n\n", 'red')
                _RESULT = False
            # Проверка cпецсимволов
            if  alnum_count >= rules[3]['l']:
                instructions_text.insert(tk.END, f"{rules[3]['title']}\n\n", 'green')
            else:
                instructions_text.insert(tk.END, f"{rules[3]['title']}\n\n", 'red')
                _RESULT = False
            # Последовательность одинаковых символов
            duplicate = False
            for i in range(len(password) - 1):
                if password[i] == password[i + 1]:
                    duplicate = True
                    instructions_text.insert(tk.END, f"{rules[4]['title']}\n\n", 'red')
                    _RESULT = False
                    break
            if duplicate == False:
                instructions_text.insert(tk.END, f"{rules[4]['title']}\n\n", 'green')
            # Годы в пароле
            pattern = r'(?<![\d])\d{4}(?![\d])' # (?![\d]) запрещает наличие цифр 
            matches = re.findall(pattern, password)
            for year in matches:
                if 1930 < int(year) < 2025: # да, можно в реальном времени обновлять через дататайм.
                    instructions_text.insert(tk.END, f"{rules[5]['title_warning']}\n\n", 'DarkOrchid')
                    break
            #print('❤️        ❤️', password)
            find_res = main_find.filter(password)
            if find_res == 'нету совпадений':
                pass
            else:
                found = '[{0} found]'.format(find_res) # для вывода найденного {слова}
                instructions_text.insert(tk.END, f"{rules[6]['title_warning']}{found}\n", 'DarkOrchid')
        instructions_text.config(state='disabled') # запрещает редакт (зарываем редакт)

        # Статус проверки
        if _RESULT:
            status_label.config(text=messages[_SEL_LANG]['ok'], fg='green')
        else:
            status_label.config(text=messages[_SEL_LANG]['not_ok'], fg='red')

    # Функция для отображения инструкции по выбору сложности пароля
    def display_rules():
        password_type = var.get()
        rules = messages[_SEL_LANG]['rules'][password_type]
        instructions_text.config(state='normal')
        instructions_text.delete(1.0, tk.END)
        
        
        for rule in rules:
            if 'title' in rule:
                instructions_text.insert(tk.END, f"{rule['title']}\n\n")
        instructions_text.config(state='disabled')

    # отказ
    # # Функция для сохранения пароля в файл 
    # def save_password():
    #     file_path = saveFile.get_file_path()
    #     if file_path:
    #         password = entry.get().strip()
    #         saveFile.save_password_to_file(file_path, password)
    #         messagebox.showinfo("Сохранено", "Ваш пароль успешно сохранен!")

    # Настройка главного окна
    root = tk.Tk()
    root.title(messages[_SEL_LANG]['app_title'])
    root.geometry("800x600+200+50")

    # Обработка закрытия окна
    def close_app():
        sys.exit() #полностью закрывает ПО

    root.protocol("WM_DELETE_WINDOW", close_app)

    # Фрейм для кнопок и полей ввода
    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    '''отказ
    # Выбор сложности пароля'''
    var = tk.StringVar(value='hard') # по умолчанию выбрана первая(hard) кнопка
    '''
    simple_radio = tk.Radiobutton(main_frame, text=messages[_SEL_LANG]['password_types'][0], variable=var, value='simple', command=display_rules)
    medium_radio = tk.Radiobutton(main_frame, text=messages[_SEL_LANG]['password_types'][1], variable=var, value='medium', command=display_rules)
    hard_radio   = tk.Radiobutton(main_frame, text=messages[_SEL_LANG]['password_types'][2], variable=var, value='hard', command=display_rules)

    simple_radio.grid(row=0, column=0, sticky='w')
    medium_radio.grid(row=1, column=0, sticky='w')
    hard_radio.grid(row=2, column=0, sticky='w')
    '''
    # Поле для ввода пароля
    #    вывод слова
    entry_label = tk.Label(main_frame, text=messages[_SEL_LANG]['entry_pass']['введите'])
    entry_label.grid(row=3, column=0, sticky='w', pady=(20, 0))

    # Функция для подсчета символов
    def update_char_count(*args):
        password = entry.get().strip()
        char_count.set(f"{messages[_SEL_LANG]['entry_pass']['kol-vo']} {len(password)}")

    #    для отображения количества символов
    char_count = tk.StringVar()
    char_count.set(f"{messages[_SEL_LANG]['entry_pass']['kol-vo']} 0")
    #    для отслеживания изменений в поле ввода
    entry_var = tk.StringVar()
    entry_var.trace_add("write", update_char_count)
    
    #   вывод отображения количества символов
    char_count_label = tk.Label(main_frame, textvariable=char_count)
    char_count_label.grid(row=5, column=0, sticky='w')
    #   само поле ввода
    entry = tk.Entry(main_frame, width=30, textvariable=entry_var)
    entry.grid(row=4, column=0, sticky='w')

    # Кнопка для проверки пароля
    check_button = tk.Button(main_frame, text=("Проверить" if _SEL_LANG=="rus" else "Check"), command=check_password)
    check_button.grid(row=6, column=0, sticky='w', pady=(20, 0))
    ''' отказ
    # Кнопка для сохранения пароля в файл
    save_button = tk.Button(main_frame, text="Сохранить пароль в файл", command=save_password, state='disabled')
    save_button.grid(row=7, column=0, sticky='w', pady=(20, 0))
    '''
    # Область для вывода Правила безопасности
    instructions_and_output_windows = tk.Label(main_frame, text=messages[_SEL_LANG]['rul'])
    instructions_and_output_windows.grid(row=0, column=1, padx=(40, 0), pady=(0, 15))

    instructions_text = tk.Text(main_frame, height=15, width=45, wrap='word', state='disabled')
    instructions_text.grid(row=1, column=1, rowspan=10, sticky='nw', padx=(40, 0))

    # Область для вывода результата проверки
    # output_label = tk.Label(main_frame, text=messages[_SEL_LANG]['result'])
    # output_label.grid(row=7, column=0, sticky='w', pady=(20, 0))

    # instructions_text = tk.Text(main_frame, height=7, width=35, wrap='word', state='disabled')
    # instructions_text.grid(row=8, column=0, sticky='w')
    instructions_text.tag_configure('green', foreground='green') #, font=('Helvetica', 12, 'bold'))
    instructions_text.tag_configure('red', foreground='red')
    instructions_text.tag_configure('DarkOrchid', foreground='DarkOrchid')

    status_label = tk.Label(main_frame, text='', font=('Arial', 14))
    status_label.grid(row=9, column=0, sticky='w', pady=(20, 0))
    
    # Первоначальное отображение правил безопасности
    display_rules()

    root.mainloop()


# ctrl + K, ctrl + C - закомментировать 
# ctrl + K, ctrl + U - раскомментировать
# Основная программа
if __name__ == "__main__":
    show_language_selection()
    if _SEL_LANG is not None: # если язык выбран то проходим
        show_main_window()