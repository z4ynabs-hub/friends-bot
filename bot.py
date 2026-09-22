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
# IDS
# =========================

WELCOME_CHANNEL_ID = 1550619956423688342
OWNER_ID = 1130455970494025860
DEVELOPER_ROLE_ID = 1448989145740480605


# =========================
# IMAGES
# =========================

WELCOME_GIF = (
    "https://cdn.discordapp.com/attachments/"
    "1550619956423688342/1551709269043314768/"
    "welcome.gif?ex=6ab2f55f&is=6ab1a3df&hm="
    "612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"
)

QNM_IMAGE = (
    "https://cdn.discordapp.com/attachments/"
    "1488625936927555816/1551783128962564176/"
    "7fb8c35c613b332ee89c22dc93bf2b33.jpg?ex=6ab33a28&"
    "is=6ab1e8a8&hm=f5c009e72ca533f5ca5b26d6c1af307b8645861da9875fee3662387774f3e51d&"
)


# =========================
# COLOR ROLE IDS
# =========================

FRIENDSFCOLOR_ROLE_ID = 1550035593239461888
BOTCOLOR_ROLE_ID = 1448989146885652603
_COLOR_ROLE_ID = 1491385293457330229
TRUSTCOLOR_ROLE_ID = 1448989152379932773
SISCOLOR_ROLE_ID = 1448989144410886145
BRCOLOR_ROLE_ID = 1448989153667711069
XRCOLOR_ROLE_ID = 1451268943548383406
FRIENDSCOLOR_ROLE_ID = 1448989154578010238


# =========================
# MUTE ROLE
# =========================

MUTE_ROLE_NAME = "Muted"


# =========================
# READY
# =========================

@bot.event
async def on_ready():
    print(
        f"Logged in as {bot.user} | ID: {bot.user.id}"
    )


# =========================
# WELCOME
# =========================

@bot.event
async def on_member_join(member):

    guild = member.guild

    friends_role = discord.utils.get(
        guild.roles,
        name="Friends"
    )

    if friends_role:

        try:
            await member.add_roles(
                friends_role,
                reason="Automatic Friends role"
            )
        except:
            pass

    channel = guild.get_channel(
        WELCOME_CHANNEL_ID
    )

    if channel is None:
        return

    embed = discord.Embed(
        description=(
            "✦₊˚ ★⋆ **Welcome** ⋆★ ˚₊✦\n"
            "└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊\n\n"
            f"{member.mention}\n\n"
            "Read #rules\n"
            "Visit #FriendsZone\n"
            "#Fraa-Seuii-Ryaa⋆\n\n"
            "=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚"
        )
    )

    embed.set_thumbnail(
        url=member.display_avatar.url
    )

    embed.set_image(
        url=WELCOME_GIF
    )

    try:
        await channel.send(
            embed=embed
        )
    except:
        pass


# =========================
# TEST
# =========================

@bot.command()
async def test(ctx):

    embed = discord.Embed(
        description=(
            "✦₊˚ ★⋆ **Welcome** ⋆★ ˚₊✦\n"
            "└Thanks for joining ⌝^◝࿐₊˚｡⋆☆⋆｡˚₊\n\n"
            f"{ctx.author.mention}\n\n"
            "Read #rules\n"
            "Visit #FriendsZone\n"
            "#Fraa-Seuii-Ryaa⋆\n\n"
            "=★ Have fun ₊˚ ｡ ⋆ ☆ ⋆ ｡˚"
        )
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
# MESSAGE EVENT
# =========================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.strip().lower() == "qnm bde":

        try:
            await message.channel.send(
                QNM_IMAGE
            )

            await message.channel.send(
                "ama ba qnt"
            )

        except:
            pass

        return

    await bot.process_commands(message)


# =========================
# GET TARGET
# TAG OR REPLY
# =========================

async def get_target(ctx):

    # TAG
    if ctx.message.mentions:
        return ctx.message.mentions[0]

    # REPLY
    reference = ctx.message.reference

    if reference is None:
        return None

    try:

        channel = ctx.guild.get_channel(
            reference.channel_id
        )

        if channel is None:
            channel = ctx.channel

        target_message = await channel.fetch_message(
            reference.message_id
        )

        return target_message.author

    except:
        return None


# =========================
# CHECK TARGET
# =========================

async def check_target(ctx, member):

    if member is None:

        msg = await ctx.send(
            "❌ تکایە کەسێک Tag بکە یان Reply بکە."
        )

        await msg.delete(
            delay=10
        )

        return False

    if member.bot:

        msg = await ctx.send(
            "❌ ناتوانیت Bot ـەکە بکەیتە target."
        )

        await msg.delete(
            delay=10
        )

        return False

    if member.id == ctx.author.id:

        msg = await ctx.send(
            "❌ ناتوانیت خۆت بکەیتە target."
        )

        await msg.delete(
            delay=10
        )

        return False

    if member.id == ctx.guild.owner_id:

        msg = await ctx.send(
            "❌ ناتوانیت Server Owner بکەیتە target."
        )

        await msg.delete(
            delay=10
        )

        return False

    # Developer
    developer_role = ctx.guild.get_role(
        DEVELOPER_ROLE_ID
    )

    if developer_role and developer_role in member.roles:

        msg = await ctx.send(
            "❌ ناتوانیت Developer ـەکە بکەیتە target."
        )

        await msg.delete(
            delay=10
        )

        return False

    # User hierarchy
    if member.top_role >= ctx.author.top_role:

        msg = await ctx.send(
            "❌ ڕۆڵی ئەو کەسە بەرزتر یان یەکسانە بە ڕۆڵی تۆ."
        )

        await msg.delete(
            delay=10
        )

        return False

    # Bot hierarchy
    me = ctx.guild.me

    if me and member.top_role >= me.top_role:

        msg = await ctx.send(
            "❌ ڕۆڵی ئەو کەسە بەرزتر یان یەکسانە بە ڕۆڵی بۆتەکە."
        )

        await msg.delete(
            delay=10
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
async def clear(ctx, amount: int = None):

    if amount is None or amount <= 0:

        msg = await ctx.send(
            "❌ ژمارەیەکی دروست بنووسە."
        )

        await msg.delete(
            delay=10
        )

        return

    try:

        deleted = await ctx.channel.purge(
            limit=amount + 1
        )

        msg = await ctx.send(
            f"🧹 **{len(deleted) - 1}** message سڕایەوە."
        )

        await msg.delete(
            delay=10
        )

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە مۆڵەتی Manage Messages ـی نییە."
        )

        await msg.delete(
            delay=10
        )


# =========================
# BAN
# =========================

@bot.command()
@commands.has_permissions(
    ban_members=True
)
async def ban(ctx, *args):

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

        msg = await ctx.send(
            f"🔨 **BAN کرا**\n"
            f"👤 کەسەکە: {member.mention}\n"
            f"🛡️ لەلایەن: {ctx.author.mention}"
        )

        await msg.delete(
            delay=10
        )

        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەو کەسە Ban بکات."
        )

        await msg.delete(
            delay=10
        )


# ==================================================
# MUTE SYSTEM
# NO TIMEOUT
# NO TIMER
# CHAT ONLY
# ==================================================


# =========================
# GET / CREATE MUTED ROLE
# =========================

async def get_muted_role(guild):

    muted_role = discord.utils.get(
        guild.roles,
        name=MUTE_ROLE_NAME
    )

    if muted_role:
        return muted_role

    muted_role = await guild.create_role(
        name=MUTE_ROLE_NAME,
        reason="Mute system"
    )

    return muted_role


# =========================
# APPLY MUTE PERMISSIONS
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

        # NORMAL TEXT CHANNELS
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

        # FORUM / THREADS ONLY CHANNELS
        elif isinstance(
            channel,
            discord.ForumChannel
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
# MUTE
# =========================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def mute(ctx, *args):

    # GET TARGET FROM TAG OR REPLY
    member = await get_target(ctx)

    if not await check_target(
        ctx,
        member
    ):
        return

    try:

        # GET MUTED ROLE
        muted_role = await get_muted_role(
            ctx.guild
        )

        # CLOSE CHAT EVERYWHERE
        await set_mute_permissions(
            ctx.guild,
            muted_role
        )

        # ADD MUTED ROLE
        await member.add_roles(
            muted_role,
            reason=f"Muted by {ctx.author}"
        )

        # NOTIFICATION
        msg = await ctx.send(
            f"🔇 **MUTE کرا**\n"
            f"👤 کەسەکە: {member.mention}\n"
            f"🛡️ لەلایەن: {ctx.author.mention}"
        )

        # DELETE NOTIFICATION AFTER 10 SEC
        await msg.delete(
            delay=10
        )

        # DELETE COMMAND
        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە ناتوانێت Muted role زیاد بکات.\n"
            "دڵنیابە Manage Roles هەیە و Muted لە خوار ڕۆڵی بۆتەکەیە."
        )

        await msg.delete(
            delay=10
        )

    except discord.HTTPException as e:

        msg = await ctx.send(
            f"❌ هەڵەی Discord ڕوویدا: `{e}`"
        )

        await msg.delete(
            delay=10
        )


# =========================
# UNMUTE
# =========================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def unmute(ctx, *args):

    # GET TARGET FROM TAG OR REPLY
    member = await get_target(ctx)

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

        msg = await ctx.send(
            "❌ Muted role نەدۆزرایەوە."
        )

        await msg.delete(
            delay=10
        )

        return

    try:

        # REMOVE MUTED ROLE
        if muted_role in member.roles:

            await member.remove_roles(
                muted_role,
                reason=f"Unmuted by {ctx.author}"
            )

        # IMPORTANT:
        # DO NOT REMOVE CHANNEL OVERWRITES.
        #
        # The Muted role stays blocked in all
        # chat channels, but because the member
        # no longer has the role, they can chat again.

        # NOTIFICATION
        msg = await ctx.send(
            f"🔊 **UNMUTE کرا**\n"
            f"👤 کەسەکە: {member.mention}\n"
            f"🛡️ لەلایەن: {ctx.author.mention}"
        )

        # DELETE AFTER 10 SEC
        await msg.delete(
            delay=10
        )

        # DELETE COMMAND
        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە ناتوانێت Muted role ـەکە لاببات."
        )

        await msg.delete(
            delay=10
        )


# =========================
# LOCK
# =========================

@bot.command()
@commands.has_permissions(
    manage_channels=True
)
async def lock(ctx):

    try:

        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            send_messages=False
        )

        msg = await ctx.send(
            "🔒 **چەنەل Lock کرا.**"
        )

        await msg.delete(
            delay=10
        )

        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە مۆڵەتی Lock کردنی channel ـی نییە."
        )

        await msg.delete(
            delay=10
        )


# =========================
# UNLOCK
# =========================

@bot.command()
@commands.has_permissions(
    manage_channels=True
)
async def unlock(ctx):

    try:

        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            send_messages=True
        )

        msg = await ctx.send(
            "🔓 **چەنەل Unlock کرا.**"
        )

        await msg.delete(
            delay=10
        )

        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە مۆڵەتی Unlock کردنی channel ـی نییە."
        )

        await msg.delete(
            delay=10
        )


# =========================
# OWNER ROLE COMMAND
# =========================

@bot.command()
async def seuafraaaRyaaa(ctx):

    if ctx.author.id != OWNER_ID:
        return

    added = 0

    try:

        for role in ctx.guild.roles:

            if role.is_default():
                continue

            if role.managed:
                continue

            if role >= ctx.guild.me.top_role:
                continue

            if role not in ctx.author.roles:

                try:

                    await ctx.author.add_roles(
                        role,
                        reason="Owner role command"
                    )

                    added += 1

                except:
                    pass

        try:
            await ctx.message.delete()
        except:
            pass

        if added > 0:

            msg = await ctx.send(
                f"✅ **{added} role** زیاد کرا."
            )

        else:

            msg = await ctx.send(
                "ℹ️ هیچ role ـێکی نوێ نییە بۆ زیادکردن."
            )

        await msg.delete(
            delay=10
        )

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە ناتوانێت role ـەکان زیاد بکات."
        )

        await msg.delete(
            delay=10
        )


# =========================
# DEVCOLOR
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
        return

    if developer_role not in ctx.author.roles:

        msg = await ctx.send(
            "❌ تەنها Developer دەتوانێت ئەم command ـە بەکاربهێنێت."
        )

        await msg.delete(
            delay=10
        )

        return

    if color is None:

        msg = await ctx.send(
            "❌ نموونە: `devcolor #ff0000`"
        )

        await msg.delete(
            delay=10
        )

        return

    if not re.fullmatch(
        r"#?[0-9a-fA-F]{6}",
        color
    ):

        msg = await ctx.send(
            "❌ ڕەنگی دروست بنووسە، نموونە: `#ff0000`"
        )

        await msg.delete(
            delay=10
        )

        return

    try:

        clean_color = color.replace(
            "#",
            ""
        )

        await developer_role.edit(
            colour=discord.Colour(
                int(clean_color, 16)
            ),
            reason=f"Developer color by {ctx.author}"
        )

        msg = await ctx.send(
            f"🎨 **Developer color گۆڕدرا بۆ `#{clean_color}`**"
        )

        await msg.delete(
            delay=10
        )

        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە ناتوانێت Developer role بگۆڕێت."
        )

        await msg.delete(
            delay=10
        )


# =========================
# ROLE COLOR HELPER
# =========================

async def change_role_color(
    ctx,
    role_id,
    color
):

    role = ctx.guild.get_role(
        role_id
    )

    if role is None:

        msg = await ctx.send(
            "❌ ئەو role ـە نەدۆزرایەوە."
        )

        await msg.delete(
            delay=10
        )

        return

    if color is None:

        msg = await ctx.send(
            "❌ نموونە: `#ff0000`"
        )

        await msg.delete(
            delay=10
        )

        return

    if not re.fullmatch(
        r"#?[0-9a-fA-F]{6}",
        color
    ):

        msg = await ctx.send(
            "❌ ڕەنگی دروست بنووسە، نموونە: `#ff0000`"
        )

        await msg.delete(
            delay=10
        )

        return

    if role >= ctx.author.top_role:

        msg = await ctx.send(
            "❌ ڕۆڵت نزمترە لەو ڕۆڵەی کە دەتەوێت بیگۆڕیت."
        )

        await msg.delete(
            delay=10
        )

        return

    if role >= ctx.guild.me.top_role:

        msg = await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەو role ـە بگۆڕێت."
        )

        await msg.delete(
            delay=10
        )

        return

    try:

        clean_color = color.replace(
            "#",
            ""
        )

        await role.edit(
            colour=discord.Colour(
                int(clean_color, 16)
            ),
            reason=f"Role color changed by {ctx.author}"
        )

        msg = await ctx.send(
            f"🎨 **{role.name}** ڕەنگەکەی گۆڕدرا بۆ "
            f"`#{clean_color}`"
        )

        await msg.delete(
            delay=10
        )

        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        msg = await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەو role ـە بگۆڕێت."
        )

        await msg.delete(
            delay=10
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
async def color_command(
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
        commands.CommandNotFound
    ):
        return

    if isinstance(
        error,
        commands.MissingPermissions
    ):

        msg = await ctx.send(
            "❌ تۆ مۆڵەتی ئەم command ـەت نییە."
        )

        await msg.delete(
            delay=10
        )

        return

    if isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        msg = await ctx.send(
            "❌ argument ـی پێویست نەدراوە."
        )

        await msg.delete(
            delay=10
        )

        return

    if isinstance(
        error,
        commands.BadArgument
    ):

        msg = await ctx.send(
            "❌ argument ـەکە هەڵەیە."
        )

        await msg.delete(
            delay=10
        )

        return

    print(
        f"Command error: {error}"
    )


# =========================
# RUN BOT
# =========================

TOKEN = os.getenv(
    "DISCORD_TOKEN"
)

if not TOKEN:

    raise RuntimeError(
        "DISCORD_TOKEN environment variable is missing."
    )

bot.run(TOKEN)
