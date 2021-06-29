from sanic_jwt import exceptions

class User:

    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}


users = [User(1, "opi-user", "~Zñujh*B2D`9T!<j")]

username_table = {u.username: u for u in users}
userid_table = {u.user_id: u for u in users}

async def my_authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None or password != user.password:
        raise exceptions.AuthenticationFailed("Incorrect username or password")

    return user