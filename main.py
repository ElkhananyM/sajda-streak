import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import random

# --- Loading Environment Variables ---
load_dotenv() # Loads variables from a .env file for local testing
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise RuntimeError("DISCORD_TOKEN not found in environment!")

# --- Bot Configuration ---
# Paste your channel ID here. If 0, the bot works in all channels.
ALLOWED_CHANNEL_ID = os.getenv("CHANNEL_ID")

# --- Bot Setup ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Data File ---
DATA_FILE = "prayer_counts.json"

# --- Arabic Motivational Quotes ---
MILESTONE_QUOTES_AR = [
    "قال رسول الله ﷺ: «الصَّلَاةُ نُورٌ» \n(صحيح مسلم) \n*The Prophet (ﷺ) said: 'Prayer is a light.' (Sahih Muslim)*",
    "قال تعالى: ﴿وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ﴾ \n(البقرة: 45) \n*Allah says: 'And seek help through patience and prayer.' (Quran 2:45)*",
    "قال رسول الله ﷺ: «أَحَبُّ الْأَعْمَالِ إِلَى اللَّهِ أَدْوَمُهَا وَإِنْ قَلَّ» \n(صحيح البخاري) \n*The Prophet (ﷺ) said: 'The most beloved of deeds to Allah are the most consistent, even if it is small.' (Sahih Bukhari)*",
    "قال تعالى: ﴿إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ﴾ \n(العنكبوت: 45) \n*Allah says: 'Indeed, prayer prohibits immorality and wrongdoing.' (Quran 29:45)*",
    "قال رسول الله ﷺ: «قُرَّةُ عَيْنِي فِي الصَّلَاةِ» \n(سنن النسائي) \n*The Prophet (ﷺ) said: 'The delight of my eyes is in prayer.' (Sunan an-Nasa'i)*",
    "قال تعالى: ﴿وَأَقِيمُوا الصَّلَاةَ وَآتُوا الزَّكَاةَ وَارْكَعُوا مَعَ الرَّاكِعِينَ﴾ \n(البقرة: 43) \n*Allah says: 'And establish prayer and give zakah and bow with those who bow.' (Quran 2:43)*",
    "قال رسول الله ﷺ: «مَنْ غَدَا إِلَى الْمَسْجِدِ وَرَاحَ، أَعَدَّ اللَّهُ لَهُ نُزُلَهُ مِنَ الْجَنَّةِ كُلَّمَا غَدَا أَوْ رَاحَ» \n(صحيح البخاري) \n*The Prophet (ﷺ) said: 'He who goes to the mosque in the morning and evening, Allah will prepare for him a place in Paradise for every morning and evening.' (Sahih Bukhari)*",
    "قال تعالى: ﴿حَافِظُوا عَلَى الصَّلَوَاتِ وَالصَّلَاةِ الْوُسْطَىٰ﴾ \n(البقرة: 238) \n*Allah says: 'Guard strictly the prayers, especially the middle prayer.' (Quran 2:238)*",
    "قال رسول الله ﷺ: «مَنْ تَقَرَّبَ إِلَيَّ شِبْرًا تَقَرَّبْتُ إِلَيْهِ ذِرَاعًا» \n(حديث قدسي - صحيح البخاري) \n*The Prophet (ﷺ) said that Allah says: 'Whoever draws near to Me by a hand’s span, I draw near to him by a cubit.' (Hadith Qudsi - Sahih Bukhari)*",
    "قال تعالى: ﴿فَاذْكُرُونِي أَذْكُرْكُمْ﴾ \n(البقرة: 152) \n*Allah says: 'So remember Me; I will remember you.' (Quran 2:152)*"
]
RESET_QUOTES_AR = [
    "قال تعالى: ﴿قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ﴾ \n(الزمر: 53) \n*Allah says: 'Say, O My servants who have transgressed against themselves, do not despair of the mercy of Allah.' (Quran 39:53)*",
    "قال رسول الله ﷺ: «إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ» \n(صحيح البخاري) \n*The Prophet (ﷺ) said: 'Verily, actions are by their intentions.' Renew your intention and begin again.*",
    "قال تعالى: ﴿فَإِنَّ مَعَ الْعُسْرِ يُسْرًا﴾ \n(الشرح: 5) \n*Allah says: 'For indeed, with hardship will be ease.' A stumble is not a fall. You can do this!*"
]
GOAL_QUOTE_AR = "قال رسول الله ﷺ: «مَنْ صَلَّى لِلَّهِ أَرْبَعِينَ يَوْمًا فِي جَمَاعَةٍ يُدْرِكُ التَّكْبِيرَةَ الْأُولَى كُتِبَتْ لَهُ بَرَاءَتَانِ: بَرَاءَةٌ مِنَ النَّارِ، وَبَرَاءَةٌ مِنَ النِّفَاقِ» \n(سنن الترمذي) \n*The Prophet (ﷺ) said: 'Whoever prays to Allah for forty days in congregation, catching the first takbir, two freedoms are written for him: freedom from the Fire and freedom from hypocrisy.' (Tirmidhi). May Allah grant you these rewards!*"


# --- Helper Functions ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Return empty dict if file is corrupted or empty
    return {}


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_rank(count):
    if count >= 200:
        return "Pillar of the Masjid"
    elif count >= 140:
        return "Devoted Worshipper"
    elif count >= 35:
        return "Consistent Worshipper"
    else:
        return "New Worshipper"


# --- Bot Events ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    print('Sajda Streak Bot is online and ready!')
    await bot.change_presence(activity=discord.Game(name="Tracking prayers with /pray"))


# --- Helper function for channel check ---
async def check_channel(interaction: discord.Interaction) -> bool:
    """Checks if the command is used in the allowed channel."""
    if ALLOWED_CHANNEL_ID != 0 and interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            f"This command can only be used in the designated prayer tracking channel. Please go there.",
            ephemeral=True
        )
        return False
    return True


# --- Bot Commands ---

@bot.tree.command(name='pray', description='Log one prayer in the mosque. Adds +1 to your streak.')
async def pray(interaction: discord.Interaction):
    if not await check_channel(interaction):
        return

    user_id = str(interaction.user.id)
    data = load_data()

    if user_id not in data:
        data[user_id] = {"count": 0, "best_streak_days": 0}

    data[user_id]["count"] += 1
    count = data[user_id]["count"]
    days = count // 5

    response_message = f"Your prayer has been counted! You are now at **{count}/200** prayers."

    # Check for milestones and add a motivational quote
    milestone_message = ""
    if count == 200:
        milestone_message = f"\n\n**Allahu Akbar! Goal Achieved!**\n{GOAL_QUOTE_AR}"
    elif count > 0 and count % 140 == 0:
        weeks = count // 35
        milestone_message = f"\n\n**Subhan'Allah! You've completed {weeks // 4} month(s)!**\n{random.choice(MILESTONE_QUOTES_AR)}"
    elif count > 0 and count % 35 == 0:
        weeks = count // 35
        milestone_message = f"\n\n**Masha'Allah! You've completed Week {weeks}!**\n{random.choice(MILESTONE_QUOTES_AR)}"
    elif count > 0 and count % 5 == 0:
        milestone_message = f"\n\n**Well done! You've completed Day {days}!**\n{random.choice(MILESTONE_QUOTES_AR)}"

    if milestone_message:
        response_message += milestone_message

    await interaction.response.send_message(response_message, ephemeral=True)
    save_data(data)


@bot.tree.command(name='status', description='Check your current prayer streak status.')
async def status(interaction: discord.Interaction):
    if not await check_channel(interaction):
        return

    user_id = str(interaction.user.id)
    data = load_data()

    if user_id not in data or data.get(user_id, {}).get("count", 0) == 0:
        best_streak = data.get(user_id, {}).get("best_streak_days", 0)
        await interaction.response.send_message(
            f"You haven't started a streak yet. Use `/pray` to begin! Your current best streak is **{best_streak} days**.",
            ephemeral=True
        )
        return

    user_data = data[user_id]
    count = user_data.get("count", 0)
    best_streak_days = user_data.get("best_streak_days", 0)
    days = count // 5
    weeks = days // 7
    rank = get_rank(count)

    embed = discord.Embed(
        title="Your Sajda Streak",
        description=f"Assalamu 'Alaikum, {interaction.user.mention}!",
        color=discord.Color.green()
    )
    if interaction.user.avatar:
        embed.set_thumbnail(url=interaction.user.avatar.url)

    embed.add_field(name="Current Rank", value=f"**{rank}**", inline=False)
    embed.add_field(name="Total Prayers", value=f"**{count} / 200**", inline=True)
    embed.add_field(name="Days Completed", value=f"**{days}**", inline=True)
    embed.add_field(name="Weeks Completed", value=f"**{weeks}**", inline=True)

    best_streak_prayers = best_streak_days * 5
    embed.add_field(
        name="Personal Best Streak",
        value=f"**{best_streak_days} Days** ({best_streak_prayers} prayers)",
        inline=False
    )
    embed.set_footer(text="Keep striving for the sake of Allah! (وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ)")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='reset', description='Reset your streak to 0. Saves your best streak.')
async def reset(interaction: discord.Interaction):
    if not await check_channel(interaction):
        return

    user_id = str(interaction.user.id)
    data = load_data()

    if user_id not in data or data[user_id]["count"] == 0:
        await interaction.response.send_message("You don't have an active streak to reset.", ephemeral=True)
        return

    current_days = data[user_id]["count"] // 5
    best_streak_days = data[user_id].get("best_streak_days", 0)

    description_message = "Your prayer count is now 0. This is an opportunity to start fresh!"

    if current_days > best_streak_days:
        data[user_id]["best_streak_days"] = current_days
        description_message = f"Masha'Allah! You set a new Personal Best of **{current_days} days**!\n\n" + description_message

    data[user_id]["count"] = 0
    save_data(data)

    embed = discord.Embed(
        title="Streak Reset - بداية جديدة",
        description=description_message,
        color=discord.Color.orange()
    )
    embed.add_field(name="A Reminder for You | تذكير لك", value=random.choice(RESET_QUOTES_AR), inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='wipe', description='Deletes ALL your data permanently. Requires confirmation.')
@app_commands.describe(confirmation="This action is irreversible. Please confirm.")
@app_commands.choices(confirmation=[
    app_commands.Choice(name="Yes, I want to permanently delete my data.", value="confirm")
])
async def wipe(interaction: discord.Interaction, confirmation: str):
    if not await check_channel(interaction):
        return

    user_id = str(interaction.user.id)
    data = load_data()

    if user_id not in data:
        await interaction.response.send_message("You have no data to wipe.", ephemeral=True)
        return

    if confirmation == 'confirm':
        del data[user_id]
        save_data(data)
        await interaction.response.send_message(
            "Your data has been permanently wiped. You can start fresh with `/pray`.",
            ephemeral=True
        )

# Run the bot
bot.run(os.environ['DISCORD_TOKEN'])