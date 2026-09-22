import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Commands without !
bot = commands.Bot(command_prefix="", intents=intents)

WELCOME_CHANNEL_ID = 1550619956423688342
OWNER_ID = 1130455970494025860
DEVELOPER_ROLE_ID = 1448989145740480605

WELCOME_GIF = "https://cdn.discordapp.com/attachments/1550619956423688342/1551709269043314768/welcome.gif?ex=6ab2f55f&is=6ab1a3df&hm=612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"

QNM_IMAGE = "https://cdn.discordapp.com/attachments/1488625936927555816/1551783128962564176/7fb8c35c613b332ee89c22dc93bf2b33.jpg?ex=6ab33a28&is=6ab1e8a8&hm=f5c009e72ca533f5ca5b26d6c1af307b8645861da9875fee3662387774f3e51d&"


# ROLE IDs
FRIENDSFCOLOR_ROLE_ID = 1550035593239461888
BOTCOLOR_ROLE_ID = 1448989146885652603
_COLOR_ROLE_ID = 1491385293457330229
TRUSTCOLOR_ROLE_ID = 1448989152379932773
SISCOLOR_ROLE_ID = 1448989144410886145
BRCOLOR_ROLE_ID = 1448989153667711069
XRCOLOR_ROLE_ID = 1451268943548383406
FRIENDSCOLOR_ROLE_ID = 1448989154578010238


@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")


# WELCOME
@bot.event
async def on_member_join(member):
    friends_role = discord.utils.get(member.guild.roles, name="Friends")

    if friends_role:
        try:
            await member.add_roles(friends_role)
        except:
            pass

    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)

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

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=WELCOME_GIF)

        await channel.send(embed=embed)


# TEST WELCOME
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

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_image(url=WELCOME_GIF)

    await ctx.send(embed=embed)

    try:
        await ctx.message.delete()
    except:
        pass


# QNM BDE
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower().strip() == "qnm bde":
        await message.channel.send(QNM_IMAGE)
        await message.channel.send("ama ba qnt")
        return

    await bot.process_commands(message)


# CLEAR
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount + 1)

    msg = await ctx.send(
        f"✅ {len(deleted) - 1} messages deleted."
    )

    await msg.delete(delay=5)


# GET TARGET FROM MENTION OR REPLY
async def get_target(ctx, member=None):
    # Mention
    if member is not None:
        return member

    # Reply
    reference = ctx.message.reference

    if reference and reference.message_id:
        try:
            if isinstance(reference.resolved, discord.Message):
                return reference.resolved.author

            replied_message = await ctx.channel.fetch_message(
                reference.message_id
            )

            return replied_message.author

        except:
            return None

    return None


# CHECK TARGET HIERARCHY
async def check_target(ctx, member):
    if member is None:
        await ctx.send(
            "❌ تاگی بکە یان لەسەر پەیامی ئەو کەسە Reply بکە.",
            delete_after=5
        )
        return False

    # Server Owner cannot be targeted
    if member.id == ctx.guild.owner_id:
        await ctx.send(
            "❌ خاوەنی سێرڤەر ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )
        return False

    # Bot itself cannot be targeted
    if member.id == bot.user.id:
        await ctx.send(
            "❌ بۆتەکە ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )
        return False

    # Developer role is protected
    developer_role = ctx.guild.get_role(DEVELOPER_ROLE_ID)

    if developer_role and developer_role in member.roles:
        await ctx.send(
            "❌ ئەم کەسە ڕۆڵی Developer ـی هەیە و ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )
        return False

    # Bot's highest role
    bot_member = ctx.guild.me

    if bot_member is None:
        await ctx.send(
            "❌ بۆتەکە نەدۆزرایەوە.",
            delete_after=5
        )
        return False

    # Target must be below bot's highest role
    if member.top_role >= bot_member.top_role:
        await ctx.send(
            "❌ ئەم کەسە ڕۆڵێکی یەکسان یان بەرزتری لە بۆتەکەی هەیە، ناتوانرێت ئەم کارەی لەگەڵ بکرێت.",
            delete_after=5
        )
        return False

    # User must have a higher role than target
    if member.top_role >= ctx.author.top_role:
        await ctx.send(
            "❌ ڕۆڵت نزمتر یان یەکسانە لە ڕۆڵی ئەو کەسەی کە دەتەوێت ئەم کارەی لەگەڵ بکەیت.",
            delete_after=5
        )
        return False

    return True


# KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kik(ctx, member: discord.Member = None):

    member = await get_target(ctx, member)

    if not await check_target(ctx, member):
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

        await msg.delete(delay=5)

    except discord.Forbidden:
        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم کەسە Kick بکات.",
            delete_after=5
        )


# BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(
    ctx,
    member: discord.Member = None,
    *,
    reason="No reason provided"
):

    member = await get_target(ctx, member)

    if not await check_target(ctx, member):
        return

    try:
        await member.ban(
            reason=reason
        )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"🔨 {member.mention} banned.\nReason: {reason}"
        )

        await msg.delete(delay=5)

    except discord.Forbidden:
        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم کەسە Ban بکات.",
            delete_after=5
        )


# UNBAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)

        await ctx.guild.unban(user)

        msg = await ctx.send(
            f"✅ {user} unbanned."
        )

        await msg.delete(delay=5)

    except discord.NotFound:
        await ctx.send(
            "❌ User not found or not banned.",
            delete_after=5
        )


# MUTE
@bot.command()
@commands.has_permissions(manage_channels=True)
async def mute(ctx, member: discord.Member = None):

    member = await get_target(ctx, member)

    if not await check_target(ctx, member):
        return

    try:
        await ctx.channel.set_permissions(
            member,
            send_messages=False
        )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"🔇 {member.mention} muted."
        )

        await msg.delete(delay=5)

    except discord.Forbidden:
        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم کەسە Mute بکات.",
            delete_after=5
        )


# UNMUTE
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unmute(ctx, member: discord.Member = None):

    member = await get_target(ctx, member)

    if not await check_target(ctx, member):
        return

    try:
        await ctx.channel.set_permissions(
            member,
            send_messages=None
        )

        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(
            f"🔊 {member.mention} unmuted."
        )

        await msg.delete(delay=5)

    except discord.Forbidden:
        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم کەسە Unmute بکات.",
            delete_after=5
        )


# LOCK
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=False
    )

    msg = await ctx.send(
        "🔒 Channel locked."
    )

    await msg.delete(delay=5)


# UNLOCK
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=True
    )

    msg = await ctx.send(
        "🔓 Channel unlocked."
    )

    await msg.delete(delay=5)


# OWNER ROLE COMMAND
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
            await ctx.author.add_roles(role)

        msg = await ctx.send(
            "✅ هەموو ڕۆڵە بەردەستەکان زیادکران."
        )

        await msg.delete(delay=5)

    except discord.Forbidden:
        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی زیادکردنی ئەو ڕۆڵانەی نییە.",
            delete_after=5
        )


# DEVELOPER COLOR
@bot.command()
async def devcolor(ctx, color: str = None):

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

    if not color.startswith("#") or len(color) != 7:
        await ctx.send(
            "❌ ڕەنگەکە دەبێت بە شێوەی `#000000` بێت.",
            delete_after=5
        )
        return

    try:
        new_color = discord.Colour.from_str(color)

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

        await msg.delete(delay=5)

    except discord.Forbidden:
        await ctx.send(
            "❌ بۆتەکە ناتوانێت ڕۆڵی Developer دەستکاری بکات.",
            delete_after=5
        )


# ROLE COLOR SYSTEM
async def change_role_color(ctx, role_id, color):

    role = ctx.guild.get_role(role_id)

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

    if not color.startswith("#") or len(color) != 7:
        await ctx.send(
            "❌ ڕەنگەکە دەبێت بە شێوەی `#000000` بێت.",
            delete_after=5
        )
        return

    try:
        new_color = discord.Colour.from_str(color)

    except ValueError:
        await ctx.send(
            "❌ ئەم Hex Color ـە دروست نییە.",
            delete_after=5
        )
        return

    bot_member = ctx.guild.me

    # Bot cannot edit its own role or roles above it
    if role >= bot_member.top_role:
        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم ڕۆڵە بگۆڕێت.",
            delete_after=5
        )
        return

    # User can edit own role and roles below it
    # User cannot edit roles above their highest role
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

        await msg.delete(delay=5)

    except discord.Forbidden:
        await ctx.send(
            "❌ بۆتەکە ناتوانێت ئەم ڕۆڵە دەستکاری بکات.",
            delete_after=5
        )


# FRIENDS F COLOR
@bot.command()
async def friendsfcolor(ctx, color: str = None):
    await change_role_color(
        ctx,
        FRIENDSFCOLOR_ROLE_ID,
        color
    )


# BOT COLOR
@bot.command()
async def botcolor(ctx, color: str = None):
    await change_role_color(
        ctx,
        BOTCOLOR_ROLE_ID,
        color
    )


# _COLOR
@bot.command(name="_color")
async def _color(ctx, color: str = None):
    await change_role_color(
        ctx,
        _COLOR_ROLE_ID,
        color
    )


# TRUST COLOR
@bot.command()
async def trustcolor(ctx, color: str = None):
    await change_role_color(
        ctx,
        TRUSTCOLOR_ROLE_ID,
        color
    )


# SIS COLOR
@bot.command()
async def siscolor(ctx, color: str = None):
    await change_role_color(
        ctx,
        SISCOLOR_ROLE_ID,
        color
    )


# BRO COLOR
@bot.command()
async def brocolor(ctx, color: str = None):
    await change_role_color(
        ctx,
        BRCOLOR_ROLE_ID,
        color
    )


# XR COLOR
@bot.command()
async def xrcolor(ctx, color: str = None):
    await change_role_color(
        ctx,
        XRCOLOR_ROLE_ID,
        color
    )


# FRIENDS COLOR
@bot.command()
async def friendscolor(ctx, color: str = None):
    await change_role_color(
        ctx,
        FRIENDSCOLOR_ROLE_ID,
        color
    )


# ERROR HANDLER
@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ تۆ دەسەڵاتی ئەم command ـەت نییە.",
            delete_after=5
        )

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ تاگی بکە یان لەسەر پەیامی ئەو کەسە Reply بکە.",
            delete_after=5
        )

    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(
            "❌ ئەم ئەندامە نەدۆزرایەوە.",
            delete_after=5
        )

    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "❌ Argument ـەکە هەڵەیە.",
            delete_after=5
        )


# RUN BOT
bot.run(os.getenv("DISCORD_TOKEN"))
