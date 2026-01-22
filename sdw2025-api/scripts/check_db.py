"""
Script para validar rapidamente os dados no SQLite (sdw2025.db).
Mostra totais e alguns registros de exemplo.
"""

from database import SessionLocal
from models import User, News


def check():
    """Valida se existem usuários e news no banco e imprime um resumo."""
    db = SessionLocal()

    try:
        total_users = db.query(User).count()
        total_news = db.query(News).count()

        print(f"Total de users: {total_users}")
        print(f"Total de news: {total_news}")

        print("\n--- Primeiros 5 users ---")
        users = db.query(User).order_by(User.id).limit(5).all()

        for u in users:
            print(
                (
                    u.id,
                    u.nome,
                    u.agencia,
                    u.conta,
                    u.cartao,
                    u.saldo,
                    u.limite_cartao,
                    u.ultima_compra,
                    u.cidade,
                )
            )

        print("\n--- Primeiras 5 news ---")
        news = db.query(News).order_by(News.id).limit(5).all()

        for n in news:
            print((n.id, n.description, n.user_id))

    finally:
        db.close()


if __name__ == "__main__":
    check()
