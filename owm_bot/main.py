import telebot
import pymysql.cursors
from telebot import types
from telebot.types import Message
import pyowm
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import pytz
import schedule
import time
from threading import Thread

connection = pymysql.connect(host='localhost', user='root', password='root', db='bot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
key = '24518df4b64477c590040eb626472721'
owm = pyowm.OWM(key)
token = '729553874:AAHxh0x2whEFh69sMw5vqaRbC_hMe3GOlug'
bot = telebot.TeleBot(token)


def isUserDuplicate(userId):
    with connection.cursor() as cursor:
        sql = f"SELECT userId FROM main where userId = {userId}"
        cursor.execute(sql)
        counter = 0
        for row in cursor:
            counter += 1
        if counter == 0:
            return False
        else:
            return True


def arrayOfSubscriptions():
    with connection.cursor() as cursor:
        sql = f"SELECT userId FROM main where subscription is not null"
        cursor.execute(sql)
        users = []
        for row in cursor:
            users.append(row.get('userId'))
        return users


def isCityExist(city):
    try:
        owm.weather_at_place(city)
        return True
    except pyowm.exceptions.api_response_error.NotFoundError:
        return False
    except pyowm.exceptions.api_call_error.APICallError:
        return False
    except pyowm.exceptions.api_call_error.APIInvalidSSLCertificateError:
        return False


def getLanguage(userId):
    with connection.cursor() as cursor:
        sql = "SELECT language FROM main where userId = " + str(userId)
        cursor.execute(sql)
        oneRow = cursor.fetchone()
        language = oneRow['language']
    return language


def getCity(userId):
    with connection.cursor() as cursor:
        sql = "SELECT lastCity FROM main where userId = " + str(userId)
        cursor.execute(sql)
        oneRow = cursor.fetchone()
        city = oneRow['lastCity']
    return city


def updateLastCity(userId, city):
    cursor = connection.cursor()
    sql = f"Update main set lastCity = %s where userId = %s"
    cursor.execute(sql, (city, str(userId)))
    connection.commit()


def updateLanguage(userId, language):
    cursor = connection.cursor()
    sql = "Update main set language = %s where userId = %s"
    cursor.execute(sql, (language, str(userId)))
    connection.commit()


def addUser(userId, username, firstName, lastName):
    cursor = connection.cursor()
    sql = f"Insert into main values (%s, %s, %s, %s, 'eng', null, null, %s, %s)"
    cursor.execute(sql, (str(userId), username, firstName, lastName, str(datetime.now()), str(datetime.now())))
    connection.commit()


def updateLastTime(userId):
    cursor = connection.cursor()
    sql = f"Update main set lastActionTime = %s where userId = %s"
    cursor.execute(sql, (datetime.now(), str(userId)))
    connection.commit()


def subscription(userId, city):
    cursor = connection.cursor()
    sql = f"Update main set subscription = %s where userId = %s"
    cursor.execute(sql, (city, str(userId)))
    connection.commit()


def deleteSubscription(userId):
    cursor = connection.cursor()
    sql = f"Update main set subscription = null where userId = %s"
    cursor.execute(sql, (str(userId)))
    connection.commit()


def getSubscription(userId):
    with connection.cursor() as cursor:
        sql = "SELECT subscription FROM main where userId = " + str(userId)
        cursor.execute(sql)
        oneRow = cursor.fetchone()
        city = oneRow['subscription']
    return city


def subscriptionForecast(userId):
    city = getSubscription(userId)
    if getLanguage(userId) == 'ukr':
        f = f'Агов, ось твій прогноз на день в м. {city}😄\n'
    elif getLanguage(userId) == 'rus':
        f = f'Эй, лови свой прогноз на день в г. {city}😄\n'
    else:
        f = f'Hey, get your daily forecast in {city}😄\n'
    sticker = ''
    forecaster = owm.three_hours_forecast(getSubscription(userId))
    forecast = forecaster.get_forecast()
    weather_list = forecast.get_weathers()
    observation = owm.weather_at_place(getSubscription(userId))
    l = observation.get_location()
    tz = TimezoneFinder().timezone_at(lng=l.get_lon(), lat=l.get_lat())
    local = pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone(tz))
    loc = local.isoformat()
    diff = int(loc[26] + loc[27] + loc[28]) - 2
    for weather in weather_list:
        temp = round(weather.get_temperature('celsius')['temp'], 1)
        status = translateStatus(weather.get_status(), userId)[0]
        hours = (weather.get_reference_time('date') + timedelta(hours=diff)).hour
        if hours < 3 or 12 <= hours < 15:
            sticker = '🕛'
        elif 3 <= hours < 6 or 15 <= hours < 18:
            sticker = '🕒'
        elif 6 <= hours < 9 or 18 <= hours < 21:
            sticker = '🕕'
        elif 9 <= hours < 12 or hours >= 21:
            sticker = '🕘'
        if hours < 10:
            hours = '0' + str(hours)
        if (weather.get_reference_time('date') + timedelta(hours=diff)).day is (
                datetime.now() + timedelta(days=0, hours=diff)).day or \
                (weather.get_reference_time('date') + timedelta(hours=diff)).day is (
                datetime.now() + timedelta(days=1, hours=diff)).day and \
                (weather.get_reference_time('date') + timedelta(hours=diff)).hour is 0:
            f += sticker + " " + str(hours) + ":00 - " + str(temp) + "°C, " + status + "\n"
    return f


def dailyForecast(userId, days):
    day = int((datetime.now()+timedelta(days=days)).day)
    month = int((datetime.now()+timedelta(days=days)).month)
    if day < 10:
        day = f"0{day}"
    if month < 10:
        month = f"0{month}"
    if getLanguage(userId) == 'ukr':
        if days == 0:
            period = 'до кінця дня'
        elif days == 1:
            period = 'на завтра'
        else:
            period = f'на {day}.{month}'
        f = f'Прогноз погоди {period} у м. {getCity(userId)}:\n'
    elif getLanguage(userId) == 'rus':
        if days == 0:
            period = 'до конца дня'
        elif days == 1:
            period = 'на завтра'
        else:
            period = f'на {day}.{month}'
        f = f'Прогноз погоды {period} в г. {getCity(userId)}:\n'
    else:
        if days == 0:
            period = 'till the end of the day'
        elif days == 1:
            period = 'for tomorrow'
        else:
            period = f'for {day}.{month}'
        f = f'Weather forecast {period} in {getCity(userId)}:\n'
    sticker = ''
    forecaster = owm.three_hours_forecast(getCity(userId))
    forecast = forecaster.get_forecast()
    weather_list = forecast.get_weathers()
    observation = owm.weather_at_place(getCity(userId))
    l = observation.get_location()
    tz = TimezoneFinder().timezone_at(lng=l.get_lon(), lat=l.get_lat())
    local = pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone(tz))
    loc = local.isoformat()
    diff = int(loc[26] + loc[27] + loc[28]) - 2
    for weather in weather_list:
        temp = round(weather.get_temperature('celsius')['temp'], 1)
        status = translateStatus(weather.get_status(), userId)[0]
        hours = (weather.get_reference_time('date') + timedelta(hours=diff)).hour
        if hours < 3 or 12 <= hours < 15:
            sticker = '🕛'
        elif 3 <= hours < 6 or 15 <= hours < 18:
            sticker = '🕒'
        elif 6 <= hours < 9 or 18 <= hours < 21:
            sticker = '🕕'
        elif 9 <= hours < 12 or hours >= 21:
            sticker = '🕘'
        if hours < 10:
            hours = '0' + str(hours)
        if (weather.get_reference_time('date') + timedelta(hours=diff)).day is (
                datetime.now() + timedelta(days=days, hours=diff)).day or \
                (weather.get_reference_time('date') + timedelta(hours=diff)).day is (
                datetime.now() + timedelta(days=days+1, hours=diff)).day and \
                (weather.get_reference_time('date') + timedelta(hours=diff)).hour is 0:
            f += sticker + " " + str(hours) + ":00 - " + str(temp) + "°C, " + status + "\n"
    return f


def translateStatus(status, userId):
    st = ''
    img = 'https://cdn.pixabay.com/photo/2017/04/09/12/45/error-2215702_960_720.png'
    img_cloud = 'http://i.vikka.ua/1/80436/151238505520597800x500.jpg'
    img_mist = 'https://ukranews.com/upload/news/2019/10/26/5a6d7dd6abf2a-screenshot-1_410x272.png?v=1'
    img_clear = 'https://fabriory.com.ua/sites/default/files/styles/large/public/1-246.jpg?itok=SFcwHWN8'
    img_snow = 'https://media.dyvys.info/2017/11/1450381224_1-696x392.jpg'
    img_rain = 'http://www.poetryclub.com.ua/upload/poem_all/00805608.jpeg'
    img_haze = 'https://static.espreso.tv/uploads/article/816944/images/im610x343-02.jpg'
    img_drizzle = 'http://topnews.pl.ua/img/20191212/a9beb0c68ca2a2e48d4ba6963b6ac9db.jpg'
    img_thunder = 'https://i.ytimg.com/vi/SyPBZp98EkY/maxresdefault.jpg'
    if getLanguage(userId) == 'ukr':
        if status[0] == "M" or status[0] == "F":
            st = "туман"
            img = img_mist
        elif status[0] == "C" and status[1] == "l" and status[2] == "e":
            st = "чисте небо"
            img = img_clear
        elif status[0] == "C" and status[1] == "l" and status[2] == "o":
            st = "хмарно"
            img = img_cloud
        elif status[0] == "S":
            st = "сніг"
            img = img_snow
        elif status[0] == "R":
            st = "дощ"
            img = img_rain
        elif status[0] == "H":
            st = "імла"
            img = img_haze
        elif status[0] == "D":
            st = "мряка"
            img = img_drizzle
        elif status[0] == "T":
            st = 'гроза'
            img = img_thunder
    elif getLanguage(userId) == 'rus':
        if status[0] == "M" or status[0] == "F":
            st = "туман"
            img = img_mist
        elif status[0] == "C" and status[1] == "l" and status[2] == "e":
            st = "чистое небо"
            img = img_clear
        elif status[0] == "C" and status[1] == "l" and status[2] == "o":
            st = "облачно"
            img = img_cloud
        elif status[0] == "S":
            st = "снег"
            img = img_snow
        elif status[0] == "R":
            st = "дождь"
            img = img_rain
        elif status[0] == "H":
            st = "мгла"
            img = img_haze
        elif status[0] == "D":
            st = "морось"
            img = img_drizzle
        elif status[0] == "T":
            st = 'гроза'
            img = img_thunder
    else:
        st = status.lower()
        if status[0] == "M" or status[0] == "F":
            img = img_mist
        elif status[0] == "C" and status[1] == "l" and status[2] == "e":
            img = img_clear
        elif status[0] == "C" and status[1] == "l" and status[2] == "o":
            img = img_cloud
        elif status[0] == "S":
            img = img_snow
        elif status[0] == "R":
            img = img_rain
        elif status[0] == "H":
            img = img_haze
        elif status[0] == "D":
            img = img_drizzle
        elif status[0] == "T":
            img = img_thunder
    return st, img


def subscriptionMessage():
    counter = 0
    for i in arrayOfSubscriptions():
        msg = subscriptionForecast(arrayOfSubscriptions()[counter])
        bot.send_message(arrayOfSubscriptions()[counter], msg)
        counter += 1


def commandsList(userId):
    if getLanguage(userId) == 'ukr':
        msg = '/setlanguage - змінити мову, якою буде надаватися інформація\n' \
              '/subscription - підписатися на місто(прогноз на день буде автоматично розсилатися в 00:00 щодня)\n' \
              '/dropsubscription - скасувати підписку\n' \
              '/forecast - поточний стан та прогноз погоди у введеному вами місті\n' \
              '/help - список доступних команд'
    elif getLanguage(userId) == 'rus':
        msg = '/setlanguage - изменить язык, которым будет предоставляться информация\n' \
              '/subscription - подписаться на город(прогноз на день буде автоматически розсылаться в 00:00 каждый день)\n' \
              '/dropsubscription - отменить подписку\n' \
              '/forecast - текущее состояние и прогноз погоды в введенном вами городе\n' \
              '/help - список доступных команд'
    else:
        msg = '/setlanguage - change language in which the information will be provided\n' \
              '/subscription - subscribe to the city(daily forecast will be sent at 00:00 every day automatically)\n' \
              '/dropsubscription - cancel the subscription\n' \
              '/forecast - current weather conditions and forecast in the city you entered\n' \
              '/help - list of available commands'
    return msg


@bot.message_handler(commands=['start'])
def start(message: Message):
    if isUserDuplicate(message.from_user.id) == False:
        addUser(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        languageKeyboard = types.InlineKeyboardMarkup()
        ukr = types.InlineKeyboardButton(text="🇺🇦 УКРАЇНСЬКА 🇺🇦", callback_data="ukr")
        languageKeyboard.add(ukr)
        rus = types.InlineKeyboardButton(text="🇷🇺 РУССКИЙ 🇷🇺", callback_data="rus")
        languageKeyboard.add(rus)
        eng = types.InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥 ENGLISH 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="eng")
        languageKeyboard.add(eng)
        bot.send_message(message.from_user.id, 'Choose language:', reply_markup=languageKeyboard)
    else:
        updateLastTime(message.from_user.id)
        bot.send_message(message.from_user.id, commandsList(message.from_user.id))


@bot.message_handler(commands=['help'])
def help(message: Message):
    bot.send_message(message.from_user.id, commandsList(message.from_user.id))
    updateLastTime(message.from_user.id)



@bot.message_handler(commands=['setlanguage'])
def changeLanguage(message: Message):
    if getLanguage(message.from_user.id) == 'ukr':
        msg = 'Оберіть нову мову:'
    elif getLanguage(message.from_user.id) == 'rus':
        msg = 'Виберите новый язык'
    else:
        msg = 'Choose new language'
    languageKeyboard = types.InlineKeyboardMarkup()
    ukr = types.InlineKeyboardButton(text="🇺🇦 УКРАЇНСЬКА 🇺🇦", callback_data="ukr")
    languageKeyboard.add(ukr)
    rus = types.InlineKeyboardButton(text="🇷🇺 РУССКИЙ 🇷🇺", callback_data="rus")
    languageKeyboard.add(rus)
    eng = types.InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥 ENGLISH 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="eng")
    languageKeyboard.add(eng)
    bot.send_message(message.from_user.id, msg, reply_markup=languageKeyboard)
    updateLastTime(message.from_user.id)


@bot.message_handler(commands=['subscription'])
def createSubscription(message: Message):
    if getLanguage(message.from_user.id) == 'ukr':
        msg = 'Введіть назву міста, на яке ви хочете оформити підписку. Прогноз погоди на день буде вам автоматично приходити в 00:00.'
    elif getLanguage(message.from_user.id) == 'rus':
        msg = 'Введите название города, на которое вы хотите оформить подписку. Прогноз погоды на день будет автоматически приходить в 00:00.'
    else:
        msg = 'Enter the name of city you want to subscribe. Daily forecast will be automatically sent to you at 00:00.'
    bot.send_message(message.from_user.id, msg)
    updateLastTime(message.from_user.id)
    bot.register_next_step_handler(message, chooseCity)


def chooseCity(message: Message):
    city = message.text
    if isCityExist(city):
        subscription(message.from_user.id, city)
        if getLanguage(message.from_user.id) == 'ukr':
            msg = f"Підписка на місто {city} оформлена."
        elif getLanguage(message.from_user.id) == 'rus':
            msg = f"Подписка на город {city} оформлена."
        else:
            msg = f"Subscription on city {city} is created."
    else:
        if getLanguage(message.from_user.id) == 'ukr':
            msg = f"Міста {city} не існує."
        elif getLanguage(message.from_user.id) == 'rus':
            msg = f"Города {city} не существует."
        else:
            msg = f"City {city} is not exists."
    bot.send_message(message.from_user.id, msg)
    updateLastTime(message.from_user.id)


@bot.message_handler(commands=['dropsubscription'])
def createSubscription(message: Message):
    city = getSubscription(message.from_user.id)
    if city is not None:
        deleteSubscription(message.from_user.id)
        if getLanguage(message.from_user.id) == 'ukr':
            msg = f'Підписка на місто {city} видалена.'
        elif getLanguage(message.from_user.id) == 'rus':
            msg = f'Подписка на город {city} удалена.'
        else:
            msg = f'Subscription on city {city} is deleted.'
    else:
        if getLanguage(message.from_user.id) == 'ukr':
            msg = 'Підписка не оформлена!'
        elif getLanguage(message.from_user.id) == 'rus':
            msg = 'Подписка не оформлена!'
        else:
            msg = 'Subscription is not created!'
    bot.send_message(message.from_user.id, msg)
    updateLastTime(message.from_user.id)


@bot.callback_query_handler(func=lambda c: True)
def setLanguage(c):
    cid = c.message.chat.id
    if c.data == 'ukr':
        updateLanguage(cid, c.data)
        bot.send_message(cid, 'Чудово, уся інформація буде вам надаватися українською мовою.\n'
                              'Проте вводити українською можна лише назви українських міст. Для іноземних міст використовуйте російську або англійську мови.\n'
                              '/help - список доступних команд')
    elif c.data == 'rus':
        updateLanguage(cid, c.data)
        bot.send_message(cid, 'Прекрасно, вся информация будет вам предоставляться на русском языке.\n'
                              '/help - список доступных команд')
    elif c.data == 'eng':
        updateLanguage(cid, c.data)
        bot.send_message(cid, 'Nice, all information for you will be provided in English.\n'
                              '/help - list of available commands')
    elif c.data == 'today':
        bot.send_message(cid, dailyForecast(cid, 0), reply_markup=keyboard)
    elif c.data == 'tomorrow':
        bot.send_message(cid, dailyForecast(cid, 1), reply_markup=keyboard)
    elif c.data == '2days':
        bot.send_message(cid, dailyForecast(cid, 2), reply_markup=keyboard)
    elif c.data == '3days':
        bot.send_message(cid, dailyForecast(cid, 3), reply_markup=keyboard)
    elif c.data == '4days':
        bot.send_message(cid, dailyForecast(cid, 4), reply_markup=keyboard)
    updateLastTime(cid)


@bot.message_handler(commands=['forecast'])
def getForecast(message: Message):
    if getLanguage(message.from_user.id) == 'ukr':
        msg = 'Введіть назву міста.'
    elif getLanguage(message.from_user.id) == 'rus':
        msg = 'Введите название города.'
    else:
        msg = 'Enter the name of city.'
    bot.send_message(message.from_user.id, msg)
    updateLastTime(message.from_user.id)
    bot.register_next_step_handler(message, getCityForecast)


def getCityForecast(message: Message):
    city = message.text
    if isCityExist(city):
        updateLastCity(message.from_user.id, city)
        observation = owm.weather_at_place(getCity(message.from_user.id))
        w = observation.get_weather()
        l = observation.get_location()
        tz = TimezoneFinder().timezone_at(lng=l.get_lon(), lat=l.get_lat())
        local = pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone(tz))
        loc = local.isoformat()
        diff = int(loc[26] + loc[27] + loc[28]) - 2
        hours = local.hour
        if hours < 10:
            hours = f'0{hours}'
        mins = local.minute
        if mins < 10:
            mins = f'0{mins}'
        secs = local.second
        if secs < 10:
            secs = f'0{secs}'
        sunrise = w.get_sunrise_time('date') + timedelta(hours=diff)
        sr_hours = sunrise.hour
        if sr_hours < 10:
            sr_hours = f'0{sr_hours}'
        sr_mins = sunrise.minute
        if sr_mins < 10:
            sr_mins = f'0{sr_mins}'
        sr_secs = sunrise.second
        if sr_secs < 10:
            sr_secs = f'0{sr_secs}'
        sunset = w.get_sunset_time('date') + timedelta(hours=diff)
        ss_hours = sunset.hour
        if ss_hours < 10:
            ss_hours = '0' + f'0{ss_hours}'
        ss_mins = sunset.minute
        if ss_mins < 10:
            ss_mins = f'0{ss_mins}'
        ss_secs = sunset.second
        if ss_secs < 10:
            ss_secs = f'0{ss_secs}'
        temp = round(w.get_temperature('celsius')['temp'], 1)
        wind = w.get_wind()['speed']
        humidity = w.get_humidity()
        clouds = w.get_clouds()
        pressure = round(w.get_pressure()['press']/1.3333)
        local_time = f'{hours}:{mins}:{secs}'
        sunrise = f'{sr_hours}:{sr_mins}:{sr_secs}'
        sunset = f'{ss_hours}:{ss_mins}:{ss_secs}'
        status = w.get_status()
        if getLanguage(message.from_user.id) == 'ukr':
            answer = f'У м. {getCity(message.from_user.id)} {translateStatus(status, message.from_user.id)[0]}\n🌡️ Температура повітря: {temp}°C\n💨 Швидкість вітру: {wind} м/с\n💧 Вологість повітря: {humidity}' \
                     f'%\n🕰 Атмосферний тиск: {pressure} мм рт ст\n☁ Хмарність: {clouds}%\n🌞 Схід сонця: {sunrise}\n🌚 Захід сонця: {sunset}\n⌚ Місцевий час: {local_time}'
        elif getLanguage(message.from_user.id) == 'rus':
            answer = f'В г. {getCity(message.from_user.id)} {translateStatus(status, message.from_user.id)[0]}\n🌡️ Температура воздуха: {temp}°C\n💨 Скорость ветра: {wind}м/с\n💧 Влажность воздуха: {humidity}' \
                     f'%\n🕰 Атмосферное давление: {pressure} мм рт ст\n☁ Облачность: {clouds}%\n🌞 Восход солнца: {sunrise}\n🌚 Закат: {sunset}\n⌚ Местное время: {local_time}'
        else:
            answer = f"There's {translateStatus(status, message.from_user.id)[0]} in {getCity(message.from_user.id)} \n🌡️ Air temperature: {temp}°C\n💨 Wind speed: {wind}m/s\n💧 Air humidity: {humidity}" \
                     f"%\n🕰 Atmospheric pressure: {pressure} mmhg\n☁ Clouds: {clouds}%\n🌞 Sunrise: {sunrise}\n🌚 Sunset: {sunset}\n⌚ Local time: {local_time}"
        dd2 = (datetime.now() + timedelta(days=2, hours=diff)).day
        if dd2 < 10:
            dd2 = '0' + str(dd2)
        dm2 = (datetime.now() + timedelta(days=2, hours=diff)).month
        if dm2 < 10:
            dm2 = '0' + str(dm2)
        dd3 = (datetime.now() + timedelta(days=3, hours=diff)).day
        if dd3 < 10:
            dd3 = '0' + str(dd3)
        dm3 = (datetime.now() + timedelta(days=3, hours=diff)).month
        if dm3 < 10:
            dm3 = '0' + str(dm3)
        dd4 = (datetime.now() + timedelta(days=4, hours=diff)).day
        if dd4 < 10:
            dd4 = '0' + str(dd4)
        dm4 = (datetime.now() + timedelta(days=4, hours=diff)).month
        if dm4 < 10:
            dm4 = '0' + str(dm4)
        global keyboard
        keyboard = types.InlineKeyboardMarkup()
        kb1 = types.InlineKeyboardButton(text=f"❌Прогноз до кінця дня у м. {getCity(message.from_user.id)}❌", callback_data="today")
        kb2 = types.InlineKeyboardButton(text=f"❌Прогноз на завтра у м. {getCity(message.from_user.id)}❌", callback_data="tomorrow")
        kb3 = types.InlineKeyboardButton(text=f"❌Прогноз на {dd2}.{dm2}" + f" у м. {getCity(message.from_user.id)}❌", callback_data="2days")
        kb4 = types.InlineKeyboardButton(text=f"❌Прогноз на {dd3}.{dm3}" + f" у м. {getCity(message.from_user.id)}❌", callback_data="3days")
        kb5 = types.InlineKeyboardButton(text=f"❌Прогноз на {dd4}.{dm4}" + f" у м. {getCity(message.from_user.id)}❌", callback_data="4days")
        keyboard.add(kb1)
        keyboard.add(kb2)
        keyboard.add(kb3)
        keyboard.add(kb4)
        keyboard.add(kb5)
        bot.send_photo(message.from_user.id, translateStatus(status, message.from_user.id)[1], caption=answer, reply_markup=keyboard)
    else:
        if getLanguage(message.from_user.id) == 'ukr':
            bot.send_message(message.from_user.id, "Такого міста не існує!")
        elif getLanguage(message.from_user.id) == 'rus':
            bot.send_message(message.from_user.id, "Такого города не существует!")
        else:
            bot.send_message(message.from_user.id, "There isn't such city")


@bot.message_handler(content_types=['text'])
def echo_msg(message: Message):
    if getLanguage(message.from_user.id) == 'ukr':
        msg = 'Спробуйте одну з команд нижче:\n'
    elif getLanguage(message.from_user.id) == 'rus':
        msg = 'Попробуйте одну из команд ниже:\n'
    else:
        msg = 'Try one of the commands from below\n'
    msg = msg + commandsList(message.from_user.id)
    updateLastTime(message.from_user.id)
    bot.send_message(message.chat.id, msg)


def do_schedule():
    schedule.every().day.at('15:25').do(subscriptionMessage)
    while True:
        schedule.run_pending()
        time.sleep(1)


def main_loop():
    thread = Thread(target=do_schedule)
    thread.start()
    bot.polling(none_stop=True, interval=1)


while True:
    try:
        print("Bot running..")
        main_loop()
        break
    except (pymysql.err.OperationalError, pymysql.err.InterfaceError, RuntimeError, telebot.apihelper.ApiException) as e:
        print('Error is catched!')
        print(e)
        bot.stop_polling()
        time.sleep(15)
        print("Running again!")