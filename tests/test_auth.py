
async def test_email_doesnt_found(client):
    response = await client.post(
        "/auth/login", data={"username": "1231testim@gmail.com", "password": "fn284gdu"}
    )
    res = response.json()
    assert response.status_code == 401
    assert res["detail"] == "Invalid login or password"


async def test_register_email_already_registred(client):
    response_post_user = await client.post(
            "/auth/register", json={"email": "test1234@gmail.com", "password": "test1234"}
        )
    response = await client.post(
        "/auth/register", json={"email": "test1234@gmail.com", "password": "test1234"}
        )
    res = response.json()
    assert response.status_code == 400
    assert res["detail"] == "Email already registred"


