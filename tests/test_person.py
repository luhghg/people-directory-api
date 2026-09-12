async def test_try_to_get_persons_without_login(client):
    response = await client.get("/people/")
    assert response.status_code == 401


async def test_try_to_get_persons_with_login(client, sama_voydet):
    response = await client.get(
        "/people/", headers={"Authorization": f"Bearer {sama_voydet}"}
    )
    assert response.status_code == 200


async def test_create_person_hr(client, sama_voydet_hr):
    response = await client.post(
        f"/people/",
        json={
            "first_name": "Ivan",
            "last_name": "Hulin",
            "work_email": "ivanahulina123@gmai.com",
            "phone": 987654321,
            "photo_url": "https://riuhekjwendjkwn",
            "date_of_birth": "2026-12-28",
            "home_adress": "Fabryczma 333",
            "national_id": 1,
        },
        headers={"Authorization": f"Bearer {sama_voydet_hr}"},
    )
    assert response.status_code == 200


async def test_get_person_by_id_with_auth_admin(client, sama_voydet_hr):
    id = 1
    post_person = await client.post(
        f"/people/",
        json={
            "first_name": "Ivan",
            "last_name": "Hulin",
            "work_email": "ivanahulina123@gmai.com",
            "phone": 987654321,
            "photo_url": "https://riuhekjwendjkwn",
            "date_of_birth": "2026-12-28",
            "home_adress": "Fabryczma 333",
            "national_id": 1,
        },
        headers={"Authorization": f"Bearer {sama_voydet_hr}"},
    )
    response = await client.get(
        f"/people/{id}", headers={"Authorization": f"Bearer {sama_voydet_hr}"}
    )
    res = response.json()
    assert "date_of_birth" in res
    assert "home_adress" in res
    assert "national_id" in res


async def test_get_person_by_id_with_auth_casual_user(
    client, sama_voydet, sama_voydet_hr
):
    id = 1
    post_person = await client.post(
        f"/people/",
        json={
            "first_name": "Ivan",
            "last_name": "Hulin",
            "work_email": "ivanahulina123@gmai.com",
            "phone": 987654321,
            "photo_url": "https://riuhekjwendjkwn",
            "date_of_birth": "2026-12-28",
            "home_adress": "Fabryczma 333",
            "national_id": 1,
        },
        headers={"Authorization": f"Bearer {sama_voydet_hr}"},
    )
    response = await client.get(
        f"/people/{id}", headers={"Authorization": f"Bearer {sama_voydet}"}
    )
    res = response.json()
    assert "date_of_birth" not in res
    assert "home_adress" not in res
    assert "national_id" not in res


async def test_user_try_to_patch(client, sama_voydet, sama_voydet_hr):
    id = 1
    post_person = await client.post(
        f"/people/",
        json={
            "first_name": "Ivan",
            "last_name": "Hulin",
            "work_email": "ivanahulina123@gmai.com",
            "phone": 987654321,
            "photo_url": "https://riuhekjwendjkwn",
            "date_of_birth": "2026-12-28",
            "home_adress": "Fabryczma 333",
            "national_id": 1,
        },
        headers={"Authorization": f"Bearer {sama_voydet_hr}"},
    )
    response = await client.patch(
        f"/people/{id}",
        json={
            "first_name": "Ivan",
            "last_name": "Hulin",
            "work_email": "ivanahulina123@gmai.com",
            "phone": 987654321,
            "photo_url": "https://riuhekjwendjkwn",
            "date_of_birth": "2026-12-28",
            "home_adress": "Fabryczma 333",
            "national_id": 1,
        },
        headers={"Authorization": f"Bearer {sama_voydet}"},
    )
    res = response.json()
    assert response.status_code == 403


async def test_admin_try_to_patch(client, sama_voydet_hr):
    id = 1
    post_person = await client.post(
        f"/people/",
        json={
            "first_name": "Ivan",
            "last_name": "Hulin",
            "work_email": "ivanahulina123@gmai.com",
            "phone": 987654321,
            "photo_url": "https://riuhekjwendjkwn",
            "date_of_birth": "2026-12-28",
            "home_adress": "Fabryczma 333",
            "national_id": 1,
        },
        headers={"Authorization": f"Bearer {sama_voydet_hr}"},
    )
    response = await client.patch(
        f"/people/{id}",
        json={
            "first_name": "Iban",
            "last_name": "Hulin",
            "work_email": "ivanahulina123@gmai.com",
            "phone": 987654321,
            "photo_url": "https://riuhekjwendjkwn",
            "date_of_birth": "2026-12-28",
            "home_adress": "Fabryczma 333",
            "national_id": 1,
        },
        headers={"Authorization": f"Bearer {sama_voydet_hr}"},
    )
    res = response.json()
    assert response.status_code == 401
