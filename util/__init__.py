import discord
import asyncio
import PIL
import aiohttp
import re

from discord.ext import commands
from io import BytesIO


async def image_url_to_pil(url: str):
    async with aiohttp.ClientSession as session:
        async with session.get(url) as r:
            img = BytesIO(await r.content.read())
    return PIL.Image.load(img)


class ImageConverter(commands.Converter):
    '''
    Convert any argument into an image if possible.
    This will not work with images attached to the message.
    If you want it to work with images on the message,
    add =None after the argument, then in the function:
        if arg is None:
            arg = await ImageConverter().image(ctx.message)
    '''

    async def convert(self, ctx, argument):
        r = re.search(r'<a?:\w+:\d{18}>', argument)
        if r:
            emoji = await commands.EmojiConverter().convert(ctx, argument)
            asset = emoji.url_as(format='png')
            data = BytesIO(await asset.read())
            return data
        elif re.search(r'https?://.+\.(png|jpg|jpeg)', argument):
            async with aiohttp.ClientSession() as session:
                async with session.get(argument) as resp:
                    if resp.status == 200:
                        return BytesIO(await resp.read())
        else:
            try:
                user = await commands.MemberConverter().convert(ctx, argument)
            except commands.MemberNotFound:
                await ctx.send(f'`{argument}`')
            else:
                avatar = user.avatar_url_as(format='png')
                data = BytesIO(await avatar.read())
                return data

    async def image(self, message):
        if len(message.attachments) > 0:
            attachment = message.attachments[0]
            if attachment.height is not None:
                return BytesIO(await attachment.read())
        else:
            user = message.author
            avatar = user.avatar_url_as(format='png')
            data = BytesIO(await avatar.read())
            return data


if __name__ == "__main__":
    im = image_url_to_pil("https://testimages.org/img/testimages_screenshot.jpg")
    im.save("Test Image.jpg")
