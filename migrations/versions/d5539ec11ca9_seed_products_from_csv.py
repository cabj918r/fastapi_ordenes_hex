"""seed_products_from_csv

Revision ID: d5539ec11ca9
Revises: 2266e754f8ef
Create Date: 2026-06-09 14:20:14.446568

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5539ec11ca9"
down_revision: Union[str, Sequence[str], None] = "2266e754f8ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Definir la estructura COMPLETA de la tabla para Alembic
    from alembic import op
    from sqlalchemy.sql import table

    products_table = table(
        "products",
        sa.column("id", sa.Integer),
        sa.column("cost", sa.Float),
        sa.column("category", sa.String),
        sa.column("name", sa.String),
        sa.column("brand", sa.String),
        sa.column("retail_price", sa.Float),
        sa.column("department", sa.String),
        sa.column("sku", sa.String),
        sa.column("distribution_center_id", sa.Integer),
    )

    # 2. Ruta hacia tu archivo CSV
    import os

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    csv_path = os.path.join(base_dir, "data", "products.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No encontré el archivo de productos en: {csv_path}")

    # 3. Leer e insertar en bloques (Batches)
    import csv

    print(f"\n[Alembic] Leyendo productos reales desde {csv_path}...")

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        batch_size = 2000

        for row in reader:
            # Mapeamos TODAS las columnas del CSV exactamente como me las pasaste
            batch.append(
                {
                    "id": int(row["id"]),
                    "cost": float(row["cost"]) if row["cost"] else 0.0,
                    "category": row["category"],
                    "name": row["name"],
                    "brand": row["brand"],
                    "retail_price": float(row["retail_price"])
                    if row["retail_price"]
                    else 0.0,
                    "department": row["department"],
                    "sku": row["sku"],
                    "distribution_center_id": int(row["distribution_center_id"])
                    if row["distribution_center_id"]
                    else None,
                }
            )

            if len(batch) >= batch_size:
                op.bulk_insert(products_table, batch)
                batch = []

        # Insertar el último bloque si quedó algo
        if batch:
            op.bulk_insert(products_table, batch)

    print("[Alembic] ¡Catálogo completo de theLook importado con éxito a Docker!")


def downgrade() -> None:
    # Si echamos hacia atrás la migración, vacía la tabla de productos
    op.execute("TRUNCATE TABLE products CASCADE;")
