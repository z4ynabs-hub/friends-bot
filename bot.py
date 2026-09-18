import os
import discord
from discord.ext import commands
import datetime

# ١. دەسەڵاتەکانی بۆتەکە
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ئایدی کەناڵی بەخێرهاتن
WELCOME_CHANNEL_ID = 1550616272805568613 


@bot.event
async def on_ready():
    print(f'بۆتەکە بە سەرکەوتوویی چالاک بوو وەک: {bot.user}')


# ---------------------------------------------------------
# ٢. سیستەمی بەخێرهاتن (لەگەڵ فەرمانی تاقیکردنەوەی !test)
# ---------------------------------------------------------
@bot.event
async def on_member_join(member):
    print(f"ئەندامێکی نوێ هات: {member.name}")
    role_name = "Friends"  
    role = discord.utils.get(member.guild.roles, name=role_name)
    
    if role:
        try:
            await member.add_roles(role)
        except Exception as e:
            print(f"کێشە لە دانی ڕۆڵ ڕوویدا: {e}")

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        try:
            file = discord.File("welcome.gif", filename="welcome.gif")
            await channel.send(
                content=f"Welcome to Friends {member.mention}! ✨",
                file=file
            )
        except Exception as e:
            print(f"کێشەیەک لە بەخێرهاتن ڕوویدا: {e}")
    else:
        print("کەناڵی بەخێرهاتن نەدۆزرایەوە، دڵنیابە لە ئایدییەکەی!")


# ---------------------------------------------------------
# ٣. کۆماندەکان (Clear, Mute, Ban, Lock, Welcome Test)
# ---------------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    if not content:
        return

    if content.startswith("!"):
        msg = content[1:].strip().split()
    else:
        msg = content.split()

    if not msg:
        return

    command = msg[0].lower()

    # --- فەرمانی تاقیکردنەوەی Welcome (!test) ---
    if command == "test":
        try:
            file = discord.File("welcome.gif", filename="welcome.gif")
            await message.channel.send(
                content=f"Welcome to Friends {message.author.mention}! ✨ (Test)",
                file=file
            )
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ گیفەکە نەدۆزرایەوە یان هەڵە هەەیە: {e}")
        return

    # --- clear ---
    if command == "clear" and len(msg) == 2 and msg[1].isdigit():
        amount = int(msg[1]) + 1
        await message.channel.purge(limit=amount)
        return

    # --- mute ---
    if command == "mute":
        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            try:
                await target_member.timeout(datetime.timedelta(minutes=10), reason="Muted by command")
                await message.channel.send(f"🤐 {target_member.mention} میوت کرا.", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ هەڵە ڕوویدا: {e}", delete_after=5)
        return

    # --- unmute ---
    if command == "unmute":
        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            try:
                await target_member.timeout(None, reason="Unmuted by command")
                await message.channel.send(f"🔊 لەسەر {target_member.mention} میوت لادرا.", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ هەڵە ڕوویدا: {e}", delete_after=5)
        return

    # --- ban ---
    if command == "ban":
        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            try:
                await target_member.ban(reason="Banned by command")
                await message.channel.send(f"🔨 {target_member.mention} بان کرا.", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ هەڵە ڕوویدا: {e}", delete_after=5)
        return

    # --- unban ---
    if command == "unban" and len(msg) == 2:
        try:
            user_id = int(msg[1])
            user = await bot.fetch_user(user_id)
            await message.guild.unban(user)
            await message.channel.send(f"🔓 بە سەرکەوتوویی بانی لەسەر لادرا.", delete_after=5)
        except Exception as e:
            await message.channel.send(f"⚠️ ئایدیەکە هەڵەیە یان بانی نەکراوە.", delete_after=5)
        return

    # --- lock ---
    if command == "lock":
        try:
            await message.channel.set_permissions(message.guild.default_role, send_messages=False)
            await message.channel.send("🔒 کەناڵەکە داخرا (Locked).")
        except Exception as e:
            await message.channel.send(f"⚠️ هەڵە ڕوویدا: {e}", delete_after=5)
        return

    # --- unlock ---
    if command == "unlock":
        try:
            await message.channel.set_permissions(message.guild.default_role, send_messages=True)
            await message.channel.send("🔓 کەناڵەکە کرایەوە (Unlocked).")
        except Exception as e:
            await message.channel.send(f"⚠️ هەڵە ڕوویدا: {e}", delete_after=5)
        return

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
