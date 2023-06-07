#!/usr/bin/env python3
"""
Main file
"""

from db import DB
from user import User
from auth import Auth

AUTH = Auth()
my_db = DB()

email = "test@test.com"
password = "SuperHashedPwd"
user_1 = AUTH.register_user(email, password)
sessionID = AUTH.create_session(email)
token = AUTH.get_reset_password_token(email)
print(user_1)

print(AUTH.update_password(token, "Jump2DaMoon"))
# print(user_1)
# user_1_0 = AUTH.get_user_from_session_id(sessionID)

use = my_db.find_user_by(email=email)
print("+++++", use)

# user = my_db.add_user("test@test.com", "PwdHashed")
# print("+++++++++", user.id)

# find_user = my_db.find_user_by(id=2)
# print("+++++USER_ID+++++++",find_user)

# print(AUTH.valid_login(email, password))
# print(user_1)
# print(sessionID)
# print(user_1_0)