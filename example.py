# run_example.py
# Exemplo de como iniciar o AzurBot com comandos pré-definidos

import discord
from dctoez.bot import AzurBot  # Import ajustado para pasta dctoez
import os

# Defina seus intents (caso queira ler mensagens ou outras features)
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler o conteúdo das mensagens

# Crie o bot, usando prefixo e sua chave ("Essemium" ou "Freemium_Key")
bot = AzurBot(
    command_prefix='!',
    subscription_key='Essemium',  # ou 'Freemium_Key'
    intents=intents
)

# Exemplo de comando customizado: !ping
@bot.command(name='ping')
async def ping(ctx):
    """Responde com Pong! para verificar se o bot está online."""
    await ctx.send('Pong!')

# Exemplo de comando para exibir descrição da assinatura: !status
@bot.command(name='status')
async def status(ctx):
    """Mostra se o bot está ativo e a descrição da assinatura atual."""
    ativo = 'ATIVO' if bot.active else 'INATIVO'
    descricao = ''
    # Exibe a descrição armazenada durante o carregamento
    try:
        descricao = bot.description
    except AttributeError:
        descricao = 'Descrição não disponível.'

    await ctx.send(f'Status da assinatura: **{ativo}**\nDescrição: {descricao}')

# Inicie o bot com o token
if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN') or '(update 2.0 i almost forgot to remove my token bot)'
    bot.run(TOKEN)
