import json
import random
import time
from datetime import datetime

tipos_evento = ["clique", "carrinho", "compra", "entrega"]

produtos = [
    "notebook",
    "celular",
    "tablet",
    "fone",
    "smartwatch"
]

status_entrega = [
    "em_separacao",
    "enviado",
    "em_transito",
    "entregue",
    "atrasado"
]

while True:
    tipo = random.choice(tipos_evento)

    evento = {
        "timestamp": datetime.now().isoformat(),
        "usuario_id": random.randint(1, 1000),
        "tipo_evento": tipo,
        "produto": random.choice(produtos),
        "valor": round(random.uniform(20, 5000), 2)
    }

    if tipo == "entrega":
        evento["status_entrega"] = random.choice(status_entrega)

    print(json.dumps(evento, ensure_ascii=False))

    time.sleep(1)