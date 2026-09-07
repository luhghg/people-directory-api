async def test_try_to_get_persons_without_login(client):
    response = await client.get("/people/")
    assert response.status_code == 401


async def test_try_to_get_persons_with_login(client, sama_voydet):
    response = await client.get("/people/", headers={"Authorization": f"Bearer {sama_voydet}"})
    assert response.status_code == 200


async def test_create_person_hr(client, sama_voydet_hr, sama_voydet_id_usera):
    id = sama_voydet_id_usera
    response = await client.post(f"/people/{id}", json={"id": id, })
 !!!!!!!!!



# async def test_get_person_by_id_with_auth_true(client, sama_voydet):
#     id = 1
#     response_person = client.post(f"/people/{id}")
#     response = await client.get(f"/people/{id}", headers={"Authorization": f"Bearer {sama_voydet}"})
#     res = response.json()
#     assert response.status_code == 200


ДОРАЗОБРАТСЯ С ПЕРСОН АЙТИ ТЕСТАМИ И СДЕЛАТЬ ВСЕ ТЕСТЫ
