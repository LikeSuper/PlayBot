import discord
from discord.ext import commands
from config import settings
import json
import requests
from discord.utils import get
from PIL import Image, ImageFont, ImageDraw
import io
import os
import youtube_dl

bot = commands.Bot(command_prefix = settings['prefix'])
bot.remove_command('help')

embedColor = 0x000000

@bot.event
async def on_ready():
	await bot.change_presence(status = discord.Status.online, activity = discord.Game('.хелп'))

@bot.command()
async def хелп(ctx):
	emb = discord.Embed(color = embedColor, title="Команды")

	emb.add_field(name = '.хай', value = 'Приветствие!')
	emb.add_field(name = '.чистка количество-очищеных-сообщений', value = 'Удалить сообщения.')
	emb.add_field(name = '.кик учасник', value = 'Кикнуть учасника.')
	emb.add_field(name = '.бан учасник причина', value = 'Забанить учасника.')
	emb.add_field(name = '.лиса', value = 'Отправляет рандомную картинку лисы.')
	emb.add_field(name = '.заходи', value = 'Зайти в войс чат с пользователем который отправил данное сообщение.')
	emb.add_field(name = '.выйди', value = 'Выйти из войс чата с пользователем который отправил данное сообщение.')
	emb.add_field(name = '.осебе', value = 'Отправить карточку пользователя.')

	await ctx.send(embed = emb)

@bot.command()
async def хай(ctx):
	author = ctx.message.author
	await ctx.send(f'Хай, {author.mention}!')

@bot.command()
async def осебе(ctx):
	img = Image.new('RGBA', (400, 200), '#111111')
	url = str(ctx.author.avatar_url)[:-10]
	res = requests.get(url, stream=True)
	res = Image.open(io.BytesIO(res.content))
	res = res.convert('RGBA')
	res = res.resize((100, 100), Image.ANTIALIAS)
	img.paste(res, (15, 15, 115, 115))
	idraw = ImageDraw.Draw(img)
	name = ctx.author.name
	tag = ctx.author.discriminator
	headline = ImageFont.truetype('arial.ttf', size=20)
	undertext = ImageFont.truetype('arial.ttf', size=12)
	idraw.text((145, 15), f'{name}#{tag}', font=headline)
	idraw.text((145, 50), f'ID: {ctx.author.id}', font=undertext)
	img.save('user_card.png')
	await ctx.send(file = discord.File(fp = 'user_card.png'))

@bot.command()
async def заходи(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild = ctx.guild)
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()

@bot.command()
async def музыка(ctx, url: str):
	song_there = os.path.isfile('song.mp3')
	try:
		if song_there:
			os.remove('song.mp3')
			print("Delete")
	except PermissionError:
		print('No delete')
	await ctx.send('Сечас все будет!')
	voice = get(bot.voice_clients, guild = ctx.guild)
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192'
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print('Music download')
		ydl.download([url])
	for file in os.listdir('./'):
		if file.endswith('.mp3'):
			name = file
			print('Rename file')
			os.rename(file, 'song.mp3')
	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'{name} stop'))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07
	song_name = name.rsplit('-', 2)
	await ctx.send(f'Играет музыка {song_name[0]}.')

@bot.command()
async def выйди(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild = ctx.guild)
	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()


@bot.command()
@commands.has_permissions(administrator = True)
async def чистка(ctx, amount = 100):
	await ctx.channel.purge(limit = int(amount) + 1)
	await ctx.send("Готово! Удалено " + amount + " сообщений.")

@bot.command()
@commands.has_permissions(administrator = True)
async def кик(ctx, member: discord.Member, *, reason = None):
	await member.kick(reason = reason)
	await ctx.send(f"Пользователь {member.mention} успешно кикнут!")

@bot.command()
@commands.has_permissions(administrator = True)
async def бан(ctx, member: discord.Member, *, reason = None):
	await member.ban(reason = reason)
	await ctx.send(f"Пользователь {member.mention} успешно забанен!")

@bot.command()
async def лиса(ctx):
    response = requests.get('https://some-random-api.ml/img/fox')
    json_data = json.loads(response.text)
    embed = discord.Embed(color = embedColor, title = 'Лиса')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

bot.run(settings['token'])