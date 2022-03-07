from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine= create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# If you use raw SQL in your main and no ORM you will need this connection:
""" while True:

#     try:
#         conn = psycopg.connect( host='localhost', dbname='fastapi', user='postgres', password='password123',
#                                 )
#         #the information will be received in dict like language (useful for json)
#         cursor=conn.cursor(row_factory=dict_row)
#         print("Database connection established")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error:", error)
#         time.sleep(2)
 """