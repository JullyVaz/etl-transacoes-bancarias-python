"""
Seed do banco SDW2025.

Este script:
- cria as tabelas no SQLite
- insere usuários a partir do CSV
- cria 1 news aleatória para cada usuário (se ainda não tiver)
"""

import random

import pandas as pd

from database import Base, SessionLocal, engine
from models import News, User

NEWS_TEMPLATES = [
    "Nova funcionalidade disponível no app!",
    "Seu limite de cartão foi atualizado.",
    "Dica: ative notificações para acompanhar suas compras.",
    "Promoção especial: cashback em compras selecionadas!",
    "Aviso: mantenha seus dados sempre atualizados.",
    "Você recebeu uma oferta personalizada no app.",
    "Segurança: revise seus acessos recentes.",
    "Seu extrato mensal já está disponível.",
    "Atualização: melhorias de desempenho no sistema.",
    "Atenção: evite compartilhar seu código de verificação.",
]


def seed():
    """Executa o seed do banco: cria tabelas, insere users e cria news."""
    Base.metadata.create_all(bind=engine)

    # Você pode trocar aqui para SDW2025_1.csv se quiser voltar ao original
    df = pd.read_csv("SDW2025_clean.csv")

    db = SessionLocal()

    try:
        # 1) Inserir usuários (somente se estiver vazio)
        if db.query(User).count() == 0:
            for _, row in df.iterrows():
                user = User(
                    id=int(row["UserID"]),
                    nome=str(row["Nome"]),
                    agencia=str(row["Agencia"]),
                    conta=str(row["Conta"]),
                    cartao=str(row["Cartao"]),
                    saldo=float(row["Saldo"]),
                    limite_cartao=float(row["LimiteCartao"]),
                    ultima_compra=str(row["UltimaCompra"]),
                    cidade=str(row["Cidade"]),
                )
                db.add(user)

            db.commit()
            print("Usuários inseridos com sucesso!")
        else:
            print("Banco já possui usuários. Pulando seed de users...")

        # 2) Criar 1 news para cada user (se ainda não tiver)
        users = db.query(User).all()
        created_news = 0

        for user in users:
            already_has_news = db.query(News).filter(News.user_id == user.id).first()
            if already_has_news:
                continue

            news = News(
                description=random.choice(NEWS_TEMPLATES),
                user_id=user.id,
            )
            db.add(news)
            created_news += 1

        db.commit()
        print(f"Seed concluído com sucesso! News criadas agora: {created_news}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
