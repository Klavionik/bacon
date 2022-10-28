from config import settings
from telegram.deps import get_telegram_client


PLUS = '⬆'
MINUS = '⬇'

price_change_message = """
Изменение цены!

🏪 *%(shop)s*
🍪 *%(product)s*
%(emoji)s %(old_price)s ₽ -> %(new_price)s ₽
"""


async def send_price_changed_notification(
    chat_id: int,
    shop: str,
    product: str,
    old_price: float,
    new_price: float,
):
    values = dict(
        shop=shop,
        product=product,
        old_price=old_price,
        new_price=new_price,
        emoji=MINUS if new_price < old_price else PLUS
    )
    telegram = get_telegram_client()
    notification = price_change_message % values
    await telegram.send_message(chat_id, notification, markdown=True)
