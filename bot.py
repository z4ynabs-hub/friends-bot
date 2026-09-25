import os
import discord
from discord.ext import commands

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
    case_insensitive=True,
    help_command=None
)

# =========================
# SETTINGS
# =========================

WELCOME_CHANNEL_ID = 1550619956423688342

OWNER_ID = 1130455970494025860

DEVELOPER_ROLE_ID = 1448989145740480605

WELCOME_GIF = (
    "https://cdn.discordapp.com/attachments/"
    "1550619956423688342/1551709269043314768/"
    "welcome.gif?ex=6ab2f55f&is=6ab1a3df&"
    "hm=612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"
)

# =========================
# LOG CHANNELS
# =========================

LOG_CHANNELS = {
    "edit_role": 1448989222433329262,
    "role": 1448989223590952990,
    "voice": 1448989224991981619,
    "mute": 1448989225826386045,
    "join_left": 1448989227156111370,
    "channel": 1448989228548493414,
    "ban": 1448989230524141599
}

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


# =========================================================
# LOG FUNCTION
# =========================================================

async def send_log(
    guild,
    log_type,
    title,
    description,
    color=discord.Colour.blurple()
):

    try:

        channel_id = LOG_CHANNELS.get(log_type)

        if channel_id is None:
            return

        channel = guild.get_channel(channel_id)

        if channel is None:
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(
            text=f"{guild.name}"
        )

        await channel.send(
            embed=embed
        )

    except Exception as e:
        print(f"Log error: {e}")


# =========================================================
# BOT READY
# =========================================================

@bot.event
async def on_ready():

    print(f"Bot is online as {bot.user}")

    print(
        f"Connected to {len(bot.guilds)} guild(s)"
    )


# =========================================================
# MEMBER JOIN
# =========================================================

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

        except discord.Forbidden:

            print(
                "Bot cannot give Friends role."
            )

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

    await send_log(
        member.guild,
        "join_left",
        "🟢 Member Joined",
        f"**Member:** {member.mention}\n"
        f"**Name:** `{member}`\n"
        f"**ID:** `{member.id}`",
        discord.Colour.green()
    )


# =========================================================
# MEMBER LEAVE
# =========================================================

@bot.event
async def on_member_remove(member):

    await send_log(
        member.guild,
        "join_left",
        "🔴 Member Left",
        f"**Member:** `{member}`\n"
        f"**ID:** `{member.id}`",
        discord.Colour.red()
    )


# =========================================================
# TEST WELCOME
# =========================================================

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


# =========================================================
# CLEAR / SAFIKA
# =========================================================

@bot.command(
    name="safika",
    aliases=["clear"]
)
@commands.has_permissions(
    manage_messages=True
)
async def safika(
    ctx,
    amount: int
):

    if amount <= 0:

        return await ctx.send(
            "❌ دانەیەکی دروست بنووسە.",
            delete_after=3
        )

    deleted = await ctx.channel.purge(
        limit=amount + 1
    )

    count = len(deleted) - 1

    msg = await ctx.send(
        f"🧹 {count} messages deleted.",
        delete_after=3
    )

    await send_log(
        ctx.guild,
        "channel",
        "🧹 Messages Cleared",
        f"**بەکارهێنەر:** {ctx.author.mention}\n"
        f"**کەناڵ:** {ctx.channel.mention}\n"
        f"**ژمارەی سڕاوەکان:** `{count}`",
        discord.Colour.orange()
    )


# =========================================================
# MUTED ROLE
# =========================================================

async def apply_muted_permissions(
    channel,
    mute_role
):

    try:

        # ---------------------------------
        # TEXT / NEWS / FORUM
        # ---------------------------------

        if isinstance(
            channel,
            (
                discord.TextChannel,
                discord.NewsChannel,
                discord.ForumChannel
            )
        ):

            overwrite = discord.PermissionOverwrite()

            overwrite.send_messages = False
            overwrite.add_reactions = False

            overwrite.send_messages_in_threads = False
            overwrite.create_public_threads = False
            overwrite.create_private_threads = False

            await channel.set_permissions(
                mute_role,
                overwrite=overwrite,
                reason="Muted role permissions"
            )

        # ---------------------------------
        # VOICE
        # ---------------------------------

        elif isinstance(
            channel,
            discord.VoiceChannel
        ):

            overwrite = discord.PermissionOverwrite()

            overwrite.speak = False
            overwrite.stream = False
            overwrite.use_voice_activation = False

            await channel.set_permissions(
                mute_role,
                overwrite=overwrite,
                reason="Muted role permissions"
            )

        # ---------------------------------
        # STAGE
        # ---------------------------------

        elif isinstance(
            channel,
            discord.StageChannel
        ):

            overwrite = discord.PermissionOverwrite()

            overwrite.speak = False
            overwrite.stream = False
            overwrite.request_to_speak = False

            await channel.set_permissions(
                mute_role,
                overwrite=overwrite,
                reason="Muted role permissions"
            )

    except discord.Forbidden:

        print(
            f"Muted permission denied in: {channel.name}"
        )

    except Exception as e:

        print(
            f"Muted permission error in "
            f"{channel.name}: {e}"
        )


# =========================================================
# GET / CREATE MUTED ROLE
# =========================================================

async def get_or_create_muted_role(
    guild
):

    mute_role = discord.utils.get(
        guild.roles,
        name="Muted"
    )

    # ---------------------------------
    # CREATE ROLE
    # ---------------------------------

    if mute_role is None:

        try:

            mute_role = await guild.create_role(
                name="Muted",
                reason="Creating Muted role"
            )

        except discord.Forbidden:

            return None

        except Exception as e:

            print(
                f"Muted role creation error: {e}"
            )

            return None

    # ---------------------------------
    # APPLY TO ALL CHANNELS
    # ---------------------------------

    for channel in guild.channels:

        await apply_muted_permissions(
            channel,
            mute_role
        )

    return mute_role


# =========================================================
# NEW CHANNEL
# =========================================================

@bot.event
async def on_guild_channel_create(channel):

    try:

        mute_role = discord.utils.get(
            channel.guild.roles,
            name="Muted"
        )

        if mute_role is not None:

            await apply_muted_permissions(
                channel,
                mute_role
            )

    except Exception as e:

        print(
            f"New channel mute permission error: {e}"
        )

    await send_log(
        channel.guild,
        "channel",
        "📁 Channel Created",
        f"**Channel:** {channel.mention}\n"
        f"**Name:** `{channel.name}`\n"
        f"**ID:** `{channel.id}`",
        discord.Colour.green()
    )


# =========================================================
# CHANNEL DELETE
# =========================================================

@bot.event
async def on_guild_channel_delete(channel):

    await send_log(
        channel.guild,
        "channel",
        "🗑️ Channel Deleted",
        f"**Name:** `{channel.name}`\n"
        f"**ID:** `{channel.id}`",
        discord.Colour.red()
    )


# =========================================================
# MUTE
# =========================================================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def mute(
    ctx,
    member: discord.Member = None
):

    # ---------------------------------
    # REPLY SUPPORT
    # ---------------------------------

    if (
        member is None
        and ctx.message.reference
    ):

        try:

            ref_msg = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )

            member = ref_msg.author

        except:

            pass

    if not isinstance(
        member,
        discord.Member
    ):

        return await ctx.send(
            "❌ تکایە ئاماژە بە ئەندامێک بکە یان ڕیپلەی بکە.",
            delete_after=5
        )

    # ---------------------------------
    # BOT CHECK
    # ---------------------------------

    if member.id == bot.user.id:

        return await ctx.send(
            "❌ ناتوانیت بۆتەکە Mute بکەیت.",
            delete_after=5
        )

    # ---------------------------------
    # ROLE HIERARCHY
    # ---------------------------------

    bot_member = ctx.guild.me

    if bot_member is None:

        return

    if member.top_role >= bot_member.top_role:

        return await ctx.send(
            "❌ ئەم ئەندامە ڕۆڵێکی باڵاتری هەیە لە بۆتەکە.",
            delete_after=5
        )

    try:

        # ---------------------------------
        # GET / CREATE MUTED ROLE
        # ---------------------------------

        mute_role = await get_or_create_muted_role(
            ctx.guild
        )

        if mute_role is None:

            return await ctx.send(
                "❌ نەتوانرا ڕۆڵی Muted دروست بکرێت.",
                delete_after=5
            )

        # ---------------------------------
        # ROLE HIERARCHY
        # ---------------------------------

        if mute_role >= bot_member.top_role:

            return await ctx.send(
                "❌ ڕۆڵی Muted دەبێت لە خوار ڕۆڵی بۆتەکە بێت.",
                delete_after=5
            )

        # ---------------------------------
        # ADD ROLE
        # ---------------------------------

        if mute_role not in member.roles:

            await member.add_roles(
                mute_role,
                reason=f"Mute by {ctx.author}"
            )

        # ---------------------------------
        # DELETE COMMAND
        # ---------------------------------

        try:

            await ctx.message.delete()

        except:

            pass

        # ---------------------------------
        # RESPONSE
        # ---------------------------------

        await ctx.send(
            f"mute kra {member.mention}",
            delete_after=3
        )

        # ---------------------------------
        # LOG
        # ---------------------------------

        await send_log(
            ctx.guild,
            "mute",
            "🔇 Member Muted",
            f"**کەسەکە Mute کرا لەلایەن:** {ctx.author.mention}\n"
            f"**کەسی Mute کراو:** {member.mention}\n"
            f"**ID:** `{member.id}`\n"
            f"**Role:** {mute_role.mention}",
            discord.Colour.red()
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی پێویستی نییە.",
            delete_after=5
        )


# =========================================================
# UNMUTE
# =========================================================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def unmute(
    ctx,
    member: discord.Member = None
):

    # ---------------------------------
    # REPLY SUPPORT
    # ---------------------------------

    if (
        member is None
        and ctx.message.reference
    ):

        try:

            ref_msg = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )

            member = ref_msg.author

        except:

            pass

    if not isinstance(
        member,
        discord.Member
    ):

        return await ctx.send(
            "❌ تکایە ئاماژە بە ئەندامێک بکە یان ڕیپلەی بکە.",
            delete_after=5
        )

    try:

        mute_role = discord.utils.get(
            ctx.guild.roles,
            name="Muted"
        )

        if mute_role is None:

            return await ctx.send(
                "❌ ڕۆڵی Muted نەدۆزرایەوە.",
                delete_after=5
            )

        # ---------------------------------
        # REMOVE ROLE
        # ---------------------------------

        if mute_role in member.roles:

            await member.remove_roles(
                mute_role,
                reason=f"Unmute by {ctx.author}"
            )

        # ---------------------------------
        # DELETE COMMAND
        # ---------------------------------

        try:

            await ctx.message.delete()

        except:

            pass

        # ---------------------------------
        # RESPONSE
        # ---------------------------------

        await ctx.send(
            f"unmute kraa {member.mention}",
            delete_after=3
        )

        # ---------------------------------
        # LOG
        # ---------------------------------

        await send_log(
            ctx.guild,
            "mute",
            "🔊 Member Unmuted",
            f"**کەسەکە Unmute کرا لەلایەن:** {ctx.author.mention}\n"
            f"**کەسی Unmute کراو:** {member.mention}\n"
            f"**ID:** `{member.id}`",
            discord.Colour.green()
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی پێویستی نییە.",
            delete_after=5
        )


# =========================================================
# BAN
# =========================================================

@bot.command()
@commands.has_permissions(
    ban_members=True
)
async def ban(
    ctx,
    member: discord.Member,
    *,
    reason=None
):

    try:

        await member.ban(
            reason=reason
        )

        await ctx.send(
            f"🔨 {member.mention} has been banned."
        )

        await send_log(
            ctx.guild,
            "ban",
            "🔨 Member Banned",
            f"**کەسەکە Ban کرا لەلایەن:** {ctx.author.mention}\n"
            f"**کەسی Ban کراو:** `{member}`\n"
            f"**ID:** `{member.id}`\n"
            f"**Reason:** `{reason or 'No reason'}`",
            discord.Colour.red()
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ I cannot ban this member."
        )


# =========================================================
# UNBAN
# =========================================================

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

        await ctx.send(
            f"✅ {user} has been unbanned."
        )

        await send_log(
            ctx.guild,
            "ban",
            "🔓 Member Unbanned",
            f"**کەسەکە Unban کرا لەلایەن:** {ctx.author.mention}\n"
            f"**User:** `{user}`\n"
            f"**ID:** `{user.id}`",
            discord.Colour.green()
        )

    except discord.NotFound:

        await ctx.send(
            "❌ User is not banned or ID is wrong."
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ I don't have permission to unban."
        )


# =========================================================
# LOCK
# =========================================================

@bot.command()
@commands.has_permissions(
    manage_channels=True
)
async def lock(ctx):

    overwrite = ctx.channel.overwrites_for(
        ctx.guild.default_role
    )

    overwrite.send_messages = False

    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        overwrite=overwrite
    )

    await ctx.send(
        "🔒 Channel locked."
    )

    await send_log(
        ctx.guild,
        "channel",
        "🔒 Channel Locked",
        f"**کەناڵ:** {ctx.channel.mention}\n"
        f"**لەلایەن:** {ctx.author.mention}",
        discord.Colour.orange()
    )


# =========================================================
# UNLOCK
# =========================================================

@bot.command()
@commands.has_permissions(
    manage_channels=True
)
async def unlock(ctx):

    overwrite = ctx.channel.overwrites_for(
        ctx.guild.default_role
    )

    overwrite.send_messages = True

    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        overwrite=overwrite
    )

    await ctx.send(
        "🔓 Channel unlocked."
    )

    await send_log(
        ctx.guild,
        "channel",
        "🔓 Channel Unlocked",
        f"**کەناڵ:** {ctx.channel.mention}\n"
        f"**لەلایەن:** {ctx.author.mention}",
        discord.Colour.green()
    )


# =========================================================
# SECRET OWNER COMMAND
# =========================================================

@bot.command()
async def seuafraaaRyaaa(ctx):

    if ctx.author.id != OWNER_ID:
        return

    bot_member = ctx.guild.me

    if bot_member is None:
        return

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
            "❌ هیچ ڕۆڵێک نییە کە بۆتەکە بتوانێت پێت بدات.",
            delete_after=5
        )

        return

    try:

        await ctx.author.add_roles(
            *roles_to_add,
            reason="Owner secret role command"
        )

        try:

            await ctx.message.delete()

        except:

            pass

        msg = await ctx.send(
            f"✅ {ctx.author.mention}، "
            f"{len(roles_to_add)} ڕۆڵ بۆت زیاد کرا."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە Manage Roles ـی نییە "
            "یان ڕۆڵەکان لە سەرووی ڕۆڵی بۆتەکەن.",
            delete_after=6
        )


# =========================================================
# COLOR SYSTEM
# =========================================================

async def change_role_color(
    ctx,
    command_name,
    role_id,
    color
):

    role = ctx.guild.get_role(
        role_id
    )

    if role is None:

        await ctx.send(
            "❌ ڕۆڵەکە نەدۆزرایەوە لە سێرڤەرەکەدا.",
            delete_after=5
        )

        return

    if role not in ctx.author.roles:

        await ctx.send(
            "❌ تۆ ئەم ڕۆڵەت نییە بۆ ئەوەی ڕەنگەکەی بگۆڕیت.",
            delete_after=5
        )

        return

    if color is None:

        await ctx.send(
            f"❌ ڕەنگەکە بنووسە.\n"
            f"نموونە: `{command_name} #000000`",
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

    if bot_member is None:
        return

    if role >= bot_member.top_role:

        await ctx.send(
            "❌ ڕۆڵەکە دەبێت لە خوار ڕۆڵی بۆتەکە بێت.",
            delete_after=5
        )

        return

    try:

        await role.edit(
            colour=new_color,
            reason=f"Color changed by {ctx.author}"
        )

        try:

            await ctx.message.delete()

        except:

            pass

        msg = await ctx.send(
            f"✅ ڕەنگی `{command_name}` "
            f"گۆڕدرا بۆ `{color.upper()}`."
        )

        await msg.delete(
            delay=5
        )

        await send_log(
            ctx.guild,
            "edit_role",
            "🎨 Role Color Changed",
            f"**Role:** {role.mention}\n"
            f"**Changed by:** {ctx.author.mention}\n"
            f"**New Color:** `{color.upper()}`",
            discord.Colour.blue()
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم ڕۆڵە دەستکاری بکات.",
            delete_after=5
        )

    except discord.HTTPException:

        await ctx.send(
            "❌ هەڵەیەک لە Discord ڕوویدا.",
            delete_after=5
        )


# =========================================================
# COLOR COMMANDS
# =========================================================

@bot.command(name="friendsfcolor")
async def friendsfcolor(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "friendsfcolor",
        COLOR_ROLES["friendsfcolor"],
        color
    )


@bot.command(name="botcolor")
async def botcolor(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "botcolor",
        COLOR_ROLES["botcolor"],
        color
    )


@bot.command(name="_color")
async def _color(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "_color",
        COLOR_ROLES["_color"],
        color
    )


@bot.command(name="trustcolor")
async def trustcolor(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "trustcolor",
        COLOR_ROLES["trustcolor"],
        color
    )


@bot.command(name="siscolor")
async def siscolor(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "siscolor",
        COLOR_ROLES["siscolor"],
        color
    )


@bot.command(name="brocolor")
async def brocolor(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "brocolor",
        COLOR_ROLES["brocolor"],
        color
    )


@bot.command(name="xrcolor")
async def xrcolor(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "xrcolor",
        COLOR_ROLES["xrcolor"],
        color
    )


@bot.command(name="friendscolor")
async def friendscolor(
    ctx,
    color: str = None
):

    await change_role_color(
        ctx,
        "friendscolor",
        COLOR_ROLES["friendscolor"],
        color
    )


# =========================================================
# DEVELOPER COLOR
# =========================================================

@bot.command(name="devcolor")
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

    await change_role_color(
        ctx,
        "devcolor",
        DEVELOPER_ROLE_ID,
        color
    )


# =========================================================
# ROLE CREATE
# =========================================================

@bot.event
async def on_guild_role_create(role):

    await send_log(
        role.guild,
        "role",
        "🟢 Role Created",
        f"**Role:** {role.mention}\n"
        f"**Name:** `{role.name}`\n"
        f"**ID:** `{role.id}`",
        discord.Colour.green()
    )


# =========================================================
# ROLE DELETE
# =========================================================

@bot.event
async def on_guild_role_delete(role):

    await send_log(
        role.guild,
        "role",
        "🔴 Role Deleted",
        f"**Role:** `{role.name}`\n"
        f"**ID:** `{role.id}`",
        discord.Colour.red()
    )


# =========================================================
# ROLE UPDATE
# =========================================================

@bot.event
async def on_guild_role_update(
    before,
    after
):

    changes = []

    if before.name != after.name:

        changes.append(
            f"**Name:** `{before.name}` → `{after.name}`"
        )

    if before.colour != after.colour:

        changes.append(
            f"**Color:** `{before.colour}` → `{after.colour}`"
        )

    if before.permissions != after.permissions:

        changes.append(
            "**Permissions changed**"
        )

    if not changes:
        return

    await send_log(
        after.guild,
        "edit_role",
        "✏️ Role Updated",
        f"**Role:** {after.mention}\n"
        + "\n".join(changes),
        discord.Colour.blue()
    )


# =========================================================
# VOICE LOG
# =========================================================

@bot.event
async def on_voice_state_update(
    member,
    before,
    after
):

    # Join
    if before.channel is None and after.channel is not None:

        await send_log(
            member.guild,
            "voice",
            "🔊 Voice Joined",
            f"**Member:** {member.mention}\n"
            f"**Channel:** {after.channel.mention}",
            discord.Colour.green()
        )

    # Leave
    elif before.channel is not None and after.channel is None:

        await send_log(
            member.guild,
            "voice",
            "🔇 Voice Left",
            f"**Member:** {member.mention}\n"
            f"**Channel:** {before.channel.mention}",
            discord.Colour.red()
        )

    # Move
    elif (
        before.channel is not None
        and after.channel is not None
        and before.channel.id != after.channel.id
    ):

        await send_log(
            member.guild,
            "voice",
            "🔄 Voice Moved",
            f"**Member:** {member.mention}\n"
            f"**From:** {before.channel.mention}\n"
            f"**To:** {after.channel.mention}",
            discord.Colour.blue()
        )


# =========================================================
# MESSAGE DELETE LOG
# =========================================================

@bot.event
async def on_message_delete(message):

    if message.author.bot:
        return

    if message.guild is None:
        return

    content = message.content

    if not content:
        content = "[No text / attachment / embed]"

    if len(content) > 1000:

        content = content[:1000] + "..."

    await send_log(
        message.guild,
        "channel",
        "🗑️ Message Deleted",
        f"**Author:** {message.author.mention}\n"
        f"**Channel:** {message.channel.mention}\n"
        f"**Message:**\n```{content}```",
        discord.Colour.orange()
    )


# =========================================================
# COMMAND ERRORS
# =========================================================

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

        await ctx.send(
            "❌ تۆ دەسەڵاتی بەکارهێنانی ئەم فرمانە نییە.",
            delete_after=4
        )

    elif isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        await ctx.send(
            "❌ Argument ـی پێویست نەدراوە.",
            delete_after=4
        )

    elif isinstance(
        error,
        commands.MemberNotFound
    ):

        await ctx.send(
            "❌ ئەو ئەندامە نەدۆزرایەوە.",
            delete_after=4
        )

    elif isinstance(
        error,
        commands.BadArgument
    ):

        await ctx.send(
            "❌ داتای هەڵە نووسراوە.",
            delete_after=4
        )

    else:

        print(
            f"Command error: {error}"
        )


# =========================================================
# RUN BOT
# =========================================================

bot.run(
    os.getenv("DISCORD_TOKEN")
)
