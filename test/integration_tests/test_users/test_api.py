from httpx import AsyncClient
import pytest
@pytest.mark.parametrize("email, password, status_code", [
    ('kot@pes.com', 'kotosdfpes', 200),
    ('kot@pes.com', 'kodfpes', 409),
    ('pes@pes.com', 'kodfpes', 200),
    ('sdlfjsdlk', 'kodfpes', 422),
]) 
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        'email': email,
        'password': password,
    })
    assert response.status_code == status_code
    
@pytest.mark.parametrize('email, password, status_code', [
    ('vlad@example.com', 'artem', 200),
    ('wrong@example.com', 'artem', 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/login', json={
        'email': email,
        'password': password,
    })
    assert response.status_code == status_code