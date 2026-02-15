from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    age: int


def main():
    try:
        user = User(name="Alice", email="alice@example.com", age=30)
    except Exception as e:
        print(f"Error creating user: {e}")
        return
    print(f"User: {user.name}")
    print(f"Email: {user.email}")
    print(f"Age: {user.age}")


if __name__ == "__main__":
    main()
