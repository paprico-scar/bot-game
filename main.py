import logging
import random
import sqlite3
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

GENDER, AGE, REGION, BEGINNING, ANSWER = range(5)

fl_dict = {'f': True}

dict_user = {'name': '', 'gender': '', 'age': '', 'region': ''}


def start(update, context):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    user = update.message.from_user
    logger.info(f'Пользователь {user.first_name} начал беседу с ботом.')
    names = cur.execute('SELECT name FROM users_tb WHERE name=?', (user.first_name,)).fetchall()
    if names:
        pass
    else:
        fl_dict['f'] = False
    dict_user['name'] = user.first_name
    reply_keyboard = [['Mужчина', 'Женщина', 'Другое']]
    update.message.reply_text(
        'Привет, меня зовут Арханвей. Я бот который будет играть\n'
        'с тобой в игру. Ты погрузишься в средневековье, где\n'
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
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    last_id = cur.execute("""SELECT MAX(id) FROM users_tb""").fetchone()
    if fl_dict['f']:
        cur.execute('UPDATE users_tb SET gender = ? WHERE name = ?', (dict_user["gender"], dict_user['name']))
        con.commit()
        cur.execute('UPDATE users_tb SET age = ? WHERE name = ?', (dict_user["age"], dict_user['name']))
        con.commit()
        cur.execute('UPDATE users_tb SET region = ? WHERE name = ?', (dict_user["region"], dict_user['name']))
        con.commit()
        logger.info(f'Информация о {user.first_name} обновлена.')
    else:
        cur.execute('INSERT INTO users_tb VALUES(?,?,?,?,?)',
                    (last_id[0] + 1, dict_user['name'], dict_user["gender"], dict_user["age"], dict_user["region"]))
        con.commit()
        logger.info(f'{user.first_name} добавлен в базу данных.')
    reply_keyboard = [['Приступим!']]
    update.message.reply_text('Хорошо приступим к игре).', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
        input_field_placeholder='Нажмите чтобы начать'))
    return BEGINNING


def beginning_of_story(update, contest):
    user = update.message.from_user
    update.message.reply_text('Однажды в средневековье в бедной крестьянской семье родился ребёнок!')
    update.message.reply_text(f'Назвали его {user.first_name}.')
    reply_keyboard = [['Плакать в колыбели', 'Лежать молча']]
    update.message.reply_text('Кроме вас в семье было много детей. И чтобы выжить вам нужно выделятся среди остальных.',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
        input_field_placeholder='Что вы сделаете?'))
    return ANSWER


def next(update, contest):
    if update.message.text == 'Плакать в колыбели':
        update.message.reply_text('Родители заметили вас и начали проявлять к вам заботу!')
    elif update.message.text == 'Лежать молча':
        update.message.reply_text('Вы не привлекли внимание родителей поэтому они продолжили работу по дому...')
    update.message.reply_text('Проходит какое-то время и вы уже обедаете за столом вместе со всеми.',
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Так как вы живёте в очень большой семье еды вам достаётся не очень много.')


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} закончил беседу с ботом.")
    update.message.reply_text(
        'Пока! Надеюсь мы скоро встретимся.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    updater = Updater('5193592133:AAGbqN6WaAmB7GE9botLB1wki32WMH689w8')
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={GENDER: [MessageHandler(Filters.regex('^(Mужчина|Женщина|Другое)$'), gender)],
                AGE: [MessageHandler(Filters.text, age)],
                REGION: [MessageHandler(Filters.text, region)],
                BEGINNING: [MessageHandler(Filters.text, beginning_of_story)],
                ANSWER: [MessageHandler(Filters.regex('^(Плакать в колыбели|Лежать молча)$'), next)]
                },
        fallbacks=[CommandHandler('cancel', cancel)]

    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()