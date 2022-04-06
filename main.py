import logging
import random
import sqlite3

# t.me/yl_game_bot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

GENDER, AGE, REGION, INFO_AND_START = range(4)

FLAG = True
CONNECTIONS = sqlite3.connect('bot_db')

dict_user = {'name': '', 'gender': '', 'age': '', 'region': ''}


def start(update, context):
    cur = CONNECTIONS.cursor()
    user = update.message.from_user
    logger.info(f'Пользователь {user.first_name} начал беседу с ботом.')
    names = cur.execute(f'''SELECT name FROM users_tb WHERE name = {user.first_name}''').fetchone()
    if names[0][0]:
        FLAG = False
    dict_user['name'] = user.first_name
    reply_keyboard = [['Mужчина', 'Женщина', 'Другое']]
    update.message.reply_text(
        'Привет, меня зовут Арханвей. Я бот который будет играть\n'
        'с тобой в игру. Ты погрузишься и средневековье, где\n'
        'будут замки, рыцари и драконы. Но для начала\n'
        'я задам тебе пару вопросов.\n\n'
        'Какой у тебя пол?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder='Впиши свой пол'
        )
    )

    return GENDER


def gender(update, context):
    user = update.message.from_user
    logger.info(f'Пол пользователя {user.first_name}: {update.message.text}.')
    dict_user['gender'] = update.message.text
    update.message.reply_text(
        'Хорошо! А теперь скажи пожалуйста сколько тебе лет',
        reply_markup=ReplyKeyboardRemove()
    )

    return AGE


def age(update, context):
    user = update.message.from_user
    logger.info(f'Возраст {user.first_name}: {update.message.text}.')
    dict_user['age'] = update.message.text
    update.message.reply_text(
        'Остался последний вопрос из какой ты страны'
    )

    return REGION


def region(update, context):
    user = update.message.from_user
    logger.info(f'{user.first_name} написал что он из {update.message.text}.')
    dict_user['region'] = update.message.text
    update.message.reply_text(
        'ок'
    )
    return ConversationHandler.END


def info_and_start(update, context):
    cur = CONNECTIONS.cursor()
    last_id = cur.execute("""SELECT MAX(id) FROM users_tb""").fetchone()
    user = update.message.from_user
    if FLAG:
        cur.execute(f'''INSERT INTO tb_order VALUES({last_id + 1}, {dict_user["name"]}, 
            {dict_user["gender"]}, {dict_user["age"]}, {dict_user["region"]})''')
        CONNECTIONS.commit()
    else:
        cur.execute(f'''UPDATE users_tb SET gender = {dict_user["gender"]}''')
        CONNECTIONS.commit()
        cur.execute(f'''UPDATE users_tb SET age = {dict_user["age"]}''')
        CONNECTIONS.commit()
        cur.execute(f'''UPDATE users_tb SET region = {dict_user["region"]}''')
        CONNECTIONS.commit()
    update.message.reply_text('Хорошо приступим к игре)')


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} закончил беседу с ботом.")
    update.message.reply_text(
        'Пока! Надеюсь мы скоро встретимся.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    updater = Updater('5294956202:AAGngiDjlf7FdpeQqkYgn6eZXhuIdpetqJM')
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={GENDER: [MessageHandler(Filters.regex('^(Mужчина|Женщина|Другое)$'), gender)],
                AGE: [MessageHandler(Filters.text, age)],
                REGION: [MessageHandler(Filters.text, region)]
                },
        fallbacks=[CommandHandler('cancel', cancel)]

    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
