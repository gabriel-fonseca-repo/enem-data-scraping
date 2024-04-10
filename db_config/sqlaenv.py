from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

sa_driver = "postgresql+psycopg2"
db_user = "postgres"
db_pass = "123"
db_host = "localhost"
db_port = "5432"
db_name = "postgres"

db_url = f"{sa_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
