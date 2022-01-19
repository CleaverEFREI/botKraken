import discord
import requests
import datetime
import time
import os
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from lxml import html


bot = commands.Bot(command_prefix="!", description = "Bot Krala")
@bot.event
async def on_ready():
	print("Ready !")


@bot.command()
async def krala(ctx, serv_id, role_name):    
    while True:
        Krala = get(ctx.guild.roles, name=role_name)
        serv = str(serv_id)
        now = datetime.datetime.now()

        headers = {
            'authority': 'metamob.fr',
            'referer': 'https://metamob.fr/kralamoure',
        }

        params = (
            ('date', str(now.year).zfill(4)+'-'+str(now.month).zfill(2)+'-'+str(now.day).zfill(2)),
            ('serveur', serv),
        )

        response = requests.get('https://metamob.fr/kralamoure', headers=headers, params=params)

        webpage = html.fromstring(response.content)
        list_of_url = webpage.xpath("//a/@href[contains(., 'evenement?id=')]")

        for id_url in list_of_url:
            time.sleep(2)
            rep_event = requests.get('https://metamob.fr'+id_url, headers=headers, params=params)
            d = rep_event.text.split('<table class="table table-bordered table-striped">\r\n\t\t\t<tbody>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t<td>\r\n\t\t\t\t\t\t<p>Date</p>\r\n\t\t\t\t\t</td>\r\n\t\t\t\t\t<td>\r\n\t\t\t\t\t\t<p>')[1].split("</p>")[0]
            d = d.split("/")
            if (d[0] == str(now.day).zfill(2)) and (d[1] == str(now.month).zfill(2)) and (d[2].split(" ")[0] == str(now.year).zfill(4)[2:]) and (d[2].split(" ")[1].split(":")[0] == str(now.hour).zfill(2) or d[2].split(" ")[1].split(":")[0] == str(now.hour+1).zfill(2)) :
                time_open = d[2].split(" ")[1]
                await ctx.send(f"{Krala.mention} Ouverture prevue aujourd'hui à {time_open}")
        time.sleep(10)


load_dotenv(dotenv_path="config")
bot.run(os.getenv("TOKEN"))