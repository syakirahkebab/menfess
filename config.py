import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('.env'), override=False)


def _get_env(name: str, default: str | None = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and (value is None or str(value).strip() == ""):
        raise RuntimeError(f"Environment variable {name} is required.")
    return "" if value is None else str(value)


def _get_int(name: str, default: int | None = None, required: bool = False) -> int:
    raw = _get_env(name, None if default is None else str(default), required=required)
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer, got: {raw}") from exc


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    bot_token: str
    db_url: str
    db_name: str
    channel_1: int
    channel_2: int
    channel_log: int
    id_admin: int
    batas_kirim: int
    biaya_kirim: int
    hastag: str
    start_msg: str
    gagalkirim_msg: str
    topup_msg: str
    reset_timezone: str
    reset_hour: int
    reset_minute: int


settings = Settings(
    api_id=_get_int("API_ID", required=True),
    api_hash=_get_env("API_HASH", required=True),
    bot_token=_get_env("BOT_TOKEN", required=True),
    db_url=_get_env("DB_URL", required=True),
    db_name=_get_env("DB_NAME", "menfess"),
    channel_1=_get_int("CHANNEL_1", required=True),
    channel_2=_get_int("CHANNEL_2", required=True),
    channel_log=_get_int("CHANNEL_LOG", required=True),
    id_admin=_get_int("ID_ADMIN", required=True),
    batas_kirim=_get_int("BATAS_KIRIM", 5),
    biaya_kirim=_get_int("BIAYA_KIRIM", 25),
    hastag=_get_env("HASTAG", "#pfrtddtzt #pfttzz #mas #mba #story #spill #tanya #pap").replace(" ", "|").lower(),
    start_msg=_get_env("START_MSG", """
❏ Hallo {mention}

𝗝𝗮𝘄𝗮𝗳𝗲𝘀𝘀 𝗔𝘂𝘁𝗼 𝗽𝗼𝘀𝘁 akan membantumu mengirimkan pesan secara anonim ke channel @JAWAFES.

silahkan baca help dan rules terlebih dahulu."""),
    gagalkirim_msg=_get_env("GAGAL_KIRIM", """
pesan anda gagal terkirim. silahkan klik button help jika anda butuh bantuan.
"""),
    topup_msg=_get_env("PESAN_TOPUP", """
Jawafess coin di gunakan untuk biaya mengirim menfess/promote ke @JAWAFES jika 5x batas kirim harian sudah habis. biaya untuk sekali mengirim adalah 25 coin.

❏ Cara Membeli Coin Jawafess
├1. klik button top up dibawah ini
├2. kirim bukti pembayaran anda <a href='https://t.me/GJNadminbot?start=start'>disini</a>
├3. nama [ nama telegram anda ]
└4. code topup anda » <code>fess {id} </code>

coin akan berkurang secara otomatis jika batas harian sudah habis. <b>harga 100 coin = 1000 rupiah</b>
"""),
    reset_timezone=_get_env("RESET_TIMEZONE", "Asia/Jakarta"),
    reset_hour=_get_int("RESET_HOUR", 1),
    reset_minute=_get_int("RESET_MINUTE", 0),
)

api_id = settings.api_id
api_hash = settings.api_hash
bot_token = settings.bot_token
db_url = settings.db_url
db_name = settings.db_name
channel_1 = settings.channel_1
channel_2 = settings.channel_2
channel_log = settings.channel_log
id_admin = settings.id_admin
batas_kirim = settings.batas_kirim
biaya_kirim = settings.biaya_kirim
hastag = settings.hastag
start_msg = settings.start_msg
gagalkirim_msg = settings.gagalkirim_msg
topup_msg = settings.topup_msg
