import logging
import sqlite3
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

GEN, AGE, REG, A, B, C, D, E, F, G, H = range(11)

user_game_info = {'f': True, 'hp': 3}

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
        user_game_info['f'] = False
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

    return GEN


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

    return REG


def region(update, context):
    user = update.message.from_user
    logger.info(f'{user.first_name} написал что он из {update.message.text}.')
    dict_user['region'] = update.message.text
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    last_id = cur.execute("""SELECT MAX(id) FROM users_tb""").fetchone()
    if user_game_info['f']:
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
    return A


def beginning_of_story(update, contest):
    user_game_info['hp'] = 3
    user = update.message.from_user
    logger.info(f'{user.first_name} начал историю.')
    update.message.reply_text('Однажды в средневековье в бедной крестьянской семье родился ребёнок!')
    update.message.reply_text(f'Назвали его {user.first_name}.')
    reply_keyboard = [['Плакать в колыбели', 'Лежать молча']]
    update.message.reply_text('Кроме вас в семье было много детей. И чтобы выжить вам нужно выделятся среди остальных.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               input_field_placeholder='Что вы сделаете?'))
    return B


def polzat(update, contest):
    user = update.message.from_user
    if update.message.text == 'Плакать в колыбели':
        update.message.reply_text('Родители заметили вас и начали проявлять к вам заботу!')
        logger.info(f'{user.first_name} выбрал "Плакать в колыбели".')
    elif update.message.text == 'Лежать молча':
        update.message.reply_text('Вы не привлекли внимание родителей поэтому они продолжили работу по дому...')
        logger.info(f'{user.first_name} выбрал "Лежать молча".')
    reply_keyboard = [['Ползать', "Сидеть в углу"]]
    update.message.reply_text(
        'Вы хотите ползать по дому и пробовать всё на вкус но люди не оборащают на вас внимания и е смотрят под ноги.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
    return C


def govor(update, contest):
    user = update.message.from_user
    if update.message.text == 'Ползать':
        update.message.reply_text('Вы ловко ползаете и уворачиваетсь от ног.')
        logger.info(f'{user.first_name} выбрал "Ползать".')
    elif update.message.text == 'Сидеть в углу':
        update.message.reply_text('Вы отсиделиь в углу и не узналми ничего нового.')
        logger.info(f'{user.first_name} выбрал "Сидеть в углу".')
    reply_keyboard = [['Научиться ходить', "Научиться говорить"]]
    update.message.reply_text('Вы задумались о будущем и вы решили чему-то научиться.',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True))
    return D


def ploh_slovo(update, contest):
    user = update.message.from_user
    if update.message.text == 'Научиться ходить':
        update.message.reply_text('Вы начали ходить теперь у вас больше шансов умереть.')
        logger.info(f'{user.first_name} выбрал "Научиться ходить".')
    elif update.message.text == 'Научиться говорить':
        update.message.reply_text('Вы заговорили посреди ночи и тем самым напугали родителей.')
        logger.info(f'{user.first_name} выбрал "Научиться говорить".')
    reply_keyboard = [['Придумать своё слово', "Повторить за отцом"]]
    update.message.reply_text('Вы услышали как вапш отекц произнес нехорошее слово.',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True))
    return E


def next(update, contest):
    user = update.message.from_user
    if update.message.text == 'Придумать своё слово':
        update.message.reply_text('Вы вы сказали странное слово но никто вас не понял.')
        logger.info(f'{user.first_name} выбрал "Придумать своё слово".')
    elif update.message.text == 'Повторить за отцом':
        update.message.reply_text('Услышав это, отец в ярости поколотил вас.')
        user_game_info['hp'] -= 1
        logger.info(f'{user.first_name} выбрал "Повторить за отцом".')
    update.message.reply_text('Проходит какое-то время и вы уже обедаете за столом вместе со всеми.')
    reply_keyboard = [['Съесть свою порцию', "Отобрать у брата"]]
    update.message.reply_text('Так как вы живёте в очень большой семье еды вам достаётся не очень много.',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True))
    return F


def night_in_bad(update, context):
    user = update.message.from_user
    if update.message.text == 'Съесть свою порцию':
        update.message.reply_text('Вы не доедаете у сожалению вы плохо развиваетесь.(у вас отнимается одно хп)')
        user_game_info['hp'] -= 1
        logger.info(f'{user.first_name} выбрал "Съесть свою порцию" и теряет одно хп))))).')
    elif update.message.text == 'Отобрать у брата':
        update.message.reply_text(
            'Старший брат оказался сильнее и он поколотил вас до беспамятства.(у вас отнимается одно хп)')
        user_game_info['hp'] -= 1
        logger.info(f'{user.first_name} выбрал "Отобрать у брата" незавидная судьба.')
    reply_keyboard = [['Присмотреться', 'Спрятаться под одеяло']]
    update.message.reply_text(
        'Вы не можете уснуть ночью. Вдруг вы видите как из окна просунулась чья-то рука и стала ощупывать кровать.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
    return G


def pole(update, context):
    user = update.message.from_user
    if update.message.text == 'Присмотреться':
        logger.info(f'{user.first_name} выбрал "Присмотреться".')
        update.message.reply_text('Присмотревшись, вы поняли что это обычная ветка.')
    elif update.message.text == 'Спрятаться под одеяло':
        logger.info(f'{user.first_name} выбрал "Спрятаться под одеяло".')
        update.message.reply_text('Рука бстро схватила вашего брата и утащила его из окна. Больше его никто не видел.')
    reply_keyboard = [['Взятся за работу', 'Отлынивать']]
    update.message.reply_text('Как только вам исполнилось 4 года вас отправили работать на поле',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True))
    return H


def igra_v_pryatki(update, context):
    user = update.message.from_user
    if update.message.text == 'Взятся за работу':
        logger.info(f'{user.first_name} выбрал "Взятся за работу".')
        update.message.reply_text(
            'Вы работали так усепрдно и сломаои плуг. Отец был в ярости! Он бил вас до потери сознания.')
        user_game_info['hp'] -= 2
    elif update.message.text == 'Отлынивать':
        logger.info(f'{user.first_name} выбрал "Отлынивать".')
        update.message.reply_text('Рука бстро схватила вашего брата и утащила его из окна. Больше его никто не видел.')
    if user_game_info['hp'] <= 0:
        reply_keyboard = [['Продолжить']]
        update.message.reply_text('Вы умерли и игра начнется заново.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        logger.info(f'{user.first_name} умер.')
        return A
    reply_keyboard = [['Играт в прятки', 'Играть в салки']]
    update.message.reply_text('Вы подросли и кже играете с ребятней.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


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
        states={GEN: [MessageHandler(Filters.regex('^(Mужчина|Женщина|Другое)$'), gender)],
                AGE: [MessageHandler(Filters.text, age)],
                REG: [MessageHandler(Filters.text, region)],
                A: [MessageHandler(Filters.text, beginning_of_story)],
                B: [MessageHandler(Filters.text, polzat)],
                C: [MessageHandler(Filters.text, govor)],
                D: [MessageHandler(Filters.text, ploh_slovo)],
                E: [MessageHandler(Filters.text, next)],
                F: [MessageHandler(Filters.text, night_in_bad)],
                G: [MessageHandler(Filters.text, pole)],
                H: [MessageHandler(Filters.text, igra_v_pryatki)]
                },
        fallbacks=[CommandHandler('cancel', cancel)]

    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
