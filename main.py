import discord
from discord.ext import commands
from config import settings
import json
import requests
from discord.utils import get
from PIL import Image, ImageFont, ImageDraw
import io
import os

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

	await ctx.send(embed = emb)

@bot.command()
async def хай(ctx):
	author = ctx.message.author
	await ctx.send(f'Хай, {author.mention}!')

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