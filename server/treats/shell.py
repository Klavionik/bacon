from storage import create_db_engine, create_db_session, models
from config import settings
from datetime import datetime as dt

engine = create_db_engine(settings.db_uri, echo=True)
Session = create_db_session(engine)

roma_data = dict(username='jediroman', language='ru', meta={'shop_1_location': 316})
perekrestok_data = dict(name='Перекресток', url_rule=r'^https://(w{3}\.)?perekrestok\.ru/cat/.+$')
perekrestok_surgut_data = dict(location_id=316, name='Сургут Агора', address='г. Сургут, ул. Профсоюзов, д. 11')
curd_snack = dict(
    title='Сырок Б.Ю. Александров',
    url='https://www.perekrestok.ru/cat/373/p/syrok-tvoroznyj-rostagroeksport-s-aromatom-vanili-glazirovannyj-20-45g-3666242'
)
curd_snack_price = dict(price=420.0, created_at=dt(2022, 9, 8, 16))
curd_snack_price_newer = dict(price=600, created_at=dt(2022, 9, 20, 15))


async def create_test_rows():
    async with Session() as session, session.begin():
        roma = models.User(**roma_data)
        perekrestok = models.Shop(**perekrestok_data)
        perekrestok_surgut = models.ShopLocation(**perekrestok_surgut_data, shop=perekrestok)
        session.add_all([roma, perekrestok, perekrestok_surgut])
        await session.commit()

    return roma
