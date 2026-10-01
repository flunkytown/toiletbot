import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os
import atexit
import aiohttp
import io
import asyncio

load_dotenv()

INTENTS = discord.Intents.all()
BOTTOKEN = os.getenv("TOKEN")
# ALEXQUOTES = [
#     "I'm so unbelievably sorry",
#     "she was wearing a short skirt",
#     "I'M NOT GAY!!!",
#     "Imagine being this gay bruh I could never \n\n im on the toilet",
#     "coke is not niche",
#     "it was made of bats"  
# ]

INTENTS.message_content = True
NAMES = os.getenv("NAMES", "").split(",")

bot = commands.Bot(command_prefix="#", intents=INTENTS)

lobotomised_users = [
    #userid, timer length

]

#-----------------------------------------------------------------------------------------
#events
#-----------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f"toilet town aint ready for me")
    print("------")
    await bot.get_channel(1535249437176102972).send("whaddup toilet town")

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id) or await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    
    for reaction in message.reactions:
        if not isinstance(reaction.emoji, str) and reaction.emoji.name == 'ralsei':
            if reaction.count == 3:
                target_channel = bot.get_channel(1536693749810200576) or await bot.fetch_channel(1536693749810200576)
                
                embed = discord.Embed(
                    description=message.content, 
                    color=discord.Color.gold(),
                    timestamp=message.created_at
                )
                embed.set_author(
                    name=message.author.display_name, 
                    icon_url=message.author.display_avatar.url
                )

                if message.attachments:
                    for attachment in message.attachments:
                        if attachment.content_type and attachment.content_type.startswith('image/'):
                            embed.set_image(url=attachment.url)
                            break
                
                await target_channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.guild is None:
        return

    if any(user_id == message.author.id for user_id, _ in lobotomised_users):
        try:
            webhooks = await message.channel.webhooks()
            webhook = discord.utils.get(webhooks, name="lobotomy")
            if webhook is None:
                webhook = await message.channel.create_webhook(name="lobotomy")

            fbacklobotomessages = [
                "gurrghh",
                "bleghhhhaeh",
                "RaErgjh",
                "oughhh.g..h...g",
                "buhbuh",
                "blblbllblblb",
                "pl",
                "wtrfvbfhnb",
                "whats good toilet town"
            ]

            def lobotomise(message):
                divmessage = message.content.split()
                if len(divmessage) <= 3:
                    divmessage = random.choice(fbacklobotomessages)
                else:
                    for i in range(len(divmessage)):
                        random.shuffle(divmessage)
                    divmessage = " ".join(divmessage)
                return divmessage

            

            await webhook.send(
                content=lobotomise(message),
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                files=[await attachment.to_file() for attachment in message.attachments],
                allowed_mentions=discord.AllowedMentions.none(),
            )
            await message.delete()
        except discord.Forbidden:
            await message.channel.send("no perms broat")
        except discord.HTTPException:
            pass

    await bot.process_commands(message)
        
#-----------------------------------------------------------------------------------------
#commands
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- hes supersonic!!! i think hes supersoooonicc!!! -------------------------------------------------------------------------------------


@bot.command()
async def whoareyou(ctx):
    """about me"""
    await ctx.send("i am toilet bot and i LOVE you")

@bot.command()
async def whatexactlyisilarilisteningtorightnow(ctx):
    """what is he listening to right now"""
    target = ctx.guild.get_member(756720223519768649) or await ctx.guild.fetch_member(756720223519768649)

    response_msg = "hes killed himself probably" 
    file_to_send = None

    if target is not None:
        for activity in target.activities:
            if isinstance(activity, discord.Spotify):
                response_msg = f"ilari is listening to *{activity.title}* from the album *{activity.album}* by *{activity.artist}*"
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(activity.album_cover_url) as resp:
                        if resp.status == 200:
                            image_bytes = await resp.read()

                            file_to_send = discord.File(io.BytesIO(image_bytes), filename="album.png")
                break 

    if file_to_send:
        await ctx.send(f"{response_msg}", file=file_to_send)
        await ctx.send("ok love you bye")
    else:
        await ctx.send(f"{response_msg}\n\n ok love you bye")

@bot.command()
async def lobotomise(ctx, timer: int, user: discord.Member = None):
    """lobotmise for a given amount of seconds"""
    if timer < 1:
        await ctx.send("timer aint 1 second BUDDY")
        return
    if user is None or user == "@everyone" or user == "@here":
        user = ctx.author
    lobotomised_users.append((user.id, timer))
    await ctx.send(f"{user.display_name} lobotmised for {timer} seconds. okay? okay. love you. MWAH kiss kiss bye bye teehee")

    await asyncio.sleep(timer)
    lobotomised_users[:] = [
        entry for entry in lobotomised_users
        if entry[0] != user.id
    ]

@bot.command()
async def kissmarrykill(ctx):
    """kiss marry kill"""
    names = random.sample(NAMES, 3)
    if ctx.author.id == 756720223519768649:
        await ctx.send(f"ok here r youre three random names: {', '.join(names)} \nok now choose who to highfive who to marry and who to kill ok stupid chud who doesnt like kissing hahah")
    else:
        await ctx.send(f"ok here r youre three random names: {', '.join(names)} \nok now choose who to kiss who to marry and who to kill ok love you MWWWWAH")
    #await ctx.send("this command dont do anything else lmao")


        
bot.run(BOTTOKEN)
