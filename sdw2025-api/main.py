"""
SDW2025 API - FastAPI + SQLite

Endpoints:
- GET  /                      -> Página inicial com link para /docs
- GET  /users                 -> Lista usuários com paginação + ordenação segura
- GET  /users/{user_id}       -> Busca um usuário pelo ID (com news)
- GET  /news                  -> Lista todas as news
- GET  /users/{user_id}/news  -> Lista news de um usuário
- POST /users/{user_id}/news  -> Cria uma news para um usuário
"""

from typing import Any, Dict, List

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import User, News
from schemas import UserOut, NewsCreate, NewsOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SDW2025 API - FastAPI + SQLite")


def get_db():
    """Cria e fecha a sessão do banco automaticamente por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def root():
    """Página inicial com link clicável para a documentação."""
    return """
    <html>
      <head>
        <title>SDW2025 API</title>
      </head>
      <body style="font-family: Arial; padding: 20px;">
        <h2>✅ API SDW2025 está rodando!</h2>
        <p>Acesse a documentação interativa:</p>
        <a href="/docs" style="font-size: 18px;">👉 Ir para /docs</a>
      </body>
    </html>
    """


# -------------------------
# USERS
# -------------------------

@app.get("/users")
def list_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Quantidade de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade máxima de registros por página"),
    sort: str = Query("id", description="Campo para ordenação (ex: id, nome, saldo, cidade)"),
    order: str = Query("asc", description="Ordem da ordenação: asc ou desc"),
) -> Dict[str, Any]:
    """Lista usuários com paginação e ordenação segura."""
    allowed_sort_fields = {
        "id": User.id,
        "nome": User.nome,
        "saldo": User.saldo,
        "cidade": User.cidade,
        "ultima_compra": User.ultima_compra,
        "agencia": User.agencia,
        "conta": User.conta,
    }

    sort_column = allowed_sort_fields.get(sort)
    if not sort_column:
        raise HTTPException(
            status_code=400,
            detail=f"Campo 'sort' inválido. Use um destes: {list(allowed_sort_fields.keys())}",
        )

    order = order.lower()
    if order not in ("asc", "desc"):
        raise HTTPException(
            status_code=400,
            detail="Campo 'order' inválido. Use 'asc' ou 'desc'.",
        )

    total = db.query(User).count()

    query = db.query(User)

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    items = query.offset(skip).limit(limit).all()
    items_out = [UserOut.model_validate(u).model_dump(mode="json") for u in items]

    return {
        "skip": skip,
        "limit": limit,
        "total": total,
        "sort": sort,
        "order": order,
        "items": items_out,
    }


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Busca um usuário pelo ID."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -------------------------
# NEWS
# -------------------------

@app.get("/news", response_model=List[NewsOut])
def list_news(db: Session = Depends(get_db)):
    """Lista todas as notícias cadastradas."""
    return db.query(News).all()


@app.get("/users/{user_id}/news", response_model=List[NewsOut])
def list_user_news(user_id: int, db: Session = Depends(get_db)):
    """Lista todas as notícias de um usuário."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.news


@app.post("/users/{user_id}/news", response_model=NewsOut)
def add_news(user_id: int, news: NewsCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    desc = news.description.strip()

    if not desc or len(desc) < 5 or desc.lower() == "string":
        raise HTTPException(status_code=400, detail="Descrição inválida")

    new_item = News(description=desc, user=user)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@app.delete("/users/{user_id}/news/{news_id}", status_code=204)
def delete_user_news(user_id: int, news_id: int, db: Session = Depends(get_db)):
    """Deleta uma notícia específica de um usuário."""
    news_item = (
        db.query(News)
        .filter(News.id == news_id, News.user_id == user_id)
        .first()
    )

    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")

    db.delete(news_item)
    db.commit()
    return

 
