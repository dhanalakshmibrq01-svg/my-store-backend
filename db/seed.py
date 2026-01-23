
# from sqlalchemy.orm import Session
# from db.models import SystemRole

# def seed_system_roles(db: Session):
#     system_roles = [
#         SystemRole(sr_id=1, sr_name="Admin"),
#         SystemRole(sr_id=2, sr_name="Employee"),
#         SystemRole(sr_id=3, sr_name="Customer")
#     ]

#     for system_role_item in system_roles:
#         existing_role = (
#             db.query(SystemRole)
#             .filter(SystemRole.sr_id == system_role_item.sr_id)
#             .first()
#         )

#         if not existing_role:
#             db.add(system_role_item)

#     db.commit()
