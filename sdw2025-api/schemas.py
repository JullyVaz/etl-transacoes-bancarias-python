"""
Schemas Pydantic da API SDW2025.

Define os modelos de entrada/saída (request/response) usados no FastAPI.
"""

from typing import List, Optional

from pydantic import BaseModel


class NewsCreate(BaseModel):
    """Schema para criar uma notícia (entrada)."""

    description: str


class NewsOut(BaseModel):
    """Schema de saída para News."""

    id: int
    description: str

    class Config:
        """Configuração do Pydantic para permitir leitura via ORM."""
        from_attributes = True


class UserOut(BaseModel):
    """Schema de saída para User (inclui lista de News)."""

    id: int
    nome: str
    agencia: str
    conta: str
    cartao: str
    saldo: float
    limite_cartao: float
    ultima_compra: Optional[str] = None
    cidade: Optional[str] = None
    news: List[NewsOut] = []

    class Config:
        """Configuração do Pydantic para permitir leitura via ORM."""
        from_attributes = True
