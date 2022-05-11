from flask import request
from flask_migrate import Migrate

from app import config, create_app
from app.autopost.autopost import Autopost, AutopostInstance
from app.autopost.filters import *
from app.handlers import AsyncHandler
from app.bots.TelegramBot import TelegramBot
from app.models import db
from app.models.youtube_model import VideoPosted


app = create_app()
db.init_app(app)
migrate = Migrate(app, db)

tb = TelegramBot(config.TELEGRAM_BOT_TOKEN, server=config.TELEGRAM_SERVER)
handler = AsyncHandler(tb)


@app.route('/bot-2Jv7Ads98U', methods=['POST'])
def update():
    print(request.json)
    handler.update(request.json)
    return {}


if __name__ == '__main__':
    if config.WEBHOOK_BASE_URL is not None:
        tb.request('setWebhook', dict(
            url=f'{config.WEBHOOK_BASE_URL}/bot-2Jv7Ads98U'
        ))

    autopost = Autopost(app_ctx=app.app_context(), tb=tb, instances=[
        # AutopostInstance(channel='UC7Elc-kLydl-NAV4g204pDQ', chat_id=-1000000000000),  # Популярная политика
    ])
    autopost.run()

    app.run('0.0.0.0', 5000)

    autopost.terminate()

    tb.request('deleteWebhook', dict(
        drop_pending_updates=config.WEBHOOK_BASE_URL is None
    ))
