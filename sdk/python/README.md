# Rivinity SDK (Python)

```python
from rivinity_sdk import RivinityClient

client = RivinityClient(base_url="http://localhost:8000/api/v1")
token = client.login("user@example.com", "password")
client.set_token(token)
print(client.get_suggestions())
```
