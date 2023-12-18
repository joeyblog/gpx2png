# gpx2png

A handy tool that creates a preview png for the points in gpx files.
It uses OpenStreetMap API for background tiles.
Comes with a discord bot.

## Preview
Plain output

![preview](https://github.com/joeyblog/gpx2png/blob/main/samples/Spain_Zaragoza_-_Zaragoza_XXL_1_338.png?raw=true)

It will look like this in a Discord Embed.

![preview](https://github.com/joeyblog/gpx2png/blob/main/samples/embed_screenshot.png?raw=true)

Created for [Spain_Zaragoza_-_Zaragoza_XXL_1_338.gpx](https://github.com/joeyblog/gpx2png/blob/main/samples/Spain_Zaragoza_-_Zaragoza_XXL_1_338.gpx)
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

## Option variables
You can change the variables for velow items as you like.
- Zoom values (default is 17 to 13 depending the route size)
- Line color (RGBA, default is 26,133,255,255 = #1A85FF)
- Point color (RGBA, default is 0,255,17,255 =  #00FF11)
- Point outline color (RGBA, default is white)
- Start point color (RGBA, default is 255,0,35, 255)
- Line width (px)
- Point size (px)
- Map margin (meters)
- Walking speed (km/h) for time calculation
