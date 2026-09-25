import discord
from discord.ext import commands
import datetime
import os
import asyncio


# =========================================================
# 1. BOT SETTINGS
# =========================================================

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


# =========================================================
# 2. IDs
# =========================================================

WELCOME_CHANNEL_ID = 1448989203508629544

LOG_CHANNELS = {
    "edit_role": 1448989222433329262,
    "role": 1448989223590952990,
    "voice": 1448989224991981619,
    "mute": 1448989225826386045,
    "join_left": 1448989227156111370,
    "channel": 1448989228548493414,
    "ban": 1448989230524141599
}

MUTED_ROLE_NAME = "Muted"


# =========================================================
# 3. READY
# =========================================================

@bot.event
async def on_ready():

    print(
        f"بۆتەکە بە سەرکەوتوویی چالاک بوو وەک: {bot.user}"
    )

    print(
        f"Bot ID: {bot.user.id}"
    )


# =========================================================
# 4. LOG SYSTEM
# =========================================================

async def send_log(
    guild,
    log_type,
    title,
    description
):

    channel_id = LOG_CHANNELS.get(log_type)

    if channel_id is None:
        return

    channel = guild.get_channel(channel_id)

    if channel is None:
        return

    embed = discord.Embed(
        title=title,
        description=description,
        timestamp=datetime.datetime.now(
            datetime.timezone.utc
        )
    )

    try:

        await channel.send(
            embed=embed
        )

    except discord.Forbidden:

        print(
            f"Log permission error: {channel_id}"
        )

    except Exception as e:

        print(
            f"Log error: {e}"
        )


# =========================================================
# 5. WELCOME
# =========================================================

@bot.event
async def on_member_join(member):

    channel = bot.get_channel(
        WELCOME_CHANNEL_ID
    )

    if channel is not None:

        try:

            file = discord.File(
                "welcome.gif",
                filename="welcome.gif"
            )

            await channel.send(
                content=f"بەخێر بێیت {member.mention}! ✨",
                file=file
            )

        except Exception as e:

            print(
                f"کێشەیەک لە بەخێرهاتن ڕوویدا: {e}"
            )


    await send_log(
        member.guild,
        "join_left",
        "📥 ئەندام هاتە ناو سێرڤەر",
        f"**کەسەکە:** {member.mention}\n"
        f"**ناو:** `{member}`\n"
        f"**ID:** `{member.id}`"
    )


# =========================================================
# 6. MEMBER LEFT
# =========================================================

@bot.event
async def on_member_remove(member):

    await send_log(
        member.guild,
        "join_left",
        "📤 ئەندام سێرڤەرەکەی جێهێشت",
        f"**کەسەکە:** {member.mention}\n"
        f"**ناو:** `{member}`\n"
        f"**ID:** `{member.id}`"
    )


# =========================================================
# 7. GET TARGET FROM TAG OR REPLY
# =========================================================

async def get_target_member(message):

    # TAG
    if message.mentions:

        member = message.mentions[0]

        if isinstance(
            member,
            discord.Member
        ):

            return member


    # REPLY
    if message.reference:

        try:

            referenced_message = await message.channel.fetch_message(
                message.reference.message_id
            )

            if isinstance(
                referenced_message.author,
                discord.Member
            ):

                return referenced_message.author


            member = message.guild.get_member(
                referenced_message.author.id
            )

            return member

        except Exception as e:

            print(
                f"Reply target error: {repr(e)}"
            )


    return None


# =========================================================
# 8. CREATE THE MUTED PERMISSION OVERWRITE
# =========================================================

def create_muted_overwrite():

    overwrite = discord.PermissionOverwrite()

    # =====================================================
    # TEXT CHAT
    # =====================================================

    overwrite.send_messages = False

    # =====================================================
    # REACTIONS
    # =====================================================

    overwrite.add_reactions = False

    # =====================================================
    # THREADS
    # =====================================================

    overwrite.send_messages_in_threads = False

    overwrite.create_public_threads = False

    overwrite.create_private_threads = False

    # =====================================================
    # VOICE
    # =====================================================

    overwrite.speak = False

    overwrite.stream = False

    overwrite.use_voice_activation = False

    # =====================================================
    # STAGE
    # =====================================================

    overwrite.request_to_speak = False

    return overwrite


# =========================================================
# 9. APPLY MUTED PERMISSIONS TO ONE CHANNEL
# =========================================================

async def apply_muted_permissions(
    channel,
    mute_role
):

    try:

        overwrite = create_muted_overwrite()

        # =================================================
        # TEXT / NEWS / FORUM
        # =================================================

        if isinstance(
            channel,
            (
                discord.TextChannel,
                discord.NewsChannel,
                discord.ForumChannel
            )
        ):

            await channel.set_permissions(
                mute_role,
                overwrite=overwrite,
                reason="Karezma Muted role"
            )

            print(
                f"✅ Muted applied to text channel: {channel.name}"
            )

            return


        # =================================================
        # VOICE
        # =================================================

        if isinstance(
            channel,
            discord.VoiceChannel
        ):

            await channel.set_permissions(
                mute_role,
                overwrite=overwrite,
                reason="Karezma Muted role"
            )

            print(
                f"✅ Muted applied to voice channel: {channel.name}"
            )

            return


        # =================================================
        # STAGE
        # =================================================

        if isinstance(
            channel,
            discord.StageChannel
        ):

            await channel.set_permissions(
                mute_role,
                overwrite=overwrite,
                reason="Karezma Muted role"
            )

            print(
                f"✅ Muted applied to stage channel: {channel.name}"
            )

            return


        # =================================================
        # CATEGORY
        # =================================================

        if isinstance(
            channel,
            discord.CategoryChannel
        ):

            await channel.set_permissions(
                mute_role,
                overwrite=overwrite,
                reason="Karezma Muted role"
            )

            print(
                f"✅ Muted applied to category: {channel.name}"
            )

            return


    except discord.Forbidden:

        print(
            f"❌ Muted permission denied in: {channel.name}"
        )

    except discord.HTTPException as e:

        print(
            f"❌ Discord error in {channel.name}: {e}"
        )

    except Exception as e:

        print(
            f"❌ Muted permission error in {channel.name}: {e}"
        )


# =========================================================
# 10. APPLY MUTED TO EVERY CHANNEL
# =========================================================

async def apply_muted_to_all_channels(
    guild,
    mute_role
):

    print(
        f"🔄 دەست پێکرد بە چێککردنی هەموو چەنالەکانی {guild.name}"
    )

    success = 0
    failed = 0

    # -----------------------------------------------------
    # ALL GUILD CHANNELS
    # -----------------------------------------------------

    for channel in guild.channels:

        try:

            await apply_muted_permissions(
                channel,
                mute_role
            )

            success += 1

        except Exception as e:

            failed += 1

            print(
                f"❌ Channel error {channel.name}: {e}"
            )

    print(
        f"✅ Muted permissions تەواوبوو | "
        f"Success: {success} | Failed: {failed}"
    )


# =========================================================
# 11. GET OR CREATE MUTED ROLE
# =========================================================

async def get_or_create_muted_role(guild):

    # -----------------------------------------------------
    # FIND EXISTING MUTED ROLE
    # -----------------------------------------------------

    mute_role = discord.utils.get(
        guild.roles,
        name=MUTED_ROLE_NAME
    )

    # -----------------------------------------------------
    # CREATE IF NOT EXISTS
    # -----------------------------------------------------

    if mute_role is None:

        try:

            mute_role = await guild.create_role(
                name=MUTED_ROLE_NAME,
                reason="Karezma mute role"
            )

            print(
                f"✅ Muted role دروستکرا لە {guild.name}"
            )

        except discord.Forbidden:

            print(
                "❌ Bot cannot create Muted role."
            )

            return None

        except Exception as e:

            print(
                f"❌ Muted role creation error: {e}"
            )

            return None


    # -----------------------------------------------------
    # EVERY TIME MUTE IS USED:
    # SCAN ALL CHANNELS AGAIN
    # -----------------------------------------------------

    await apply_muted_to_all_channels(
        guild,
        mute_role
    )

    return mute_role


# =========================================================
# 12. NEW CHANNEL -> AUTOMATICALLY APPLY MUTED
# =========================================================

@bot.event
async def on_guild_channel_create(channel):

    try:

        mute_role = discord.utils.get(
            channel.guild.roles,
            name=MUTED_ROLE_NAME
        )

        if mute_role is not None:

            await apply_muted_permissions(
                channel,
                mute_role
            )

            print(
                f"✅ Muted permission بۆ چەنالی نوێ دانرا: "
                f"{channel.name}"
            )

    except Exception as e:

        print(
            f"New channel mute permission error: {e}"
        )


    await send_log(
        channel.guild,
        "channel",
        "📁 کەناڵ دروستکرا",
        f"**کەناڵ:** {channel.mention}\n"
        f"**ناو:** `{channel.name}`\n"
        f"**ID:** `{channel.id}`"
    )


# =========================================================
# 13. CHANNEL DELETE
# =========================================================

@bot.event
async def on_guild_channel_delete(channel):

    await send_log(
        channel.guild,
        "channel",
        "🗑️ کەناڵ سڕایەوە",
        f"**کەناڵ سڕایەوە:** `{channel.name}`\n"
        f"**ID:** `{channel.id}`"
    )


# =========================================================
# 14. ROLE CREATE
# =========================================================

@bot.event
async def on_guild_role_create(role):

    await send_log(
        role.guild,
        "edit_role",
        "➕ ڕۆڵ دروستکرا",
        f"**ڕۆڵ:** {role.mention}\n"
        f"**ناوی ڕۆڵ:** `{role.name}`"
    )


# =========================================================
# 15. ROLE DELETE
# =========================================================

@bot.event
async def on_guild_role_delete(role):

    await send_log(
        role.guild,
        "edit_role",
        "🗑️ ڕۆڵ سڕایەوە",
        f"**ڕۆڵ سڕایەوە:** `{role.name}`\n"
        f"**ID:** `{role.id}`"
    )


# =========================================================
# 16. ROLE UPDATE
# =========================================================

@bot.event
async def on_guild_role_update(
    before,
    after
):

    changes = []

    if before.name != after.name:

        changes.append(
            f"**ناوی کۆن:** `{before.name}`\n"
            f"**ناوی نوێ:** `{after.name}`"
        )

    if before.colour != after.colour:

        changes.append(
            f"**ڕەنگی کۆن:** `{before.colour}`\n"
            f"**ڕەنگی نوێ:** `{after.colour}`"
        )

    if before.permissions != after.permissions:

        changes.append(
            "**Permission ـەکان گۆڕدران.**"
        )

    if not changes:
        return

    await send_log(
        after.guild,
        "edit_role",
        "✏️ ڕۆڵ دەستکاری کرا",
        f"**ڕۆڵ:** {after.mention}\n"
        + "\n".join(changes)
    )


# =========================================================
# 17. ROLE ADD / REMOVE
# =========================================================

@bot.event
async def on_member_update(
    before,
    after
):

    before_roles = set(
        before.roles
    )

    after_roles = set(
        after.roles
    )

    added_roles = after_roles - before_roles

    removed_roles = before_roles - after_roles


    # -----------------------------------------------------
    # ROLE ADDED
    # -----------------------------------------------------

    for role in added_roles:

        if role.is_default():
            continue

        if role.name == MUTED_ROLE_NAME:
            continue

        await send_log(
            after.guild,
            "role",
            "➕ ڕۆڵ زیادکرا",
            f"**ڕۆڵ زیادکرا بۆ:** {after.mention}\n"
            f"**ڕۆڵ:** {role.mention}\n"
            f"**کەسی خاوەنی ڕۆڵ:** {after.mention}"
        )


    # -----------------------------------------------------
    # ROLE REMOVED
    # -----------------------------------------------------

    for role in removed_roles:

        if role.is_default():
            continue

        if role.name == MUTED_ROLE_NAME:
            continue

        await send_log(
            after.guild,
            "role",
            "➖ ڕۆڵ لابرا",
            f"**ڕۆڵ لابرا لە:** {after.mention}\n"
            f"**ڕۆڵ:** {role.mention}\n"
            f"**کەسی خاوەنی ڕۆڵ:** {after.mention}"
        )


# =========================================================
# 18. VOICE LOG
# =========================================================

@bot.event
async def on_voice_state_update(
    member,
    before,
    after
):

    if member.bot:
        return


    # -----------------------------------------------------
    # JOIN
    # -----------------------------------------------------

    if (
        before.channel is None
        and after.channel is not None
    ):

        await send_log(
            member.guild,
            "voice",
            "🔊 چوونە Voice",
            f"**کەسەکە:** {member.mention}\n"
            f"**Voice:** {after.channel.mention}"
        )

        return


    # -----------------------------------------------------
    # LEAVE
    # -----------------------------------------------------

    if (
        before.channel is not None
        and after.channel is None
    ):

        await send_log(
            member.guild,
            "voice",
            "🔇 دەرچوون لە Voice",
            f"**کەسەکە:** {member.mention}\n"
            f"**Voice:** {before.channel.mention}"
        )

        return


    # -----------------------------------------------------
    # MOVE
    # -----------------------------------------------------

    if (
        before.channel is not None
        and after.channel is not None
        and before.channel.id != after.channel.id
    ):

        await send_log(
            member.guild,
            "voice",
            "🔄 گواستنەوەی Voice",
            f"**کەسەکە:** {member.mention}\n"
            f"**لە:** {before.channel.mention}\n"
            f"**بۆ:** {after.channel.mention}"
        )


# =========================================================
# 19. MESSAGE DELETE LOG
# =========================================================

@bot.event
async def on_message_delete(message):

    if message.guild is None:
        return

    if message.author.bot:
        return


    content = message.content.strip()

    if not content:

        content = (
            "ناوەڕۆکی ئەم نامەیە بەردەست نییە."
        )


    deleter = None


    try:

        await asyncio.sleep(1)

        async for entry in message.guild.audit_logs(
            limit=10,
            action=discord.AuditLogAction.message_delete
        ):

            if (
                entry.target
                and entry.target.id == message.author.id
            ):

                if (
                    datetime.datetime.now(
                        datetime.timezone.utc
                    ) - entry.created_at
                ).total_seconds() < 5:

                    deleter = entry.user

                    break

    except Exception as e:

        print(
            f"Delete audit log error: {e}"
        )


    if deleter is None:

        deleter_text = (
            "نادیار / Discord نەیدۆزیوەتەوە"
        )

    else:

        deleter_text = deleter.mention


    await send_log(
        message.guild,
        "channel",
        "🗑️ چاتەکە سڕایەوە",
        f"**چاتەکە سڕایەوە لەلایەن:** {deleter_text}\n"
        f"**چاتەکە:** {content}\n"
        f"**خاوەنی چاتەکە:** {message.author.mention}\n"
        f"**کەناڵ:** {message.channel.mention}"
    )


# =========================================================
# 20. MAIN COMMAND SYSTEM
# =========================================================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.guild is None:
        return


    content = message.content.strip()

    if not content:
        return


    parts = content.split()

    # -----------------------------------------------------
    # CASE INSENSITIVE
    # -----------------------------------------------------

    command = parts[0].lower()


    # =====================================================
    # SAFIKA
    # =====================================================

    if command == "safika":

        if not message.author.guild_permissions.administrator:

            await message.channel.send(
                f"❌ {message.author.mention} تەنها ئەدمین دەتوانێت ئەم کۆماندە بەکاربهێنێت.",
                delete_after=5
            )

            return


        if (
            len(parts) < 2
            or not parts[1].isdigit()
        ):

            await message.channel.send(
                "❌ نموونە: `Safika 1000`",
                delete_after=5
            )

            return


        amount = int(
            parts[1]
        )


        if amount <= 0:

            await message.channel.send(
                "❌ ژمارەکە دەبێت زیاتر لە 0 بێت.",
                delete_after=5
            )

            return


        amount = min(
            amount,
            1000
        )


        try:

            deleted = await message.channel.purge(
                limit=amount + 1,
                bulk=True
            )


            await message.channel.send(
                f"✅ `{len(deleted)}` نامە سڕایەوە.",
                delete_after=3
            )


        except discord.Forbidden:

            await message.channel.send(
                "❌ بۆتەکە دەسەڵاتی سڕینەوەی نامەی نییە.",
                delete_after=5
            )


        except Exception as e:

            print(
                f"Safika error: {e}"
            )

            await message.channel.send(
                "❌ کێشەیەک لە سڕینەوەی نامەکان ڕوویدا.",
                delete_after=5
            )


        return


    # =====================================================
    # MUTE
    # =====================================================

    if command == "mute":

        if not message.author.guild_permissions.administrator:

            await message.channel.send(
                f"❌ {message.author.mention} تەنها ئەدمین دەتوانێت Mute بەکاربهێنێت.",
                delete_after=5
            )

            return


        target = await get_target_member(
            message
        )


        if target is None:

            await message.channel.send(
                "❌ کەسێک Tag بکە یان Reply ـی نامەکەی بکە و بنووسە `Mute`.",
                delete_after=5
            )

            return


        if target.id == bot.user.id:

            await message.channel.send(
                "❌ ناتوانم خۆم Mute بکەم.",
                delete_after=5
            )

            return


        if target.id == message.guild.owner_id:

            await message.channel.send(
                "❌ ناتوانرێت خاوەنی سێرڤەر Mute بکرێت.",
                delete_after=5
            )

            return


        me = message.guild.me

        if me is None:

            await message.channel.send(
                "❌ بۆتەکە ناتوانێت زانیاری ڕۆڵەکەی بدۆزێتەوە.",
                delete_after=5
            )

            return


        if target.top_role >= me.top_role:

            await message.channel.send(
                "❌ ڕۆڵی ئەو کەسە لە ڕۆڵی بۆتەکە بەرزترە یان یەکسانە.",
                delete_after=5
            )

            return


        try:

            # =================================================
            # FIND / CREATE MUTED ROLE
            # AND APPLY TO ALL CHANNELS
            # =================================================

            mute_role = await get_or_create_muted_role(
                message.guild
            )


            if mute_role is None:

                await message.channel.send(
                    "❌ بۆتەکە ناتوانێت ڕۆڵی Muted دروست بکات.",
                    delete_after=5
                )

                return


            # =================================================
            # CHECK ROLE HIERARCHY
            # =================================================

            if mute_role >= me.top_role:

                await message.channel.send(
                    "❌ ڕۆڵی `Muted` دەبێت لە خوار ڕۆڵی بۆتەکە بێت.",
                    delete_after=6
                )

                return


            # =================================================
            # ADD MUTED ROLE
            # =================================================

            if mute_role not in target.roles:

                await target.add_roles(
                    mute_role,
                    reason=f"Karezma Mute by {message.author}"
                )


            # =================================================
            # DELETE COMMAND
            # =================================================

            try:

                await message.delete()

            except:

                pass


            # =================================================
            # MUTE MESSAGE
            # =================================================

            await message.channel.send(
                f"mute kra {target.mention}",
                delete_after=2
            )


            # =================================================
            # MUTE LOG
            # =================================================

            await send_log(
                message.guild,
                "mute",
                "🔇 کەسەکە Mute کرا",
                f"**کەسەکە Mute کرا لەلایەن:** {message.author.mention}\n"
                f"**کەسی Mute کراو:** {target.mention}\n"
                f"**ڕۆڵ:** {mute_role.mention}"
            )


        except discord.Forbidden:

            await message.channel.send(
                "❌ بۆتەکە دەسەڵاتی زیادکردنی ڕۆڵی نییە.",
                delete_after=5
            )


        except Exception as e:

            print(
                f"Mute error: {e}"
            )

            await message.channel.send(
                "❌ کێشەیەک لە Mute ڕوویدا.",
                delete_after=5
            )


        return


    # =====================================================
    # UNMUTE
    # =====================================================

    if command == "unmute":

        if not message.author.guild_permissions.administrator:

            await message.channel.send(
                f"❌ {message.author.mention} تەنها ئەدمین دەتوانێت Unmute بەکاربهێنێت.",
                delete_after=5
            )

            return


        target = await get_target_member(
            message
        )


        if target is None:

            await message.channel.send(
                "❌ کەسێک Tag بکە یان Reply ـی بکە و بنووسە `Unmute`.",
                delete_after=5
            )

            return


        try:

            mute_role = discord.utils.get(
                message.guild.roles,
                name=MUTED_ROLE_NAME
            )


            if mute_role is None:

                await message.channel.send(
                    "❌ ڕۆڵی `Muted` بوونی نییە.",
                    delete_after=5
                )

                return


            if mute_role in target.roles:

                await target.remove_roles(
                    mute_role,
                    reason=f"Karezma Unmute by {message.author}"
                )


            try:

                await message.delete()

            except:

                pass


            # =================================================
            # UNMUTE MESSAGE
            # =================================================

            await message.channel.send(
                f"unmute kraa {target.mention}",
                delete_after=2
            )


            # =================================================
            # UNMUTE LOG
            # =================================================

            await send_log(
                message.guild,
                "mute",
                "🔊 کەسەکە Unmute کرا",
                f"**کەسەکە Unmute کرا لەلایەن:** {message.author.mention}\n"
                f"**کەسی Unmute کراو:** {target.mention}"
            )


        except discord.Forbidden:

            await message.channel.send(
                "❌ بۆتەکە ناتوانێت ڕۆڵی Muted لەسەر ئەو کەسە لاببات.",
                delete_after=5
            )


        except Exception as e:

            print(
                f"Unmute error: {e}"
            )

            await message.channel.send(
                "❌ کێشەیەک لە Unmute ڕوویدا.",
                delete_after=5
            )


        return


    # =====================================================
    # BFRA
    # =====================================================

    if command == "bfra":

        if not message.author.guild_permissions.administrator:

            await message.channel.send(
                f"❌ {message.author.mention} تەنها ئەدمین دەتوانێت Bfra بەکاربهێنێت.",
                delete_after=5
            )

            return


        target = await get_target_member(
            message
        )


        if target is None:

            await message.channel.send(
                "❌ کەسێک Tag بکە یان Reply ـی بکە و بنووسە `Bfra`.",
                delete_after=5
            )

            return


        if target.id == bot.user.id:

            await message.channel.send(
                "❌ ناتوانم خۆم Bfra بکەم.",
                delete_after=5
            )

            return


        if target.top_role >= message.guild.me.top_role:

            await message.channel.send(
                "❌ ڕۆڵی ئەو کەسە لە ڕۆڵی بۆتەکە بەرزترە یان یەکسانە.",
                delete_after=5
            )

            return


        try:

            await target.ban(
                reason=f"Karezma Bfra by {message.author}"
            )


            try:

                await message.delete()

            except:

                pass


            await message.channel.send(
                f"Frenraa✈️ {target.mention}",
                delete_after=2
            )


            await send_log(
                message.guild,
                "ban",
                "🔨 کەسەکە Bfra کرا",
                f"**کەسەکە Bfra کرا لەلایەن:** {message.author.mention}\n"
                f"**کەسی Bfra کراو:** {target.mention}\n"
                f"**هۆکار:** Karezma Bfra"
            )


        except discord.Forbidden:

            await message.channel.send(
                "❌ بۆتەکە دەسەڵاتی Bfra کردنی ئەو کەسە نییە.",
                delete_after=5
            )


        except Exception as e:

            print(
                f"Bfra error: {e}"
            )

            await message.channel.send(
                "❌ کێشەیەک لە Bfra ڕوویدا.",
                delete_after=5
            )


        return


    # =====================================================
    # UNBAN
    # =====================================================

    if command == "unban":

        if not message.author.guild_permissions.administrator:

            await message.channel.send(
                f"❌ {message.author.mention} تەنها ئەدمین دەتوانێت Unban بەکاربهێنێت.",
                delete_after=5
            )

            return


        user = None


        if (
            len(parts) >= 2
            and parts[1].isdigit()
        ):

            try:

                user = await bot.fetch_user(
                    int(parts[1])
                )

            except:

                user = None


        elif message.reference:

            try:

                referenced_message = await message.channel.fetch_message(
                    message.reference.message_id
                )

                user = referenced_message.author

            except:

                user = None


        if user is None:

            await message.channel.send(
                "❌ ID ـی بەکارهێنەر بنووسە یان Reply بکە و `Unban` بنووسە.",
                delete_after=5
            )

            return


        try:

            await message.guild.unban(
                user,
                reason=f"Karezma Unban by {message.author}"
            )


            try:

                await message.delete()

            except:

                pass


            await message.channel.send(
                f"✅ {user.mention} Unban کرا.",
                delete_after=3
            )


            await send_log(
                message.guild,
                "ban",
                "🔓 کەسەکە Unban کرا",
                f"**کەسەکە Unban کرا لەلایەن:** {message.author.mention}\n"
                f"**کەسی Unban کراو:** {user.mention}"
            )


        except discord.NotFound:

            await message.channel.send(
                "❌ ئەم بەکارهێنەرە Ban نەکراوە.",
                delete_after=5
            )


        except discord.Forbidden:

            await message.channel.send(
                "❌ بۆتەکە دەسەڵاتی Unban کردنی نییە.",
                delete_after=5
            )


        except Exception as e:

            print(
                f"Unban error: {e}"
            )

            await message.channel.send(
                "❌ کێشەیەک لە Unban ڕوویدا.",
                delete_after=5
            )


        return


    # =====================================================
    # LOCK
    # =====================================================

    if command == "lock":

        if not message.author.guild_permissions.manage_channels:

            await message.channel.send(
                f"❌ {message.author.mention} تۆ دەسەڵاتی Lock کردنی کەناڵت نییە.",
                delete_after=5
            )

            return


        try:

            await message.channel.set_permissions(
                message.guild.default_role,
                send_messages=False,
                reason=f"Locked by {message.author}"
            )


            try:

                await message.delete()

            except:

                pass


            await message.channel.send(
                "🔒 کەناڵەکە Lock کرا.",
                delete_after=3
            )


        except discord.Forbidden:

            await message.channel.send(
                "❌ بۆتەکە دەسەڵاتی Lock کردنی کەناڵی نییە.",
                delete_after=5
            )


        except Exception as e:

            print(
                f"Lock error: {e}"
            )


        return


    # =====================================================
    # UNLOCK
    # =====================================================

    if command == "unlock":

        if not message.author.guild_permissions.manage_channels:

            await message.channel.send(
                f"❌ {message.author.mention} تۆ دەسەڵاتی Unlock کردنی کەناڵت نییە.",
                delete_after=5
            )

            return


        try:

            await message.channel.set_permissions(
                message.guild.default_role,
                send_messages=None,
                reason=f"Unlocked by {message.author}"
            )


            try:

                await message.delete()

            except:

                pass


            await message.channel.send(
                "🔓 کەناڵەکە Unlock کرا.",
                delete_after=3
            )


        except discord.Forbidden:

            await message.channel.send(
                "❌ بۆتەکە دەسەڵاتی Unlock کردنی کەناڵی نییە.",
                delete_after=5
            )


        except Exception as e:

            print(
                f"Unlock error: {e}"
            )


        return


# =========================================================
# 21. ERROR HANDLER
# =========================================================

@bot.event
async def on_command_error(
    ctx,
    error
):

    if isinstance(
        error,
        (
            commands.CommandNotFound,
            commands.MissingPermissions
        )
    ):

        return


    print(
        f"Command error: {repr(error)}"
    )


# =========================================================
# 22. RUN BOT
# =========================================================

TOKEN = os.getenv(
    "DISCORD_TOKEN"
)

if not TOKEN:

    raise RuntimeError(
        "DISCORD_TOKEN environment variable is missing."
    )


bot.run(TOKEN)
