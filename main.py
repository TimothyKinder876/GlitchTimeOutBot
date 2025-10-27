import discord
from email import message
from discord.ext import commands
import logging 
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename=os.path.join(os.getcwd(), 'glitchbot.log'),encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

glitchvals = ["glitch", "gl1tch", "gljtch", "glytch", "glftch", "glftch", "glvtch", "glxtch"]

bot = commands.Bot(command_prefix='!', intents=intents)
logger = logging.getLogger('glitchbot')
logging.getLogger('glitchbot').addHandler(handler)
logging.getLogger('glitchbot').setLevel(logging.DEBUG)

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
              
            logger.info(f"Deleted message in {message.channel}: {message.content} by {message.author}")
        except discord.Forbidden:
            logger.error(f"Permission error: Cannot delete message in {message.channel}")
        except discord.HTTPException as e:
            logger.error(f"Failed to delete message: {e}")

    await bot.process_commands(message)
   
   #replace fuck
    if "fuck" in message.content.lower():
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} WE do NOT USE that FUCKING language HERE you FUCKING RETARD.")
            logger.info(f"Deleted message in {message.channel}: {message.content} by {message.author}")
        except discord.Forbidden:
            logger.error(f"Permission error: Cannot delete message in {message.channel}")
        except discord.HTTPException as e:
            logger.error(f"Failed to delete message: {e}")
   



@bot.event 
async def on_message_delete(message):
    logger.info(f"Message deleted in {message.channel}: {message.content} by {message.author}")

if __name__ == "__main__":
    asyncio.run(main())