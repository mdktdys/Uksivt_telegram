import httpx
from my_secrets import API_KEY
from models.timings_model import Timings

class DataService:
    def __init__(self) -> None:
        self.base_url: str | None = 'https://api.uksivt.xyz/'
        self.client: httpx.AsyncClient = httpx.AsyncClient()
        self.headers: dict[str, str] = {
            'x-api-key': API_KEY
        }


    async def get_timings(self) -> list[Timings]:
        url: str = f"{self.base_url}/api/v1/timings/"

        response: httpx.Response = await self.client.get(url, headers=self.headers)
        if response.status_code == 200:
            timings = response.json()
            return [Timings(**timing) for timing in timings]
        return None


    async def close(self) -> None:
        await self.client.aclose()