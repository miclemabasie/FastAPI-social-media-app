from main import *


@app.get("users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User)
    users = users.fetchall()
    return users