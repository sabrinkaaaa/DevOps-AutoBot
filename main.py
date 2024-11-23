import telebot
from telebot import types
import pyodbc
from decimal import Decimal


bot = telebot.TeleBot('7957536264:AAHahGGQYgKvsPbymHw-t2Oow640QXFNcwM')

name = ''

#Подключаемся к БД
server = 'localhost'
database = 'Autos'
username = 'hello'
password = 'hello'
driver = 'ODBC Driver 18 for SQL Server'

# Создайте строку подключения
connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'

# значения для поиска машинки
user_data = {}



"""def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Напиши своё имя")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')
        
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет" :
        bot.send_message(message.from_user.id, "Привет! Чтобы зарегистрироваться, напиши /reg \nЧтобы подобрать машину, напиши /ChooseAuto")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Напиши своё имя")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    elif message.text == '/ChooseAuto':
        bot.register_next_step_handler(message, ChooseAuto)  # следующий шаг – функция get_name

    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message): #получаем имя
    global name
    name = message.text
    bot.register_next_step_handler(message, get_text_messages)
    if message.text == "Мася":
        bot.send_message(message.from_user.id, "Сабрина тебя любит")

    else:
        bot.send_message(message.from_user.id, "Записал")




def ChooseAuto(message):
    bot.send_message(message.from_user.id, "Ты выбираешь машину")


bot.polling(none_stop=True, interval=0)        
        
        """

def find_closest(numbers, target):
    # Проверяем, что список не пустой
    if not numbers:
        return None

    # Преобразуем target в тип Decimal, если это не Decimal
    target = Decimal(target)

    # Преобразуем элементы списка в тип Decimal, если они не Decimal
    numbers = [Decimal(num) for num in numbers]

    # Находим ближайшее число, используя min с ключом abs разности
    closest = min(numbers, key=lambda x: abs(x - target))
    return numbers.index(closest)




def sql_query_select_all(message):
    # Подключение к базе данных
    try:
        conn = pyodbc.connect(connection_string)
        print("Успешное подключение к SQL Server")

        # первая сортировка
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM autos WHERE price <= {user_data['max_price']}")
        rows = cursor.fetchall()
        if len(rows) > 0:
            cursor.execute(f"SELECT * FROM autos WHERE price <= {user_data['max_price']} AND body = '{user_data['body_type']}'")
            rows = cursor.fetchall()
            if len(rows) > 0:
                cursor.execute(f"SELECT * FROM autos WHERE price <= {user_data['max_price']} AND body = '{user_data['body_type']}'"
                               f"AND drive = '{user_data['drive_type']}'")
                rows = cursor.fetchall()
                if len(rows) > 0:
                    cursor.execute(
                        f"SELECT * FROM autos WHERE price <= {user_data['max_price']} AND body = '{user_data['body_type']}'"
                        f"AND drive = '{user_data['drive_type']}' AND region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        for i in range(len(rows)):
                            bot.reply_to(message,"Машинка № " + str(i+1) + ":\n" +
                                  rows[i][1] + "\n" +
                                  str(rows[i][3]) + " $\n"
                                  )
                    else:
                        print("четвёртый иф не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos WHERE price <= {user_data['max_price']} AND body = '{user_data['body_type']}'"
                            f"AND drive = '{user_data['drive_type']}'")
                        bot.reply_to(message, "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            bot.reply_to(message,"Машинка № " + str(i+1) + ":\n" +
                                  rows[i][1] + "\n" +
                                  str(rows[i][3]) + " $\n"
                                  )

                else:
                    print("третий иф не прошёл")

                    cursor.execute(
                        f"SELECT * FROM autos WHERE price <= {user_data['max_price']} AND body = '{user_data['body_type']}'"
                        f"AND region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:

                        for i in range(len(rows)):
                            bot.reply_to(message, "Машинка № " + str(i + 1) + ":\n" +
                                         rows[i][1] + "\n" +
                                         str(rows[i][3]) + " $\n"
                                         )
                    else:
                        print("четвёртый иф в третьем ифе не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos WHERE price <= {user_data['max_price']} AND body = '{user_data['body_type']}'")
                        bot.reply_to(message,
                                     "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            bot.reply_to(message, "Машинка № " + str(i + 1) + ":\n" +
                                         rows[i][1] + "\n" +
                                         str(rows[i][3]) + " $\n"
                                         )

            else:
                print("второй иф не прошёл")

                cursor.execute(
                    f"SELECT * FROM autos WHERE price <= {user_data['max_price']}"
                    f"AND drive = '{user_data['drive_type']}'")
                rows = cursor.fetchall()
                if len(rows) > 0:
                    cursor.execute(
                        f"SELECT * FROM autos WHERE price <= {user_data['max_price']}"
                        f"AND drive = '{user_data['drive_type']}' AND region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        for i in range(len(rows)):
                            bot.reply_to(message, "Машинка № " + str(i + 1) + ":\n" +
                                         rows[i][1] + "\n" +
                                         str(rows[i][3]) + " $\n"
                                         )
                    else:
                        print("четвёртый иф не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos WHERE price <= {user_data['max_price']}"
                            f"AND drive = '{user_data['drive_type']}'")
                        bot.reply_to(message,
                                     "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            bot.reply_to(message, "Машинка № " + str(i + 1) + ":\n" +
                                         rows[i][1] + "\n" +
                                         str(rows[i][3]) + " $\n"
                                         )

                else:
                    print("третий иф не прошёл")

                    cursor.execute(
                        f"SELECT * FROM autos WHERE price <= {user_data['max_price']}"
                        f"AND region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:

                        for i in range(len(rows)):
                            bot.reply_to(message, "Машинка № " + str(i + 1) + ":\n" +
                                         rows[i][1] + "\n" +
                                         str(rows[i][3]) + " $\n"
                                         )
                    else:
                        print("четвёртый иф в третьем ифе не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos WHERE price <= {user_data['max_price']}")
                        bot.reply_to(message,
                                     "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            bot.reply_to(message, "Машинка № " + str(i + 1) + ":\n" +
                                         rows[i][1] + "\n" +
                                         str(rows[i][3]) + " $\n"
                                         )
        else:
            print("первый иф не прошёл")

            cursor.execute(
                f"SELECT * FROM autos WHERE body = '{user_data['body_type']}'")
            rows = cursor.fetchall()
            if len(rows) > 0:
                cursor.execute(
                    f"SELECT * FROM autos WHERE body = '{user_data['body_type']}'"
                    f"AND drive = '{user_data['drive_type']}'")
                rows = cursor.fetchall()
                if len(rows) > 0:
                    cursor.execute(
                        f"SELECT * FROM autos WHERE body = '{user_data['body_type']}'"
                        f"AND drive = '{user_data['drive_type']}' AND region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))

                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                         rows[index][1] + "\n" +
                                         str(rows[index][3]) + " $\n"
                                         )
                    else:
                        print("четвёртый иф не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos WHERE body = '{user_data['body_type']}'"
                            f"AND drive = '{user_data['drive_type']}'")
                        bot.reply_to(message,
                                     "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))

                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                     rows[index][1] + "\n" +
                                     str(rows[index][3]) + " $\n"
                                     )

                else:
                    print("третий иф не прошёл")

                    cursor.execute(
                        f"SELECT * FROM autos WHERE body = '{user_data['body_type']}'"
                        f"AND region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:

                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))

                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                     rows[index][1] + "\n" +
                                     str(rows[index][3]) + " $\n"
                                     )
                    else:
                        print("четвёртый иф в третьем ифе не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos WHERE  body = '{user_data['body_type']}'")
                        bot.reply_to(message,
                                     "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))

                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                     rows[index][1] + "\n" +
                                     str(rows[index][3]) + " $\n"
                                     )

            else:
                print("второй иф не прошёл")

                cursor.execute(
                    f"SELECT * FROM autos WHERE drive = '{user_data['drive_type']}'")
                rows = cursor.fetchall()
                if len(rows) > 0:
                    cursor.execute(
                        f"SELECT * FROM autos WHERE drive = '{user_data['drive_type']}' AND region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))

                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                     rows[index][1] + "\n" +
                                     str(rows[index][3]) + " $\n"
                                     )
                    else:
                        print("четвёртый иф не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos WHERE drive = '{user_data['drive_type']}'")
                        bot.reply_to(message,
                                     "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))

                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                     rows[index][1] + "\n" +
                                     str(rows[index][3]) + " $\n"
                                     )

                else:
                    print("третий иф не прошёл")

                    cursor.execute(
                        f"SELECT * FROM autos WHERE region = '{user_data['region']}'")
                    rows = cursor.fetchall()
                    if len(rows) > 0:

                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))

                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                     rows[index][1] + "\n" +
                                     str(rows[index][3]) + " $\n"
                                     )
                    else:
                        print("четвёртый иф в третьем ифе не прошёл")
                        cursor.execute(
                            f"SELECT * FROM autos")
                        bot.reply_to(message,
                                     "Мы не смогли найти машинку, полностью подходящью под этот запрос, но подобрали похожие варианты! ")
                        rows = cursor.fetchall()
                        numbers = []

                        for i in range(len(rows)):
                            numbers.append(int(rows[i][3]))


                        index = find_closest(numbers, Decimal(user_data['max_price']))

                        bot.reply_to(message, "Я решил что самая подходящая машинка для вас будет:\n" +
                                     rows[index][1] + "\n" +
                                     str(rows[index][3]) + " $\n"
                                     )



        '''# Пример запроса к базе данных
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM autos")  # Вывести версию SQL Server
        rows = cursor.fetchall()
        print(len(rows))
        # Вывод результата запроса
        for row in rows:
            print(len(row))

        # Закрыть соединение
        cursor.close()
        conn.close()'''
    except Exception as e:
        print("Ошибка при подключении к SQL Server:", e)




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! \n"
                                               "Меня зовут Ботик. Выбери, что ты хочешь сделать:\n"
                                               "Чтобы познакомиться, напиши /reg \n"
                                               "Чтобы выбрать машинку, напиши /ChooseAuto")

@bot.message_handler(commands=['ChooseAuto'])
def start_choosing_auto(message):
    bot.send_message(message.chat.id, "Давай подберем для тебя машину.")
    ask_max_price(message)

# Вопрос: максимальная цена
def ask_max_price(message):
    msg = bot.send_message(message.chat.id, "Введите максимальную цену машины в $:")
    bot.register_next_step_handler(msg, process_max_price)

def process_max_price(message):
    if message.text.isdigit():
        max_price = int(message.text)
        user_data['max_price'] = max_price
        ask_body_type(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")
        ask_max_price(message)

# Вопрос: тип кузова
def ask_body_type(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    options = ["Sedan", "Hatchback", "SUV", "Truck", "Coupe"]
    for option in options:
        markup.add(option)
    msg = bot.send_message(message.chat.id, "Выберите тип кузова:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_body_type)

def process_body_type(message):
    user_data['body_type'] = message.text
    ask_drive_type(message)

# Вопрос: тип привода
def ask_drive_type(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    options = ["Front-wheel", "Rear-wheel", "All-wheel"]
    for option in options:
        markup.add(option)
    msg = bot.send_message(message.chat.id, "Выберите тип привода:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_drive_type)

def process_drive_type(message):
    user_data['drive_type'] = message.text
    ask_region(message)

# Вопрос: регион производителя
def ask_region(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    options = ["Europe", "Asia", "America", "Russia"]
    for option in options:
        markup.add(option)
    msg = bot.send_message(message.chat.id, "Выберите регион производителя:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_region)


def process_region(message):
    user_data['region'] = message.text
    bot.send_message(message.chat.id, f"Спасибо! Мы ищем машину по следующим данным:\n\n"
                                      f"Максимальная цена в $: {user_data['max_price']}\n"
                                      f"Тип кузова: {user_data['body_type']}\n"
                                      f"Тип привода: {user_data['drive_type']}\n"
                                      f"Регион производителя: {user_data['region']}",
                     reply_markup=types.ReplyKeyboardRemove())
    sql_query_select_all(message)

"""@bot.message_handler(content_types=['text'])
def start(message):

    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет! \n"
                                               "Меня зовут Ботик. Выбери, что ты хочешь сделать:\n"
                                               "Чтобы познакомиться, напиши /reg \n"
                                               "Чтобы выбрать машинку, напиши /ChooseAuto")
    elif message.text == "/reg":
        bot.send_message(message.from_user.id, "Сейчас переброшу на метод регистрации")
        bot.send_message(message.from_user.id, "Напиши своё имя")
        bot.register_next_step_handler(message, get_name)

    elif message.text == "/ChooseAuto":
        bot.send_message(message.from_user.id, "Сейчас переброшу на метод подбора машинок")
        choosing_auto(message)
        #bot.register_next_step_handler(message, choosing_auto)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(content_types=['text'])
def get_name(message): #получаем имя
    global name
    name = message.text
    bot.register_next_step_handler(message, start)
    if message.text == "Мася":
        bot.send_message(message.from_user.id, "Сабрина тебя любит")

    else:
        bot.send_message(message.from_user.id, "Записал")

@bot.message_handler(commands=['ChooseAuto'])
def choosing_auto(message):
    bot.send_message(message.from_user.id,"Добро пожаловать в выбор машинок")
    
    #sql_query_select_all()
    bot.send_message(message.from_user.id,'Введи начальную цену, для машинки в $')
    bot.register_next_step_handler(message, get_pice1);

def get_pice1(message):
    price1 = 0
    while price1 == 0:
        try:
            price1 = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no)
    question= 'Нижний ценовой диапозон ' + str(price1) + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call, price1):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )');
        print(price1)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Не Запомню : )');"""


bot.polling(none_stop=True, interval=0)
