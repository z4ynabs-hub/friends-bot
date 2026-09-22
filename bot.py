import os
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
# SETTINGS
# =========================

WELCOME_CHANNEL_ID = 1550619956423688342

# Discord User ID ـی خۆت
OWNER_ID = 1130455970494025860

# Developer Role ID
DEVELOPER_ROLE_ID = 1448989145740480605

# Muted Role
MUTE_ROLE_NAME = "Muted"

WELCOME_GIF = (
    "https://cdn.discordapp.com/attachments/"
    "1550619956423688342/1551709269043314768/"
    "welcome.gif?ex=6ab2f55f&is=6ab1a3df&"
    "hm=612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"
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
# BOT READY
# =========================

@bot.event
async def on_ready():

    print(
        f"Bot is online as {bot.user}"
    )


# =========================
# MEMBER JOIN
# =========================

@bot.event
async def on_member_join(member):

    friends_role = discord.utils.get(
        member.guild.roles,
        name="Friends"
    )

    if friends_role:
        try:
            await member.add_roles(friends_role)
        except discord.Forbidden:
            print("Bot cannot give Friends role.")

    channel = member.guild.get_channel(
        WELCOME_CHANNEL_ID
    )

    if channel is None:
        return

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
# CLEAR
# =========================

@bot.command()
@commands.has_permissions(
    manage_messages=True
)
async def clear(ctx, amount: int):

    if amount <= 0:
        return await ctx.send(
            "❌ دانەیەکی دروست بنووسە.",
            delete_after=3
        )

    deleted = await ctx.channel.purge(
        limit=amount + 1
    )

    msg = await ctx.send(
        f"🧹 {len(deleted) - 1} messages deleted."
    )

    await msg.delete(
        delay=3
    )


# =========================================================
# GET TARGET
#
# بە دوو شێوە:
#
# mute @user
#
# یان:
#
# Reply -> mute
# =========================================================

async def get_target(ctx):

    # =========================
    # TAG
    # =========================

    if ctx.message.mentions:

        return ctx.message.mentions[0]


    # =========================
    # REPLY
    # =========================

    if ctx.message.reference:

        try:

            replied_message = (
                ctx.message.reference.resolved
            )

            if isinstance(
                replied_message,
                discord.Message
            ):

                return replied_message.author

        except:
            pass


        try:

            replied_message = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )

            return replied_message.author

        except:
            pass


    return None


# =========================================================
# MUTED ROLE
# =========================================================

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


# =========================================================
# APPLY MUTE PERMISSIONS
# =========================================================

async def apply_mute_permissions(
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

        if isinstance(
            channel,
            (
                discord.TextChannel,
                discord.NewsChannel,
                discord.ForumChannel
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


# =========================================================
# MUTE
#
# mute @user
#
# OR
#
# Reply -> mute
#
# NO TIMEOUT
# NO TIMER
# NO AUTO UNMUTE
# =========================================================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def mute(ctx):

    member = await get_target(
        ctx
    )

    if member is None:

        msg = await ctx.send(
            "❌ تکایە کەسەکە Tag بکە یان Reply بکە."
        )

        await msg.delete(
            delay=5
        )

        return


    # =========================
    # SELF CHECK
    # =========================

    if member.id == ctx.author.id:

        msg = await ctx.send(
            "❌ ناتوانیت خۆت Mute بکەیت."
        )

        await msg.delete(
            delay=5
        )

        return


    # =========================
    # SERVER OWNER
    # =========================

    if member.id == ctx.guild.owner_id:

        msg = await ctx.send(
            "❌ ناتوانیت Server Owner Mute بکەیت."
        )

        await msg.delete(
            delay=5
        )

        return


    # =========================
    # BOT HIERARCHY
    # =========================

    bot_member = ctx.guild.me

    if (
        member.top_role >= bot_member.top_role
        and member.id != ctx.guild.owner_id
    ):

        msg = await ctx.send(
            "❌ ڕۆڵی ئەو کەسە بەرزتر یان یەکسانە بە ڕۆڵی بۆتەکە."
        )

        await msg.delete(
            delay=5
        )

        return


    try:

        # =========================
        # GET MUTED ROLE
        # =========================

        muted_role = await get_muted_role(
            ctx.guild
        )


        # =========================
        # CHECK ROLE HIERARCHY
        # =========================

        if muted_role >= bot_member.top_role:

            msg = await ctx.send(
                "❌ `Muted` role دەبێت لە خوار ڕۆڵی بۆتەکە بێت."
            )

            await msg.delete(
                delay=5
            )

            return


        # =========================
        # BLOCK ALL CHAT CHANNELS
        # =========================

        await apply_mute_permissions(
            ctx.guild,
            muted_role
        )


        # =========================
        # ADD MUTED ROLE
        # =========================

        if muted_role not in member.roles:

            await member.add_roles(
                muted_role,
                reason=f"Muted by {ctx.author}"
            )


        # =========================
        # NOTIFICATION
        # =========================

        msg = await ctx.send(
            f"🔇 **MUTE کرا**\n"
            f"👤 کەسەکە: {member.mention}\n"
            f"🛡️ لەلایەن: {ctx.author.mention}"
        )

        await msg.delete(
            delay=10
        )


        # =========================
        # DELETE COMMAND
        # =========================

        try:
            await ctx.message.delete()
        except:
            pass


    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە مۆڵەتی پێویستی نییە.\n"
            "دڵنیابە `Manage Roles` و `Manage Channels` هەیە.",
            delete_after=6
        )


# =========================================================
# UNMUTE
#
# unmute @user
#
# OR
#
# Reply -> unmute
# =========================================================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def unmute(ctx):

    member = await get_target(
        ctx
    )

    if member is None:

        msg = await ctx.send(
            "❌ تکایە کەسەکە Tag بکە یان Reply بکە."
        )

        await msg.delete(
            delay=5
        )

        return


    muted_role = discord.utils.get(
        ctx.guild.roles,
        name=MUTE_ROLE_NAME
    )


    if muted_role is None:

        msg = await ctx.send(
            "❌ `Muted` role نەدۆزرایەوە."
        )

        await msg.delete(
            delay=5
        )

        return


    try:

        # =========================
        # REMOVE MUTED ROLE
        # =========================

        if muted_role in member.roles:

            await member.remove_roles(
                muted_role,
                reason=f"Unmuted by {ctx.author}"
            )


        # =========================
        # NOTIFICATION
        # =========================

        msg = await ctx.send(
            f"🔊 **UNMUTE کرا**\n"
            f"👤 کەسەکە: {member.mention}\n"
            f"🛡️ لەلایەن: {ctx.author.mention}"
        )

        await msg.delete(
            delay=10
        )


        # =========================
        # DELETE COMMAND
        # =========================

        try:
            await ctx.message.delete()
        except:
            pass


    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت Muted role ـەکە لاببات.",
            delete_after=6
        )


# =========================
# BAN
# =========================

@bot.command()
@commands.has_permissions(
    ban_members=True
)
async def ban(ctx, member: discord.Member, *, reason=None):

    try:

        await member.ban(
            reason=reason
        )

        await ctx.send(
            f"🔨 {member.mention} has been banned."
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ I cannot ban this member."
        )


# =========================
# UNBAN
# =========================

@bot.command()
@commands.has_permissions(
    ban_members=True
)
async def unban(ctx, user_id: int):

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

    except discord.NotFound:

        await ctx.send(
            "❌ User is not banned or ID is wrong."
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ I don't have permission to unban."
        )


# =========================
# LOCK
# =========================

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


# =========================
# UNLOCK
# =========================

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
# DEVELOPER ROLE COLOR
# =========================================================

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


# =========================================================
# GENERAL ROLE COLOR FUNCTION
# =========================================================

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
            "❌ Role نەدۆزرایەوە.",
            delete_after=5
        )

        return


    if color is None:

        await ctx.send(
            f"❌ نموونە: `{role.name} #000000`",
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


    # =========================
    # USER ROLE HIERARCHY
    # =========================

    if role >= ctx.author.top_role:

        await ctx.send(
            "❌ ڕۆڵت نزمترە لەو ڕۆڵەی کە دەتەوێت بیگۆڕیت.",
            delete_after=5
        )

        return


    # =========================
    # BOT ROLE HIERARCHY
    # =========================

    bot_member = ctx.guild.me

    if role >= bot_member.top_role:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەو role ـە بگۆڕێت.",
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
            f"🎨 ڕەنگی **{role.name}** گۆڕدرا بۆ `{color.upper()}`."
        )

        await msg.delete(
            delay=5
        )


    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەو role ـە بگۆڕێت.",
            delete_after=5
        )


# =========================================================
# COLOR COMMANDS
# =========================================================

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


@bot.command(
    name="_color"
)
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

        return


    if isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        await ctx.send(
            "❌ Argument ـی پێویست نەدراوە.",
            delete_after=4
        )

        return


    if isinstance(
        error,
        commands.MemberNotFound
    ):

        await ctx.send(
            "❌ ئەو ئەندامە نەدۆزرایەوە.",
            delete_after=4
        )

        return


    if isinstance(
        error,
        commands.BadArgument
    ):

        await ctx.send(
            "❌ داتای هەڵە نووسراوە.",
            delete_after=4
        )

        return


    print(
        f"Command Error: {error}"
    )


# =========================
# RUN BOT
# =========================

bot.run(
    os.getenv("DISCORD_TOKEN")
)
