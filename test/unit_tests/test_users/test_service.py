from users.service import UserService
import pytest
@pytest.mark.parametrize('user_id, email, exists', [
    (1, 'test@test.com', True),
    (2, 'vlad@example.com', True),
    (3, 'sdfsfd', False),
])
async def test_find_by_id(user_id, email, exists):
    user = await UserService.find_by_id(user_id)
    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user