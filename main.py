import discord
import os

from discord.ext import commands

bot = commands.Bot('?', intents=discord.Intents.all())

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

bot.run('OTAxNTE5OTcwMDI0OTgwNTIw.YXRD5g.YOfK21LZar_Layy4fFLVFa_mJ4A')
