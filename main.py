import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import idle

import config
from bot import Bot, Database, data


async def reset_menfess() -> None:
    if not data:
        return
    db = Database(data[0])
    updated = await db.reset_menfess()
    await Bot().kirim_pesan(x=str(updated))
    print('BOT BERHASIL DIRESET')


scheduler = AsyncIOScheduler(timezone=config.settings.reset_timezone)
scheduler.add_job(
    reset_menfess,
    trigger='cron',
    hour=config.settings.reset_hour,
    minute=config.settings.reset_minute,
    max_instances=1,
    coalesce=True,
)


async def main() -> None:
    bot = Bot()
    scheduler.start()
    try:
        await bot.start()
        await idle()
    finally:
        scheduler.shutdown(wait=False)
        if bot.is_connected:
            await bot.stop()


if __name__ == '__main__':
    asyncio.run(main())
