# 📄 Documentação do DcToEz

## ✅ Descrição

O **DcToEz** é um bot desenvolvido com `discord.py` que verifica automaticamente a validade da chave de assinatura e a versão atual do bot ao inicializá-lo. Caso a chave esteja inativa ou a versão esteja desatualizada, o bot encerrará automaticamente.

---

## ⚙️ Pré-requisitos

* Python 3.8 ou superior
* Bibliotecas:

  * `discord.py`
  * `aiohttp`

Instalação:

```bash
pip install discord.py aiohttp
```

---

## 🔧 Estrutura do Projeto

```
├── run.py
└── dctoez
    └── bot.py
    └── __init__.py
```

---


## 🚀 Como iniciar o Bot

1. Crie um script, por exemplo `run_bot.py`, com o seguinte conteúdo:

   ```python
   import discord
   from AzurBot import AzurBot

   intents = discord.Intents.default()
   intents.message_content = True  # Caso precise ler o conteúdo das mensagens

   # Substitua "Essemium" pela sua chave de assinatura (Essemium ou Freemium_Key)
   bot = AzurBot(command_prefix="!", subscription_key="Essemium", intents=intents)

   # Inicie o bot com seu token
   bot.run("SEU_TOKEN_AQUI")
   ```

2. No terminal, execute:

   ```bash
   python run_bot.py
   ```

3. O bot irá:

   * Verificar a versão disponível; se desatualizado, fechará com erro.
   * Carregar e validar sua chave de assinatura; se inativa, ficará inativo e não responderá comandos.

---

## ⚙️ Comandos e Eventos

### Eventos

* **on\_ready**: Disparado ao conectar-se ao Discord. Exibe status da assinatura e versão.

### Exemplo de Comando

Você pode adicionar comandos normalmente. Exemplo de `/ping`:

```python
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
```

---
