import httpx
from my_secrets import API_KEY
from models.user_model import User


class UserService:
    def __init__(self) -> None:
        self.base_url: str | None = 'https://api.uksivt.xyz'
        self.client: httpx.AsyncClient = httpx.AsyncClient()
        self.headers: dict[str, str] = {
            'x-api-key': API_KEY
        }


    async def get_user(self, user_id: int) -> User | None:
        url: str = f"{self.base_url}/api/v2/users/telegram"

        response: httpx.Response = await self.client.get(url, headers=self.headers, params={"user_id": user_id})
        if response.status_code == 200:
            user = response.json()
            return User(**user)
        return None


    async def close(self) -> None:
        await self.client.aclose()