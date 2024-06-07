import discord #type: ignore
from discord import app_commands #type: ignore
import os
from dotenv import load_dotenv #type: ignore

load_dotenv()
 
id_do_servidor = os.getenv('ID-SERVIDOR')

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync(guild=discord.Object(id=id_do_servidor))
            self.synced = True
        print(f"Entramos como {self.user}.")

aclient = MyClient()

@aclient.tree.command(guild=discord.Object(id=id_do_servidor), name='teste', description='Testando')
async def slash_test(interaction: discord.Interaction):
    await interaction.response.send_message("Estou funcionando!", ephemeral=False)

@aclient.tree.command(guild=discord.Object(id=id_do_servidor), name='ban', description='Banir um membro')
async def slash_ban(interaction: discord.Interaction, member: discord.Member, motivo: str = "Não especificado"):
    if interaction.user.guild_permissions.ban_members:
        await interaction.guild.ban(member, reason=motivo)
        await interaction.response.send_message(f"{member.display_name} foi banido por: {motivo}.", ephemeral=True)
    else:
        await interaction.response.send_message("Você não tem permissão para banir membros.", ephemeral=True)

aclient.run(os.getenv('TOKEN-BOT'))
