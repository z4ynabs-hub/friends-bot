import os
import discord
from discord.ext import commands
import datetime

# ١. دەسەڵاتەکانی بۆتەکە
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ئایدی کەناڵی چاتی گشتی (تەنها ژمارەکە بەبێ لینک)
WELCOME_CHANNEL_ID = 1550616272805568613 


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
# ٣. کۆماندەکان (Clear, Mute, Unmute, Ban, Unban, Lock, Unlock)
# ---------------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.strip().split()
    if not msg:
        return

    command = msg[0].lower()

    # --- (!clear 10) سڕینەوەی نامەکان ---
    if command == "!clear" and len(msg) == 2 and msg[1].isdigit():
        if not message.author.guild_permissions.manage_messages:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        amount = int(msg[1]) + 1
        await message.channel.purge(limit=amount)
        await message.channel.send(f"✅ {msg[1]} پەیام سڕێنرانەوە.", delete_after=3)
        return

    # --- (!mute) ---
    if command == "!mute":
        if not message.author.guild_permissions.moderate_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            await target_member.timeout(datetime.timedelta(minutes=10), reason="Muted by command")
            await message.channel.send(f"🤐 {target_member.mention} میوت کرا.", delete_after=5)
            await message.delete()
        return

    # --- (!unmute) ---
    if command == "!unmute":
        if not message.author.guild_permissions.moderate_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            await target_member.timeout(None, reason="Unmuted by command")
            await message.channel.send(f"🔊 لەسەر {target_member.mention} میوت لادرا.", delete_after=5)
            await message.delete()
        return

    # --- (!ban) ---
    if command == "!ban":
        if not message.author.guild_permissions.ban_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            await target_member.ban(reason="Banned by command")
            await message.channel.send(f"🔨 {target_member.mention} بان کرا.", delete_after=5)
            await message.delete()
        return

    # --- (!unban) ---
    if command == "!unban" and len(msg) == 2:
        if not message.author.guild_permissions.ban_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        try:import os
import discord
from discord.ext import commands
import datetime

# ١. دەسەڵاتەکانی بۆتەکە
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ئایدی نوێی کەناڵی بەخێرهاتن
WELCOME_CHANNEL_ID = 1550616272805568613 


@bot.event
async def on_ready():
    print(f'بۆتەکە بە سەرکەوتوویی چالاک بوو وەک: {bot.user}')


# ---------------------------------------------------------
# ٢. سیستەمی بەخێرهاتن و دانی ڕۆڵی Friends بە شێوەی ئۆتۆماتیکی
# ---------------------------------------------------------
@bot.event
async def on_member_join(member):
    # دانی ڕۆڵی Friends بە ئەندامی نوێ
    role_name = "Friends"  
    role = discord.utils.get(member.guild.roles, name=role_name)
    
    if role:
        try:
            await member.add_roles(role)
        except Exception as e:
            print(f"کێشە لە دانی ڕۆڵ ڕوویدا: {e}")

    # ناردنی گیف و نامەی بەخێرهاتن لەو کەناڵەی کە ئایدییەکەت داوە
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
# ٣. کۆماندەکان (Clear, Mute, Unmute, Ban, Unban, Lock, Unlock)
# ---------------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.strip().split()
    if not msg:
        return

    command = msg[0].lower()

    # --- (!clear 10) ---
    if command == "!clear" and len(msg) == 2 and msg[1].isdigit():
        if not message.author.guild_permissions.manage_messages:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        amount = int(msg[1]) + 1
        await message.channel.purge(limit=amount)
        await message.channel.send(f"✅ {msg[1]} پەیام سڕێنرانەوە.", delete_after=3)
        return

    # --- (!mute) ---
    if command == "!mute":
        if not message.author.guild_permissions.moderate_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            await target_member.timeout(datetime.timedelta(minutes=10), reason="Muted by command")
            await message.channel.send(f"🤐 {target_member.mention} میوت کرا.", delete_after=5)
            await message.delete()
        return

    # --- (!unmute) ---
    if command == "!unmute":
        if not message.author.guild_permissions.moderate_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            await target_member.timeout(None, reason="Unmuted by command")
            await message.channel.send(f"🔊 لەسەر {target_member.mention} میوت لادرا.", delete_after=5)
            await message.delete()
        return

    # --- (!ban) ---
    if command == "!ban":
        if not message.author.guild_permissions.ban_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = referenced_msg.author

        if target_member:
            await target_member.ban(reason="Banned by command")
            await message.channel.send(f"🔨 {target_member.mention} بان کرا.", delete_after=5)
            await message.delete()
        return

    # --- (!unban) ---
    if command == "!unban" and len(msg) == 2:
        if not message.author.guild_permissions.ban_members:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        try:
            user_id = int(msg[1])
            user = await bot.fetch_user(user_id)
            await message.guild.unban(user)
            await message.channel.send(f"🔓 بە سەرکەوتوویی بانی لەسەر لادرا.", delete_after=5)
        except Exception as e:
            await message.channel.send(f"⚠️ هەڵەیەک ڕوویدا یان ئایدیەکە هەڵەیە.", delete_after=5)
        return

    # --- (!lock) ---
    if command == "!lock":
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        await message.channel.set_permissions(message.guild.default_role, send_messages=False)
        await message.channel.send("🔒 کەناڵەکە داخرا (Locked).")
        return

    # --- (!unlock) ---
    if command == "!unlock":
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
        await message.channel.send("🔓 کەناڵەکە کرایەوە (Unlocked).")
        return

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
            user_id = int(msg[1])
            user = await bot.fetch_user(user_id)
            await message.guild.unban(user)
            await message.channel.send(f"🔓 بە سەرکەوتوویی بانی لەسەر لادرا.", delete_after=5)
        except Exception as e:
            await message.channel.send(f"⚠️ هەڵەیەک ڕوویدا یان ئایدیەکە هەڵەیە.", delete_after=5)
        return

    # --- (!lock) داخستنی کەناڵ ---
    if command == "!lock":
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        await message.channel.set_permissions(message.guild.default_role, send_messages=False)
        await message.channel.send("🔒 کەناڵەکە داخرا (Locked).")
        return

    # --- (!unlock) کردنەوەی کەناڵ ---
    if command == "!unlock":
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send(f"❌ {message.author.mention} تۆ ڕۆڵت نییە!", delete_after=6)
            return

        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
        await message.channel.send("🔓 کەناڵەکە کرایەوە (Unlocked).")
        return

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
