
from db import models


current_logged_in_ids = set()

def set_active_user(db):
    
    db.query(models.DbUser).update({"is_active": "NO"}, synchronize_session=False)

   
    if current_logged_in_ids:
        db.query(models.DbUser)\
            .filter(models.DbUser.user_id.in_(current_logged_in_ids))\
            .update({"is_active": "YES"}, synchronize_session=False)

    
    db.commit()