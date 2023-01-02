from nanoid import generate
import random
from time import time
import json
from base.models import Credentials

fixtures = []

for i in range(40):
    created_at = int(time() * 1000) - random.randint(0, 10000000)
    Credentials.objects.create(
        id=generate(size=8),
        website=random.choice(["google.com", "fb.com", "twitter.com", "youtube.com"]),
        password=random.choice(["ay0123?!", "sHEEsH99!", "HUH!?1223"]),
        login=random.choice(["keluma", "kevin@gmail.com", "luis@yahoo.com"]),
        created_at=created_at,
        updated_at=created_at + random.randint(0, 10000000),
        autofill=random.choice([True, False]),
    )
