from typing import List
import os
from sqlalchemy import ForeignKey, Integer, create_engine, DateTime, insert, select, update
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, Session
from typing import Optional
from datetime import date, datetime

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

DB_ENGINE = create_engine(f"sqlite:///{SCRIPT_FOLDER}\data\database.db", echo=True)

# DATABASE ARCHITECTURE
class dec_base(DeclarativeBase): pass

class prices(dec_base):
    __tablename__ = "prices"
    Product: Mapped[List["products"]] = relationship(back_populates="Product")

    Id: Mapped[int] = mapped_column(primary_key=True)
    ProductId: Mapped[int] = mapped_column(ForeignKey("products.Id"))
    Date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    Currency: Mapped[str] = mapped_column()
    Price: Mapped[float] = mapped_column()
    Name: Mapped[str] = mapped_column()
    Store: Mapped[str] = mapped_column()
    Url: Mapped[str] = mapped_column()

class products(dec_base):
    __tablename__ = "products"
    Product: Mapped["prices"] = relationship(back_populates="Product")

    Id: Mapped[int] = mapped_column(primary_key=True)
    ProductName: Mapped[str] = mapped_column()
    ProductModel: Mapped[str] = mapped_column()
    ProductBrand: Mapped[str] = mapped_column()
    ProductFilters: Mapped[str] = mapped_column()
    Created: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    LastUpdate: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    """class benchmarks(dec_base):
    __tablename__ = "benchmarks" """
    
dec_base.metadata.create_all(DB_ENGINE)

stmt = products(
    ProductName="GeForce RTX 3050",
    ProductModel="EX",
    ProductBrand="Galax",
    ProductFilters="")
with Session(DB_ENGINE) as ses:
    ses.add(stmt)
    ses.commit()

"""stmt = prices(
    ProductId=1,
    Date=datetime.now(),
    Currency="R$",
    Price=1720.59,
    Name="Placa De Vídeo Galax Geforce RTX 3050 Ex 8GB GDDR6",
    Store="KaBuM!",
    Url="https://www.kabum.com.br/produto/320250/placa-de-video-galax-nvidia-geforce-rtx-3050-ex-oc-8gb-gddr6-lhr-1-click-128-bits-35nsl8md6yex?srsltid=Ad5pg_E93vNYIyyNwSwnn5Vm7KG2F1dCN33aqOb-c2uw65qxlW761FCmP6U")"""

"""with Session(DB_ENGINE) as ses:
    ses.add(stmt)
    ses.commit()"""

"""with Session(DB_ENGINE) as ses:
    stmt = select(prices)
    result = ses.execute(stmt).scalars()

    for i in result:
            print(f"{i.Price} //// {i.Store}")"""

CURR_PROD_ID = 1
time_stmt = update(products).where(products.Id == CURR_PROD_ID).values(Created = datetime.now())
with Session(DB_ENGINE) as ses:
    ses.execute(time_stmt)
    ses.commit()
