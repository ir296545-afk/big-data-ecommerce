import json
import random
import time
from datetime import datetime

tipos_evento = ["clique", "carrinho", "compra", "entrega"]
produtos = ["notebook", "celular", "tablet", "fone", "smartwatch"]

while True:
    evento = {
        "timestamp": datetime.now().isoformat(),
        "usuario_id": random.randint(1, 1000),
        "tipo_evento": random.choice(tipos_evento),
        "produto": random.choice(produtos),
        "valor": round(random.uniform(20, 5000), 2)
    }

    print(json.dumps(evento, ensure_ascii=False))

    time.sleep(1)
