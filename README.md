# gpx2png

A tool that creates a preview png for the points in gpx files.
Comes with a discord bot.

## Requirement
- diccord.py
- gpxpy
- geopy
- pillow
- dotenv
- emoji

## How to use
Method 1: Make .env file and put your token as BOT_TOKEN, then run bot.py. The bot will be triggered if you
  - send gpx file(s), or
  - reply "check" to the already sent message with gpx file(s)

Method 2: Modify gpx2png.py and load local file without the bot. I put some comments in the source for this method.

## Options
I haven't put the option variable together, but you can change them as you like.
- Zoom values (default is 17 to 13 depending the route size)
- Line color (RGBA, default is 26,133,255,255 = #1A85FF)
- Point color (RGBA, default is 0,255,17,255 =  #00FF11)
- Point outline color (RGBA, default is white)
- Start point color (RGBA, default is 255,0,35, 255)
- Line width (px)
- Point size (px)
- Map margin (meters)
- Walking speed (km/h) for time calculation
