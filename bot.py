import os
import asyncio

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
        self._chat_watch_task = None
        self._chat_status = {}
        self._monitored_chats = [
            (config.channel_1, 'channel 1'),
            (config.channel_2, 'channel 2'),
            (config.channel_log, 'channel log'),
        ]

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

        for channel_id, channel_name in self._monitored_chats:
            await self._validate_chat_access(channel_id, channel_name, bot_me.id, announce_ok=True)

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
        self._chat_watch_task = asyncio.create_task(self._watch_chat_access())

        print('BOT TELAH AKTIF')

    async def _validate_chat_access(self, channel_id: int, channel_name: str, bot_id: int, announce_ok: bool = False):
        status_key = f'{channel_id}:{channel_name}'
        previous_status = self._chat_status.get(status_key)
        try:
            await self.get_chat(channel_id)
            bot_member = await self.get_chat_member(channel_id, bot_id)
            if bot_member.status not in ['administrator', 'owner']:
                self._chat_status[status_key] = False
                if previous_status is not False:
                    print(f'⚠️  [PERINGATAN] Bot belum admin pada {channel_name} ({channel_id}).')
                    print('    Fitur yang butuh izin admin bisa gagal, tetapi bot tetap berjalan.')
            else:
                if self._chat_status.get(status_key) is False:
                    print(f'✅ [PULIH] {channel_name} ({channel_id}) kini terbaca lagi, bot sudah admin.')
                self._chat_status[status_key] = True
                if announce_ok:
                    print(f'✅ Akses {channel_name} ({channel_id}) terbaca, bot sudah admin.')
        except Exception as exc:
            self._chat_status[status_key] = False
            if previous_status is not False:
                print(f'⚠️  [PERINGATAN] Gagal membaca {channel_name} ({channel_id}).')
                print('    Pastikan ID benar, bot sudah masuk, dan sudah menjadi admin.')
                print(f'    Detail error: {type(exc).__name__}: {exc}')
                print('    Bot tetap dijalankan tanpa menghentikan proses startup.')

    async def _watch_chat_access(self):
        while True:
            await asyncio.sleep(30)
            if not hasattr(self, 'id_bot'):
                continue
            for channel_id, channel_name in self._monitored_chats:
                await self._validate_chat_access(channel_id, channel_name, self.id_bot)

    async def stop(self):
        if self._chat_watch_task:
            self._chat_watch_task.cancel()
            self._chat_watch_task = None
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
