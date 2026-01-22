"""
Modelos SQLAlchemy da API SDW2025.

Contém as tabelas:
- users
- news
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """Representa um usuário do sistema bancário."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    agencia = Column(String, nullable=False)
    conta = Column(String, nullable=False)
    cartao = Column(String, nullable=False)
    saldo = Column(Float, default=0.0)
    limite_cartao = Column(Float, default=0.0)
    ultima_compra = Column(String, nullable=True)
    cidade = Column(String, nullable=True)

    news = relationship(
        "News",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class News(Base):
    """Representa uma notícia vinculada a um usuário."""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="news")
