import discord
import io
from PIL import Image
import gpx2png
from dotenv import load_dotenv
import os

#load bot token from /env file placed in the same directory as this file.
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #this is for previewing already sent files. just reply "check" to the message with the gpx files
    if(message.content =="check"):
        channel = message.channel
        replied = await channel.fetch_message(message.reference.message_id)
        if len(replied.attachments) > 0:

            async with channel.typing():
                await message.delete()
                await replied.delete()
                total = str(len(replied.attachments))
                print("found "+total+" attachments")
                count = 1
                for attachment in replied.attachments:
                    print(str(count)+"/"+total + " files")
                    count+=1
                    file_url = attachment.url
                    filename = file_url.split('/')[-1]
                    print(filename)

                    if file_url.lower().endswith('.gpx'):
                        result = gpx2png.convert(file_url)
                        image_data = result["data"]
                        distance = result["total"]
                        time = result["walk"]
                        if(distance > 1000):
                            distance = '{:.2f}'.format(distance / 1000) + "km"
                        else:
                            distance = '{:.0f}'.format(distance) + "m"
                        location = result["location"]
                        address = location["city"]+" "+location["flag"]
                        embed = discord.Embed(title="GPX Overview", description=f"[{filename}]({file_url})")
                        embed.add_field(name="Address",value=address, inline=False)
                        embed.add_field(name="Total Distance",value=distance, inline=True)
                        embed.add_field(name="Walking time",value=time, inline=True)
                        embed.set_image(url="attachment://gpx_image.png")
                        file = discord.File(fp=image_data, filename="gpx_image.png")
                        await channel.send(embed=embed, file=file)
        print("done")

    #if gpx file is sent, bot will make a preview
    if len(message.attachments) > 0:
        total = str(len(message.attachments))
        print("found "+total+" attachments")
        await message.delete()
        async with message.channel.typing():
            count = 1
            for attachment in message.attachments:
                print(str(count)+"/"+total + " files")
                count+=1
                file_url = attachment.url
                filename = file_url.split('/')[-1]
                print(filename)
                if file_url.lower().endswith('.gpx'):
                    result = gpx2png.convert(file_url)
                    image_data = result["data"]
                    distance = result["total"]
                    time = result["walk"]
                    if(distance > 1000):
                        distance = '{:.2f}'.format(distance / 1000) + "km"
                    else:
                        distance = '{:.0f}'.format(distance) + "m"
                    location = result["location"]
                    address = location["city"]+" "+location["flag"]
                    embed = discord.Embed(title="GPX Overview", description=f"[{filename}]({file_url})")
                    embed.add_field(name="Address",value=address, inline=False)
                    embed.add_field(name="Total Distance",value=distance, inline=True)
                    embed.add_field(name="Walking time",value=time, inline=True)
                    embed.set_image(url="attachment://gpx_image.png")
                    file = discord.File(fp=image_data, filename="gpx_image.png")
                    print("sending embed")
                    await message.channel.send(embed=embed, file=file)
        print("done")

#run
client.run(TOKEN)
