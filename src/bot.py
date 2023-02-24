import logging
import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings  # noqa: E402

from telegram import bot  # noqa: E402


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if settings.TELEGRAM_WEBHOOK_URL:
    logger.info("Webhook started!")
    # TODO: set webhook url
else:
    logger.info("Long polling started!")
    bot.infinity_polling(logger_level=logging.INFO)
