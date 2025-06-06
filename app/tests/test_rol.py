import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.session import get_db
from app.core.security import get_password_hash
from app.db.models.user import User
from app.db.models.user import UserRole

@pytest.mark.anyio
async def test_admin_can_create_and_delete_product(client, get_token):
    token = await get_token("admin")
    headers = {"Authorization": f"Bearer {token}"}

    # Crear producto
    response = await client.post("/api/v1/products/", json={
        "name": "Laptop",
        "description": "Dell XPS",
        "category_id": 1  # debes asegurarte de que esta categoría exista
    }, headers=headers)
    assert response.status_code in (200, 201)

    product_id = response.json()["id"]

    # Eliminar producto
    response = await client.delete(f"/api/v1/products/{product_id}", headers=headers)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_operator_can_create_but_not_delete_product(client, get_token):
    token = await get_token("operador")
    headers = {"Authorization": f"Bearer {token}"}

    # Crear producto
    response = await client.post("/api/v1/products/", json={
        "name": "Mouse",
        "description": "Logitech",
        "category_id": 1
    }, headers=headers)
    assert response.status_code in (200, 201)

    product_id = response.json()["id"]

    # Intentar eliminar producto
    response = await client.delete(f"/api/v1/products/{product_id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.anyio
async def test_visualizador_cannot_create_or_delete_product(client, get_token):
    token = await get_token("visualizador")
    headers = {"Authorization": f"Bearer {token}"}

    # Intentar crear producto
    response = await client.post("/api/v1/products/", json={
        "name": "Teclado",
        "description": "Mecánico",
        "category_id": 1
    }, headers=headers)
    assert response.status_code == 403

    # Intentar eliminar producto inexistente
    response = await client.delete("/api/v1/products/999", headers=headers)
    assert response.status_code == 403

@pytest.mark.anyio
async def test_all_can_view_products(client, get_token):
    for role in ["admin", "operador", "visualizador"]:
        token = await get_token(role)
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/v1/products/", headers=headers)
        assert response.status_code == 200
