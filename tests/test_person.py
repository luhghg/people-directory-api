async def test_try_to_get_persons_without_login(client):
    response = await client.get("/people/")
    assert response.status_code == 401


async def test_try_to_get_persons_with_login(client):
    response = await client.get("/people/")
    assert response.status_code == 401


доделать фикстуру  авторизацией и сделать все тесті для персн и остальніх роутеров после написать рид ми и н єтом конец 
