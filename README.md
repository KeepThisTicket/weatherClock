# Eli's weatherClock #

An digital analog clock but instead of showing the hours, the clock shows the weather at that hour of the day. So instead of showing 1, it will show the weather forecast for 1AM/PM. Click on the hour for more detailed information such as wind, precipitation and more. Once in the detailed view, simply click the center again to return to the analog clock face.

[Video demo](https://youtu.be/qGV7r33nt4c)

You will need to:
- Acquire Pi Zero W and a Pimoroni 4" touchscreen
- Install a full Raspbian distribution (not lite)
- Install python ```pynput``` module. Pynput needs X11 which is on full Raspbian distributions.
- Obtain your own [OpenWeatherMap](https://openweathermap.org/) API key from and change your location to where you are
- Follow the ["Setting up your Raspberry Pi"](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-hyperpixel-4) instructions to setup the Pi to push display to the Pimoroni screen
- Print the two parts of the case (files found in repo). CAD found [here](CAD files for enclosure located [here](https://cad.onshape.com/documents/a04351220114f9397820b114/w/0854a09a8bd19b8df2167e54/e/af44268ed043f94be60c93c6)
---

NOTE: I have experienced an issue with running this on the Pi Zero W - after a few days, the program starts to get super slow and at some point the program closes itself. A few contributors have provided some potential solutions and these are under test.

For any questions/comments - you can open an issue or contact me directly at k3vinwu25@gmail.com !
---
If you want you can create autostart script (for xfce4 you should put it into ~/.config/autostart) with the contents like this:

cd  /home/plotn/github/weatherClock/
while :
do
  if test "$(ps aux | grep python3 | grep weather | wc -l)" -eq "0"
  then
    python3 ./weatherClock.py & disown
  else
    echo "already started"
  fi
  sleep 5
done
