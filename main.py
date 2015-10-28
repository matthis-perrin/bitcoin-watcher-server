from app.db.user import User

user_id = User.create()
user = User.get(user_id)
print user.user_id, user.creation_time, user.last_seen
