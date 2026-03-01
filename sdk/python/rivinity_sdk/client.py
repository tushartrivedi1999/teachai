import httpx


class RivinityClient:
    def __init__(self, base_url: str):
        self._client = httpx.Client(base_url=base_url, timeout=20.0)

    def set_token(self, token: str) -> None:
        self._client.headers.update({"Authorization": f"Bearer {token}"})

    def register(self, full_name: str, email: str, password: str) -> str:
        res = self._client.post("/auth/register", json={"full_name": full_name, "email": email, "password": password})
        res.raise_for_status()
        return res.json()["access_token"]

    def login(self, email: str, password: str) -> str:
        res = self._client.post("/auth/login", json={"email": email, "password": password})
        res.raise_for_status()
        return res.json()["access_token"]

    def create_course(self, title: str, field: str, level: str, objectives: list[str]):
        res = self._client.post("/courses", json={"title": title, "field": field, "level": level, "objectives": objectives})
        res.raise_for_status()
        return res.json()

    def get_suggestions(self):
        res = self._client.get("/suggestions")
        res.raise_for_status()
        return res.json()
