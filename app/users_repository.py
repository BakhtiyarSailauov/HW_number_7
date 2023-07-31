from models import User


class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []

    def save(self, user: User):
        user.id = len(self.users) + 1
        self.users.append(user)

    def get_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_by_id(self, id: int) -> User:
        for user in self.users:
            if user.id == id:
                return user
        return None
