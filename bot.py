import asyncio
from string import printable
from PIL import Image, ImageFilter


import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import find, get

bot = Bot(command_prefix='?')


@bot.event
async def on_ready():
    print(f'Client logged in as {bot.user.name}')
    print(f'Client ID {bot.user.id}')


@bot.event
async def on_member_join(member: discord.Member):
    """Welcomes new arrivals and changes their nickname if a character in it isn't default ASCII."""
    # TODO: Stop using system_channel as message destination.
    # TODO: Add some more functionality (auto-roles, anti-ban evasion)
    channel = member.guild.system_channel
    for character in member.name:
        if character not in printable:
            await channel.send(f"Due to non-ascii character \"{character}\" in your name we've changed it to Rule 7.")
            await member.edit(reason='Rule 7', nick='Rule 7')
    await channel.send(f'{member.mention} has joined {member.guild}!')


#@bot.event
#async def on_message(message):
#    print(message)
#    if message.author.id == 332892446985814026:
#        return
#    if message.attachments:
#        for atch in message.attachments:
#            await message.channel.send(atch.filename)
#    await message.channel.send(message)

@bot.event
async def on_member_remove(member: discord.Member):
    channel = member.guild.system_channel
    await channel.send(f'{member.mention} has left us.')


@bot.command()
async def set_channel(ctx, channel_name: str):
    """Set's the servers `system_channel`. This is currently used to send messages upon client events."""
    # TODO: Change this function to not use the system_channel as a destination to welcomes, since it might
    #  (and probably is
    # being used) be used for other purposes.
    # TODO: Set up some sort of options file so we don't have to call this every time the bot is launched.
    find_channel = discord.utils.get(ctx.message.guild.text_channels, name=channel_name)
    try:
        await ctx.message.guild.edit(system_channel=find_channel)
    except:
        await ctx.message.channel.send('I do not have the required permissions.')
        return
    print(ctx.message.guild.system_channel)
    await ctx.message.channel.send(f'New default channel: {find_channel}')


@bot.command()
async def aesthetics(ctx, *args):
    """Novelty command and Ned's proudest work. It mainly serves as a "Hello World!" for Ned."""
    channel = ctx.message.channel
    decorated_text = ''.join([f' _`{character}`_ ' for character in ' '.join(list(args))])
    await channel.send(decorated_text)


@bot.command()
async def iter(ctx):
    messages = ctx.message.channel.history(limit=None)
    channel = ctx.message.channel
    authors = {}
    c = 0
    async for message in messages:
        c += 1
        if message.author.name not in authors:
            authors[message.author.name] = 1
        else:
            authors[message.author.name] += 1
    await channel.send(f'Found {c} messages')
    await channel.send(f'{authors}')


@bot.command()
async def needsmoreedge(ctx):
    """"Adds much needed edge to the last posted image (still kinda buggy bear with me"""
    messages = ctx.message.channel.history(limit=2)
    async for message in messages:
        if message.attachments:
            for attch in message.attachments:
               #This kinda takes an image at random, I think I'll keep the history limit=2 for the momment
               #It seems to pick the lastest image first. If you call the command again it'll go to the next one.
               #TODO: Figure out a way to only take the last image.
                await attch.save('some_file.jpeg')
    image = Image.open('some_file.jpeg')
    if image:
        edge_image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        edge_image = edge_image.save('returned_file.jpeg')
        await ctx.message.channel.send(file=discord.File('returned_file.jpeg'))



@bot.command()
async def quit(ctx):
    """Basic quit command."""
    # TODO: Make it so the admin of any given guild is allowed to use this and have a command that let's them set
    # quit permission for other users.
    if ctx.message.author.id != 138001563158446081:
        await ctx.message.channel.send("I can't let you do that..")
        return
    await ctx.message.channel.send('Quitting...')
    await bot.logout()


bot.run('token')
# I like keeping my tokens here
