# app id: 1001134833189257297
# perm integer: 67584

import discord
import crawler
import bdchan_crawler
import movie



token = open("token.txt", "r").read()

client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '!khobor' in message.content.lower():
        topic = message.content.lower().split(' ')[1]
        urls = crawler.crawl(topic)
        for url in urls:
            try:
                await message.channel.send(url.text)
            except AttributeError:
                await message.channel.send(url)
    if '!bdchan' in message.content.lower():
        links = bdchan_crawler.crawl()
        for url in links:
            await message.channel.send(url)
    if '!movie' in message.content.lower():
        query = ''
        words = message.content.lower().split(' ')
        for c in range(1, len(words)):
            query += words[c]
            query += ' '
        movies = movie.get_rec(query)
        for data in movies:
            await message.channel.send(
                f"```{data['title']} \n {data['release_date']} \n tmdb rating:{data['rating']}  \n {data['overview']}```"
            )




client.run(token)
