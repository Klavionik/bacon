import contextlib
import dataclasses
import locale
from datetime import datetime

from celery import shared_task
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.timezone import now
from loguru import logger

from web.products.models import ProductUpdate, Retailer
from web.users.models import User


@contextlib.contextmanager
def override_locale(locale_name: str, category: int = locale.LC_ALL):
    current_locale = locale.getlocale()
    locale.setlocale(category, locale_name)
    yield
    locale.setlocale(category, current_locale)


@shared_task
def refresh_products():
    logger.info("Run scheduled products refresh.")

    for retailer in Retailer.objects.scrapable():
        logger.info(f"Refresh {retailer.title} products.")
        product_updates = retailer.update_products()
        changed_updates = [
            dataclasses.asdict(update) for update in product_updates if update.product_changed
        ]

        if changed_updates:
            finished_at = now()
            send_product_update_notifications.delay(
                retailer.display_title, finished_at.timestamp(), changed_updates
            )

        logger.info("Refresh finished.")

    logger.info("Refresh complete.")


@shared_task
def send_product_update_notifications(
    retailer: str, finished_at: float, changed_products: list[dict]
):
    finished_at = datetime.fromtimestamp(finished_at)
    product_updates = [ProductUpdate(**product) for product in changed_products]
    users = User.objects.notifiable().with_products_ids()

    with override_locale("ru_RU.utf8"), translation.override("ru_RU"):
        for user in users:
            updates = [
                update for update in product_updates if update.product_id in set(user.products_ids)
            ]

            if not len(updates):
                continue

            logger.info(
                f"Trying to send notification to {user.get_username()}, {len(updates)} products."
            )

            ctx = {"updates": updates, "retailer": retailer, "finished_at": finished_at}
            notification = render_to_string("product_update.html", context=ctx)

            try:
                user.send_products_update_notification(notification)
                logger.info("Notification sent.")
            except Exception as exc:
                logger.error(f"Notification wasn't sent. Reason: {exc}.")
