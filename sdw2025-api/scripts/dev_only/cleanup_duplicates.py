"""Remove registros duplicados da tabela News (user_id + description)."""

# pylint: disable=wrong-import-position

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import SessionLocal
from models import News


def cleanup_duplicates():
    """Remove duplicatas mantendo apenas a primeira ocorrência."""
    db = SessionLocal()

    all_news = db.query(News).order_by(News.user_id, News.description, News.id).all()

    seen = set()
    removed = 0

    for n in all_news:
        key = (n.user_id, n.description)
        if key in seen:
            db.delete(n)
            removed += 1
        else:
            seen.add(key)

    db.commit()
    db.close()

    print(f"✅ Duplicadas removidas: {removed}")


if __name__ == "__main__":
    cleanup_duplicates()
