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

def get_mouse_click_coor(x, y):


    # when this event is triggered, it means someone pressed the screen, therefore we should check what state we are
    # going into (clock mode, or hourly detail mode)

    global cursor_x
    global cursor_y
    # 0 = clock, 1 = hourly detail
    global mode

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

    if (touchInBox(cursor_x, cursor_y, hour1_x, hour1_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 1 WAS TOUCHED !")
        hourTouched = 1
    elif (touchInBox(cursor_x, cursor_y, hour2_x, hour2_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 2 WAS TOUCHED !")
        hourTouched = 2
    elif (touchInBox(cursor_x, cursor_y, hour3_x, hour3_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 3 WAS TOUCHED !")
        hourTouched = 3
    elif (touchInBox(cursor_x, cursor_y, hour4_x, hour4_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 4 WAS TOUCHED !")
        hourTouched = 4
    elif (touchInBox(cursor_x, cursor_y, hour5_x, hour5_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 5 WAS TOUCHED !")
        hourTouched = 5
    elif (touchInBox(cursor_x, cursor_y, hour6_x, hour6_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 6 WAS TOUCHED !")
        hourTouched = 6
    elif (touchInBox(cursor_x, cursor_y, hour7_x, hour7_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 7 WAS TOUCHED !")
        hourTouched = 7
    elif (touchInBox(cursor_x, cursor_y, hour8_x, hour8_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 8 WAS TOUCHED !")
        hourTouched = 8
    elif (touchInBox(cursor_x, cursor_y, hour9_x, hour9_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 9 WAS TOUCHED !")
        hourTouched = 9
    elif (touchInBox(cursor_x, cursor_y, hour10_x, hour10_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 10 WAS TOUCHED !")
        hourTouched = 10
    elif (touchInBox(cursor_x, cursor_y, hour11_x, hour11_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 11 WAS TOUCHED !")
        hourTouched = 11
    elif (touchInBox(cursor_x, cursor_y, hour12_x, hour12_y, hourlyTouchSize, hourlyTouchSize)):
        print("hour 12 WAS TOUCHED !")
        hourTouched = 12

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
        if (tomorrow == False):
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
        print("current hour: " + time.strftime("%H") + " " + meridiem) # current hour
        print("forecast hour: " + str(int(time.strftime("%H"))+num)) # forecast hour
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

def draw_clock(h, m, s, pen): # draw a clock using the pen i created
    # Draw the clock face
    #pen.up()
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
    angle = (minute / 60) * 360  # optional + (s/60) * 6
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
    
    # every x minutes, fetch new weather data
    if m % weatherUpdatePeriod == 0 and s == 0:
        res = requests.get(url)
        data = res.json()
        print("")
        print("** FETCHED NEW DATA **")
        print("")

    if mode == 0:
        draw_clock(h, m, s, pen)
        updateForecast()

        print("hourCursor: " + str(hourCursor))

        if(1-hourCursor < 0):
            bg_hour1.shape(idImage_array[12-abs(1-hourCursor)])
        else:
            bg_hour1.shape(idImage_array[1-hourCursor])

        if(2-hourCursor < 0):
            bg_hour2.shape(idImage_array[12-abs(2-hourCursor)])
        else:
            bg_hour2.shape(idImage_array[2-hourCursor])

        if(3-hourCursor < 0):
            bg_hour3.shape(idImage_array[12-abs(3-hourCursor)])
        else:
            bg_hour3.shape(idImage_array[3-hourCursor])
        
        if(4-hourCursor < 0):
            bg_hour4.shape(idImage_array[12-abs(4-hourCursor)])
        else:
            bg_hour4.shape(idImage_array[4-hourCursor])

        if(5-hourCursor < 0):
            bg_hour5.shape(idImage_array[12-abs(5-hourCursor)])
        else:
            bg_hour5.shape(idImage_array[5-hourCursor])

        if(6-hourCursor < 0):
            bg_hour6.shape(idImage_array[12-abs(6-hourCursor)])
        else:
            bg_hour6.shape(idImage_array[6-hourCursor])
        
        if(7-hourCursor < 0):
            bg_hour7.shape(idImage_array[12-abs(7-hourCursor)])
        else:
            bg_hour7.shape(idImage_array[7-hourCursor])

        if(8-hourCursor < 0):
            bg_hour8.shape(idImage_array[12-abs(8-hourCursor)])
        else:
            bg_hour8.shape(idImage_array[8-hourCursor])

        if(9-hourCursor < 0):
            bg_hour9.shape(idImage_array[12-abs(9-hourCursor)])
        else:
            bg_hour9.shape(idImage_array[9-hourCursor])

        if(10-hourCursor < 0):
            bg_hour10.shape(idImage_array[12-abs(10-hourCursor)])
        else:
            bg_hour10.shape(idImage_array[10-hourCursor])

        if(11-hourCursor < 0):
            bg_hour11.shape(idImage_array[12-abs(11-hourCursor)])
        else:
            bg_hour11.shape(idImage_array[11-hourCursor])

        if(12-hourCursor < 0):
            bg_hour12.shape(idImage_array[12-abs(12-hourCursor)])
        else:
            bg_hour12.shape(idImage_array[12-hourCursor])

    wn.update()

    # cursor / touch logic
    print("MODE:" + str(mode))
    print(cursor_x, cursor_y)

        print("screen was touched")
    turtle.onscreenclick(get_mouse_click_coordinate)

    
    if cursor_x != -1 and cursor_y != -1:

    time.sleep(1)

    pen.clear()

# if you don't do this, window will open and close immediately, should be the last line of your program
# wn.mainloop()
