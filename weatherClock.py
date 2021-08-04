#!/usr/bin/python3
import time
import turtle
import math
import requests
import json
import logging
import sys
import os
import getopt
from datetime import datetime, timedelta


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
# currently set to Vancouver, BC CANADA
latitude = 49.2827
longitude = -123.1207
path = os.path.dirname(os.path.realpath(__file__)) + '\\'

api_key = False
try:
    with open('settings.json', 'r') as settings:
        api_key = json.loads(settings.read()).get("ApiKey")
except FileNotFoundError:
    logging.info("'settings.json' file not found. Checking command line parameters.")

if not api_key:
    try:
        options, remaining = getopt.getopt(sys.argv[1:], 'a:l:h', ["apikey=", "loglevel=", "help"])
        logging.info(f"Remaining arguments will not be used:{remaining}")
        logging.debug(f"Options: {options}")
        log_level = 'warning'
        for opt, arg in options:
            if opt in ['-a', '--apikey']:
                api_key = arg
            elif opt in ['-l', '--loglevel']:
                log_level = arg
            elif opt in ['-h', '--help']:
                print('usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]')
            else:
                logging.info(f"Parameter unused: {opt}={arg}")
        if not api_key:
            raise ValueError("Missing -a or --apikey parameter.")
        if log_level.lower() == 'debug':
            logging.basicConfig(level=logging.DEBUG)
        elif log_level.lower() == 'info' or log_level.lower() == 'information':
            logging.basicConfig(level=logging.INFO)
        elif log_level.lower() == 'warn' or log_level.lower() == 'warning':
            logging.basicConfig(level=logging.WARNING)
        elif log_level.lower() == 'error':
            logging.basicConfig(level=logging.ERROR)
    except getopt.GetoptError:
        logging.error('usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]')


url_params = f'lat={latitude}&lon={longitude}&exclude=current,minutely,daily,alerts,flags&appid={api_key}&units=metric'
url = f'http://api.openweathermap.org/data/2.5/onecall?{url_params}'

weatherUpdatePeriod = 10

temp_array = [0] * 12
id_array = [0] * 12
idImage_array = [""] * 12
currentHour = 0
hour_cursor = 0

res = requests.get(url)
if res.ok:
    data = res.json()
else:
    data = None
    res.raise_for_status()

logging.debug(data)

cursor_x = 0
cursor_y = 0

weatherText = turtle.Turtle()
weatherText.hideturtle()
weatherText_Description = -30
weatherText_Data = 30
weatherText_vertSpacing = 25
weatherText_DescriptionFontSize = 11
weatherText_DataFontSize = 10

weatherDividerPen = turtle.Turtle()
weatherDividerPen.hideturtle()

degree_sign = u"\N{DEGREE SIGN}"

# 1 - hourly detail mode, 0 - analog clock face mode
mode = 0
# determines radius for user touch when going into hourly detail mode
hourlyTouchSize = 25

deg_to_radians = 0.0174533
# determines how big clock is
radius = 210
hour1_x, hour1_y = math.cos(60*deg_to_radians)*radius, math.sin(60*deg_to_radians)*radius
hour2_x, hour2_y = math.cos(30*deg_to_radians)*radius, math.sin(30*deg_to_radians)*radius
hour3_x, hour3_y = math.cos(0*deg_to_radians)*radius, math.sin(0*deg_to_radians)*radius
hour4_x, hour4_y = math.cos(-30*deg_to_radians)*radius, math.sin(-30*deg_to_radians)*radius
hour5_x, hour5_y = math.cos(-60*deg_to_radians)*radius, math.sin(-60*deg_to_radians)*radius
hour6_x, hour6_y = math.cos(-90*deg_to_radians)*radius, math.sin(-90*deg_to_radians)*radius
hour7_x, hour7_y = math.cos(-120*deg_to_radians)*radius, math.sin(-120*deg_to_radians)*radius
hour8_x, hour8_y = math.cos(-150*deg_to_radians)*radius, math.sin(-150*deg_to_radians)*radius
hour9_x, hour9_y = math.cos(-180*deg_to_radians)*radius, math.sin(-180*deg_to_radians)*radius
hour10_x, hour10_y = math.cos(-210*deg_to_radians)*radius, math.sin(-210*deg_to_radians)*radius
hour11_x, hour11_y = math.cos(-240*deg_to_radians)*radius, math.sin(-240*deg_to_radians)*radius
hour12_x, hour12_y = math.cos(-270*deg_to_radians)*radius, math.sin(-270*deg_to_radians)*radius


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
    global hour_cursor

    cursor_x = x
    cursor_y = y
    logging.debug("cursor pressed: x, y")
    logging.debug(cursor_x, cursor_y)

    hour_cursor = int(time.strftime("%I"))
    current_meridiem = str(time.strftime('%p'))

    hour_touched = -1

    if touch_in_box(cursor_x, cursor_y, hour1_x, hour1_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 1
    elif touch_in_box(cursor_x, cursor_y, hour2_x, hour2_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 2
    elif touch_in_box(cursor_x, cursor_y, hour3_x, hour3_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 3
    elif touch_in_box(cursor_x, cursor_y, hour4_x, hour4_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 4
    elif touch_in_box(cursor_x, cursor_y, hour5_x, hour5_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 5
    elif touch_in_box(cursor_x, cursor_y, hour6_x, hour6_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 6
    elif touch_in_box(cursor_x, cursor_y, hour7_x, hour7_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 7
    elif touch_in_box(cursor_x, cursor_y, hour8_x, hour8_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 8
    elif touch_in_box(cursor_x, cursor_y, hour9_x, hour9_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 9
    elif touch_in_box(cursor_x, cursor_y, hour10_x, hour10_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 10
    elif touch_in_box(cursor_x, cursor_y, hour11_x, hour11_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 11
    elif touch_in_box(cursor_x, cursor_y, hour12_x, hour12_y, hourlyTouchSize, hourlyTouchSize):
        hour_touched = 12
    logging.debug(f"hour {hour_touched} WAS TOUCHED !")

    tomorrow_date = None
    if hour_touched < currentHour:
        hours_ahead = 12-currentHour+hour_touched
        if current_meridiem == "PM":
            tomorrow_date = datetime.today() + timedelta(days=1)
            touched_meridiem = "AM"
        else:
            touched_meridiem = "PM"
    else:
        hours_ahead = hour_touched - currentHour
        touched_meridiem = current_meridiem

    logging.info(f"Touched hour is {str(hours_ahead)} hours ahead")

    if mode == 0 and hour_touched != -1:
        # go to hourly detail mode
        mode = 1
        # ? to do?: add the button touches for different hours

        # remove the clock hands from showing
        pen.clear()

        # without this there is some weird line
        weatherText.penup()

        weatherText.goto(weatherText_Description, weatherText_vertSpacing*3)
        weatherText.color("white")
        # day of the week
        weatherText.write("Day", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold"))

        weatherText.goto(weatherText_Data, weatherText_vertSpacing*3)
        if not tomorrow_date:
            weatherText.write(datetime.today().strftime('%A'),
                              align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(tomorrow_date.strftime('%A'),
                              align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        # hour of the day
        weatherText.goto(weatherText_Description, weatherText_vertSpacing*2)
        weatherText.write("hour", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold"))

        weatherText.goto(weatherText_Data, weatherText_vertSpacing*2)
        weatherText.write(str(hour_touched) + " " + touched_meridiem,
                          align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        # temperature
        weatherText.goto(weatherText_Description, weatherText_vertSpacing)
        weatherText.write("temp", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold"))

        weatherText.goto(weatherText_Data, weatherText_vertSpacing)
        weatherText.write(str(round_half_up(data["hourly"][hours_ahead]["temp"], 1)) + degree_sign,
                          align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        
        # Feels like
        weatherText.goto(weatherText_Description, 0)
        weatherText.write("Feels like", align="right",
                          font=("Verdana", weatherText_DescriptionFontSize, "bold"))

        weatherText.goto(weatherText_Data, 0)
        weatherText.write(str(round_half_up(data["hourly"][hours_ahead]["feels_like"], 1)) + degree_sign,
                          align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        # POP
        weatherText.goto(weatherText_Description, -weatherText_vertSpacing)
        weatherText.write("POP", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold"))

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing)
        weatherText.write(str(int(data["hourly"][hours_ahead]["pop"]*100)) + " %",
                          align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        # Rain
        weatherText.goto(weatherText_Description, -weatherText_vertSpacing*2)
        weatherText.write("Rain", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold"))

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing*2)
        if 'rain' not in data["hourly"][hours_ahead]:
            weatherText.write("--", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(str(data["hourly"][hours_ahead]["rain"]["1h"]) + " mm",
                              align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        # Wind
        weatherText.goto(weatherText_Description, -weatherText_vertSpacing*3)
        weatherText.write("Wind", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold"))

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing*3)
        weatherText.write(str(data["hourly"][hours_ahead]["wind_speed"]) + " km/h",
                          align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.hideturtle()

        weatherDividerPen.pensize(3)

        weatherDividerPen.penup()
        weatherDividerPen.goto(0, -80)
        weatherDividerPen.color("white")
        weatherDividerPen.setheading(90)
        weatherDividerPen.pendown()
        weatherDividerPen.fd(160)
        weatherDividerPen.hideturtle()

    elif mode == 1 and touch_in_box(cursor_x, cursor_y, 0, 0, 200, 200):
        mode = 0  # go back to clock mode
        weatherText.clear()  # remove hourly details from screen
        weatherDividerPen.clear()

    cursor_x = -1
    cursor_y = -1


def update_forecast():
    
    global hour_cursor

    # weather ID breakdown https://openweathermap.org/weather-conditions
    # use https://ezgif.com/maker for gif conversion

    logging.debug("---- update_forecast() ----")

    current_hour = int(time.strftime("%H"))
    if current_hour > 12:
        hour_cursor = current_hour - 12
        meridiem = "PM"
    elif current_hour == 0:
        hour_cursor = 12
        meridiem = "AM"
    else:
        hour_cursor = current_hour
        meridiem = "AM"
        
    logging.debug("hour_cursor: " + str(hour_cursor))

    for num in range(12):
        # current hour
        logging.debug("current hour: " + time.strftime("%H") + " " + meridiem)
        # forecast hour
        logging.debug("forecast hour: " + str(int(time.strftime("%H"))+num))
        logging.debug("temperature: " + str(data["hourly"][num]["temp"]))
        logging.debug("feels like: " + str(data["hourly"][num]["feels_like"]))
        logging.debug("wind speed: " + str(data["hourly"][num]["wind_speed"]))
        logging.debug(data["hourly"][num]["weather"][0]["description"])
        logging.debug("weather ID: " + str(data["hourly"][num]["weather"][0]["id"]))
        logging.debug("POP: " + str(data["hourly"][num]["pop"]))

        if 'rain' not in data["hourly"][num]:
            logging.debug("no rain data")
        else:
            logging.info("rain: " + str(data["hourly"][num]["rain"]))

        temp_array[num] = data["hourly"][num]["temp"]
        id_array[num] = data["hourly"][num]["weather"][0]["id"]

        if 232 >= id_array[num] >= 200:
            idImage_array[num] = f"{path}11d@2x.gif"
        elif 321 >= id_array[num] >= 300:
            idImage_array[num] = f"{path}09d@2x.gif"
        elif 504 >= id_array[num] >= 500:
            idImage_array[num] = f"{path}10d@2x.gif"
        elif id_array[num] == 511:
            idImage_array[num] = f"{path}13d@2x.gif"
        elif 531 >= id_array[num] >= 520:
            idImage_array[num] = f"{path}09d@2x.gif"
        elif 622 >= id_array[num] >= 600:
            idImage_array[num] = f"{path}13d@2x.gif"
        elif 781 >= id_array[num] >= 701:
            idImage_array[num] = f"{path}50d@2x.gif"
        elif id_array[num] == 800:
            idImage_array[num] = f"{path}01d@2x.gif"
        elif id_array[num] == 801:
            idImage_array[num] = f"{path}02d@2x.gif"
        elif id_array[num] == 802:
            idImage_array[num] = f"{path}03d@2x.gif"
        elif id_array[num] == 803 or id_array[num] == 804:
            idImage_array[num] = f"{path}04d@2x.gif"
        else:
            logging.error("Invalid weather ID")

    logging.debug(temp_array)
    logging.debug(id_array)
    logging.debug(idImage_array)

    for image in idImage_array:
        wn.addshape(image)


wn = turtle.Screen()
wn.bgcolor("black")
wn.screensize()
# wn.setup(width=600, height=600)
# Make full screen
wn.setup(width=1.0, height=1.0)
wn.title("WeatherClock 0.0.0")
# turns off the animation, so you can't see anything when it is drawing
wn.tracer(0)

# turtle.Screen().get‌​canvas()._root().over‌​rideredirect(True) # attempting to make borderless fullscreen

# create our drawing pen
pen = turtle.Turtle()
pen.hideturtle()
# 0 is fastest it can go
pen.speed(0)
pen.pensize(3)

bg_hour1 = turtle.Turtle()
bg_hour1.goto(hour1_x, hour1_y)

bg_hour2 = turtle.Turtle()
bg_hour2.goto(hour2_x, hour2_y)

bg_hour3 = turtle.Turtle()
bg_hour3.goto(hour3_x, hour3_y)

bg_hour4 = turtle.Turtle()
bg_hour4.goto(hour4_x, hour4_y)

bg_hour5 = turtle.Turtle()
bg_hour5.goto(hour5_x, hour5_y)

bg_hour6 = turtle.Turtle()
bg_hour6.goto(hour6_x, hour6_y)

bg_hour7 = turtle.Turtle()
bg_hour7.goto(hour7_x, hour7_y)

bg_hour8 = turtle.Turtle()
bg_hour8.goto(hour8_x, hour8_y)

bg_hour9 = turtle.Turtle()
bg_hour9.goto(hour9_x, hour9_y)

bg_hour10 = turtle.Turtle()
bg_hour10.goto(hour10_x, hour10_y)

bg_hour11 = turtle.Turtle()
bg_hour11.goto(hour11_x, hour11_y)

bg_hour12 = turtle.Turtle()
bg_hour12.goto(hour12_x, hour12_y)

s = 0
# time.sleep(10)


# draw a clock using the pen i created
def draw_clock(hour, minute, second, pen):
    pen.hideturtle()

    # Draw the hour hand
    pen.penup()
    pen.goto(0, 0)
    pen.color("white")
    pen.setheading(90)
    angle = (hour / 12) * 360 + (minute/60) * 30
    pen.rt(angle)
    pen.pendown()
    pen.fd(100)

    # Draw the minute hand
    pen.penup()
    pen.goto(0, 0)
    pen.color("white")
    pen.setheading(90)
    angle = (minute / 60) * 360  # optional + (s/60) * 6
    pen.rt(angle)
    pen.pendown()
    pen.fd(170)

    # Draw the second hand
    pen.penup()
    pen.goto(0, 0)
    pen.color("red")
    pen.setheading(90)
    angle = (second / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(75)    


canvas = wn.getcanvas()
top_window = canvas.winfo_toplevel()
running = True
# wn.onkeypress(fun=exit(), key='q')


def on_close():
    global running
    running = False


top_window.protocol("WM_DELETE_WINDOW", on_close)
wn.listen()

while running:
    
    logging.info("\n... Main Loop Start ...\n")

    h = int(time.strftime("%I"))
    m = int(time.strftime("%M"))
    s = int(time.strftime("%S"))

    logging.debug(f"{str(h)}:{str(m)}:{str(s)}")

    # every x minutes, fetch new weather data
    if m % weatherUpdatePeriod == 0 and s == 0:
        res = requests.get(url)
        data = res.json()
        logging.debug("** FETCHED NEW DATA **")

    if mode == 0:
        draw_clock(h, m, s, pen)
        update_forecast()

        logging.debug(f"hour_cursor: {str(hour_cursor)}")

        if 1-hour_cursor < 0:
            bg_hour1.shape(idImage_array[12 - abs(1 - hour_cursor)])
        else:
            bg_hour1.shape(idImage_array[1 - hour_cursor])

        if 2-hour_cursor < 0:
            bg_hour2.shape(idImage_array[12 - abs(2 - hour_cursor)])
        else:
            bg_hour2.shape(idImage_array[2 - hour_cursor])

        if 3-hour_cursor < 0:
            bg_hour3.shape(idImage_array[12 - abs(3 - hour_cursor)])
        else:
            bg_hour3.shape(idImage_array[3 - hour_cursor])

        if 4-hour_cursor < 0:
            bg_hour4.shape(idImage_array[12 - abs(4 - hour_cursor)])
        else:
            bg_hour4.shape(idImage_array[4 - hour_cursor])

        if 5-hour_cursor < 0:
            bg_hour5.shape(idImage_array[12 - abs(5 - hour_cursor)])
        else:
            bg_hour5.shape(idImage_array[5 - hour_cursor])

        if 6-hour_cursor < 0:
            bg_hour6.shape(idImage_array[12 - abs(6 - hour_cursor)])
        else:
            bg_hour6.shape(idImage_array[6 - hour_cursor])

        if 7-hour_cursor < 0:
            bg_hour7.shape(idImage_array[12 - abs(7 - hour_cursor)])
        else:
            bg_hour7.shape(idImage_array[7 - hour_cursor])

        if 8-hour_cursor < 0:
            bg_hour8.shape(idImage_array[12 - abs(8 - hour_cursor)])
        else:
            bg_hour8.shape(idImage_array[8 - hour_cursor])

        if 9-hour_cursor < 0:
            bg_hour9.shape(idImage_array[12 - abs(9 - hour_cursor)])
        else:
            bg_hour9.shape(idImage_array[9 - hour_cursor])

        if 10-hour_cursor < 0:
            bg_hour10.shape(idImage_array[12 - abs(10 - hour_cursor)])
        else:
            bg_hour10.shape(idImage_array[10 - hour_cursor])

        if 11-hour_cursor < 0:
            bg_hour11.shape(idImage_array[12 - abs(11 - hour_cursor)])
        else:
            bg_hour11.shape(idImage_array[11 - hour_cursor])

        if 12-hour_cursor < 0:
            bg_hour12.shape(idImage_array[12 - abs(12 - hour_cursor)])
        else:
            bg_hour12.shape(idImage_array[12 - hour_cursor])

    wn.update()

    # cursor / touch logic
    # this returns the coordinate of the press !
    turtle.onscreenclick(get_mouse_click_coordinate)
    logging.debug("MODE:" + str(mode))
    logging.debug(cursor_x, cursor_y)

    if cursor_x != -1 and cursor_y != -1:
        logging.debug("screen was touched")

    time.sleep(1)

    pen.clear()

# if you don't do this, window will open and close immediately, should be the last line of your program
# wn.mainloop()
