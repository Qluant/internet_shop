from bot import executor, dp
from multiprocessing import Process
from website import app


def main() -> None:
    flask_app = Process(target=app.run)
    bot_kwargs = {
        'dispatcher': dp,
        'skip_updates': True,
    }
    bot_app = Process(target=executor.start_polling, kwargs=bot_kwargs)
    flask_app.start()
    bot_app.start()

if __name__ == "__main__":
    main()
