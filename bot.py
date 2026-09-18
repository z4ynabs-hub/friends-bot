import discord
from discord.ext import commands
import datetime

# ١. دەسەڵاتەکانی بۆتەکە
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="", intents=intents)

# ئایدی کەناڵی چاتی گشتی (تەنها ژمارەکە بەبێ لینک)
WELCOME_CHANNEL_ID = 1448989203508629544 


@bot.event
async def on_ready():
    print(f'بۆتەکە بە سەرکەوتوویی چالاک بوو وەک: {bot.user}')


# ---------------------------------------------------------
# ٢. سیستەمی بەخێرهاتن (Welcome GIF)
# ---------------------------------------------------------
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        try:
            file = discord.File("welcome.gif", filename="welcome.gif")
            await channel.send(
                content=f"بەخێر بێیت {member.mention}! ✨",
                file=file
            )
        except Exception as e:
            print(f"کێشەیەک لە بەخێرهاتن ڕوویدا: {e}")


# ---------------------------------------------------------
# ٣. کۆماندەکان (Shetika, Mute, Ban) بە Replay یان Tag
# ---------------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.strip().split()
    if not msg:
        return

    command = msg[0].lower()

    # --- (shetika 100) ---
    if command == "shetika" and len(msg) == 2 and msg[1].isdigit():
        if not message.author.guild_permissions.manage_messages:
            await message.channel.send(
                f"❌ {message.author.mention} تۆ ڕۆڵت نییە! بڕۆ بە ئاڤلۆ بڵێ.",
                delete_after=6
            )
            return

        amount = int(msg[1]) + 1
        await message.channel.purge(limit=amount)
        await message.channel.send(f"✅ {msg[1]} پەیام سڕێنرانەوە.", delete_after=3)
        return

    # --- (mute بە ڕەیپڵای یان تاگ) ---
    if command == "mute":
        if not message.author.guild_permissions.moderate_members:
            await message.channel.send(
                f"❌ {message.author.mention} تۆ ڕۆڵت نییە تا کەس میوت بکەیت! بڕۆ بە ئاڤلۆ بڵێ.",
                delete_after=6
            )
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            if target_member.top_role >= message.author.top_role:
                await message.channel.send(f"⚠️ ناتوانیت ئەم کەسە میوت بکەیت!", delete_after=5)
                return

            await target_member.timeout(datetime.timedelta(minutes=10), reason="Muted by command")
            await message.channel.send(f"🤐 {target_member.mention} بۆ ماوەی ۱۰ خولەک میوت کرا.", delete_after=5)
            await message.delete()
        return

    # --- (ban بە ڕەیپڵای یان تاگ) ---
    if command == "ban":
        if not message.author.guild_permissions.ban_members:
            await message.channel.send(
                f"❌ {message.author.mention} تۆ ڕۆڵی بانت نییە! بڕۆ بە ئاڤلۆ بڵێ.",
                delete_after=6
            )
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            if target_member.top_role >= message.author.top_role:
                await message.channel.send(f"⚠️ ناتوانیت ئەم کەسە بان بکەیت!", delete_after=5)
                return

            await target_member.ban(reason="Banned by command")
            await message.channel.send(f"🔨 {target_member.mention} بان کرا لە سێرڤەر.", delete_after=5)
            await message.delete()
        return

    await bot.process_commands(message)
   # تۆکنی نوێکراوەی بۆتەکەت لێرە بپێستە
bot.run("MTU1MDU0NDM2NTkxNzcwNDMzMg.G4fcWn.yn7kSvUXFRJe5obpbm_Fj079w-6Eg0EaTb_3Lw") 
