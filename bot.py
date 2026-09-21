import os
import discord
from discord.ext import commands

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
                "ơೃ࿐ --- ⋆ #FriendsZone ⋆ ---\n"
                "ơೃ࿐ --- ⋆ #Fraa-Seuii-Ryaa⋆ ---\n\n"
                "=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚"
            )
            # داناینی وێنەی پروفایلی کەسەکە بە گەورەیی لەناو عیمبەدەکەدا
            embed.set_image(url=member.display_avatar.url)
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

    # --- Test ---
    if command == "test":
        try:
            embed = discord.Embed(color=0x2f3136)
            embed.description = (
                "✦₊˚ ★⋆ Welcome ⋆★ ˚₊✦\n\n"
                "└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊\n\n"
                f"{message.author.mention}\n\n"
                "ơೃ࿐ --- ⋆ #rules ⋆ ---\n"
                "ơೃ࿐ --- ⋆ #FriendsZone ⋆ ---\n"
                "ơೃ࿐ --- ⋆ #Fraa-Seuii-Ryaa ⋆ ---\n\n"
                "=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚ (Test)"
            )
            # داناینی وێنەی پروفایلی بەکارهێنەر لە کۆماندی تەستدا بە گەورەیی
            embed.set_image(url=message.author.display_avatar.url)
            await message.channel.send(embed=embed)
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}")
        return

    # --- Clear (تەنها بۆ ئادمینەکان) ---
    if command == "clear":
        if not message.author.guild_permissions.manage_messages:
            return
        if len(msg) == 2 and msg[1].isdigit():
            count = int(msg[1])
            amount = count + 1
            deleted = await message.channel.purge(limit=amount)
            actual_deleted = len(deleted) - 1
            if actual_deleted > 0:
                await message.channel.send(f"🧹 {actual_deleted} chat srawa.", delete_after=5)
        return

    # --- Mute (تەنها بۆ ئادمینەکان + پشکنینی پلەی ڕۆڵ) ---
    if command == "mute":
        if not message.author.guild_permissions.manage_roles and not message.author.guild_permissions.administrator:
            return
        
        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = ref_msg.author

        if target_member:
            if message.author != message.guild.owner and target_member.top_role >= message.author.top_role:
                await message.channel.send(f"⚠️ {message.author.mention} natwani kaseki rolabarz yan yaksani xot mute bkay!", delete_after=5)
                await message.delete()
                return

            try:
                await message.channel.set_permissions(target_member, send_messages=False)
                if target_member.voice:
                    await target_member.edit(mute=True)

                await message.channel.send(f"mute kra badaxawa bot bojarekitr aqllba {target_member.mention}", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ Halla ruywyda: {e}", delete_after=5)
        return

    # --- Unmute (تەنها بۆ ئادمینەکان) ---
    if command == "unmute":
        if not message.author.guild_permissions.manage_roles and not message.author.guild_permissions.administrator:
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = ref_msg.author

        if target_member:
            if message.author != message.guild.owner and target_member.top_role >= message.author.top_role:
                await message.channel.send(f"⚠️ {message.author.mention} natwani unmute kaseki rollbarz bkay!", delete_after=5)
                await message.delete()
                return

            try:
                await message.channel.set_permissions(target_member, overwrite=None)
                if target_member.voice:
                    await target_member.edit(mute=False)

                await message.channel.send(f"unmute kra aqllba {target_member.mention}", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ Halla rwyda: {e}", delete_after=5)
        return

    # --- Ban (تەنها بۆ ئۆوێنەر و جێگری ئۆوێنەر یان ئادمینە باڵاکان) ---
    if command == "ban":
        if not message.author.guild_permissions.ban_members:
            return

        target_member = None
        if message.mentions:
            target_member = message.mentions[0]
        elif message.reference:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            target_member = ref_msg.author

        if target_member:
            if message.author != message.guild.owner and target_member.top_role >= message.author.top_role:
                await message.channel.send(f"⚠️ Natwani admin ban bkay!", delete_after=5)
                await message.delete()
                return

            try:
                await target_member.ban(reason="Banned by command")
                await message.channel.send(f"ban kra badaxawa {target_member.mention}", delete_after=5)
                await message.delete()
            except Exception as e:
                await message.channel.send(f"⚠️ Halla rwyda: {e}", delete_after=5)
        return

    # --- Unban ---
    if command == "unban" and len(msg) == 2:
        if not message.author.guild_permissions.ban_members:
            return
        try:
            user_id = int(msg[1])
            user = await bot.fetch_user(user_id)
            await message.guild.unban(user)
            await message.channel.send(f"🔓 Unbanned successfully.", delete_after=5)
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    # --- Lock (تەنها بۆ ئادمینەکان) ---
    if command == "lock":
        if not message.author.guild_permissions.manage_channels:
            return
        try:
            await message.channel.set_permissions(message.guild.default_role, send_messages=False)
            await message.channel.send("🔒 Channel locked.", delete_after=5)
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    # --- Unlock (تەنها بۆ ئادمینەکان) ---
    if command == "unlock":
        if not message.author.guild_permissions.manage_channels:
            return
        try:
            await message.channel.set_permissions(message.guild.default_role, send_messages=True)
            await message.channel.send("🔓 Channel unlocked.", delete_after=5)
            await message.delete()
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}", delete_after=5)
        return

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
