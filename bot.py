import os
import sys

import requests
from pyrogram import Client
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats

import config
from plugins import Database

data = []


class Bot(Client):
    def __init__(self):
        super().__init__(
            'alterbase_bot',
            api_id=config.api_id,
            api_hash=config.api_hash,
            plugins={"root": "plugins"},
            bot_token=config.bot_token,
            in_memory=True,
        )

    async def start(self):
        await super().start()
        bot_me = await self.get_me()

        db = Database(bot_me.id)
        os.system('clear')
        if not await db.cek_user_didatabase():
            print('[!] Menambahkan data bot ke database...')
            await db.tambah_databot()
        print('[!] Database telah ready')
        print(f'[!] Database: {config.db_name}')
        print('================')

        for channel_id, channel_name in [
            (config.channel_1, 'channel 1'),
            (config.channel_2, 'channel 2'),
            (config.channel_log, 'channel log'),
        ]:
            try:
                await self.get_chat(channel_id)
                await self.get_chat_member(channel_id, bot_me.id)
            except Exception as exc:
                print(f'Harap periksa kembali ID [ {channel_id} ] pada {channel_name}')
                print('Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print(f'Detail error: {type(exc).__name__}: {exc}')
                print('-> Bot terpaksa dihentikan')
                sys.exit(1)

        self.username = bot_me.username
        self.id_bot = bot_me.id
        data.clear()
        data.append(self.id_bot)
        await self.set_bot_commands(
            [
                BotCommand('status', '📊 check status'),
                BotCommand('topup', '💰 top up coin'),
            ],
            BotCommandScopeAllPrivateChats(),
        )

        print('BOT TELAH AKTIF')

    async def stop(self):
        await super().stop()
        print('BOT BERHASIL DIHENTIKAN')

    async def kirim_pesan(self, x: str):
        pelanggan = Database(config.id_admin).get_pelanggan()
        pesan = f'<b>TOTAL USER ( {pelanggan.total_pelanggan} ) PENGGUNA 📊</b>\n'
        pesan += f'➜ <i>Total user yang mengirim menfess hari ini adalah {x}/{pelanggan.total_pelanggan} user</i>\n'
        pesan += '➜ <i>Berhasil direset menjadi 0 menfess</i>'
        url = f'https://api.telegram.org/bot{config.bot_token}'
        response = requests.get(
            f'{url}/sendMessage',
            params={'chat_id': config.channel_log, 'text': pesan, 'parse_mode': 'HTML'},
            timeout=20,
        )
        a = response.json()
        requests.post(
            f'{url}/pinChatMessage',
            params={'chat_id': config.channel_log, 'message_id': a['result']['message_id'], 'parse_mode': 'HTML'},
            timeout=20,
        )
        requests.post(
            f'{url}/deleteMessage',
            params={'chat_id': config.channel_log, 'message_id': a['result']['message_id'] + 1, 'parse_mode': 'HTML'},
            timeout=20,
        )
