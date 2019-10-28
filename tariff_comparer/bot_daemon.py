import daemon
from telegram_bot import run_bot

with daemon.DaemonContext():
    run_bot()