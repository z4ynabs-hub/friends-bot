import os
import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1550619956423688342 

@bot.event
async def on_ready():
    print(f'Bot active: {bot.user}')

@bot.event
async def on_member_join(member):
    role_name = "Friends"  
    role = discord.utils.get(member.guild.roles, name=role_name)
    
    if role:
        try:
            await member.add_roles(role)
        except Exception as e:
            print(f"Role error: {e}")

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
            embed.set_image(url="https://i.ibb.co/jkLCqDJX/welcome.gif") #
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Welcome error: {e}")

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
            embed.set_image(url="https://i.ibb.co/jkLCqDJX/welcome.gif") #
            await message.channel.send(embed=embed)
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}")
        return

    if command == "clear" and len(msg) == 2 and msg[1].isdigit():
        count = int(msg[1])
        amount = count + 1
        deleted = await message.channel.purge(limit=amount)
        actual_deleted = len(deleted) - 1
        if actual_deleted > 0:
            await message.channel.send(f"🧹 {actual_deleted} chati sraw laubra.", delete_after=5)
        return

    if command == "mute":
        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = ref_msg.author

        if target_member:
            try:
                await target_member.timeout(datetime.timedelta(minutes=10), reason="Muted")
                await message.channel.send(f"🤐 {target_member.mention} mute kra.", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    if command == "unmute":
        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = ref_msg.author

        if target_member:
            try:
                await target_member.timeout(None, reason="Unmuted")
                await message.channel.send(f"🔊 {target_member.mention} unmute kra.", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    if command == "ban":
        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = ref_msg.author

        if target_member:
            try:
                await target_member.ban(reason="Banned")
                await message.channel.send(f"🔨 {target_member.mention} ban kra.", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    if command == "unban" and len(msg) == 2:
        try:
            user_id = int(msg[1])
            user = await bot.fetch_user(user_id)
            await message.guild.unban(user)
            await message.channel.send(f"🔓 Unbanned successfully.", delete_after=5)
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    if command == "lock":
        try:
            await message.channel.set_permissions(message.guild.default_role, send_messages=False)
            await message.channel.send("🔒 Channel locked.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    if command == "unlock":
        try:
            await message.channel.set_permissions(message.guild.default_role, send_messages=True)
            await message.channel.send("🔓 Channel unlocked.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
