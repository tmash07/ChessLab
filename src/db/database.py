from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from dotenv import dotenv_values
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
config = dotenv_values(PROJECT_ROOT / ".env")

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=config['CHESSLAB_DB_USER'],
    password=config['CHESSLAB_DB_PASSWORD'],
    host=config['CHESSLAB_DB_HOST'],
    port=int(config.get('CHESSLAB_DB_PORT') or '3306'),
    database=config['CHESSLAB_DB_NAME']
)

engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True
)

SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)