from storage import create_db_engine, create_db_session
from config import settings
from .signals import products_update

import watcher.notifications

engine = create_db_engine(settings.db_uri)
Session = create_db_session(engine)
