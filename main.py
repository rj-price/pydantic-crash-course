from pydantic import BaseModel


class APIConfig(BaseModel):
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 1000
    temperature: float = 0.7


# Create a config
config = APIConfig(api_key="sk-abc123")

print(config.model)  # gpt-4
print(config.max_tokens)  # 1000
print(config.api_key)  # sk-abc123
