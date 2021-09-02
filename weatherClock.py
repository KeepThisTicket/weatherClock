import time
import turtle
import math
import requests
from pprint import pprint
#from pynput.mouse import Listener
from datetime import datetime
from datetime import timedelta

# currently set to Moscow / Derevlevo
latitude = 55.646841
longtitude = 37.538984

gl_y_shift = 15
gl_x_shift = -15

tempColor = "gray"

url = 'http://api.openweathermap.org/data/2.5/onecall?lat=55.646841&lon=37.538984&exclude=current,minutely,daily,alerts,flags&appid=KEYHERE&units=metric'

weatherUpdatePeriod = 10

temp_array = [0] * 12
temp_feel_array = [0] * 12
wind_array = [0] * 12
temp_array_was = [0] * 12
temp_feel_array_was = [0] * 12
wind_array_was = [0] * 12
id_array = [0] * 12
idImage_array = [""] * 12
idImage_array_was = [""] * 12
currentHour = 0
hourCursor = 0

res = requests.get(url)
data = res.json()

print(data)

cursor_x = 0
cursor_y = 0

weatherText = turtle.Turtle()
weatherText.hideturtle()
weatherText_Description = -10
weatherText_Data = 10
weatherText_vertSpacing = 17
tempText_vertSpacing = -9
tempText_horzSpacing = 11
tempText_FontSize = 11
weatherText_DescriptionFontSize = 11
weatherText_DataFontSize = 10

weatherDividerPen = turtle.Turtle()
weatherDividerPen.hideturtle()

degree_sign = u"\N{DEGREE SIGN}"


mode = 0 # 1 - hourly detail mode, 0 - analog clock face mode

hourlyTouchSize = 25 # determines radius for user touch when going into hourly detail mode

deg_to_radians = 0.0174533
radius = 120 # determines how big clock is
hour_x = [0] * 12
hour_y = [0] * 12
hour_x[0] = math.cos(60*deg_to_radians)*radius
hour_y[0] = math.sin(60*deg_to_radians)*radius
hour_x[1] = math.cos(30*deg_to_radians)*radius
hour_y[1] = math.sin(30*deg_to_radians)*radius
hour_x[2] = math.cos(0*deg_to_radians)*radius
hour_y[3] = math.sin(0*deg_to_radians)*radius
hour_x[3] = math.cos(-30*deg_to_radians)*radius
hour_y[3] = math.sin(-30*deg_to_radians)*radius
hour_x[4] = math.cos(-60*deg_to_radians)*radius
hour_y[4] = math.sin(-60*deg_to_radians)*radius
hour_x[5] = math.cos(-90*deg_to_radians)*radius
hour_y[5] = math.sin(-90*deg_to_radians)*radius
hour_x[6] = math.cos(-120*deg_to_radians)*radius
hour_y[6] = math.sin(-120*deg_to_radians)*radius
hour_x[7] = math.cos(-150*deg_to_radians)*radius
hour_y[7] = math.sin(-150*deg_to_radians)*radius
hour_x[8] = math.cos(-180*deg_to_radians)*radius
hour_y[8] = math.sin(-180*deg_to_radians)*radius
hour_x[9] = math.cos(-210*deg_to_radians)*radius
hour_y[9] = math.sin(-210*deg_to_radians)*radius
hour_x[10] = math.cos(-240*deg_to_radians)*radius
hour_y[10] = math.sin(-240*deg_to_radians)*radius
hour_x[11] = math.cos(-270*deg_to_radians)*radius
hour_y[11] = math.sin(-270*deg_to_radians)*radius

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
    global mode # 0 = clock, 1 = hourly detail

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
        if (touchInBox(cursor_x, cursor_y, hour_x[i], hour_y[i], hourlyTouchSize, hourlyTouchSize)):
            hourTouched = i + 1
            print("hour {hourTouched} WAS TOUCHED !")

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
        mode = 1 # go to hourly detail mode
        # TODO add the button touches for different hours
        
        pen.clear() # remove the clock hands from showing

        weatherText.penup() # without this there is some weird ass line 

        weatherText.goto(weatherText_Description + gl_x_shift, weatherText_vertSpacing*3 + gl_y_shift)
        weatherText.color("white")
        weatherText.write("Day", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # day of the week

        weatherText.goto(weatherText_Data + gl_x_shift, weatherText_vertSpacing*3 + gl_y_shift)
        if (tomorrow == False):
            weatherText.write(datetime.today().strftime('%A'), align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(tomorrowDate.strftime('%A'), align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description + gl_x_shift, weatherText_vertSpacing*2 + gl_y_shift)
        weatherText.write("hour", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # hour of the day

        weatherText.goto(weatherText_Data + gl_x_shift, weatherText_vertSpacing*2 + gl_y_shift)
        weatherText.write(str(hourTouched) + " " + touchedMeridiem, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description + gl_x_shift, weatherText_vertSpacing + gl_y_shift)
        weatherText.write("temp", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # temperature

        weatherText.goto(weatherText_Data + gl_x_shift, weatherText_vertSpacing + gl_y_shift)
        weatherText.write(str(round_half_up(data["hourly"][hoursAhead]["temp"], 1)) + degree_sign, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        
        weatherText.goto(weatherText_Description + gl_x_shift, 0 + gl_y_shift)
        weatherText.write("Feels like", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # Feels like

        weatherText.goto(weatherText_Data + gl_x_shift, 0 + gl_y_shift)
        weatherText.write(str(round_half_up(data["hourly"][hoursAhead]["feels_like"], 1)) + degree_sign, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description + gl_x_shift, -weatherText_vertSpacing + gl_y_shift)
        weatherText.write("POP", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # POP

        weatherText.goto(weatherText_Data + gl_x_shift, -weatherText_vertSpacing + gl_y_shift)
        weatherText.write(str(int(data["hourly"][hoursAhead]["pop"]*100)) + " %", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description + gl_x_shift, -weatherText_vertSpacing*2 + gl_y_shift)
        weatherText.write("Rain", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # Rain

        weatherText.goto(weatherText_Data + gl_x_shift, -weatherText_vertSpacing*2 + gl_y_shift)
        if 'rain' not in data["hourly"][hoursAhead]:
            weatherText.write("--", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(str(data["hourly"][hoursAhead]["rain"]["1h"]) + " mm", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description + gl_x_shift, -weatherText_vertSpacing*3 + gl_y_shift)
        weatherText.write("Wind", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # Wind

        weatherText.goto(weatherText_Data + gl_x_shift, -weatherText_vertSpacing*3 + gl_y_shift)
        weatherText.write(str(data["hourly"][hoursAhead]["wind_speed"]) + " km/h", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.hideturtle()

        weatherDividerPen.pensize(3)

        weatherDividerPen.penup()
        weatherDividerPen.goto(0 + gl_x_shift, -80 + gl_y_shift)
        weatherDividerPen.color("white")
        weatherDividerPen.setheading(90)
        weatherDividerPen.pendown()
        weatherDividerPen.fd(160)
        weatherDividerPen.hideturtle()

    elif (mode == 1 and touchInBox(cursor_x, cursor_y, 0, 0, 200, 200)):
        mode = 0 # go back to clock mode
        weatherText.clear() # remove hourly details from screen
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
        temp_feel_array[num] = data["hourly"][num]["feels_like"]
        wind_array[num] = data["hourly"][num]["wind_speed"]
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
    print(temp_feel_array)
    print(wind_array)
    print(id_array)
    print(idImage_array)

    for image in idImage_array:
        wn.addshape(image)


wn = turtle.Screen()
wn.bgcolor("black")
wn.screensize()
#wn.setup(width=600, height=600)
wn.setup(width = 1.0, height = 1.0) # Make fullscreen
wn.title("Moscow / Derevlevo")
wn.tracer(0) # turns off the animation, so you can't see anything when it is drawing

# turtle.Screen().get‌​canvas()._root().over‌​rideredirect(True) # attempting to make borderless fullscreen

# create our drawing pen
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0) # 0 is fastest it can go
pen.pensize(3)

bg_hour = []
bg_hourtext = []
bg_windtext = []

for i in range(0, 12):
    bg_hour_i = turtle.Turtle()
    bg_hour_i.goto(hour_x[i] + gl_x_shift, hour_y[i] + gl_y_shift)
    bg_hour.append(bg_hour_i)

    bg_hourtext_i = turtle.Turtle()
    bg_hourtext_i.color(tempColor)
    bg_hourtext_i.hideturtle()
    bg_hourtext.append(bg_hourtext_i)

    bg_windtext_i = turtle.Turtle()
    bg_windtext_i.color(tempColor)
    bg_windtext_i.hideturtle()
    bg_windtext.append(bg_windtext_i)

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
    pen.goto(0 + gl_x_shift,0 + gl_y_shift)
    pen.color("white")
    pen.setheading(90)
    angle = (h / 12) * 360 + (m/60) * 30
    pen.rt(angle)
    pen.pendown()
    pen.fd(45)

    # Draw the minute hand
    pen.penup()
    pen.goto(0 + gl_x_shift,0 + gl_y_shift)
    pen.color("yellow")
    pen.setheading(90)
    angle = (m / 60) * 360  # optional + (s/60) * 6
    pen.rt(angle)
    pen.pendown()
    pen.fd(70)

    # Draw the second hand
    pen.penup()
    pen.goto(0 + gl_x_shift,0 + gl_y_shift)
    pen.color("gray")
    pen.setheading(90)
    angle = (s / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(85)

wasM = 0

while True:

    print("")
    print("... Main Loop Start ... ")
    print("")

    h = int(time.strftime("%I"))
    m = int(time.strftime("%M"))
    s = int(time.strftime("%S"))

    print(str(h) + " " + str(m) + " " + str(s))

    needUpdate = False

    if (m % weatherUpdatePeriod == 0 and s == 0): # every x minutes, fetch new weather data
        res = requests.get(url)
        data = res.json()
        print("")
        print("** FETCHED NEW DATA **")
        print("")
        needUpdate = True

    if (mode == 0):
        draw_clock(h, m, s, pen)
        updateForecast()

        print("hourCursor: " + str(hourCursor))

        for i in range(1, 13):
            if(i-hourCursor < 0):
                j = 12-abs(i-hourCursor)
            else:
                j = i-hourCursor
            if(idImage_array[j] != idImage_array_was[j]):
                bg_hour[i-1].shape(idImage_array[j])
                idImage_array_was[j] = idImage_array[j]
            if ((needUpdate) or (temp_array[j] != temp_array_was[j]) or (temp_feel_array[j] != temp_feel_array_was[j]) or
                        (wind_array[j] != wind_array_was[j])):
                bg_hourtext[i-1].clear()
                bg_hourtext[i-1].penup()
                x_shift = 0
                y_shift = 0
                #print(idImage_array[i-1])
                if ((idImage_array[j] == "04d@2x.gif") or (idImage_array[j] == "02d@2x.gif")):
                    x_shift = -4
                    y_shift = -8
                if (idImage_array[j] == "11d@2x.gif"):
                    x_shift = -6
                    y_shift = 3
                if ((idImage_array[j] == "09d@2x.gif") or  (idImage_array[j] == "10d@2x.gif")):
                    x_shift = -4
                    y_shift = 3
                if (idImage_array[j] == "03d@2x.gif"):
                    x_shift = 0
                    y_shift = -5
                if (temp_array[j]<10):
                    x_shift = x_shift - 5    
                bg_hourtext[i-1].goto(hour_x[i-1] + tempText_horzSpacing + x_shift + gl_x_shift, hour_y[i-1] + tempText_vertSpacing + y_shift + gl_y_shift)
                v = int(round(temp_array[j]))
                v2 = int(round(temp_feel_array[j]))
                bg_hourtext[i-1].write(str(round(temp_array[j])), align="right", font=("Verdana", tempText_FontSize, "bold"))
                # looks bad
                #if (v == v2):
                #    bg_hourtext[i-1].write(str(round(temp_array[j])), align="right", font=("Verdana", tempText_FontSize, "bold"))
                #else:
                #    bg_hourtext[i-1].write(str(round(temp_array[j])) + "|" + str(round(temp_feel_array[j])),
                #        align="right", font=("Verdana", tempText_FontSize, "bold"))
                if (i in range(1,6)):
                    bg_windtext[i-1].clear()
                    bg_windtext[i-1].penup()
                    bg_windtext[i-1].goto(hour_x[i-1] + tempText_horzSpacing +  x_shift + 110 + gl_x_shift, hour_y[i-1] + tempText_vertSpacing + y_shift + gl_y_shift)
                    bg_windtext[i-1].write(str(wind_array[j]) + " km/h", align="right", font=("Verdana", tempText_FontSize, ""))
                if (i in range(7,12)):
                    bg_windtext[i-1].clear()
                    bg_windtext[i-1].penup()
                    bg_windtext[i-1].goto(hour_x[i-1] + tempText_horzSpacing +  x_shift - 50 + gl_x_shift, hour_y[i-1] + tempText_vertSpacing + y_shift + gl_y_shift)
                    bg_windtext[i-1].write(str(wind_array[j]), align="right", font=("Verdana", tempText_FontSize, ""))
            temp_array_was[j] = temp_array[j]
            temp_feel_array_was[j] = temp_feel_array[j]
            wind_array_was[j] = wind_array[j]
    #if (wasM != m):
    wn.update()
    wasM = m
    # cursor / touch logic
    turtle.onscreenclick(get_mouse_click_coor) # this returns the coordinate of the press !
    print("MODE:" + str(mode))
    print(cursor_x, cursor_y)

    if(cursor_x != -1 and cursor_y != -1):
        print("screen was touched")



    time.sleep(1)

    pen.clear()

wn.mainloop() # if you don't do this, window will open and close immediately, should the the last line of your program
