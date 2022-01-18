import requests
import datetime
import time
import discord
from lxml import html

client = discord.Client()
client.run("VOTRE TOKEN ICI")

@client.event
async def on_ready():
    print("Le bot est prêt !")



serv = str(51)
now = datetime.datetime.now()

headers = {
    'authority': 'metamob.fr',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://metamob.fr/kralamoure',
    'accept-language': 'fr-FR,fr;q=0.9',
    'cookie': 'PHPSESSID=12c70492ab1ab94352bda64fa57b58de',
}

params = (
    ('date', str(now.year).zfill(4)+'-'+str(now.month).zfill(2)+'-'+str(now.day).zfill(2)),
    ('serveur', serv),
)


def check_event():
    response = requests.get('https://metamob.fr/kralamoure', headers=headers, params=params)

    webpage = html.fromstring(response.content)
    list_of_url = webpage.xpath("//a/@href[contains(., 'evenement?id=')]")

    for id_url in list_of_url:
        time.sleep(2)
        rep_event = requests.get('https://metamob.fr'+id_url, headers=headers, params=params)
        d = rep_event.text.split('<table class="table table-bordered table-striped">\r\n\t\t\t<tbody>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t<td>\r\n\t\t\t\t\t\t<p>Date</p>\r\n\t\t\t\t\t</td>\r\n\t\t\t\t\t<td>\r\n\t\t\t\t\t\t<p>')[1].split("</p>")[0]
        d = d.split("/")
        print(d)
        if (d[0] == str(now.day).zfill(2)) and (d[1] == str(now.month).zfill(2)) and (d[2].split(" ")[0] == str(now.year).zfill(4)[2:]) and (d[2].split(" ")[1].split(":")[0] == str(now.hour).zfill(2) or str(now.hour+1).zfill(2)):
            return True


