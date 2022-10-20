#!/usr/bin/python3
import time
import turtle
import math
import requests
import json
import logging
import sys
import os
import locale
import getopt
from datetime import datetime, timedelta
try:
    from pynput.keyboard import Key
    from pynput.keyboard import Controller as KController
    #from pynput.mouse import Button # not used
    from pynput.mouse import Controller as MController
except ImportError:
    print("Install python 'pynput' module")
import gettext
#from gettext import gettext
#from gettext import dgettext #Can't use because it don't generate lose error.pot/ logging.pot files
# set current language default to english USA
lang_translations = gettext.translation('messages', localedir='locales', languages=['en_US'])
lang_translations.install()
# define _() shortcut for translations
_ = lang_translations.gettext
#_d = dgettext

keyboard = KController()
mouse = MController()

# move the mouse in the topleft corner - it look better than it would be "in front of"
mouse.position = (0, 0)

path = os.path.dirname(os.path.realpath(__file__))

print(_("Starting WeatherClock..."))
#region Get command parameters and initialize tags
try:
    options, remaining = getopt.getopt(sys.argv[1:], 'a:l:h', [
        "apikey=", "loglevel=", "latitude=", "longitude=", "help"])
    if remaining:
        print(_("Remaining arguments will not be used: {0}").format(remaining))
    if options:
        print(_("Options: {0}").format(options))
    api_key = None
    theme = "default"
    language = "en_US"
    log_level = None
    latitude = None
    longitude = None
    units = "metric"
    temperature_values = False 
    wind_values = False
    use_hour24 = False
    values_color = "gray"
    global_x_shift = 0
    global_y_shift = 0
    weather_text_description = -30
    weather_text_data = 30
    weather_text_vert_spacing = 40
    weather_text_color = "white"
    temperature_text_vert_spacing = -9
    temperature_text_horz_spacing = 11
    temperature_text_font_size = 11
    weather_text_description_font_size = 20
    weather_text_data_font_size = 19
    hourly_touch_size = 50
    radius = 265
    wn_title = _("WeatherClock") + "\n0.0.0"
    divider_start = -125
    divider_end = 275
    hour_hand = 100
    hour_hand_color = "white"
    minute_hand = 170
    minute_hand_color = "yellow"
    second_hand = 75
    second_hand_color = "gray"
    wind_text_left_shift = 50
    wind_text_right_shift = 65
    wind_text_no_measure_text = False
    
    for opt, arg in options:
        if opt in ['-a', '--apikey']:
            api_key = arg
        elif opt in ['-l', '--loglevel']:
            log_level = arg
        elif opt in ['-n', '--latitude']:
            latitude = arg
        elif opt in ['-s', '--longitude']:
            longitude = arg
        elif opt in ['-u', '--units']:
            if arg.lower() in ['metric', 'imperial']:
                units = arg
            else:
                #raise ValueError('[-u|--units] ' + _d('error', 'must be one of:') + "metric, imperial")
                raise ValueError('[-u|--units] ' + _("must be one of:") + "metric, imperial")
        elif opt in ['-h', '--help']:
            #logging.error(_d("logging",'usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]'))
            logging.error(_('usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]'))
            #print(_d("logging",'usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]'))
            print(_('usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]'))
            exit(0)
        else:
            print(f"Parameter unused: {opt}={arg}")
except getopt.GetoptError:
    #print(_d("logging",'usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]'))
    print(_('usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]'))
    #raise ValueError(_d("error","Missing one or more parameters."))
    raise ValueError(_("Missing one or more parameters."))
#endregion

#region Get settings parameters
try:
    with open('settings.json', 'r') as settings_json:
        settings = json.loads(settings_json.read())
        if not api_key:
            api_key_setting = settings.get('ApiKey')
            api_key = api_key_setting if api_key_setting else False
        theme = settings.get('Theme')    
        if not log_level:
            log_level = settings.get('LogLevel')
        if not latitude:
            latitude = settings.get('Latitude')
        if not longitude:
            longitude = settings.get('Longitude')
        if not units:
            units = settings.get('Units')
        if not temperature_values:
            temperature_values = settings.get('TemperatureValues').lower() in ['1', 'true', 'on']
        if not wind_values:
            wind_values = settings.get('WindValues').lower() in ['1', 'true', 'on']
        if not use_hour24:
            use_hour24 = settings.get('UseHour24').lower() in ['1', 'true', 'on']
        language = settings.get('Language')
        values_color = settings.get('ValuesColor')
        global_x_shift = int(settings.get('GlobalXShift'))
        global_y_shift = int(settings.get('GlobalYShift'))
        weather_text_description = int(settings.get('WeatherTextDescription'))
        weather_text_data = int(settings.get('WeatherTextData'))
        weather_text_vert_spacing = int(settings.get('WeatherTextVertSpacing'))
        weather_text_color = settings.get('WeatherTextColor')
        temperature_text_vert_spacing = int(settings.get('TemperatureTextVertSpacing'))
        temperature_text_horz_spacing = int(settings.get('TemperatureTextHorzSpacing'))
        temperature_text_font_size = int(settings.get('TemperatureTextFontSize'))
        weather_text_description_font_size = int(settings.get('WeatherTextDataFontSize'))
        weather_text_data_font_size = int(settings.get('WeatherTextDataFontSize'))
        # determines radius for user touch when going into hourly detail mode
        hourly_touch_size = int(settings.get('HourlyTouchSize'))
        # determines how big clock is
        radius = int(settings.get('Radius'))
        wn_title += settings.get('Title')
        divider_start = int(settings.get('DividerStart'))
        divider_end = int(settings.get('DividerEnd'))
        hour_hand = int(settings.get('HourHand'))
        hour_color = settings.get('HourColor')
        minute_hand = int(settings.get('MinuteHand'))
        minute_color = settings.get('MinuteColor')
        second_hand = int(settings.get('SecondHand'))
        second_color = settings.get('SecondColor')
        wind_text_left_shift = int(settings.get('WindTextLeftShift'))
        wind_text_right_shift = int(settings.get('WindTextRightShift'))
        wind_text_no_measure_text = settings.get('WindTextNoMeasureText').lower() in ['1', 'true', 'on']
        
except FileNotFoundError:
    #print(_d("error","'settings.json' file not found. Using command line parameters."))
    print(_("'settings.json' file not found. Using command line parameters."))
#endregion

if not api_key:
    #raise ValueError(_d("error","No ApiKey given. Use ApiKey in settings.json or use parameter: [-a|--apikey]."))
    raise ValueError(_("No ApiKey given. Use ApiKey in settings.json or use parameter: [-a|--apikey]."))

if log_level.lower() == 'debug':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
elif log_level.lower()[:4] == 'info': #'info' or 'information'
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
elif log_level.lower()[:4] == 'warn': #'warn' or 'warning'
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
elif log_level.lower() == 'error':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)
else:
    #logging.error(_d("logging","Log Level set to invalid value: {0}").format(log_level))
    logging.error(_("Log Level set to invalid value: {0}").format(log_level))
    #raise ValueError(_d("error","LogLevel (--loglevel) must be one of: ") + "[Debug|Info|Information|Warn|Warning|Error]")
    raise ValueError("LogLevel (--loglevel) " + _("must be one of:") + " [Debug|Info|Information|Warn|Warning|Error]")

#region Change language
language_list = ['en_US','en_GB','nl_NL','de_DE']
for l in language_list:
    if l.lower() == language.lower():
        # Change i18n translation language
        logging.info(_("Language changed to {0}").format(l))
        lang_translations = gettext.translation('messages', localedir='locales', languages=[l])
        lang_translations.install()
        _ = lang_translations.gettext
        logging.info(_("Language changed to {0}").format(l))
        
        # Get current language
        ext = "UTF-8"
        lang, enc = locale.getlocale()
        if lang == None:
            lang, enc = locale.getdefaultlocale()
        lang = lang or 'en_US'
        enc = enc or ext
        lang_now = locale.normalize(".".join((lang, enc)))
        
        # Try to set system settings to new language
        lang_new = locale.normalize(".".join((l, ext)))
        if lang_new != lang_now:
            try:
                #locale.setlocale(locale.LC_ALL, '')
                locale.setlocale(locale.LC_ALL, locale.normalize(".".join((l, ext))))
            except locale.Error:
                logging.error(_("Failed to change system language."))
                logging.error(_("Make sure locale '" + str(l) + ".UTF8' is generated on your system" ))
                locale.setlocale(locale.LC_ALL, None)
                continue
        break #exit for loop
del language_list, lang, enc, ext, lang_now, lang_new
#endregion

url_params = f'lat={latitude}&lon={longitude}&exclude=current,minutely,daily,alerts,flags&appid={api_key}'
if units:
    url_params += f"&units={units}"
else:
    logging.info("Units not set. OpenWeatherMap.org defaults to 'standard'.")
url = f'http://api.openweathermap.org/data/2.5/onecall?{url_params}'

ini_done = False
weatherUpdatePeriod = 10
current_hour12 = 0
current_hour24 = 0
current_meridiem = ""
tomorrow_date = datetime.today() + timedelta(days=1)

temp_array = [0] * 12
temp_feel_array = [0] * 12
wind_array = [0] * 12
temp_array_was = [0] * 12
temp_feel_array_was = [0] * 12
wind_array_was = [0] * 12
id_array = [0] * 12
idImage_array = [""] * 12
idImage_array_was = [""] * 12

res = requests.get(url)
if res.ok:
    data = res.json()
else:
    data = None
    res.raise_for_status()

logging.debug(data)

cursor_x = -1
cursor_y = -1

weatherText = turtle.Turtle()
weatherText.hideturtle()

weatherDividerPen = turtle.Turtle()
weatherDividerPen.hideturtle()

degree_sign = u" \N{DEGREE SIGN}"
if units.lower() == "imperial":
    degree_sign += "F"  #Fahrenheit
elif units.lower() == "metric":
    degree_sign += "C"  #Celsius
else:
    degree_sign += "K"  #Kelvin

# 1 - hourly detail mode, 0 - analog clock face mode
mode = 0

hour_x = []
hour_y = []

for i in range(60, -300, -30):
    i_r = math.radians(i)
    hour_x.append((math.cos(i_r)*radius))
    hour_y.append((math.sin(i_r)*radius))

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def touch_in_box(touch_x, touch_y, center_x, center_y, size_x, size_y):
    if center_x - size_x/2 < touch_x < center_x + size_x/2 and center_y + size_y/2 > touch_y > center_y - size_y/2:
        return True
    else:
        return False


def get_mouse_click_coordinate(x, y):

    # when this event is triggered, it means someone pressed the screen, therefore we should check what state we are
    # going into (clock mode, or hourly detail mode)

    global cursor_x
    global cursor_y
    # 0 = clock, 1 = hourly detail
    global mode
 
    cursor_x = x
    cursor_y = y
    #logging.debug(_d("logging","cursor pressed: x, y"))
    logging.debug(_("cursor pressed: x, y"))
    logging.debug(f'{cursor_x}, {cursor_y}')

    hour_touched = -1
    #determines which hour was touched
    for i in range(0, 12):
        if touch_in_box(cursor_x, cursor_y, hour_x[i], hour_y[i], hourly_touch_size, hourly_touch_size):
            hour_touched = i + 1
            break
    if hour_touched >= 0:
        #logging.debug(_d("logging","hour {0} WAS TOUCHED !").format(str(hour_touched)))
        logging.debug(_("hour {0} WAS TOUCHED !").format(str(hour_touched)))
        
        tomorrow = False
        touched_meridiem = current_meridiem
        if hour_touched < current_hour12 and not current_hour12 == 12:
            hours_ahead = 12-current_hour12+hour_touched
        else:
            if current_hour12 == 12 and not hour_touched == 12:
                hours_ahead = hour_touched
            else:
                hours_ahead = hour_touched - current_hour12
        if hours_ahead >= 0:
            #logging.info(_d("logging","Touched hour is {0} hours ahead").format(str(hours_ahead)))
            logging.info(_("Touched hour is {0} hours ahead").format(str(hours_ahead)))
            touched_meridiem = (datetime.today() + timedelta(hours=hours_ahead)).strftime("%p")
            if current_meridiem == "PM" and touched_meridiem == "AM":
                tomorrow = True

    # goto right mode (detail or not)
    if hour_touched != -1:
        if mode == 1:
            weatherText.clear()  # remove hourly details from screen
            weatherDividerPen.clear()
        else:
            pen.clear() # remove the clock hands from showing
        # go to hourly detail mode
        mode = 1

        # without this there is some weird line
        weatherText.penup()
        weatherText.color(weather_text_color)

        # day of the week
        weatherText.goto(weather_text_description + global_x_shift, weather_text_vert_spacing * 3 + global_y_shift)
        weatherText.write(_("Day"), align="right", font=("Verdana", weather_text_description_font_size, "bold"))

        weatherText.goto(weather_text_data + global_x_shift, weather_text_vert_spacing * 3 + global_y_shift)
        if not tomorrow:
            weatherText.write(datetime.today().strftime('%A'),
                              align="left", font=("Verdana", weather_text_data_font_size, "bold"))
        else:
            weatherText.write(tomorrow_date.strftime('%A'),
                              align="left", font=("Verdana", weather_text_data_font_size, "bold"))

        # hour of the day
        weatherText.goto(weather_text_description + global_x_shift, weather_text_vert_spacing * 2 + global_y_shift)
        weatherText.write(_("Hour"), align="right", font=("Verdana", weather_text_description_font_size, "bold"))

        weatherText.goto(weather_text_data + global_x_shift, weather_text_vert_spacing * 2 + global_y_shift)
        if use_hour24:
                                                     
            if current_hour24 + hours_ahead > 23:
                if hour_touched == 12:
                    weatherText.write("0",
                                    align="left", font=("Verdana", weather_text_data_font_size, "bold"))
                else:
                    weatherText.write(str(hour_touched),
                                    align="left", font=("Verdana", weather_text_data_font_size, "bold"))
            else:
                weatherText.write(str(current_hour24 + hours_ahead),
                                align="left", font=("Verdana", weather_text_data_font_size, "bold"))
        else:
            weatherText.write(str(hour_touched) + " " + touched_meridiem,
                          align="left", font=("Verdana", weather_text_data_font_size, "bold"))

        # temperature
        weatherText.goto(weather_text_description + global_x_shift, weather_text_vert_spacing + global_y_shift)
        weatherText.write(_("Temp"), align="right", font=("Verdana", weather_text_description_font_size, "bold"))

        weatherText.goto(weather_text_data + global_x_shift, weather_text_vert_spacing + global_y_shift)
        weatherText.write(str(round_half_up(data["hourly"][hours_ahead]["temp"], 1)) + degree_sign,
                          align="left", font=("Verdana", weather_text_data_font_size, "bold"))

        # Feels like
        weatherText.goto(weather_text_description + global_x_shift, global_y_shift)
        weatherText.write(_("Feels like"), align="right",
                          font=("Verdana", weather_text_description_font_size, "bold"))

        weatherText.goto(weather_text_data + global_x_shift, global_y_shift)
        weatherText.write(str(round_half_up(data["hourly"][hours_ahead]["feels_like"], 1)) + degree_sign,
                          align="left", font=("Verdana", weather_text_data_font_size, "bold"))

        # POP - Probability of precipitation
        weatherText.goto(weather_text_description + global_x_shift, -weather_text_vert_spacing + global_y_shift)
        weatherText.write(_("POP"), align="right", font=("Verdana", weather_text_description_font_size, "bold"))

        weatherText.goto(weather_text_data + global_x_shift, -weather_text_vert_spacing + global_y_shift)
        weatherText.write(str(int(data["hourly"][hours_ahead]["pop"]*100)) + " %",
                          align="left", font=("Verdana", weather_text_data_font_size, "bold"))

        # Rain
        weatherText.goto(weather_text_description + global_x_shift, -weather_text_vert_spacing * 2 + global_y_shift)
        weatherText.write(_("Rain"), align="right", font=("Verdana", weather_text_description_font_size, "bold"))

        weatherText.goto(weather_text_data + global_x_shift, -weather_text_vert_spacing * 2 + global_y_shift)
        if 'rain' not in data["hourly"][hours_ahead]:
            weatherText.write("--", align="left", font=("Verdana", weather_text_data_font_size, "bold"))
        else:
            weatherText.write(str(data["hourly"][hours_ahead]["rain"]["1h"]) + " mm",
                              align="left", font=("Verdana", weather_text_data_font_size, "bold"))

        # Wind
        weatherText.goto(weather_text_description + global_x_shift, -weather_text_vert_spacing * 3 + global_y_shift)
        weatherText.write(_("Wind"), align="right", font=("Verdana", weather_text_description_font_size, "bold"))

        weatherText.goto(weather_text_data + global_x_shift, -weather_text_vert_spacing * 3 + global_y_shift)
        weatherText.write(str(data["hourly"][hours_ahead]["wind_speed"]) + " km/h",
                          align="left", font=("Verdana", weather_text_data_font_size, "bold"))

        weatherText.hideturtle()

        weatherDividerPen.pensize(3)

        weatherDividerPen.penup()
        weatherDividerPen.goto(global_x_shift, divider_start + global_y_shift)
        weatherDividerPen.color("white")
        weatherDividerPen.setheading(90)
        weatherDividerPen.pendown()
        weatherDividerPen.fd(divider_end)
        weatherDividerPen.hideturtle()

    elif mode == 1 and touch_in_box(cursor_x, cursor_y, 0, 0, 200, 200):
        mode = 0  # go back to clock mode
        weatherText.clear()  # remove hourly details from screen
        weatherDividerPen.clear()

    cursor_x = -1
    cursor_y = -1


def update_forecast():

    # weather ID breakdown https://openweathermap.org/weather-conditions
    # use https://ezgif.com/maker for gif conversion

    logging.debug("---- update_forecast() ----")

    for num in range(12):
 
        if use_hour24:
            #logging.debug(_d("logging","current hour: ") + str(current_hour24)) # current hour 24
            logging.debug(_("current hour: ") + str(current_hour24)) # current hour 24
            if current_hour24 + num < 24:
                #logging.debug(_d("logging","forecast hour: ") + str(current_hour24+num)) # forecast hour 24
                logging.debug(_("forecast hour: ") + str(current_hour24+num)) # forecast hour 24
            else:
                #logging.debug(_d("logging","forecast hour: ") + str(current_hour24+num-24)) # forecast hour 24
                logging.debug(_("forecast hour: ") + str(current_hour24+num-24)) # forecast hour 24
        else:
            #logging.debug(_d("logging","current hour: ") + str(current_hour12) + " " + current_meridiem)
            logging.debug(_("current hour: ") + str(current_hour12) + " " + current_meridiem)
            #logging.debug(_d("logging","forecast hour: ") + str(int(current_hour12)+num))
            logging.debug(_("forecast hour: ") + str(int(current_hour12)+num))

        #logging.debug(_d("logging","temperature: ") + str(data["hourly"][num]["temp"]))
        logging.debug(_("temperature: ") + str(data["hourly"][num]["temp"]))
        #logging.debug(_d("logging","feels like: ") + str(data["hourly"][num]["feels_like"]))
        logging.debug(_("feels like: ") + str(data["hourly"][num]["feels_like"]))
        #logging.debug(_d("logging","wind speed: ") + str(data["hourly"][num]["wind_speed"]))
        logging.debug(_("wind speed: ") + str(data["hourly"][num]["wind_speed"]))
        logging.debug(data["hourly"][num]["weather"][0]["description"])
        #logging.debug(_d("logging","weather ID: ") + str(data["hourly"][num]["weather"][0]["id"]))
        logging.debug(_("weather ID: ") + str(data["hourly"][num]["weather"][0]["id"]))
        #logging.debug(_d("logging","POP: ") + str(data["hourly"][num]["pop"]))
        logging.debug(_("POP: ") + str(data["hourly"][num]["pop"]))

        if 'rain' not in data["hourly"][num]: #check rain
            #logging.debug(_d("logging","no rain data"))
            logging.debug(_("no rain data"))
        else:
            #logging.debug(_d("logging","Rain: ") + str(data["hourly"][num]["rain"]))
            logging.debug(_("Rain: ") + str(data["hourly"][num]["rain"]))

        temp_array[num] = data["hourly"][num]["temp"]
        temp_feel_array[num] = data["hourly"][num]["feels_like"]
        wind_array[num] = data["hourly"][num]["wind_speed"]      
        id_array[num] = data["hourly"][num]["weather"][0]["id"]

        path_theme = os.path.join(path, theme)

        if   200 <= id_array[num] <= 232:
            idImage_array[num] = os.path.join(path_theme, "11d@2x.gif")
        elif 300 <= id_array[num] <= 321:
            idImage_array[num] = os.path.join(path_theme, "09d@2x.gif")
        elif 500 <= id_array[num] <= 504:
            idImage_array[num] = os.path.join(path_theme, "10d@2x.gif")
        elif id_array[num] == 511:
            idImage_array[num] = os.path.join(path_theme, "13d@2x.gif")
        elif 520 <= id_array[num] <= 531:
            idImage_array[num] = os.path.join(path_theme, "09d@2x.gif")
        elif 600 <= id_array[num] <= 622:
            idImage_array[num] = os.path.join(path_theme, "13d@2x.gif")
        elif 701 <= id_array[num] <= 781:
            idImage_array[num] = os.path.join(path_theme, "50d@2x.gif")
        elif id_array[num] == 800:
            idImage_array[num] = os.path.join(path_theme, "01d@2x.gif")
        elif id_array[num] == 801:
            idImage_array[num] = os.path.join(path_theme, "02d@2x.gif")
        elif id_array[num] == 802:
            idImage_array[num] = os.path.join(path_theme, "03d@2x.gif")
        elif 803 <= id_array[num] <= 804:
            idImage_array[num] = os.path.join(path_theme, "04d@2x.gif")
        else:
            #logging.error(_d("error","Invalid weather ID"))
            logging.error(_("Invalid weather ID"))

    logging.debug(temp_array)
    logging.debug(id_array)
    logging.debug(idImage_array)

    for image in idImage_array:
        wn.addshape(image)


wn = turtle.Screen()
wn.bgcolor("black")
wn.screensize()
#wn.setup(width=600, height=600)
# Make full screen
wn.setup(width=1.0, height=1.0)
wn.title(wn_title)
# turns off the animation, so you can't see anything when it is drawing
wn.tracer(0)

# create our drawing pen
pen = turtle.Turtle()
pen.hideturtle()
# 0 is fastest it can go
pen.speed(0)
pen.pensize(3)

bg_hour = []
bg_hourtext = []
bg_windtext = []

for i in range(0, 12):
    bg_hour_i = turtle.Turtle()
    bg_hour_i.goto(hour_x[i] + global_x_shift, hour_y[i] + global_y_shift)
    bg_hour.append(bg_hour_i)

    bg_hourtext_i = turtle.Turtle()
    bg_hourtext_i.color(values_color)
    bg_hourtext_i.hideturtle()
    bg_hourtext.append(bg_hourtext_i)

    bg_windtext_i = turtle.Turtle()
    bg_windtext_i.color(values_color)
    bg_windtext_i.hideturtle()
    bg_windtext.append(bg_windtext_i)

s = 0
# time.sleep(10)


# draw a clock using the pen i created
def draw_clock(hour, minute, second, pen):
    pen.hideturtle()

    # Draw the hour hand
    pen.penup()
    pen.goto(global_x_shift, global_y_shift)
    pen.color(hour_color)
    pen.pensize(6)
    pen.setheading(90)
    angle = (hour / 12) * 360 + (minute/60) * 30
    pen.rt(angle)
    pen.pendown()
    pen.fd(hour_hand)

    # Draw the minute hand
    pen.penup()
    pen.goto(global_x_shift, global_y_shift)
    pen.color(minute_color)
    pen.setheading(90)
    angle = (minute / 60.0) * 360  # optional + (s/60) * 6
    pen.rt(angle)
    pen.pendown()
    pen.fd(minute_hand)

    # Draw the second hand
    pen.penup()
    pen.goto(global_x_shift, global_y_shift)
    pen.color(second_color)
    pen.setheading(90)
    angle = (second / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(second_hand)
    
    return pen

# makes the program fullscreen when you launch it
keyboard.press(Key.alt)
keyboard.press(Key.f11)
time.sleep(0.05)
keyboard.release(Key.f11)
keyboard.release(Key.alt)
time.sleep(1)   

canvas = wn.getcanvas()
top_window = canvas.winfo_toplevel()
running = True
# wn.onkeypress(fun=exit(), key='q')


def on_close():
    global running
    running = False


top_window.protocol("WM_DELETE_WINDOW", on_close)
top_window.overrideredirect(True)
wn.listen()

#def main():
while running:
    try:
        if ini_done == False:
            #logging.debug(_d("logging","\n... Main Loop Start ...\n"))
            logging.debug(_("\n... Main Loop Start ...\n"))

        s = int(time.strftime("%S"))
        if s == 0 or ini_done == False:
            m = int(time.strftime("%M"))
        if m == 0 or ini_done == False:
            current_hour12 = int(time.strftime("%I"))
            current_hour24 = int(time.strftime("%H"))
            current_meridiem = time.strftime('%p')
            h = current_hour12
            tomorrow_date = datetime.today() + timedelta(days=1)

        if use_hour24:
            logging.debug(f"{str(current_hour24)}:{str(m)}:{str(s)}")
        else:
            logging.debug(f"{str(current_hour12)}:{str(m)}:{str(s)} " + current_meridiem)

        # every x minutes, fetch new weather data
        if (m % weatherUpdatePeriod == 0 and s == 0) or ini_done == False:
            res = requests.get(url)
            data = res.json()
            #logging.debug(_d("logging","** FETCHED NEW DATA **"))
            logging.debug(_("** FETCHED NEW DATA **"))
            update_forecast()

        if mode == 0: #clock
            pen = draw_clock(h, m, s, pen)

            logging.debug(f"current_hour12: {current_hour12}")
            
            for i in range(1, 13):
                if (i - current_hour12 < 0):
                    j = 12 - abs(i - current_hour12)
                else:
                    j = i - current_hour12
                if(idImage_array[j] != idImage_array_was[j]):
                    bg_hour[i-1].shape(idImage_array[j])
                    idImage_array_was[j] = idImage_array[j]
                    
                if ((temp_array[j] != temp_array_was[j]) or (temp_feel_array[j] != temp_feel_array_was[j]) or
                        (wind_array[j] != wind_array_was[j])):
                    if (temperature_values):
                        bg_hourtext[i-1].clear()
                        bg_hourtext[i-1].penup()
                        x_shift = 0
                        y_shift = 0
                        if (("04d@2x.gif" in idImage_array[j]) or ("02d@2x.gif" in idImage_array[j])):
                            x_shift = -7
                            y_shift = -8
                        if ("11d@2x.gif" in idImage_array[j]):
                            x_shift = -9
                            y_shift = 3
                        if (("09d@2x.gif" in idImage_array[j]) or  ("10d@2x.gif" in idImage_array[j])):
                            x_shift = -6
                            y_shift = 3
                        if ("03d@2x.gif" in idImage_array[j]):
                            x_shift = -3
                            y_shift = -5
                        if (temp_array[j] < 10):
                            x_shift = x_shift + 4
                        bg_hourtext[i-1].goto(hour_x[i-1] + temperature_text_horz_spacing + x_shift - 20 + global_x_shift, hour_y[i-1] + temperature_text_vert_spacing + y_shift + global_y_shift)
                        v = int(round(temp_array[j]))
                        v2 = int(round(temp_feel_array[j]))
                        bg_hourtext[i-1].write(str(round(temp_array[j])), align="left", font=("Verdana", temperature_text_font_size, "bold"))
                    if (wind_values):   
                        bg_windtext[i-1].clear()
                        bg_windtext[i-1].penup()
                        kmh = " km/h"
                        if (wind_text_no_measure_text):
                            kmh = ""
                        if (i in range(1,6)):
                            bg_windtext[i-1].goto(hour_x[i-1] + temperature_text_horz_spacing +  x_shift + wind_text_right_shift + global_x_shift, hour_y[i-1] + temperature_text_vert_spacing + y_shift + global_y_shift)
                            bg_windtext[i-1].write(str(wind_array[j]) + kmh, align="left", font=("Verdana", temperature_text_font_size, ""))
                        if (i in range(7,12)):
                            bg_windtext[i-1].goto(hour_x[i-1] + temperature_text_horz_spacing +  x_shift - wind_text_left_shift + global_x_shift, hour_y[i-1] + temperature_text_vert_spacing + y_shift + global_y_shift)
                            bg_windtext[i-1].write(str(wind_array[j]) + kmh, align="right", font=("Verdana", temperature_text_font_size, ""))
                temp_array_was[j] = temp_array[j]
                temp_feel_array_was[j] = temp_feel_array[j]
                wind_array_was[j] = wind_array[j]                    

        wn.update()

        # cursor / touch logic
        # this returns the coordinate of the press !
        turtle.onscreenclick(get_mouse_click_coordinate)
        #logging.debug(_d("logging","MODE: ") + str(mode))
        logging.debug(_("MODE: ") + str(mode))
        logging.debug("cursor_x: " + str(cursor_x) + "; cursor_y: " + str(cursor_y))

        if cursor_x != -1 and cursor_y != -1:
            #logging.debug(_d("logging","screen was touched"))
            logging.debug(_("screen was touched"))

        ini_done = True

        time.sleep(1)

        pen.clear()

    except KeyboardInterrupt:
        logging.info(_("Exiting WeatherClock."))
        exit(0)

# if you don't do this, window will open and close immediately, should be the last line of your program
# this line is technically unreachable code since the above while loop also closes the script.
# wn.mainloop()

# if __name__=="__main__":
#     logging.debug(_d("logging","weatherClock.py is running directly"))
#     main()
# else:
#     logging.debug(_d("logging","weatherClock.py is being imported"))
