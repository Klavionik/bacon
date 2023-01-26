from storage import create_db_engine, create_db_session
from storage.models import *  # noqa
from config import settings
from ptpython import embed

engine = create_db_engine(settings.db_uri, echo=True)
Session = create_db_session(engine)


def configure(repl):
    repl.show_signature = True
    repl.use_code_colorscheme('monokai')
    repl.color_depth = 'DEPTH_24_BIT'
    repl.insert_blank_line_after_output = False
    repl.complete_while_typing = False
    repl.confirm_exit = False


embed(globals(), locals(), configure)
