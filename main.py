from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(gt=0, le=120)
    email: EmailStr


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
