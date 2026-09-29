import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import ollama
import os
import atexit
import aiohttp
import io

load_dotenv()

INTENTS = discord.Intents.all()
MODEL = "qwen3:8b"
BOTTOKEN = os.getenv("TOKEN")
ALEXQUOTES = [
    "I'm so unbelievably sorry",
    "she was wearing a short skirt",
    "I'M NOT GAY!!!",
    "Imagine being this gay bruh I could never \n\n im on the toilet",
    "coke is not niche",
    "it was made of bats"  
]

INTENTS.message_content = True
bot = commands.Bot(command_prefix="#", intents=INTENTS)


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
        await ctx.send(f"{response_msg}\n\n ok love you bye", file=file_to_send)
    else:
        await ctx.send(f"{response_msg}\n\n ok love you bye")
        
@bot.command()
async def alexgpt(ctx, prompt: str):
    """talk to the real alex"""
    if not prompt:
        await ctx.send("no prompt")
        return
    response = "yo shit failed to go thru sorry"
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"You are Alex. You are casual, a little stupid, oft unintentionally funny, and somewhat nonsensical. You've said many funny things, for example: {ALEXQUOTES}. ONE SENTENCE ONLY."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            top_p=1.0,
            temperature=1.4,
            max_completion_tokens=200
        )
    
    except Exception as e:
        response = f"yo shit failed to go thru.... sorry..... please dont hit me..... {str(e)}"
    
    await ctx.send(response.choices[0].message.content)
    


bot.run(BOTTOKEN)
