from database import SessionLocal
from models import News

def cleanup_duplicates():
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
