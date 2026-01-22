"""Remove registros da tabela News onde description é exatamente 'string'."""

# pylint: disable=wrong-import-position

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import SessionLocal
from models import News


def delete_string_news():
    """Apaga todas as News com description='string'."""
    db = SessionLocal()

    deleted = db.query(News).filter(News.description == "string").delete()
    db.commit()
    db.close()

    print(f"✅ News removidas com description='string': {deleted}")


if __name__ == "__main__":
    delete_string_news()
