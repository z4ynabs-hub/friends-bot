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
WELCOME_CHANNEL_ID = 1550619956423688342 

@bot.event
async def on_ready():
    print(f'بۆتەکە بە سەرکەوتوویی چالاک بوو وەک: {bot.user}')

# ---------------------------------------------------------
# ٢. سیستەمی بەخێرهاتن بە Embed و لینکی گیفەکەی خۆت
# ---------------------------------------------------------
@bot.event
async def on_member_join(member):
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
            embed = discord.Embed(color=0x2f3136)
            embed.description = (
                "✦₊˚ ★⋆ Welcome ⋆★ ˚₊✦\n\n"
                "└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊\n\n"
                f"{member.mention}\n\n"
                "ơೃ࿐ --- ⋆ #rules ⋆ ---\n"
                "ơೃ࿐ --- ⋆ #unknown ⋆ ---\n"
                "ơೃ࿐ --- ⋆ #unknown ⋆ ---\n\n"
                "=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚"
            )
            
            # لینکی گیفەکەی خۆت کە لە دیسکۆرد ئۆپلۆدت کردووە
            embed.set_image(url="https://cdn.discordapp.com/attachments/1550619956423688342/1550988205237739570/welcome.gif?ex=6ab055d4&is=6aaf0454&hm=819d4831efa34240243d77e6af086bf1adf53b749701fac8e1d4855c70481c29&")

            await channel.send(embed=embed)
        except Exception as e:
            print(f"کێشەیەک لە بەخێرهاتن ڕوویدا: {e}")

# ---------------------------------------------------------
# ٣. کۆماندەکان (Test, Clear, Mute, Unmute, Ban, Unban, Lock, Unlock)
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

    # --- تاقیکردنەوەی Welcome بە Embed (!test) ---
    if command == "test":
        try:
            embed = discord.Embed(color=0x2f3136)
            embed.description = (
                "✦₊˚ ★⋆ Welcome ⋆★ ˚₊✦\n\n"
                "└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊\n\n"
                f"{message.author.mention}\n\n"
                "ơೃ࿐ --- ⋆ #rules ⋆ ---\n"
                "ơೃ࿐ --- ⋆ #unknown ⋆ ---\n"
                "ơೃ࿐ --- ⋆ #unknown ⋆ ---\n\n"
                "=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚ (Test)"
            )
            
            embed.set_image(url="https://cdn.discordapp.com/attachments/1550619956423688342/1550988205237739570/welcome.gif?ex=6ab055d4&is=6aaf0454&hm=819d4831efa34240243d77e6af086bf1adf53b749701fac8e1d4855c70481c29&")
            
            await message.channel.send(embed=embed)
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ هەڵە هەەیە: {e}")
        return

    # --- clear ---
    if command == "clear" and len(msg) == 2 and msg[1].isdigit():
        count = int(msg[1])
        amount = count + 1
        deleted = await message.channel.purge(limit=amount)
        actual_deleted = len(deleted) - 1
        if actual_deleted > 0:
            await message.channel.send(f"🧹 {actual_deleted} چاتی سڕاوە لەناوبرا.", delete_after=5)
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
            if target_member.top_role >= message.guild.me.top_role:
                await message.channel.send("⚠️ ناتوانم ئەم کەسە میوت بکەم، چونکە ڕۆڵەکەی لە من بەرزترە یان یەکسانە!", delete_after=5)
                await message.delete()
                return

            try:
                duration = datetime.timedelta(minutes=10)
                await target_member.timeout(duration, reason="Muted by command")
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
            if target_member.top_role >= message.guild.me.top_role:
                await message.channel.send("⚠️ ناتوانم ئەم کەسە بان بکەم، چونکە ڕۆڵەکەی لە من بەرزترە یان یەکسانە!", delete_after=5)
                await message.delete()
                return

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
            await message.channel.send("🔒 کەناڵەکە داخرا (Locked).", delete_after=5)
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ هەڵە ڕوویدا: {e}", delete_after=5)
        return

    # --- unlock ---
    if command == "unlock":
        try:
            await message.channel.set_permissions(message.guild.default_role, send_messages=True)
            await message.channel.send("🔓 کەناڵەکە کرایەوە (Unlocked).", delete_after=5)
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ هەڵە ڕوویدا: {e}", delete_after=5)
        return

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
