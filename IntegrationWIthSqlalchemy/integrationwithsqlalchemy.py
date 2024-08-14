import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, String, create_engine, inspect, select, func
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship("Address", back_populates="user_account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name}, fullname = {self.fullname})"

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    '''OBS: user_account abaixo é apenas um atributo que recebe relationship, então para facilitar eu coloquei o nome de quem 
    ele está se relacionando.
        OBS: O (User) que está como argumento no relationship é o nome da class e não o nome da tabela.'''
    user_account = relationship("User", back_populates="address")
    def __repr__(self):
         return f"Address(id = {self.id}, E-mail = {self.email})"

print(User.__tablename__)
print(Address.__tablename__)

# conexão com banco de dados
engine = create_engine("sqlite://")

# criando as classes do código python como tabelas no banco de dados
Base.metadata.create_all(engine)

# depreciado - será removido em futuro release
# print(engine.table_names())

# Investiga o esquema do banco de dados
inspetor = inspect(engine)

print(inspetor.has_table("user_account"))
print(inspetor.get_table_names())
print((inspetor.get_columns("address")))
print(inspetor.default_schema_name)

# persistir as informações no banco sqlite
with Session(engine) as session:
    john = User(
        name="John",
        fullname="John Jacobs",
        address=[Address(email="john@email.com")],
    )
    felix = User(
        name="Felix",
        fullname="Felix Jacobs",
        address=[Address(email="felix@email.com"),Address(email="felixjacobs@email.com")],
    )
    samuel = User(
        name="Samuel",
        fullname="Samuel king"
    )

    session.add_all([john, felix, samuel])

    session.commit()

stmt = select(User).where(User.name.in_(['John', 'Felix', 'Samuel']))
print("Recuperando os usuários a partir de condição de filtragem")
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print("Recuperando os endereços a partir de condição de filtragem")
print("Obs: O usuário de id 2 tem mais endereços")
for address in session.scalars(stmt_address):
    print(address)

stmt_address = select(Address).where(Address.user_id.in_([1]))
print("Recuperando os endereços a partir de condição de filtragem")
for address in session.scalars(stmt_address):
    print(address)

#print("Consultando todos os usuários sem filtragem")
#stmt_users = select(User)
#for usuario in session.scalars(stmt_users):
#    print(usuario)

#recuperando info de maneira organizada em maneira decrescente
#Obs: para organizar de maneira crescente basta retira os "desc()" : User.fullname.desc()
stmt_order = select(User).order_by(User.fullname.desc())
for result in session.scalars(stmt_order):
    print(result)

print("==========================")
print("Utilizando o select com o join")

stmt_join = select(User.fullname, Address.email).join_from(Address, User)
#print("Resultado errado, pois está maneira de apresentar o resultado é errada")
#for result_join  in session.scalars(stmt):
#    print(result_join)

#O correto é pegar o atributo stmt_join e utilizar na connection
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nResultado correto")
print("\nExecutando statement a partir da connection")
for resultado in results:
    print(resultado)

print("==================================")
stmt_count = select(func.count('*')).select_from(User)
print('\nTotal de instancias')
for result_count in session.scalars(stmt_count):
    print(result_count)
