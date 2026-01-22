"""
Teste simples de criação de News para um usuário no banco.
"""

from database import SessionLocal
from models import News


def test_create_news():
    """Cria uma news manualmente para o user_id=1."""
    db = SessionLocal()
    try:
        news = News(description="Teste de news via script", user_id=1)
        db.add(news)
        db.commit()
        print("News criada com sucesso!")
    finally:
        db.close()


if __name__ == "__main__":
    test_create_news()
