import discord
import requests
import datetime
import time
import os
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from lxml import html

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix="!", description="Bot Krala")


@bot.event
async def on_ready():
    print("Ready !")


@bot.command()
async def krala(ctx, serv, role_name, alarmtime = 2, checktime=1):
    """
    Commande pour lancer le bot sur le salon souhaité 
    serv : serveur de jeu cible
    role_name : nom 
    alarmtime : en heure
    checktime : en heure
    """
    checktime = checktime*60*60
    while True:
        Krala = get(ctx.guild.roles, name=role_name)
        now = datetime.datetime.now()

        headers = {
            "HTTP-X-APIKEY": os.getenv("API"),
        }

        params = (
            (
                "date_debut",
                str(now.year).zfill(4)
                + "-"
                + str(now.month).zfill(2)
                + "-"
                + str(now.day).zfill(2),
            ),
            (
                "date_fin",
                str(now.year).zfill(4)
                + "-"
                + str(now.month).zfill(2)
                + "-"
                + str(now.day + 1).zfill(2),
            ),
            ("serveur", serv),
        )

        response = requests.get(
            "https://api.metamob.fr/kralamoures", headers=headers, params=params
        )

        for rep in response.json():
            req_crea = requests.get(
                "https://api.metamob.fr/utilisateurs/" + rep["createur"],
                headers=headers,
            )
            d = rep["date"]
            d = d.split("-")
            d = d[:2] + d[2].split(" ")
            if (
                (d[2] == str(now.day).zfill(2))
                and (d[1] == str(now.month).zfill(2))
                and (d[0] == str(now.year).zfill(4))
                and (now.hour+alarmtime>int(d[3].split(":")[0]))
                and (now.hour<=int(d[3].split(":")[0]))
            ):
                await ctx.send(
                    f"""{Krala.mention}
                    :pushpin: Ouverture prévue bientôt ! :pushpin: 
                    :alarm_clock:  {d[3]} 
                    :pencil:  {rep['nombre_utilisateurs']} personnes inscrites
                    :notepad_spiral:  {rep['description']}
                    Pseudo créateur: {req_crea.json()['pseudo']}, Contact : {req_crea.json()['contact']}
                    https://metamob.fr/kralamoure/evenement?id={rep['id']}"""
                )
        time.sleep(checktime)


bot.run(os.getenv("TOKEN"))
