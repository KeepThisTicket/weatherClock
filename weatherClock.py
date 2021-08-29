import time
import turtle
import math
import requests
from pprint import pprint
from pynput.mouse import Listener
from datetime import datetime
from datetime import timedelta

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def touchInBox(touch_x, touch_y, center_x, center_y, size_x, size_y):
    if (touch_x > center_x - size_x/2 and touch_x < center_x + size_x/2 and touch_y > center_y - size_y/2 and touch_y < center_y + size_y/2):
        return True
    else:
        return False

def switch_meridiem(currentMeridiem):
    if (currentMeridiem == "AM"):
        return "PM"
    return "AM"

def determine_weather_pictogram(weather_id):
    # weather ID breakdown https://openweathermap.org/weather-conditions
    # use https://ezgif.com/maker for gif conversion
    if weather_id >= 200 and weather_id <= 232:
        return "11d@2x.gif"
    elif weather_id >= 300 and weather_id <= 321:
        return "09d@2x.gif"
    elif weather_id >= 500 and weather_id <= 504:
        return "10d@2x.gif"
    elif weather_id == 511:
        return "13d@2x.gif"
    elif weather_id >= 520 and weather_id <= 531:
        return "09d@2x.gif"
    elif weather_id >= 600 and weather_id <= 622:
        return "13d@2x.gif"
    elif weather_id >= 701 and weather_id <= 781:
        return "50d@2x.gif"
    elif weather_id == 800:
        return "01d@2x.gif"
    elif weather_id == 801:
        return "02d@2x.gif"
    elif weather_id == 802:
        return "03d@2x.gif"
    elif weather_id == 803 or weather_id == 804:
        return "04d@2x.gif"

    print("Invalid weather ID")

def determine_hour_index(current_hour, num):
    if (current_hour + num) > 12:
        return current_hour + num - 13
    return current_hour + num - 1

def get_mouse_click_coor(x, y):

    # when this event is triggered, it means someone pressed the screen, therefore we should check what state we are going into (clock mode, or hourly detail mode)
    global mode # 0 = clock, 1 = hourly detail

    hourTouched = -1
    if (touchInBox(x, y, hour1_x, hour1_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 1
    elif (touchInBox(x, y, hour2_x, hour2_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 2
    elif (touchInBox(x, y, hour3_x, hour3_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 3
    elif (touchInBox(x, y, hour4_x, hour4_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 4
    elif (touchInBox(x, y, hour5_x, hour5_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 5
    elif (touchInBox(x, y, hour6_x, hour6_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 6
    elif (touchInBox(x, y, hour7_x, hour7_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 7
    elif (touchInBox(x, y, hour8_x, hour8_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 8
    elif (touchInBox(x, y, hour9_x, hour9_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 9
    elif (touchInBox(x, y, hour10_x, hour10_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 10
    elif (touchInBox(x, y, hour11_x, hour11_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 11
    elif (touchInBox(x, y, hour12_x, hour12_y, hourlyTouchSize, hourlyTouchSize)):
        hourTouched = 12

    current_hour = int(time.strftime("%I"))
    currentMeridiem = time.strftime("%p")
    
    #print("currentMeridiem %s" % currentMeridiem)

    tomorrow = False        
    if (hourTouched < current_hour): # touched_hour < current_hour = other meridiam
        hoursAhead = 12 - current_hour + hourTouched
        touchedMeridiem = switch_meridiem(currentMeridiem)
    elif (hourTouched >= current_hour): # touched_hour >= current_hour = same meridiam
        hoursAhead = hourTouched - current_hour
        if (hourTouched == 12): # touching 12, there change meridiam
            touchedMeridiem = switch_meridiem(currentMeridiem)
        else:
            touchedMeridiem = currentMeridiem
    if (currentMeridiem == "PM" and touchedMeridiem == "AM"):
        tomorrow = True
        tomorrowDate = datetime.today() + timedelta(days=1)

    #print("hour %s was toched; from %s we are %s hour ahead and stating %s" % (hourTouched, current_hour, hoursAhead, touchedMeridiem))
    #print(data["hourly"][hoursAhead])

    if (mode == 0 and hourTouched != -1):
        mode = 1 # go to hourly detail mode
        
        pen.clear() # remove the clock hands from showing

        weatherText.penup() # without this there is some weird ass line 

        weatherText.goto(weatherText_Description, weatherText_vertSpacing*3)
        weatherText.color("white")
        weatherText.write("Day", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # day of the week

        weatherText.goto(weatherText_Data, weatherText_vertSpacing*3)
        if (tomorrow == False):
            weatherText.write(datetime.today().strftime('%A'), align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(tomorrowDate.strftime('%A'), align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, weatherText_vertSpacing*2)
        weatherText.write("hour", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # hour of the day

        weatherText.goto(weatherText_Data, weatherText_vertSpacing*2)
        weatherText.write(str(hourTouched) + " " + touchedMeridiem, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, weatherText_vertSpacing)
        weatherText.write("temp", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # temperature

        weatherText.goto(weatherText_Data, weatherText_vertSpacing)
        weatherText.write(str(round_half_up(data["hourly"][hoursAhead]["temp"], 1)) + degree_sign, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        
        weatherText.goto(weatherText_Description, 0)
        weatherText.write("Feels like", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # Feels like

        weatherText.goto(weatherText_Data, 0)
        weatherText.write(str(round_half_up(data["hourly"][hoursAhead]["feels_like"], 1)) + degree_sign, align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, -weatherText_vertSpacing)
        weatherText.write("POP", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # POP (Probability of precipitation)

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing)
        weatherText.write(str(int(data["hourly"][hoursAhead]["pop"]*100)) + " %", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, -weatherText_vertSpacing*2)
        weatherText.write("Rain", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # Rain

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing*2)
        if 'rain' not in data["hourly"][hoursAhead]:
            weatherText.write("--", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))
        else:
            weatherText.write(str(data["hourly"][hoursAhead]["rain"]["1h"]) + " mm", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.goto(weatherText_Description, -weatherText_vertSpacing*3)
        weatherText.write("Wind", align="right", font=("Verdana", weatherText_DescriptionFontSize, "bold")) # Wind

        weatherText.goto(weatherText_Data, -weatherText_vertSpacing*3)
        weatherText.write(str(data["hourly"][hoursAhead]["wind_speed"]) + " km/h", align="left", font=("Verdana", weatherText_DataFontSize, "bold"))

        weatherText.hideturtle()

        weatherDividerPen.pensize(3)

        weatherDividerPen.penup()
        weatherDividerPen.goto(0, -80)
        weatherDividerPen.color("white")
        weatherDividerPen.setheading(90)
        weatherDividerPen.pendown()
        weatherDividerPen.fd(160)
        weatherDividerPen.hideturtle()

    elif (mode == 1 and touchInBox(x, y, 0, 0, 200, 200)):
        mode = 0 # go back to clock mode
        weatherText.clear() # remove hourly details from screen
        weatherDividerPen.clear()

def update_forecast(data): 
    idImage_array = [""] * 12

    hourCursor = 0
    current_hour = int(time.strftime("%H"))
    if current_hour > 12:
        hourCursor = current_hour - 12
    elif current_hour == 0:
        hourCursor = 12
    else:
        hourCursor = current_hour
        
    for num in range(12):
        weather_id = data["hourly"][num]["weather"][0]["id"]
        hour_index = determine_hour_index(hourCursor, num)

        idImage_array[hour_index] = determine_weather_pictogram(weather_id)

    for image in idImage_array:
        wn.addshape(image)

    return hourCursor, idImage_array

def draw_clock(h, m, s, pen): # draw a clock using the pen i created
    pen.hideturtle()

    # Draw the hour hand
    pen.penup()
    pen.goto(0,0)
    pen.color("white")
    pen.setheading(90)
    angle = (h / 12) * 360 + (m/60) * 30
    pen.rt(angle)
    pen.pendown()
    pen.fd(100)

    # Draw the minute hand
    pen.penup()
    pen.goto(0,0)
    pen.color("white")
    pen.setheading(90)
    angle = (m / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(170)

    # Draw the second hand
    pen.penup()
    pen.goto(0,0)
    pen.color("red")
    pen.setheading(90)
    angle = (s / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(75)    

latitude = "52.3757341"
longtitude = "9.7594483"
api_key = "APIKEY"

url = "http://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=current,minutely,daily,alerts,flags&appid=%s&units=metric" % (latitude, longtitude, api_key)

weatherUpdatePeriod = 30 # update interval for the weather data in minutes

data = requests.get(url).json()

#print(data)

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

mode = 0 # 1 - hourly detail mode, 0 - analog clock face mode

hourlyTouchSize = 25 # determines radius for user touch when going into hourly detail mode

deg_to_radians = 0.0174533
radius = 210 # determines how big clock is
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

wn = turtle.Screen()
wn.bgcolor("black")
wn.screensize()
#wn.setup(width=600, height=600)
wn.setup(width = 1.0, height = 1.0) # Make fullscreen
wn.title("WeatherClock 0.0.0")
wn.tracer(0) # turns off the animation, so you can't see anything when it is drawing

# turtle.Screen().get‌​canvas()._root().over‌​rideredirect(True) # attempting to make borderless fullscreen

# create our drawing pen
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0) # 0 is fastest it can go
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

while True:

    h = int(time.strftime("%I"))
    m = int(time.strftime("%M"))
    s = int(time.strftime("%S"))
    hourCursor = 0

    if (m % weatherUpdatePeriod == 0 and s == 0):
        data = requests.get(url).json()

    if (mode == 0):
        draw_clock(h, m, s, pen)
        hourCursor, idImage_array = update_forecast(data)

        bg_hour1.shape(idImage_array[0])
        bg_hour2.shape(idImage_array[1])
        bg_hour3.shape(idImage_array[2])
        bg_hour4.shape(idImage_array[3])
        bg_hour5.shape(idImage_array[4])
        bg_hour6.shape(idImage_array[5])
        bg_hour7.shape(idImage_array[6])
        bg_hour8.shape(idImage_array[7])
        bg_hour9.shape(idImage_array[8])
        bg_hour10.shape(idImage_array[9])
        bg_hour11.shape(idImage_array[10])
        bg_hour12.shape(idImage_array[11])

    wn.update()

    # cursor / touch logic
    turtle.onscreenclick(get_mouse_click_coor) # this returns the coordinate of the press !
    time.sleep(1)
    pen.clear()

wn.mainloop() # if you don't do this, window will open and close immediately, should the the last line of your program
