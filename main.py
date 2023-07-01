import telebot 
import customers_db as cdb
import sqlite3




#admin rules: 688443502
admins = (688443502)


bot = telebot.TeleBot('6296572743:AAH8fGKrbMeitQGrS-beC2gcMUsE4PvV05E')
cdb.construct()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = (message.chat.id, message.from_user.first_name, message.from_user.last_name, 'None', 0, message.from_user.username, 'DEFAULT')
    cdb.cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", user)
    cdb.connection.commit()

    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '! Твой никнейм: ' + message.from_user.username + ' Если хочешь поменять его, нажми /nickname' )
    bot.send_message(message.chat.id, "Чтобы узнать свой id, нажми /info")
    bot.send_message(688443502, 'NEW REGISTRATION: '+ str(user[0]) +' ' + str(user[1]) + ' '+ str(user[5]))

@bot.message_handler(commands=['nickname'])
def nickname_change(message):
    bot.send_message(message.chat.id, 'Введи желаемый никнейм')
    cdb.change_status(message.chat.id, 'CHANGE NICKNAME')

@bot.message_handler(commands=['info'])
def info(message):
    cdb.cursor.execute("select * from users where userid='" + str(message.chat.id) +"'" )
    result = cdb.cursor.fetchone()
    status = result[6]
    if status != 'DEFAULT':
        bot.send_message(message.chat.id, 'Access denied')
    else: 
        bot.send_message(message.chat.id, result[0])

@bot.message_handler(commands=['add_player'])
def add_player(message):
     bot.send_message(message.chat.id, 'Круто что вы решили стать игроком! Давайте же зарегестрируем вас как игрока. Наччнем с простого: какое ваше имя?(пример ответа: Василий)')
     cdb.change_status(message.chat.id, 'ADD_PLAYER_NAME')    
     player = (message.chat.id, None, None, None, None, None )
     cdb.cursor.execute("insert into players values(?, ?, ?, ?, ?, ?)", player)

@bot.message_handler(commands=['player_info'])
def player_info(message):
    bot.message_handler(message.chat.id, 'Введите никнейм игрока и мы посмотрим что у нас есть.')
    cdb.change_status(message.chat.id, 'PLAYER_INFO')




@bot.message_handler(func=lambda message: True)
def answer(message):
    cdb.cursor.execute("select * from users where userid='" + str(message.chat.id) +"'" )
    result = cdb.cursor.fetchone()
    status = result[6]
    match status:
        case 'DEFAULT':
            bot.send_message(message.chat.id, 'Введите команду, если что-то нужно')
        case 'CHANGE NICKNAME':
            cdb.change_status('DEFAULT')
            cdb.connection.commit()
            bot.send_message(message.chat.id, 'Никней успешно сменен')
        case 'ADD_PLAYER_NAME':
            cdb.change_player_atribute(message.chat.id, 'name', message.text)
            cdb.change_status(message.chat.id, 'ADD_PLAYER_SURNAME')
            bot.send_message(message.chat.id, "Отлично! Теперь введите вашу фамилию(пример ответа: Петров):")
        case 'ADD_PLAYER_SURNAME':
            cdb.change_player_atribute(message.chat.id, 'surname', message.text)
            cdb.change_status(message.chat.id, 'ADD_PLAYER_SCHOOL')
            bot.send_message(message.chat.id, "Отлично! Теперь введите номер учебного заведения или название(пример ответа: 239, 30, ФТШ):")
        case 'ADD_PLAYER_SCHOOL':
            cdb.change_player_atribute(message.chat.id, 'school', message.text)
            cdb.change_status(message.chat.id, 'ADD_PLAYER_STEAM')
            bot.send_message(message.chat.id, """Осталось лишь привязать steam и регистрация готова. Для этого пришлите ваш steam64 код(*это нужно для просмотра статистики вашего аккаунта; пример ответа:12345678901234567)  \n Обратите внимание, что аккаунт steam можно будет перепривязать только в экстренном случае через админа @n3ke27 
                             """)
        case 'ADD_PLAYER_STEAM':
            cdb.change_player_atribute(message.chat.id, 'steam', message.text)
            cdb.change_status(message.chat.id, 'DEFAULT')
            bot.send_message(message.chat.id, 'Поздравляем, теперь вы зарегестрированы как игрок! Чтобы вступить в комнаду, дождитесь приглашения или создайте свою с помощью команды /add_team')                 
        case 'PLAYER_INFO':
            bot.send_message(message.chat.id, cdb.player_info(message.text))
            cdb.change_status(message.chat.id, 'DEFAULT')
    
bot.infinity_polling()

