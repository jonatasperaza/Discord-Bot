from aiohttp import web
import asyncio
import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

id_do_servidor = os.getenv('ID_SERVIDOR')

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            try:
                await self.tree.sync(guild=discord.Object(id=id_do_servidor))
                self.synced = True
            except discord.HTTPException as e:
                print(f"Erro ao sincronizar os comandos: {e}")
                await asyncio.sleep(15)  # Atraso para evitar rate limiting
        print(f"Entramos como {self.user}.")

    async def on_error(self, event, *args, **kwargs):
        print(f"Erro detectado: {event}, {args}, {kwargs}")

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

def run_bot():
    try:
        aclient.run(os.getenv('TOKEN_BOT'))
    except Exception as e:
        print(f"Erro ao iniciar o bot: {e}")

app = web.Application()
routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    return web.Response(text="Bot is running!")

app.add_routes(routes)

loop = asyncio.get_event_loop()
loop.run_in_executor(None, run_bot)
web.run_app(app, host='0.0.0.0', port=8080)
