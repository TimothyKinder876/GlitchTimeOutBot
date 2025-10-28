import discord
from email import message
from discord.ext import commands
import logging 
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import asyncio
#import twitchGet

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename=os.path.join(os.getcwd(), 'glitchbot.log'),encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

glitchvals = ["glitch", "gl1tch", "gljtch", "glytch", "glftch", "glftch", "glvtch", "glxtch"]
glitchbotnames = ["glitchtimeoutbot", "glitch timeout bot", "glitch_timeout_bot", "glitchbot", "bot"]
sixsivens = ['67', "sixty seven", "six seven", "sixseven", "six-seven", '6 7', "6seven", "six7", "six7", "6seven"]
krabbyID = 474632123291140098
illuID = 662719984627089479
clankerresponse = "https://media.discordapp.net/attachments/1071573041554923689/1073798575445790760/image0-136.gif?ex=6900d89a&is=68ff871a&hm=41e9193d2ad82d7e777962d52fb86cb3990da7c798986aa5bbc2f298c136b5ec&"
rapemember = "https://cdn.discordapp.com/attachments/1185392185810620469/1432540251515125830/attachment-1-2-1.gif?ex=69016c93&is=69001b13&hm=a1dde9a7ecdd94af4d052a2b4b20c5416bca463ba013eaa069500a958ba4f888&"
sixsevenresponse = "https://cdn.discordapp.com/attachments/727462539935481957/962769524673888326/d65407e9b004361d68c9f7e4dcb037f5a92d4c42b2f5075b48faa8feadf38bd7_1.gif.gif?ex=6901007e&is=68ffaefe&hm=488f3610bd1e5dea598b1cb00f45d99f64559dc70fa25f733e3d4c1e3ec71f42&"
catgif = "https://tenor.com/view/thousand-yard-stare-cat-gif-10000743455859339871"
GUILD_ID = discord.Object(id=1185392185810620466)

COOLDOWN = timedelta(minutes=10)
last_response_times = {}

bot = commands.Bot(command_prefix='!', intents=intents)
logger = logging.getLogger('glitchbot')
logging.getLogger('glitchbot').addHandler(handler)
logging.getLogger('glitchbot').setLevel(logging.DEBUG)

"""async def is_streamer_live(interaction: discord.Interaction, streamer: str):
    stream = twitchGet.is_streamer_live(streamer)
    thumbnail = stream["thumbnail_url"].replace("{width}", "800").replace("{height}", "500")
    print(thumbnail)
    embed = discord.Embed(title= f"🟢 {stream["user_name"]} IS LIVE 🟢", description=stream["title"], url=f"https://twitch.tv/{stream["user_name"].lower()}", color=discord.Color.blurple())
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="Game", value= stream["game_name"])
    await interaction.response.send_message(embed=embed)"""

async def _shutdown_on_enter():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, input, "Press Enter to shut down the bot...\n")
    await bot.close()

async def main():
    async with bot:
        asyncio.create_task(_shutdown_on_enter())
        await bot.start(token)

async def timeout_member(message: discord.Message, member: discord.Member, seconds: int, *, reason: str = "NONE"):
    # discord.Member.timeout expects an absolute 'until' datetime (UTC), not a duration
    until = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    try:
        # Some discord.py builds expect the 'until' argument positionally (positional-only).
        # Try calling positionally first to avoid "positional-only arguments passed as keyword" errors.
        await member.timeout(until, reason=reason)
        await message.channel.send(f"Timed out {member.mention} for {seconds}s. Reason: {reason}")
    except discord.Forbidden:
        await message.channel.send("I don't have permission to timeout that user.")
    except discord.HTTPException as e:
        await message.channel.send(f"Failed to timeout user: {e}")

@bot.event
async def on_ready():
    print(f"Bot Ready: {bot.user.name}; {bot.user.id}")

@bot.event
async def on_message(message):
    # avoid reacting to other bots (including itself)
    if message.author.bot:
        return

    # Delete by exact content
    if any(word in message.content.lower() for word in glitchvals) and "@" in message.content:
        try:
            await message.delete()
            await timeout_member(message, message.author, 60, reason="Being Fat and Gay")
            await message.channel.send(f"{rapemember}")
              
            logger.info(f"Deleted message in {message.channel}: {message.content} by {message.author}")
        except discord.Forbidden:
            logger.error(f"Permission error: Cannot delete message in {message.channel}")
        except discord.HTTPException as e:
            logger.error(f"Failed to delete message: {e}")


    await bot.process_commands(message)
   
   #replace fuck
    if "sex" in message.content.lower() and any(word in message.content.lower() for word in glitchbotnames):
        await message.channel.send(f"{catgif}")
        await message.channel.send(f"{message.author.mention} No")
        return

    if "fuck" in message.content.lower():
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} WE do NOT USE that FUCKING language HERE you FUCKING RETARD.")
            logger.info(f"Deleted message in {message.channel}: {message.content} by {message.author}")
        except discord.Forbidden:
            logger.error(f"Permission error: Cannot delete message in {message.channel}")
        except discord.HTTPException as e:
            logger.error(f"Failed to delete message: {e}")
            return

    if any(word in message.content.lower() for word in sixsivens):
        await message.channel.send(f"{message.author.mention} unfunny moron detected, deploying xk7 approved countermeasures.")
        await message.channel.send(f"{sixsevenresponse}")
        return

    if "clanker" in message.content.lower():
        await message.channel.send(f"{clankerresponse}")
        return

    if message.author.id == krabbyID and any(word in message.content.lower() for word in glitchbotnames):
        now = datetime.now(timezone.utc)
        last = last_response_times.get(message.author.id)

        # Check if cooldown expired
        if last is None or now - last >= COOLDOWN:
            last_response_times[message.author.id] = now
            await message.channel.send("fatty")
        else:
            # Cooldown active
            remaining = COOLDOWN - (now - last)
            minutes = int(remaining.total_seconds() // 60) + 1
            await message.channel.send(f"Please wait {minutes} more minute(s) before I respond again.")
            return
        
    if any(word in message.content.lower() for word in glitchbotnames):
        try:
           await message.channel.send(f"{message.author.mention} what do you want.")
           logger.info(f"responded to retards in {message.channel}")
        except discord.Forbidden:
            logger.error(f"Permission error: Cannot send message in {message.channel}")
        except discord.HTTPException as e:
            logger.error(f"Failed to send message: {e}")
            return

@bot.event 
async def on_message_delete(message):
    logger.info(f"Message deleted in {message.channel}: {message.content} by {message.author}")

if __name__ == "__main__":
    asyncio.run(main())