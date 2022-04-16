import discord
import PIL
import io

from discord.ext import commands
from util import ImageConverter
from PIL import Image, ImageFilter


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(self.__class__.__name__ + " intialized.")

    @commands.Command
    async def vdop(self, ctx: commands.Context, image: ImageConverter=None):
        if image is None:
            image = await ImageConverter().image(ctx.message)
        image = Image.open(image).convert('L').convert('RGBA')
        pantera = Image.open('resources/pantera.png').convert('RGBA')
        vdop = Image.open("resources/vdop.png").convert('RGBA')
        pw, ph = pantera.width, pantera.height
        vw, vh = vdop.width, vdop.height
        if image.height < (ph + vh):
            newheight = round((ph + vh) * 1.75 + 20)
            newwidth = (newheight / image.height) * image.width
        elif image.width < (pw + vw):
            newwidth = round((pw + pw) * 1.75 + 20)
            newheight = (newwidth / image.width) * image.height
        else:
            newwidth, newheight = image.width, image.height
        image = image.resize((int(newwidth), int(newheight)))
        image.alpha_composite(pantera, (0, 0))
        image.alpha_composite(vdop, (image.width - vw, image.height - vh))
        # image.show()
        # buffer = io.BytesIO()
        # image.save(buffer, 'jpg')
        # image = discord.File(buffer, filename="vdop.jpg")
        # await ctx.send(file=image)
        im = io.BytesIO()
        image.save(im, 'PNG')
        im = im.getvalue()
        image = discord.File(io.BytesIO(im), filename='vdop.png')
        e = discord.Embed(title=f'Pantera - Vulgar Display of Power', color=0xFF0000)
        e.set_image(url='attachment://vdop.png')
        await ctx.send(file=image, embed=e)

    @commands.command()
    async def idiot(self, ctx, image: ImageConverter = None):
        if image is None:
            image = await ImageConverter().image(ctx.message)
        image = discord.File(image, filename='Image.png')
        await ctx.send(file=image)


    @commands.command()
    async def mogus_pallete(self, ctx, image: ImageConverter = None):
        if image is None:
            image = await ImageConverter().image(ctx.message)
        mogos = PIL.Image.load("resources/Mogos.png")
        # mogus_pallete = mogos.


def setup(bot):
    cog = Images(bot)
    bot.add_cog(cog)
