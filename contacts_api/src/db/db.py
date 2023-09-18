from configparser import ConfigParser
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

file_config = Path(__file__).parent.parent.joinpath('conf/config.ini')
config = ConfigParser()
config.read(file_config)

username = config.get('DATA_BASE', 'USERNAME')
password = config.get('DATA_BASE', 'PASSWORD')
domain = config.get('DATA_BASE', 'DOMAIN')
port = config.get('DATA_BASE', 'PORT')
database = config.get('DATA_BASE', 'DATABASE_NAME')

URI = f'postgresql://{username}:{password}@{domain}:{port}/{database}'

engine = create_engine(URI, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    finally:
        db.close()

if __name__ == '__main__':
    pass