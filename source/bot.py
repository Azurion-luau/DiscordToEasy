ONLINE_CONFIG_URL = "https://discordbottoeasy.netlify.app/freemium/key/online/t.json"
VERSION_URL = "https://discordbottoeasy.netlify.app/download/ver.txt"

class AzurBot(commands.Bot):
    def __init__(self, command_prefix: str, subscription_key: str, intents: discord.Intents, **options):
        super().__init__(command_prefix=command_prefix, intents=intents, **options)
        self.subscription_key = subscription_key
        self.active = False
        self.description = ''  # Armazena a descrição da chave
        self.reload_task = None
        self.online_config_url = ONLINE_CONFIG_URL
        self.version_url = VERSION_URL

    async def setup_hook(self):
        print("[INFO] Configurando AzurBot...")

        # Verifica a versão
        await self._check_version()

        # Carrega config inicial
        await self._load_config()

        # Inicia recarga periódica
        self.reload_task = self.loop.create_task(self._periodic_reload())

        print("[INFO] Configuração do AzurBot concluída.")

    async def _check_version(self):
        print("[INFO] Verificando versão do bot...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.version_url) as response:
                    response.raise_for_status()
                    remote_version = (await response.text()).strip()

            print(f"[INFO] Versão disponível: {remote_version} | Versão atual: {BOT_VERSION}")

            if self._version_compare(remote_version, BOT_VERSION) > 0:
                print(f"[ERROR] Sua versão ({BOT_VERSION}) está desatualizada! Atualize para a versão {remote_version}.")
                await self.close()
                sys.exit(1)
        except Exception as e:
            print(f"[WARN] Não foi possível verificar a versão: {e}")

    def _version_compare(self, v1, v2):
        """Compara duas versões em formato string. Retorna: 1 se v1 > v2, -1 se v1 < v2, 0 se igual."""
        v1_parts = list(map(int, v1.strip('V').split('.')))
        v2_parts = list(map(int, v2.strip('V').split('.')))
        return (v1_parts > v2_parts) - (v1_parts < v2_parts)

    async def _load_config(self):
        print(f"[INFO] Carregando configuração de {self.online_config_url}...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.online_config_url) as response:
                    response.raise_for_status()
                    data = await response.json()

            # Suporta JSON com ou sem o wrapper 'keys'
            key_data = data.get(self.subscription_key)
            if key_data is None:
                key_data = data.get('keys', {}).get(self.subscription_key)

            if not key_data:
                print(f"[WARN] Chave '{self.subscription_key}' não encontrada no sistema.")
                self.active = False
                return

            key_status = key_data.get('status', False)
            self.description = key_data.get('descricao', 'Sem descrição.')

            print(f"[INFO] Descrição da chave '{self.subscription_key}': {self.description}")

            if key_status:
                print(f"[INFO] Chave '{self.subscription_key}' ATIVA.")
                self.active = True
            else:
                print(f"[WARN] Chave '{self.subscription_key}' está INATIVA no sistema.")
                self.active = False

        except aiohttp.ClientError as e:
            print(f"[ERROR] Falha ao buscar configuração online: {e}")
            self.active = False
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON malformado: {e}")
            self.active = False
        except Exception as e:
            print(f"[ERROR] Erro inesperado: {e}")
            self.active = False

    async def _periodic_reload(self, interval: int = 300):
        await self.wait_until_ready()
        while not self.is_closed():
            await self._load_config()
            await asyncio.sleep(interval)

    def dispatch(self, event_name: str, *args, **kwargs):
        if not self.active and event_name != 'ready':
            return
        super().dispatch(event_name, *args, **kwargs)

    async def process_commands(self, message):
        if not self.active:
            return
        await super().process_commands(message)

    async def on_ready(self):
        status = 'ATIVO' if self.active else 'INATIVO'
        print(f"Bot online como {self.user} (ID: {self.user.id}). Assinatura: {status}")
