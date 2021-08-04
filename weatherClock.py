import time
import turtle
import math
import requests
from pprint import pprint
from pynput.mouse import Listener
from datetime import datetime
from datetime import timedelta

# currently set to Vancouver, BC CANADA
latitude = 49.2827
longtitude = -123.1207

url = 'http://api.openweathermap.org/data/2.5/onecall?lat=49.2827&lon=-123.1207&exclude=current,minutely,daily,alerts,flags&appid=APIKEYHERE&units=metric'

weatherUpdatePeriod = 10

temp_array = [0] * 12
id_array = [0] * 12
idImage_array = [""] * 12
currentHour = 0
hourCursor = 0

res = requests.get(url)
data = res.json()

print(data)

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


mode = 0  # 1 - hourly detail mode, 0 - analog clock face mode

hourlyTouchSize = 25  # determines radius for user touch when going into hourly detail mode

radius = 210  # determines how big clock is
hours = []

for i in range(60, -300, -30):
    i_r = math.radians(i)
    hours.append((math.cos(i_r)*radius, math.sin(i_r)*radius))


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def touchInBox(touch_x, touch_y, center_x, center_y, size_x, size_y):
    if (touch_x > center_x - size_x/2 and touch_x < center_x + size_x/2 and touch_y > center_y - size_y/2 and touch_y < center_y + size_y/2):
        return True
    else:
        return False


def get_mouse_click_coor(x, y):

    # when this event is triggered, it means someone pressed the screen, therefore we should check what state we are going into (clock mode, or hourly detail mode)

    global cursor_x
    global cursor_y
    global mode  # 0 = clock, 1 = hourly detail

    cursor_x = x
    cursor_y = y
    print("cursor pressed: x, y")
    print(cursor_x, cursor_y)

    currentHour = int(time.strftime("%H"))
    if currentHour > 12:
        hourCursor = currentHour - 12
        currentMeridiem = "PM"
    elif currentHour == 0:
        hourCursor = 12
        currentMeridiem = "AM"
    else:
        hourCursor = currentHour
        currentMeridiem = "AM"

    hourTouched = -1

    for i in range(0, 12):
        if (touchInBox(cursor_x, cursor_y, hours[i][0], hours[i][1], hourlyTouchSize, hourlyTouchSize)):
            print(f"hour {i+1} WAS TOUCHED !")
            hourTouched = i+1

    tomorrow = False
    if (hourTouched < currentHour):
        hoursAhead = 12-currentHour+hourTouched
        if (currentMeridiem == "PM"):
            tomorrow = True
            tomorrowDate = datetime.today() + timedelta(days=1)
            touchedMeridiem = "AM"
        else:
            touchedMeridiem = "PM"
    elif (hourTouched >= currentHour):
        hoursAhead = hourTouched - currentHour
        touchedMeridiem = currentMeridiem

    print("Touched hour is " + str(hoursAhead) + " hours ahead")

    if (mode == 0 and hourTouched != -1):
        mode = 1  # go to hourly detail mode
        # TODO add the button touches for different hours

        pen.clear()  # remove the clock hands from showing

        weatherText.penup()  # without this there is some weird ass line

        weatherText.goto(weatherText_Description, weatherText_vertSpacing*3)
        weatherText.color("white")
        weatherText.write("Day", align="right", font=(
            "Verdana", weatherText_DescriptionFontSize, "bold"))  # day of the week

        weatherText.goto(weatherText_Data, weatherText_vertSpacing*3)
        if (tomorrow == False):
            weatherText.write(datetime.today().strftime('%A'), align="left", font=(
                "Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(tomorrowDate.strftime('%A'), align="left", font=(
                "Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, weatherText_vertSpacing*2)
        weatherText.write("hour", align="right", font=(
            "Verdana", weatherText_DescriptionFontSize, "bold"))  # hour of the day

        weatherText.goto(weatherText_Data, weatherText_vertSpacing*2)
        weatherText.write(str(hourTouched) + " " + touchedMeridiem,
                          align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, weatherText_vertSpacing)
        weatherText.write("temp", align="right", font=(
            "Verdana", weatherText_DescriptionFontSize, "bold"))  # temperature

        weatherText.goto(weatherText_Data, weatherText_vertSpacing)
        weatherText.write(str(round_half_up(data["hourly"][hoursAhead]["temp"], 1)) +
                          degree_sign, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, 0)
        weatherText.write("Feels like", align="right", font=(
            "Verdana", weatherText_DescriptionFontSize, "bold"))  # Feels like

        weatherText.goto(weatherText_Data, 0)
        weatherText.write(str(round_half_up(data["hourly"][hoursAhead]["feels_like"], 1)) +
                          degree_sign, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, -weatherText_vertSpacing)
        weatherText.write("POP", align="right", font=(
            "Verdana", weatherText_DescriptionFontSize, "bold"))  # POP

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing)
        weatherText.write(str(int(data["hourly"][hoursAhead]["pop"]*100)) + " %",
                          align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, -weatherText_vertSpacing*2)
        weatherText.write("Rain", align="right", font=(
            "Verdana", weatherText_DescriptionFontSize, "bold"))  # Rain

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing*2)
        if 'rain' not in data["hourly"][hoursAhead]:
            weatherText.write(
                "--", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(str(data["hourly"][hoursAhead]["rain"]["1h"]) + " mm",
                              align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, -weatherText_vertSpacing*3)
        weatherText.write("Wind", align="right", font=(
            "Verdana", weatherText_DescriptionFontSize, "bold"))  # Wind

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing*3)
        weatherText.write(str(data["hourly"][hoursAhead]["wind_speed"]) + " km/h",
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

    elif (mode == 1 and touchInBox(cursor_x, cursor_y, 0, 0, 200, 200)):
        mode = 0  # go back to clock mode
        weatherText.clear()  # remove hourly details from screen
        weatherDividerPen.clear()

    cursor_x = -1
    cursor_y = -1


def updateForecast():

    global hourCursor

    # weather ID breakdown https://openweathermap.org/weather-conditions
    # use https://ezgif.com/maker for gif conversion

    print("")
    print("---- updateForecast() ----")

    currentHour = int(time.strftime("%H"))
    if currentHour > 12:
        hourCursor = currentHour - 12
        meridiem = "PM"
    elif currentHour == 0:
        hourCursor = 12
        meridiem = "AM"
    else:
        hourCursor = currentHour
        meridiem = "AM"

    print("hourCursor: " + str(hourCursor))

    for num in range(12):
        print("")
        print("current hour: " + time.strftime("%H") +
              " " + meridiem)  # current hour
        # forecast hour
        print("forecast hour: " + str(int(time.strftime("%H"))+num))
        print("temperature: " + str(data["hourly"][num]["temp"]))
        print("feels like: " + str(data["hourly"][num]["feels_like"]))
        print("wind speed: " + str(data["hourly"][num]["wind_speed"]))
        # pprint(data["hourly"][num]["weather"][0]["description"])
        print("weather ID: " + str(data["hourly"][num]["weather"][0]["id"]))
        print("POP: " + str(data["hourly"][num]["pop"]))

        if 'rain' not in data["hourly"][num]:
            print("no rain data")
        else:
            print("rain: " + str(data["hourly"][num]["rain"]))

        temp_array[num] = data["hourly"][num]["temp"]
        id_array[num] = data["hourly"][num]["weather"][0]["id"]

        if id_array[num] >= 200 and id_array[num] <= 232:
            # do something
            idImage_array[num] = "11d@2x.gif"
        elif id_array[num] >= 300 and id_array[num] <= 321:
            # do something
            idImage_array[num] = "09d@2x.gif"
        elif id_array[num] >= 500 and id_array[num] <= 504:
            # do something
            idImage_array[num] = "10d@2x.gif"
        elif id_array[num] == 511:
            # do someting
            idImage_array[num] = "13d@2x.gif"
        elif id_array[num] >= 520 and id_array[num] <= 531:
            # do something
            idImage_array[num] = "09d@2x.gif"
        elif id_array[num] >= 600 and id_array[num] <= 622:
            # do something
            idImage_array[num] = "13d@2x.gif"
        elif id_array[num] >= 701 and id_array[num] <= 781:
            # do something
            idImage_array[num] = "50d@2x.gif"
        elif id_array[num] == 800:
            # do something
            idImage_array[num] = "01d@2x.gif"
        elif id_array[num] == 801:
            # do something
            idImage_array[num] = "02d@2x.gif"
        elif id_array[num] == 802:
            # do something
            idImage_array[num] = "03d@2x.gif"
        elif id_array[num] == 803 or id_array[num] == 804:
            # do something
            idImage_array[num] = "04d@2x.gif"
        else:
            print("Invalid weather ID")

    print(temp_array)
    print(id_array)
    print(idImage_array)

    for image in idImage_array:
        wn.addshape(image)


wn = turtle.Screen()
wn.bgcolor("black")
wn.screensize()
#wn.setup(width=600, height=600)
wn.setup(width=1.0, height=1.0)  # Make fullscreen
wn.title("WeatherClock 0.0.0")
# turns off the animation, so you can't see anything when it is drawing
wn.tracer(0)

# turtle.Screen().get‌​canvas()._root().over‌​rideredirect(True) # attempting to make borderless fullscreen

# create our drawing pen
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)  # 0 is fastest it can go
pen.pensize(3)

bg_hours = [turtle.Turtle()]*12
for i in range(0, 12):
    bg_hours[i].goto(hours[i][1], hours[i][2])

s = 0
# time.sleep(10)


def draw_clock(h, m, s, pen):  # draw a clock using the pen i created
    # Draw the clock face
    # pen.up()
    # pen.goto(0, 210)
    # pen.setheading(180)
    # pen.color("green")
    # pen.pendown()
    # pen.circle(210)

    # Draw lines for the hours
    # pen.penup()
    # pen.goto(0,0)
    # pen.setheading(90)

    # for _ in range(12):
    #     pen.fd(190)
    #     pen.pendown()
    #     pen.fd(20)
    #     pen.penup()
    #     pen.goto(0,0)
    #     pen.rt(30)

    pen.hideturtle()

    # Draw the hour hand
    pen.penup()
    pen.goto(0, 0)
    pen.color("white")
    pen.setheading(90)
    angle = (h / 12) * 360 + (m/60) * 30
    pen.rt(angle)
    pen.pendown()
    pen.fd(100)

    # Draw the minute hand
    pen.penup()
    pen.goto(0, 0)
    pen.color("white")
    pen.setheading(90)
    angle = (m / 60) * 360  # optional + (s/60) * 6
    pen.rt(angle)
    pen.pendown()
    pen.fd(170)

    # Draw the second hand
    pen.penup()
    pen.goto(0, 0)
    pen.color("red")
    pen.setheading(90)
    angle = (s / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(75)


while True:

    print("")
    print("... Main Loop Start ... ")
    print("")

    h = int(time.strftime("%I"))
    m = int(time.strftime("%M"))
    s = int(time.strftime("%S"))

    print(str(h) + " " + str(m) + " " + str(s))

    if (m % weatherUpdatePeriod == 0 and s == 0):  # every x minutes, fetch new weather data
        res = requests.get(url)
        data = res.json()
        print("")
        print("** FETCHED NEW DATA **")
        print("")

    if (mode == 0):
        draw_clock(h, m, s, pen)
        updateForecast()

        print("hourCursor: " + str(hourCursor))

        for i in range(1, 13):
            if(i-hourCursor < 0):
                bg_hours[i-1].shape(idImage_array[12-abs(i-hourCursor)])
            else:
                bg_hours[i-1].shape(idImage_array[i-hourCursor])

    wn.update()

    # cursor / touch logic
    # this returns the coordinate of the press !
    turtle.onscreenclick(get_mouse_click_coor)
    print("MODE:" + str(mode))
    print(cursor_x, cursor_y)

    if(cursor_x != -1 and cursor_y != -1):
        print("screen was touched")

    time.sleep(1)

    pen.clear()

wn.mainloop()  # if you don't do this, window will open and close immediately, should the the last line of your program
