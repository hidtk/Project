import sqlite3
import telebot
from telebot import types
import datetime
from datetime import date

# инициализация бота
bot = telebot.TeleBot('6783696391:AAGnlTAbl9VQH9Ud_kbpnFNPSriTw0_p2CQ')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            #if call.data == 'elect':
                #return elect(call.message)
            if call.data == 'duch':
                bot.send_message(call.message.chat.id, 'К сожалению эта функция ещё не готова.')
            elif call.data == '1oppos':
                return pos_za_op_pass(call.message)
            elif call.data == 'drasp_pass':
                return drasp_pass(call.message)
            elif call.data == 'prop':
                return prop(call.message)
            elif call.data == 'reg':
                return re_reg(call.message)
            elif call.data == 'uch':
                return uch(call.message)
            elif call.data == 'star':
                return star(call.message)
            elif call.data == 'ped':
                return ped(call.message)
            elif call.data == 'star_pass':
                return star_pass(call.message)
            elif call.data == 'star_menu':
                return star_menu(call.message)
            elif call.data[0] == 's':
                return full_name(call.message, call.data)
            elif 'otmetz' in call.data:
                return vistavleie_za_op_star_para1(call.message, call.data)
            elif 'otmets' in call.data:
                return vistavleie_za_segodnya_star_para(call.message, call.data)
            elif 'OtmetzPara' in call.data:
                return vistavleie_za_op_star_para2(call.message, call.data[10:])
            elif 'OtmetPara' in call.data:
                return vistavleie_za_segodnya_star_para1(call.message, call.data[9:])
            elif 'kohecotm' in call.data:
                return vistavleie_za_segodnya_star_para2(call.message, call.data[8:])
            elif 'kohezcotm' in call.data:
                return vistavleie_za_op_star_para3(call.message, call.data[9:])
            elif 'drasp' in call.data:
                return drasp_pass2(call.message, call.data[5:])
            elif call.data == '1pos':
                return pos_segodnya(call.message)
            elif call.data == '1postar':
                return pos_segodnya_star(call.message)
            elif call.data == '1oppostar':
                return vistavlenie_za_datu_star(call.message)
            elif call.data == 'korzina':
                return korzina(call.message)
            elif call.data == 'zkhkjkk':
                return zhizhi(call.message)
            elif call.data == 'odnor':
                return odnor(call.message)
            elif call.data == 'pos_segodnya_star':
                return pos_segodnya_star(call.message)
            elif call.data == 'menu':
                return menu(call.message)
            elif 'ch_pl' in call.data:
                bot.send_message(call.message.chat.id, 'Введите место встречи')
                id_sd = call.data[5:]
                bot.register_next_step_handler(call.message, new_place, id_sd)
            elif call.data == 'del_tovar':
                bot.send_message(call.message.chat.id, 'Введите id товара для удаления')
                bot.register_next_step_handler(call.message, del_tovar)
            elif call.data == 'open_sd':
                return open_sd(call.message)
            elif call.data == 'buyers_data':
                return buyers_data(call.message)
            elif call.data == 'tovar_data':
                return tovar_data(call.message)
            elif call.data == 'nazad':
                return centre(call.message)
            elif call.data == 'op_wait':
                return op_wait(call.message)
            elif call.data == 'call_wait':
                return call_wait(call.message)
            elif call.data == 'cur_wait':
                return cur_wait(call.message)
            elif call.data == 'ed_status':
                return ed_status(call.message)
            elif call.data == 'edit_passw':
                return edit_passw(call.message)
            elif call.data == 'choose_place':
                return choose_place(call.message)
            elif call.data == 'add_tovar':
                return add_tovar(call.message)
            elif call.data == 'rassilka':
                return rassilka(call.message)
            elif call.data == 'close_sd':
                return close_sd(call.message)
            elif call.data[0] == 'g':
                return group(call.message, call.data)
            else:
                with sqlite3.connect('journal.db') as db:
                    pass


            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="ЛФОАЛЫА",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        with sqlite3.connect('journal.db') as db:
            cursor = db.cursor()
            sp = cursor.execute('SELECT tg_id FROM Users').fetchall()
            sp1 = cursor.execute('SELECT starosta_nick FROM Groups').fetchall()
            b = []
            for i in sp1:
                b.append(i[0])
            a = []
            for i in sp:
                a.append(i[0])
            if '@' + message.chat.username in b:
                inf = cursor.execute('SELECT reg FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
                if inf == 1:
                    cursor.execute('UPDATE Users SET class = ? WHERE tg_id = ?', [2, message.chat.id])
                    return star_menu(message)
                else:
                    cursor.execute('''INSERT INTO Users VALUES (?,?,?,?,?,?,?);''', (message.chat.id, 0, 0, 0, 0, 0, 0))
                    cursor.execute('UPDATE Users SET class = ? WHERE tg_id = ?', [2, message.chat.id])
                    return star(message)
            elif message.chat.id in a:
                inf = cursor.execute('SELECT reg FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
                if inf == 1:
                    return menu(message)
                elif inf == 0:
                    return reg(message)
                else:
                    photo = open('/Users/tkamzolov/PycharmProjects/pythonProject1/images/start.jpg', 'rb')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("Регистрация", callback_data='reg')
                    markup.add(item1)
                    bot.send_photo(message.chat.id, photo=photo, caption='Добро пожаловать в журнал посещаемости! \t'
                                                                         'Для того чтобы начать нужно пройти регистрацию.',
                                   reply_markup=markup)
            else:
                return reg(message)


@bot.message_handler(commands=['регистрация'])
def re_reg(message):
    if message.chat.type == 'private':
        return reg(message)


def reg(message):
    if message.chat.type == 'private':
        with sqlite3.connect('journal.db') as db:
            cursor = db.cursor()
            u_id = message.chat.id
            info = cursor.execute('SELECT * FROM Users WHERE tg_id = ?', [u_id])
            if info.fetchone() is None:
                cursor.execute('''INSERT INTO Users VALUES (?,?,?,?,?,?,?);''', (u_id, 0, 0, 0, 0, 1, 0))
            cursor.execute(f'UPDATE Users SET tg_nick = ?  WHERE tg_id = ?', ['@' + message.chat.username,
                                                                              message.chat.id])
            return uch(message)


def uch(message):
    if message.chat.type == 'private':
        with sqlite3.connect('journal.db') as db:
            cursor = db.cursor()
            markup = types.InlineKeyboardMarkup(row_width=1)
            inf = cursor.execute('SELECT group_name, group_id FROM Groups')
            item1 = types.InlineKeyboardButton("перепройти регистрацию", callback_data='reg')
            markup.add(item1)
            for i in inf:
                item = types.InlineKeyboardButton(f"{i[0]}", callback_data=f'{i[1]}')
                markup.add(item)
            bot.send_message(message.chat.id, 'Здравствуйте, ученик. Выберите группу в которой учитесь.',
                             reply_markup=markup)


def star(message):
    if message.chat.type == 'private':
        with sqlite3.connect('journal.db') as db:
            cursor = db.cursor()
            inf = cursor.execute(f'SELECT tg_nick FROM Users WHERE class = {2}').fetchone()
            if '@' + str(message.chat.username) in inf:
                return star_pass(message)
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("перепройти регистрацию", callback_data='reg')
                markup.add(item1)
                bot.send_message(message.chat.id, 'врунишка', reply_markup=markup)


def ped(message):
    pass


def group(message, grp):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        group = cursor.execute('SELECT group_name FROM Groups WHERE group_id = ?', [grp]).fetchone()[0]
        cursor.execute('UPDATE Users SET group_name = ? WHERE tg_id = ?', [group, message.chat.id])
        inf = cursor.execute('SELECT fio, student_id FROM Students WHERE group_name = ?', [group])
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in inf:
            item = types.InlineKeyboardButton(f"{i[0]}", callback_data=f'{i[1]}')
            markup.add(item)
        bot.send_message(message.chat.id, 'Выберите своё ФИО в списке.\n '
                                          'Если вы выбрали не ту группу - нажмите на кнопку "перепройти регистрацию".',
                         reply_markup=markup)


def full_name(message, student_id):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        name = cursor.execute('SELECT fio FROM Students WHERE student_id = ?', [student_id]).fetchone()[0]
        cursor.execute('UPDATE Users SET reg = ? WHERE tg_id = ?', [1, message.chat.id])
        cursor.execute('UPDATE Users SET full_name = ? WHERE tg_id = ?', [name, message.chat.id])
        cl = cursor.execute('SELECT class FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
    bot.send_message(message.chat.id,
                     'ФИО сохранено. Регистрация пройдена.')
    if cl == 1:
        return menu(message)
    elif cl == 2:
        return star_menu(message)


@bot.message_handler(commands=['menu'])
def menu_pass(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
    info1 = cursor.execute('SELECT reg FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
    if info1 != 1:
        bot.send_message(message.chat.id, f'Здравствуйте, для начала пройдите регистрацию.')
        return start(message)
    else:
        return menu(message)


bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Посещаемость за сегодня", callback_data='1pos')
    item2 = types.InlineKeyboardButton("Посещаемость за определённый день", callback_data='1oppos')
    item3 = types.InlineKeyboardButton("Кол-во пропущенных часов", callback_data='prop')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Добро пожаловать в меню', reply_markup=markup)


def prop(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        info = cursor.execute('SELECT otmetka, day, para FROM Poseh WHERE tg_id = ?',
                                 [message.chat.id]).fetchall()
        neuvazh = []
        uvazh = []
        n = 0
        u = 0
        for i in info:
            if i[0] == 2:
                n += 2
                neuvazh.append(f'День {i[1]}, пара №{i[2]}, {i[0]} часа')
            elif i[0] == 1:
                n += 1
                neuvazh.append(f'День {i[1]}, пара №{i[2]}, {i[0]} час')
            elif i[0] == 3:
                u += 2
                uvazh.append(f'День {i[1]}, пара №{i[2]}')
        inf = '\n'.join(neuvazh)
        inf1 = '\n'.join(uvazh)
        bot.send_message(message.chat.id, f'Часов пар пропушено по неуважительной причине: {n}\n'
                                          f'Список пар: {inf}\n'
                                          f'\nЧасов пар пропушено по уважительной причине: {u}\n'
                                          f'Список пар: {inf1}')
        return menu(message)


def pos_segodnya(message):
    dt = date.today()
    wk = datetime.datetime.today().weekday()
    if wk == 6:
        bot.send_message(message.chat.id, 'Сегодня выходной')
        return star_menu(message)
    dt1 = '2023-09-01'
    n = str(dt1).split('-')
    n1 = str(dt).split('-')
    week1 = datetime.date(int(n1[0]), int(n1[1]), int(n1[2])).isocalendar()[1]
    week = datetime.date(int(n[0]), int(n[1]), int(n[2])).isocalendar()[1]
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        otmetki = cursor.execute('SELECT para, otmetka FROM Poseh WHERE tg_id = ? AND day = ?',
                                 [message.chat.id, dt]).fetchall()
        b = []
        for i in otmetki:
            if int(i[0]) == 1:
                if int(i[1]) == 0:
                    b.append(['1', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['1', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['1', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['1', 'Отсутствовал 2 часа'])
                else:
                    b.append(['1', 'Не проставлена'])
            elif int(i[0]) == 2:
                if int(i[1]) == 0:
                    b.append(['2', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['2', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['2', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['2', 'Отсутствовал 2 часа'])
                else:
                    b.append(['2', 'Не проставлена'])
            elif int(i[0]) == 3:
                if int(i[1]) == 0:
                    b.append(['3', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['3', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['3', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['3', 'Отсутствовал 2 часа'])
                else:
                    b.append(['3', 'Не проставлена'])
            elif int(i[0]) == 4:
                if int(i[1]) == 0:
                    b.append(['4', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['4', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['4', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['4', 'Отсутствовал 2 часа'])
                else:
                    b.append(['4', 'Не проставлена'])
            elif int(i[0]) == 5:
                if int(i[1]) == 0:
                    b.append(['5', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['5', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['5', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['5', 'Отсутствовал 2 часа'])
                else:
                    b.append(['5', 'Не проставлена'])
        inf = cursor.execute('SELECT group_name FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
        if (week1 - week + 1) % 2 == 0:
            info1 = cursor.execute(
                'SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                'AND day = ? AND nedelya = ?', [inf, str(wk), 2]).fetchone()
        else:
            info1 = cursor.execute(
                'SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                'AND day = ? AND nedelya = ?', [inf, str(wk), 1]).fetchone()
        if len(b) == 0:
            infoday = 'Посещаемость не проставлена'
        else:
            infoday = []
            for i in range(len(b)):
                infoday.append(f'\n{b[i][0]} пара  {b[i][1]}\n')
        if (week1 - week + 1) % 2 == 0:
            a = 'Четная'
        else:
            a = 'Нечетная'
        infoday = ''.join(infoday)
        bot.send_message(message.chat.id, f'Дата {dt}, неделя №{week1 - week + 1}, {a}\n'
                                          f'\n1 пара  {info1[0]}\n'
                                          f'\n2 пара {info1[1]}\n'
                                          f'\n3 пара {info1[2]}\n'
                                          f'\n4 пара {info1[3]}\n'
                                          f'\n5 пара {info1[4]}\n'
                                          f'{infoday}')
        return menu(message)


def pos_za_op_pass(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, 'Напишите день за который хотите посмотреть свою посещаемость.'
                                          'Формат даты должен быть такой: Год-месяц-число. (через малый дефис)\n'
                                          'Пример: "2023-09-01" - 1 сентября 2023 года.')
    bot.register_next_step_handler(message, pos_za_op)


def pos_za_op(message):
    with sqlite3.connect('journal.db') as db:
        if message.text.count('-') == 2 and message.text[:4] in ['2023', '2024', '2025', '2026'] and message.text[5:7] in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] and  message.text[8:10] in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',  '27', '28', '29', '30', '31']:
            cursor = db.cursor()
            dt = message.text
            n1 = str(dt).split('-')
            wk = datetime.date(year=int(n1[0]), month=int(n1[1]), day=int(n1[2])).weekday()
            if wk == 6:
                bot.send_message(message.chat.id, 'Выходной')
                return star_menu(message)
            dt1 = '2023-09-01'
            n = str(dt1).split('-')
            week1 = datetime.date(int(n1[0]), int(n1[1]), int(n1[2])).isocalendar()[1]
            week = datetime.date(int(n[0]), int(n[1]), int(n[2])).isocalendar()[1]
            with sqlite3.connect('journal.db') as db:
                cursor = db.cursor()
                otmetki = cursor.execute('SELECT para, otmetka FROM Poseh WHERE tg_id = ? AND day = ?',
                                         [message.chat.id, dt]).fetchall()
                b = []
                for i in otmetki:
                    if int(i[0]) == 1:
                        if int(i[1]) == 0:
                            b.append(['1', 'Присутствовал'])
                        elif int(i[1]) == 3:
                            b.append(['1', 'Отсутствие по уважительной причине'])
                        elif int(i[1]) == 1:
                            b.append(['1', 'Отсутствовал 1 час'])
                        elif int(i[1]) == 2:
                            b.append(['1', 'Отсутствовал 2 часа'])
                        else:
                            b.append(['1', 'Не проставлена'])
                    elif int(i[0]) == 2:
                        if int(i[1]) == 0:
                            b.append(['2', 'Присутствовал'])
                        elif int(i[1]) == 3:
                            b.append(['2', 'Отсутствие по уважительной причине'])
                        elif int(i[1]) == 1:
                            b.append(['2', 'Отсутствовал 1 час'])
                        elif int(i[1]) == 2:
                            b.append(['2', 'Отсутствовал 2 часа'])
                        else:
                            b.append(['2', 'Не проставлена'])
                    elif int(i[0]) == 3:
                        if int(i[1]) == 0:
                            b.append(['3', 'Присутствовал'])
                        elif int(i[1]) == 3:
                            b.append(['3', 'Отсутствие по уважительной причине'])
                        elif int(i[1]) == 1:
                            b.append(['3', 'Отсутствовал 1 час'])
                        elif int(i[1]) == 2:
                            b.append(['3', 'Отсутствовал 2 часа'])
                        else:
                            b.append(['3', 'Не проставлена'])
                    elif int(i[0]) == 4:
                        if int(i[1]) == 0:
                            b.append(['4', 'Присутствовал'])
                        elif int(i[1]) == 3:
                            b.append(['4', 'Отсутствие по уважительной причине'])
                        elif int(i[1]) == 1:
                            b.append(['4', 'Отсутствовал 1 час'])
                        elif int(i[1]) == 2:
                            b.append(['4', 'Отсутствовал 2 часа'])
                        else:
                            b.append(['4', 'Не проставлена'])
                    elif int(i[0]) == 5:
                        if int(i[1]) == 0:
                            b.append(['5', 'Присутствовал'])
                        elif int(i[1]) == 3:
                            b.append(['5', 'Отсутствие по уважительной причине'])
                        elif int(i[1]) == 1:
                            b.append(['5', 'Отсутствовал 1 час'])
                        elif int(i[1]) == 2:
                            b.append(['5', 'Отсутствовал 2 часа'])
                        else:
                            b.append(['5', 'Не проставлена'])
                inf = cursor.execute('SELECT group_name FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
                if (week1 - week + 1) % 2 == 0:
                    info1 = cursor.execute(
                        'SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                        'AND day = ? AND nedelya = ?', [inf, str(wk), 2]).fetchone()
                else:
                    info1 = cursor.execute(
                        'SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                        'AND day = ? AND nedelya = ?', [inf, str(wk), 1]).fetchone()
                if len(b) == 0:
                    infoday = 'Посещаемость не проставлена'
                else:
                    infoday = []
                    for i in range(len(b)):
                        infoday.append(f'\n{b[i][0]} пара  {b[i][1]}\n')
                if (week1 - week + 1) % 2 == 0:
                    a = 'Четная'
                else:
                    a = 'Нечетная'
                infoday = ''.join(infoday)
                bot.send_message(message.chat.id, f'Дата {dt}, неделя №{week1 - week + 1}, {a}\n'
                                                  f'\n1 пара  {info1[0]}\n'
                                                  f'\n2 пара {info1[1]}\n'
                                                  f'\n3 пара {info1[2]}\n'
                                                  f'\n4 пара {info1[3]}\n'
                                                  f'\n5 пара {info1[4]}\n'
                                                  f'{infoday}')
            return menu(message)
        else:
            bot.send_message(message.chat.id, 'Вы указали некорректную дату.')
            return menu(message)


def star_pass(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Я не староста", callback_data='reg')
    markup.add(item1)
    bot.send_message(message.chat.id,
                     'Введите свой пароль', reply_markup=markup)
    bot.register_next_step_handler(message, star_reg_pass)


def star_reg_pass(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        info = cursor.execute(f'SELECT password FROM Users WHERE tg_nick = ?',
                              ['@' + str(message.chat.username)]).fetchone()[0]
        if message.text == info:
            return star_reg(message)


def star_reg(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        markup = types.InlineKeyboardMarkup(row_width=1)
        inf = cursor.execute('SELECT group_name, group_id FROM Groups')
        item1 = types.InlineKeyboardButton("перепройти регистрацию", callback_data='reg')
        markup.add(item1)
        for i in inf:
            item = types.InlineKeyboardButton(f"{i[0]}", callback_data=f'{i[1]}')
            markup.add(item)
        bot.send_message(message.chat.id, 'Здравствуйте, Староста. Выберите группу в которой учитесь.',
                         reply_markup=markup)


@bot.message_handler(commands=['star_menu'])
def star_menu_pass(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        info = cursor.execute('SELECT tg_nick FROM Users WHERE class = ?', [2]).fetchone()
        if ('@' + str(message.chat.username)) not in info:
            bot.send_message(message.chat.id,
                             'У вас нет доступа к журналу старосты.')
        else:
            info1 = cursor.execute('SELECT reg FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
            if info1 != 1:
                bot.send_message(message.chat.id, f'Здравствуйте, староста, для начала пройдите регистрацию.')
                return start(message)
            else:
                return star_menu(message)


def star_menu(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
    inf = cursor.execute('SELECT full_name FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Проставить посещаемость за сегодня", callback_data='1postar')
    item2 = types.InlineKeyboardButton("Проставить посещаемость за определённый день", callback_data='1oppostar')
    item3 = types.InlineKeyboardButton("Кол-во пропущенных часов учеником", callback_data='prop11')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, f'Здравствуйте, {inf}. Вы попали в меню старосты.\n Если хотите посмотреть '
                                      f'собственную статистику нажмите на кнопку - /menu.\n'
                                      f'В меню старосты всегда можно попасть прописав команду "/star_menu".',
                     reply_markup=markup)


def pos_segodnya_star(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        grp = cursor.execute('SELECT group_name FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
        inf = cursor.execute('SELECT fio, student_id FROM Students WHERE group_name = ?', [grp])
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Вернуться в меню старосты", callback_data='star_menu')
        markup.add(item1)
        for i in inf:
            item = types.InlineKeyboardButton(f"{i[0]}", callback_data=f'otmets{i[1]}')
            markup.add(item)
        bot.send_message(message.chat.id, 'Выберите ФИО ученика в списке.', reply_markup=markup)


def vistavleie_za_segodnya_star_para(message, uch):
    dt = date.today()
    wk = datetime.datetime.today().weekday()
    if wk == 6:
        bot.send_message(message.chat.id, 'Сегодня выходной')
        return star_menu(message)
    dt1 = '2023-09-01'
    n = str(dt1).split('-')
    n1 = str(dt).split('-')
    week1 = datetime.date(int(n1[0]), int(n1[1]), int(n1[2])).isocalendar()[1]
    week = datetime.date(int(n[0]), int(n[1]), int(n[2])).isocalendar()[1]
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        uchenik = cursor.execute('SELECT fio FROM Students WHERE student_id = ?', [uch[6:]]).fetchone()[0]
        uchenik1 = cursor.execute('SELECT tg_id FROM Users WHERE full_name = ?', [uchenik]).fetchone()[0]
        otmetki = cursor.execute('SELECT para, otmetka FROM Poseh WHERE tg_id = ? AND day = ?',
                                 [uchenik1, dt]).fetchall()
        b = []
        for i in otmetki:
            if int(i[0]) == 1:
                if int(i[1]) == 0:
                    b.append(['1', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['1', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['1', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['1', 'Отсутствовал 2 часа'])
                else:
                    b.append(['1', 'Не проставлена'])
            elif int(i[0]) == 2:
                if int(i[1]) == 0:
                    b.append(['2', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['2', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['2', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['2', 'Отсутствовал 2 часа'])
                else:
                    b.append(['2', 'Не проставлена'])
            elif int(i[0]) == 3:
                if int(i[1]) == 0:
                    b.append(['3', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['3', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['3', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['3', 'Отсутствовал 2 часа'])
                else:
                    b.append(['3', 'Не проставлена'])
            elif int(i[0]) == 4:
                if int(i[1]) == 0:
                    b.append(['4', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['4', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['4', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['4', 'Отсутствовал 2 часа'])
                else:
                    b.append(['4', 'Не проставлена'])
            elif int(i[0]) == 5:
                if int(i[1]) == 0:
                    b.append(['5', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['5', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['5', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['5', 'Отсутствовал 2 часа'])
                else:
                    b.append(['5', 'Не проставлена'])
        inf = cursor.execute('SELECT group_name FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
        if (week1 - week + 1) % 2 == 0:
            info1 = cursor.execute('SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                               'AND day = ? AND nedelya = ?', [inf, str(wk), 2]).fetchone()
        else:
            info1 = cursor.execute(
                'SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                'AND day = ? AND nedelya = ?', [inf, str(wk), 1]).fetchone()
        if len(b) == 0:
            infoday = 'Посещаемость не проставлена'
        else:
            infoday = []
            for i in range(len(b)):
                infoday.append(f'\n{b[i][0]} пара  {b[i][1]}\n')
        if (week1 - week + 1) % 2 == 0:
            a = 'Четная'
        else:
            a = 'Нечетная'
        infoday = ''.join(infoday)
        bot.send_message(message.chat.id, f'Дата {dt}, неделя №{week1 - week + 1}, {a}\n'
                                          f'\n1 пара  {info1[0]}\n'
                                          f'\n2 пара {info1[1]}\n'
                                          f'\n3 пара {info1[2]}\n'
                                          f'\n4 пара {info1[3]}\n'
                                          f'\n5 пара {info1[4]}\n'
                                          f'{infoday}')
        post = cursor.execute('SELECT para FROM Poseh WHERE tg_id = ? AND day = ?', [uchenik1, dt]).fetchall()
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in post:
            item = types.InlineKeyboardButton(f"{i[0]} пара", callback_data=f'OtmetPara{i[0]},{uchenik1}')
            markup.add(item)
        bot.send_message(message.chat.id, 'Выберите на какой паре вы хотите отметить ученика. ',
                         reply_markup=markup)


def vistavleie_za_segodnya_star_para1(message, uch):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Присутствовал", callback_data=f'kohecotm{uch},0')
    item2 = types.InlineKeyboardButton("Отсутствовал 1 час", callback_data=f'kohecotm{uch},1')
    item3 = types.InlineKeyboardButton("Отсутствовал 2 часа", callback_data=f'kohecotm{uch},2')
    item4 = types.InlineKeyboardButton("Отсутствие по уважительной причине", callback_data=f'kohecotm{uch},3')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Выберите отметку', reply_markup=markup)


def vistavleie_za_segodnya_star_para2(message, info):
    dt = date.today()
    op = info.split(',')
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        grp = cursor.execute('SElECT group_name FROM Users WHERE tg_id = ?', [op[1]]).fetchone()[0]
        group_id = cursor.execute('SELECT group_id FROM Groups WHERE group_name = ?', [grp]).fetchone()[0]
        k = cursor.execute('SELECT otmetka FROM Poseh WHERE para = ? AND tg_id = ? AND day = ?',
                           [op[0], op[1], dt])
        if k is not None:
            cursor.execute('UPDATE Poseh SET otmetka = ? WHERE para = ? AND tg_id = ? AND day = ?',
                           [int(op[2]), op[0], op[1], dt])
        else:
            cursor.execute('''INSERT INTO Poseh VALUES (?,?,?,?,?);''', [dt, op[1], op[0], int(op[3]), group_id])
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton("Выбор другого ученика", callback_data='pos_segodnya_star')
        item1 = types.InlineKeyboardButton("Меню cтаросты", callback_data='star_menu')
        markup.add(item, item1)
        bot.send_message(message.chat.id, 'Отметка проставлена. Для отметки этого же ученика на другой паре -'
                                          ' просто кликните по сообщению выше на другую нужную вам пару.',
                         reply_markup=markup)


def vistavleie_za_op_star_para1(message, uch):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, 'Напишите день за который хотите выставить посещаемость.'
                                          'Формат даты должен быть такой: Год-месяц-число. (через малый дефис)\n'
                                          'Пример: "2023-09-01" - 1 сентября 2023 года.')
    bot.register_next_step_handler(message, vistavleie_za_op_star_para, uch)


def vistavleie_za_op_star_para(message, uch):
    dt = message.text
    n1 = str(dt).split('-')
    wk = datetime.date(year=int(n1[0]), month=int(n1[1]), day=int(n1[2])).weekday()
    if wk == 6:
        bot.send_message(message.chat.id, 'Сегодня выходной')
        return star_menu(message)
    dt1 = '2023-09-01'
    n = str(dt1).split('-')
    n1 = str(dt).split('-')
    week1 = datetime.date(int(n1[0]), int(n1[1]), int(n1[2])).isocalendar()[1]
    week = datetime.date(int(n[0]), int(n[1]), int(n[2])).isocalendar()[1]
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        uchenik = cursor.execute('SELECT fio FROM Students WHERE student_id = ?', [uch[6:]]).fetchone()[0]
        uchenik1 = cursor.execute('SELECT tg_id FROM Users WHERE full_name = ?', [uchenik]).fetchone()[0]
        otmetki = cursor.execute('SELECT para, otmetka FROM Poseh WHERE tg_id = ? AND day = ?',
                                 [uchenik1, dt]).fetchall()
        b = []
        for i in otmetki:
            if int(i[0]) == 1:
                if int(i[1]) == 0:
                    b.append(['1', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['1', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['1', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['1', 'Отсутствовал 2 часа'])
                else:
                    b.append(['1', 'Не проставлена'])
            elif int(i[0]) == 2:
                if int(i[1]) == 0:
                    b.append(['2', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['2', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['2', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['2', 'Отсутствовал 2 часа'])
                else:
                    b.append(['2', 'Не проставлена'])
            elif int(i[0]) == 3:
                if int(i[1]) == 0:
                    b.append(['3', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['3', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['3', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['3', 'Отсутствовал 2 часа'])
                else:
                    b.append(['3', 'Не проставлена'])
            elif int(i[0]) == 4:
                if int(i[1]) == 0:
                    b.append(['4', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['4', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['4', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['4', 'Отсутствовал 2 часа'])
                else:
                    b.append(['4', 'Не проставлена'])
            elif int(i[0]) == 5:
                if int(i[1]) == 0:
                    b.append(['5', 'Присутствовал'])
                elif int(i[1]) == 3:
                    b.append(['5', 'Отсутствие по уважительной причине'])
                elif int(i[1]) == 1:
                    b.append(['5', 'Отсутствовал 1 час'])
                elif int(i[1]) == 2:
                    b.append(['5', 'Отсутствовал 2 часа'])
                else:
                    b.append(['5', 'Не проставлена'])
        inf = cursor.execute('SELECT group_name FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
        if (week1 - week + 1) % 2 == 0:
            info1 = cursor.execute(
                'SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                'AND day = ? AND nedelya = ?', [inf, str(wk), 2]).fetchone()
        else:
            info1 = cursor.execute(
                'SELECT f_para, s_para, tr_para, to_para, ti_para FROM Raspisanie WHERE groupvrasp = ? '
                'AND day = ? AND nedelya = ?', [inf, str(wk), 1]).fetchone()
        if len(b) == 0:
            infoday = 'Посещаемость не проставлена'
        else:
            infoday = []
            for i in range(len(b)):
                infoday.append(f'\n{b[i][0]} пара  {b[i][1]}\n')
        if (week1 - week + 1) % 2 == 0:
            a = 'Четная'
        else:
            a = 'Нечетная'
        infoday = ''.join(infoday)
        bot.send_message(message.chat.id, f'Дата {dt}, неделя №{week1 - week + 1}, {a}\n'
                                          f'\n1 пара  {info1[0]}\n'
                                          f'\n2 пара {info1[1]}\n'
                                          f'\n3 пара {info1[2]}\n'
                                          f'\n4 пара {info1[3]}\n'
                                          f'\n5 пара {info1[4]}\n'
                                          f'{infoday}')
        k = 1
        infoday1 = []
        for i in info1:
            if 'Нет пары' in i and i != '':
                k += 1
                continue
            else:
                infoday1.append(str(k))
                k += 1
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in infoday1:
            item = types.InlineKeyboardButton(f"{i} пара", callback_data=f'OtmetzPara{i},{uchenik1},{dt}')
            markup.add(item)
        bot.send_message(message.chat.id, 'Выберите на какой паре вы хотите отметить ученика. ',
                         reply_markup=markup)


def vistavleie_za_op_star_para2(message, uch):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Присутствовал", callback_data=f'kohezcotm{uch},0')
    item2 = types.InlineKeyboardButton("Отсутствовал 1 час", callback_data=f'kohezcotm{uch},1')
    item3 = types.InlineKeyboardButton("Отсутствовал 2 часа", callback_data=f'kohezcotm{uch},2')
    item4 = types.InlineKeyboardButton("Отсутствие по уважительной причине", callback_data=f'kohezcotm{uch},3')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Выберите отметку', reply_markup=markup)


def vistavleie_za_op_star_para3(message, info):
    op = info.split(',')
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        grp = cursor.execute('SElECT group_name FROM Users WHERE tg_id = ?', [int(op[1])]).fetchone()[0]
        group_id = cursor.execute('SELECT group_id FROM Groups WHERE group_name = ?', [str(grp)]).fetchone()[0]
        k = cursor.execute('SELECT otmetka FROM Poseh WHERE para = ? AND tg_id = ? AND day = ?',
                       [op[0], op[1], op[2]]).fetchone()
        if k is not None:
            cursor.execute('UPDATE Poseh SET otmetka = ? WHERE para = ? AND tg_id = ? AND day = ?',
                           [int(op[3]), op[0], op[1], op[2]])
        else:
            cursor.execute('''INSERT INTO Poseh VALUES (?,?,?,?,?);''', [op[2], op[1], op[0], int(op[3]), group_id])
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Меню cтаросты", callback_data='star_menu')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Отметка проставлена. Для отметки этого же ученика на другой паре -'
                                          ' просто кликните по сообщению выше на другую нужную вам пару.',
                         reply_markup=markup)


def vistavlenie_za_datu_star(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        grp = cursor.execute('SELECT group_name FROM Users WHERE tg_id = ?', [message.chat.id]).fetchone()[0]
        inf = cursor.execute('SELECT fio, student_id FROM Students WHERE group_name = ?', [grp])
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Вернуться в меню старосты", callback_data='star_menu')
        markup.add(item1)
        for i in inf:
            item = types.InlineKeyboardButton(f"{i[0]}", callback_data=f'otmetz{i[1]}')
            markup.add(item)
        bot.send_message(message.chat.id, 'Выберите ФИО ученика в списке.', reply_markup=markup)


def ped_pass(message):
    bot.send_message(message.chat.id,
                     'В разработке')
    return reg(message)


@bot.message_handler(commands=['adminka'])
def adminka_pass1(message):
    bot.send_message(message.chat.id, 'Напишите пароль:')
    bot.register_next_step_handler(message, adminka_pass2)


def adminka_pass2(message):
    if message.text == '1':
        return adminka(message)
    else:
        bot.send_message(message.chat.id, 'Пароль неверный')
        return adminka_pass1(message)


def adminka(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Добавить/поменять расписание", callback_data='drasp_pass')
    item2 = types.InlineKeyboardButton("Добавить ученика", callback_data='duch')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Добро пожаловать в комнату админа', reply_markup=markup)


def drasp_pass(message):
    with sqlite3.connect('journal.db') as db:
        cursor = db.cursor()
        markup = types.InlineKeyboardMarkup(row_width=1)
        inf = cursor.execute('SELECT group_name, group_id FROM Groups')
        for i in inf:
            item = types.InlineKeyboardButton(f"{i[0]}", callback_data=f'drasp{i[1]}')
            markup.add(item)
        bot.send_message(message.chat.id, 'Выберите группу.',
                         reply_markup=markup)


def drasp_pass2(message, grp):
    bot.send_message(message.chat.id, 'Напишите День на который хотите добавить расписание.\n'
                                      'Формат даты должен быть такой: Год-месяц-число. (через малый дефис)\n'
                                          'Пример: "2023-09-01" - 1 сентября 2023 года.')
    bot.register_next_step_handler(message, drasp_pass3, grp)


def drasp_pass3(message, grp):
    if message.text[:4] in ['2023', '2024', '2025', '2026']:
        if message.text[5:7] in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            if message.text[8:10] in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                                      '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
                                      '27', '28', '29', '30', '31']:
                if message.text[4] == '-' and message.text[7] == '-':
                    op = message.text
                    bot.send_message(message.chat.id, 'Отправьте одним сообщением расписание на день в формате :\n\n'
                                                    'Первая пара;вторая пара;третья пара;четвертая пара;пятая пара\n\n'
                                                      'Пример: "1. 09:30 – 11:05\n\n<Нет пары>;\n\n2. 11:20 – 12:55\n\nОсновы'
                                                      ' российской государственности Босов Д. В.\n\nПрактика (3 – 17 нед'
                                                      '.) в 318 (ОП);".\n\n В сообщение обязательно должно быть не меньше 4х '
                                                      'знаков ";"')
                    bot.register_next_step_handler(message, drasp, op, grp)
    else:
        bot.send_message(message.chat.id, 'Дата введена неправильно, попробуйте еще раз.')
        return drasp_pass2


def drasp(message, op, grp):
    with sqlite3.connect('journal.db') as db:
        if message.text.count(';') < 4:
            bot.send_message('Расписание введено неправильно.')
            return drasp_pass2(message, grp)
        else:
            dt1 = '2023-09-01'
            n = str(dt1).split('-')
            n1 = str(op).split('-')
            wk = datetime.date(year=int(n1[0]), month=int(n1[1]), day=int(n1[2])).weekday()
            week1 = datetime.date(int(n1[0]), int(n1[1]), int(n1[2])).isocalendar()[1]
            week = datetime.date(int(n[0]), int(n[1]), int(n[2])).isocalendar()[1]
            cursor = db.cursor()
            s = message.text.split(';')
            para1 = s[0] + '\n' + '\n'
            para2 = s[1] + '\n' + '\n'
            para3 = s[2] + '\n' + '\n'
            para4 = s[3] + '\n' + '\n'
            para5 = s[4] + '\n'
            group_ = cursor.execute('SELECT group_name FROM Groups WHERE group_id = ?', [grp]).fetchone()[0]
            if (week1 + week + 1) % 2 == 0:
                k = 2
                ch = cursor.execute('SELECT f_para,s_para,tr_para,to_para,ti_para FROM Raspisanie WHERE groupvrasp = ?'
                                    ' AND day = ? AND nedelya = ?', [group_, wk, 2]).fetchone()
            else:
                k = 1
                ch = cursor.execute('SELECT f_para,s_para,tr_para,to_para,ti_para FROM Raspisanie WHERE groupvrasp = ? AND day = ? AND nedelya = ?', [group_, wk, 1]).fetchone()
            if ch is None:
                pass
            else:
                cursor.execute('DELETE FROM Raspisanie WHERE groupvrasp = ? AND day = ? AND nedelya = ?', [group_, wk, k])
            cursor.execute('''INSERT INTO Raspisanie VALUES (?,?,?,?,?,?,?,?);''', [wk, group_, para1, para2,
                                                                                    para3, para4, para5, k])
            bot.send_message(message.chat.id, 'Выполнено.')
            return adminka(message)


bot.polling()