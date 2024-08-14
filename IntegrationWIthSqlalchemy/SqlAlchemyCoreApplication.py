# Outro recurso do sqlalchemy : Metadata|| Core
# Outra forma de criar um schema sql sem fazer pelo o ORM
from sqlalchemy import create_engine, MetaData, Table, column, Integer, String, ForeignKey, Column, text

engine = create_engine("sqlite:///memory")

metadata_obj = MetaData()
user = Table(
    'User',
    metadata_obj,
    Column('User_id',Integer, primary_key=True),
    Column('User_name', String(40), nullable=False),
    Column('email-address', String(60)),
    Column('nickname', String(50), nullable=False)
)

user_prefs = Table(
  'user_prefs', metadata_obj,
    Column('pref_id',Integer,primary_key=True),
    Column('user_id',Integer,ForeignKey("User.User_id"), nullable= False),
    Column('pref_name',String(40), nullable=False),
    Column('pref_value', String(100))
)

print("\nInfo da tabela user_prefs")
print(user_prefs.primary_key)
print(user_prefs.constraints)

print(metadata_obj.tables)
for table in metadata_obj.sorted_tables:
    print(table)

metadata_obj.create_all(engine)
sql_insert = text("insert into user values(1,'Igor','email@email.com','Igor')")
with engine.connect() as conn:
    result_insert = conn.execute(sql_insert)
    print("Insert realizado com sucesso")

print('\nExecutando statement sql')
sql = text('select * from user')
# No sqlalchemy core atual utiliza-se a estrutura a seguir para fazer a conexão e a consulta:
with engine.connect() as conn:
    result = conn.execute(sql)
    for row in result:
        print(row)


metadata_db_obj= MetaData()
financial_info = Table(
    'financial_info',
    metadata_db_obj,
    Column('id',Integer, primary_key=True),
    Column('value', String(100), nullable=False),
)
print("\nInfo da tabela financial_info")
print(financial_info.primary_key)
print(financial_info.constraints)




