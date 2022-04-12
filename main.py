import logging
import sqlite3
import pretty_errors
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

# логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

GEN, AGE, REG, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = range(29)

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


def beginning_of_story(update, context):
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


def polzat(update, context):
    user = update.message.from_user
    if update.message.text == 'Плакать в колыбели':
        update.message.reply_text('Родители заметили вас и начали проявлять к вам заботу!')
        logger.info(f'{user.first_name} выбрал "Плакать в колыбели".')
    elif update.message.text == 'Лежать молча':
        update.message.reply_text('Вы не привлекли внимание родителей поэтому они продолжили работу по дому...')
        logger.info(f'{user.first_name} выбрал "Лежать молча".')
    reply_keyboard = [['Ползать', "Сидеть в углу"]]
    update.message.reply_text(
        'Вы хотите ползать по дому и пробовать всё на вкус, но люди не оборащают на вас внимания и не смотрят под ноги.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
    return C


def govor(update, context):
    user = update.message.from_user
    if update.message.text == 'Ползать':
        update.message.reply_text('Вы ловко ползаете и уворачиваетсь от ног.')
        logger.info(f'{user.first_name} выбрал "Ползать".')
    elif update.message.text == 'Сидеть в углу':
        update.message.reply_text('Вы отсиделись в углу и не узнали ничего нового.')
        logger.info(f'{user.first_name} выбрал "Сидеть в углу".')
    reply_keyboard = [['Научиться ходить', "Научиться говорить"]]
    update.message.reply_text('Вы задумались о будущем и вы решили чему-то научиться.',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True))
    return D


def ploh_slovo(update, context):
    user = update.message.from_user
    if update.message.text == 'Научиться ходить':
        update.message.reply_text('Вы начали ходить теперь у вас больше шансов умереть.')
        logger.info(f'{user.first_name} выбрал "Научиться ходить".')
    elif update.message.text == 'Научиться говорить':
        update.message.reply_text('Вы заговорили посреди ночи и тем самым напугали родителей.')
        logger.info(f'{user.first_name} выбрал "Научиться говорить".')
    reply_keyboard = [['Придумать своё слово', "Повторить за отцом"]]
    update.message.reply_text('Вы услышали как ваш отец произнёс нехорошее слово.',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True))
    return E


def next(update, context):
    user = update.message.from_user
    if update.message.text == 'Придумать своё слово':
        update.message.reply_text('Вы вы сказали странное слово, но никто вас не понял.')
        logger.info(f'{user.first_name} выбрал "Придумать своё слово".')
    elif update.message.text == 'Повторить за отцом':
        update.message.reply_text('Услышав это, отец в ярости поколотил вас.(у вас отнимается одно хп)')
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
        update.message.reply_text('Вы не доедаете, к сожалению вы плохо развиваетесь.(у вас отнимается одно хп)')
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
        update.message.reply_text('Рука быстро схватила вашего брата и утащила его из окна. Больше его никто не видел.')
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
            'Вы работали так усепрдно и сломали плуг. Отец был в ярости! Он бил вас до /'
            'потери сознания.(у вас отнимается два хп)')
        user_game_info['hp'] -= 2
    elif update.message.text == 'Отлынивать':
        logger.info(f'{user.first_name} выбрал "Отлынивать".')
        update.message.reply_text('Вы отлыниваете от работы. Ваши родные раздрожены этим фактом.')
    if user_game_info['hp'] <= 0:
        reply_keyboard = [['Продолжить']]
        update.message.reply_text('Вы умерли и игра начнется заново.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        logger.info(f'{user.first_name} умер.')
        return A
    reply_keyboard = [['Играть в прятки', 'Играть в салки']]
    update.message.reply_text('Вы подросли и уже играете с ребятней.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return I


def pole_2(update, context):
    user = update.message.from_user
    if update.message.text == 'Играть в прятки':
        logger.info(f'{user.first_name} выбрал "Играть в прятки"')
        update.message.reply_text(
            'Вы спрятались настолько хорошо, что вас нашли только через три дня.(у вас отнимается одно хп)')
        user_game_info['hp'] -= 1
    elif update.message.text == 'Играть в салки':
        logger.info(f'{user.first_name} выбрал "Играть в салки"')
        update.message.reply_text('Вы очень изворотливы поэтому вы никогда не водили в игре.')
    if user_game_info['hp'] <= 0:
        reply_keyboard = [['Продолжить']]
        update.message.reply_text('Вы умерли и игра начнется заново.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        logger.info(f'{user.first_name} умер.')
        return A
    reply_keyboard = [['Дёрнуть коня за хвост', "Взяться за плуг"]]
    update.message.reply_text('Отец поймал вас и отправил работатль на поле, но пахать вам страшно лень.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return J


def chel(update, context):
    user = update.message.from_user
    if update.message.text == 'Дёрнуть коня за хвост':
        logger.info(f'{user.first_name} выбрал "Дёрнуть коня за хвост"')
        update.message.reply_text(
            'Конь вас хорошенько легнул.(у вас отнимается два хп)')
        user_game_info['hp'] -= 2
    elif update.message.text == 'Взяться за плуг':
        logger.info(f'{user.first_name} выбрал "Взяться за плуг"')
        update.message.reply_text('Вы проработали так весь день. Перспектива работать так всю вам не понравилась.')
    if user_game_info['hp'] <= 0:
        reply_keyboard = [['Продолжить']]
        update.message.reply_text('Вы умерли и игра начнется заново.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        logger.info(f'{user.first_name} умер.')
        return A
    reply_keyboard = [['Не обращать внимания', 'Рассказать взырослым']]
    update.message.reply_text('Работая на поле, вы замечаете странного человека, который смотрит за вами.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return K


def scotina(update, context):
    user = update.message.from_user
    if update.message.text == 'Не обращать внимания':
        logger.info(f'{user.first_name} выбрал "Не обращать внимания"')
        update.message.reply_text('Вскоре ваше поле разграбили у вашей семьи упал доход.')
    elif update.message.text == 'Рассказать взырослым':
        logger.info(f'{user.first_name} выбрал "Рассказать взырослым"')
        update.message.reply_text(
            'Вы рассказываете об этом человеке взрослым и потом вы узнаёте, что это был местый вор. Его завтра повесят.')
    reply_keyboard = [['Пускай гуляют', 'Махать палкой, чтобы шла обратно']]
    update.message.reply_text('Ваша ленивая скотина зашла на землю, принадлежащую Лорду.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return L


def batya_i_voyna(update, context):
    user = update.message.from_user
    if update.message.text == 'Пускай гуляют':
        logger.info(f'{user.first_name} выбрал "Пускай гуляют"')
        update.message.reply_text('Вашу скотну заметил Лорд. Вашего отца оштрафовали. Теперь ваша семья нищая.')
    elif update.message.text == 'Махать палкой, чтобы шла обратно':
        logger.info(f'{user.first_name} выбрал "Махать палкой, чтобы шла обратно"')
        update.message.reply_text(
            'Ваша скотина лениво пошла, помяв вас при этом. Зато вы не потревожили Лорда.(у вас отнимается одно хп)')
        user_game_info['hp'] -= 1
    if user_game_info['hp'] <= 0:
        reply_keyboard = [['Продолжить']]
        update.message.reply_text('Вы умерли и игра начнется заново.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        logger.info(f'{user.first_name} умер.')
        return A
    reply_keyboard = [['Идти куда глаза глядят', 'Шастаться по деревне']]
    update.message.reply_text('Лорд призвал вашего отца в армию. Платить оброк нечем.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return M


def traktir(update, context):
    user = update.message.from_user
    if update.message.text == 'Идти куда глаза глядят':
        logger.info(f'{user.first_name} выбрал "Идти куда глаза глядят"')
        update.message.reply_text('Глаза глядели в сторону трактира.')
    if update.message.text == 'Шастаться по деревне':
        logger.info(f'{user.first_name} выбрал "Шастаться по деревне"')
        update.message.reply_text('Вы ничего не делаете и ничего не происходит. Удивительно!')
    reply_keyboard = [['Позвать стражников', 'Подойти ближе']]
    update.message.reply_text('Вы оказались вечером у берега реки. На илистых камнях двигается сгорбленный силуэт.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return N


def utopec(update, context):
    user = update.message.from_user
    if update.message.text == 'Позвать стражников':
        reply_keyboard = [['Ну ладно']]
        logger.info(f'{user.first_name} выбрал "Позвать стражников"')
        update.message.reply_text('Вы вернулись на это место со стражей, но силуэт исчез.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    elif update.message.text == 'Подойти ближе':
        logger.info(f'{user.first_name} выбрал "Подойти ближе"')
        reply_keyboard = [['Очень жаль']]
        update.message.reply_text(
            'Подойдя ближе, вы распознали ожившего утопца и бросились бежать.\n'
            'Ваша спина исполосована гнилыми когтями. (у вас отнимается одно хп)',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        user_game_info['hp'] -= 1
        if user_game_info['hp'] <= 0:
            reply_keyboard = [['Продолжить']]
            update.message.reply_text('Вы умерли и игра начнется заново.',
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            logger.info(f'{user.first_name} умер.')
            return A
    return O


def v_traktire(update, context):
    reply_keyboard = [['Заказать похлёбку', 'Спросить про подработку']]
    update.message.reply_text('Вы дошли до старого трактира. \n'
                              'Внутри грязно и откуда-то из полутьмы на вас вопросительно смотрит трактирщик.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return P


def food_or_work(update, context):
    user = update.message.from_user
    if update.message.text == 'Заказать похлёбку':
        logger.info(f'{user.first_name} выбрал "Заказать похлёбку"')
        update.message.reply_text('В еде были кости и сено. О чаевых не может быть и речи.(у вас прибавляется одно хп)')
        user_game_info['hp'] += 1
        reply_keyboard = [['Расплатиться', 'Убежать']]
        update.message.reply_text('Трактирщик требует денег',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return S
    if update.message.text == 'Спросить про подработку':
        logger.info(f'{user.first_name} выбрал "Спросить про подработку"')
        update.message.reply_text('Трактирщик позвал за собой. Вам предстоит средневековое собеседование.')
        reply_keyboard = [['Усердно драить котёл', 'Налить туда воды и молиться']]
        update.message.reply_text('Трактирщик указал на огромный грязный котёл посреди кухни. Его надо отмыть.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return Q


def plata(update, context):
    user = update.message.from_user
    if update.message.text == 'Расплатиться':
        logger.info(f'{user.first_name} выбрал "Расплатиться"')
        update.message.reply_text('Кажется, у вас и денег то нет. Трактирщик разозлился и поколотил вас дубиной. \n'
                                  '(у вас отнимается одно хп)')
        user_game_info['hp'] -= 1
        if user_game_info['hp'] <= 0:
            reply_keyboard = [['Продолжить']]
            update.message.reply_text('Вы умерли и игра начнется заново.',
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            logger.info(f'{user.first_name} умер.')
            return A
    if update.message.text == 'Убежать':
        logger.info(f'{user.first_name} выбрал "Убежать"')
        update.message.reply_text('Вам удалось убежать')
    reply_keyboard = [['Бежать со всех ног', 'Узнать, что эти господа делают в столь поздний час']]
    update.message.reply_text('Вы возвращаетесь домой через лес. Внезапно перед вами появляются двое.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return T


def lydi(update, context):
    user = update.message.from_user
    if update.message.text == 'Бежать со всех ног':
        logger.info(f'{user.first_name} выбрал "Бежать со всех ног"')
        update.message.reply_text('Повернувшись назад для побега, вы обнаружили ещё двоих людей. Бежать не получится.')
    if update.message.text == 'Узнать, что эти господа делают в столь поздний час':
        logger.info(f'{user.first_name} выбрал "Узнать, что эти господа делают в столь поздний час"')
        update.message.reply_text('Вы вежливо поинтересовались, кто эти господа. \n'
                                  'Но на вас только подозрительно ухмыльнулись')
    reply_keyboard = [['Достать всё, что есть', 'Изобразить юродивого']]
    update.message.reply_text('Человек со шрамом достаёт кинжал и направляет его на вас. Деньги или жизнь?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return U


def urodivyi(update, context):
    user = update.message.from_user
    if update.message.text == 'Достать всё, что есть':
        logger.info(f'{user.first_name} выбрал "Достать всё, что есть"')
        update.message.reply_text('Вы опустошили карманы. Ничего там, конечно, не было. \n'
                                  'На что эти бандиты рассчитывали?')
    if update.message.text == 'Изобразить юродивого':
        logger.info(f'{user.first_name} выбрал "Изобразить юродивого"')
        update.message.reply_text('Вы стали нести окалесицу, но это не помешало бандитам обыскать вас.')
    reply_keyboard = [['Пойти дальше', 'Вернуться']]
    update.message.reply_text('Человек со шрамом: "А ты не так прост как кажешься. Мы с тобой ещё увидимся".',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return V


def derevnya(update, context):
    user = update.message.from_user
    if update.message.text == 'Пойти дальше':
        logger.info(f'{user.first_name} выбрал "Пойти дальше"')
        update.message.reply_text('Вы не знаете куда пойти и возвращаетесь обратно в деревню.')
    if update.message.text == 'Вернуться':
        logger.info(f'{user.first_name} выбрал "Вернуться"')
        update.message.reply_text('Вы решили вернуться обратно в деревню.')
    reply_keyboard = [['Взять деньги']]
    update.message.reply_text('Пока вы шли до дома вы нашли пару золотых монет на земле.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return W


def bandits(update, context):
    user = update.message.from_user
    reply_keyboard = [['Отказаться', 'Идти']]
    update.message.reply_text('Вас встретил посланец из банды и требует пойти с ним.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return X



def work(update, context):
    user = update.message.from_user
    if update.message.text == 'Усердно драить котёл':
        logger.info(f'{user.first_name} выбрал "Усердно драить котёл"')
        update.message.reply_text('Вы ободрали руки в кровь. Хорошо, что ничем не заразились.\n'
                                  ' (у вас отнимается одно хп)')
        user_game_info['hp'] -= 1
        if user_game_info['hp'] <= 0:
            reply_keyboard = [['Продолжить']]
            update.message.reply_text('Вы умерли и игра начнется заново.',
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            logger.info(f'{user.first_name} умер.')
            return A
    if update.message.text == 'Налить туда воды и молиться':
        update.message.reply_text('Вы налили воды в котёл. Но зачем?')
    reply_keyboard = [['Драить котёл', 'Попросить другую работу']]
    update.message.reply_text('Котёл всё ещё грязный.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return R


def cotel(update, context):
    user = update.message.from_user
    if update.message.text == 'Драить котёл':
        logger.info(f'{user.first_name} выбрал "Драить котёл"')
        reply_keyboard = [['Драить котёл', 'Попросить другую работу']]
        update.message.reply_text('Грязь стала отходить! Трактирщику понравился чистый котёл, он дал вам'
                                  'немного денег и вы ушли.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return W


def bandits_2(update, context):
        user = update.message.from_user
        if update.message.text == 'Отказаться':
            logger.info(f'{user.first_name} выбрал "Отказаться"')
            update.message.reply_text('На следующий день вас подстерегли бандиты и забрали всё, что у вас  было.'
                                      ' Бандиты не прощают измены. (у вас отнимается одно хп)')
            user_game_info['hp'] -= 1
            if user_game_info['hp'] <= 0:
                reply_keyboard = [['Продолжить']]
                update.message.reply_text('Вы умерли и игра начнется заново.',
                                          reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                logger.info(f'{user.first_name} умер.')
                return A
        if update.message.text == 'Идти':
            logger.info(f'{user.first_name} выбрал "Идти"')
            update.message.reply_text('Вы неохотно согласились пойти с бандитами.'
                                      'Они вывели вас в лес и обобрали до нитки.'
                                      'Теперь у вас ничего нет.')
        reply_keyboard = [['Просить милостыню', 'Шататься по деревне']]
        update.message.reply_text('Вы в отчаянии, хотите есть, и у вас нет денег.',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return Y


def milostynya(update, context):
    user = update.message.from_user
    if update.message.text == 'Просить милостыню':
        logger.info(f'{user.first_name} выбрал "Просить милостыню"')
        update.message.reply_text('Вокруг только бедные крестьяне. Ни у кого нет денег вам на пожертвования.')
    if update.message.text == 'Шататься по деревне':
        logger.info(f'{user.first_name} выбрал "Шататься по деревне"')
        update.message.reply_text('Ваш живот урчит на всю деревню.')
    reply_keyboard = [['Идти в кузню']]
    update.message.reply_text('Пока вы ходили по деревне вы услышали, что в кузне нужны рабочие.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Z


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} закончил беседу с ботом.")
    update.message.reply_text(
        'Пока! Надеюсь мы скоро встретимся.')

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
                H: [MessageHandler(Filters.text, igra_v_pryatki)],
                I: [MessageHandler(Filters.text, pole_2)],
                J: [MessageHandler(Filters.text, chel)],
                K: [MessageHandler(Filters.text, scotina)],
                L: [MessageHandler(Filters.text, batya_i_voyna)],
                M: [MessageHandler(Filters.text, traktir)],
                N: [MessageHandler(Filters.text, utopec)],
                O: [MessageHandler(Filters.text, v_traktire)],
                P: [MessageHandler(Filters.text, food_or_work)],
                Q: [MessageHandler(Filters.text, work)],
                R: [MessageHandler(Filters.text, cotel)],
                S: [MessageHandler(Filters.text, plata)],
                T: [MessageHandler(Filters.text, lydi)],
                U: [MessageHandler(Filters.text, urodivyi)],
                V: [MessageHandler(Filters.text, derevnya)],
                W: [MessageHandler(Filters.text, bandits)],
                X: [MessageHandler(Filters.text, bandits_2)],
                Y: [MessageHandler(Filters.text, milostynya)],
                Z: ["""Продолжение следует..."""],

                },
        fallbacks=[CommandHandler('cancel', cancel)]

    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
