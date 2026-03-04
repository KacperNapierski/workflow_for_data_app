from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends


db_engine = create_engine(
    "postgresql+psycopg://postgres:postgres@localhost/db"
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)


async def get_session():
    with Session(db_engine) as session:
        #limits to one session per request
        yield session


SessionDep = Annotated[Session, Depends(get_session)]