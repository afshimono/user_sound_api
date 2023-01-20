from sqlalchemy import ForeignKey, Numeric, DateTime,Table, Column, Integer, String, ARRAY, MetaData, create_engine
import urllib.parse

from user_sound import settings

env_vars = settings.env_vars
url_str = f"postgresql://{urllib.parse.quote_plus(env_vars.db_login)}:{urllib.parse.quote_plus(env_vars.db_password)}"\
    + f"@{env_vars.db_url}/{env_vars.db_name}"
engine = create_engine(url_str)
meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, unique=True),
    Column('name', String, nullable=False),
    Column('address', String, nullable=False),
    Column('image', String, nullable=False),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at',DateTime, nullable=True)
)

audio = Table(
    'audio', meta,
    Column('session_id', Integer, primary_key=True),
    Column('step_count', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("users.id"), nullable=False),
    Column('selected_tick', Integer, nullable=False),
    Column('ticks', ARRAY(Numeric), nullable=False),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at',DateTime, nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at',DateTime, nullable=True)
)

meta.create_all(engine)
