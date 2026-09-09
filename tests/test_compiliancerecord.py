async def test_create_cmp_hr(client, sama_voydet_hr):
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

    post_cmp = await client.post(f"/people/{id}/compiliance",
                                 json={
                                 "person_id": 1,
                                 "record_type": "visa",
                                 "status": "pending",
                                 "issued_date": "2026-12-12",
                                 "expires_date": "2026-12-12",
                                 "notes": None,
                                 "document_url": None
                                 },
                                 headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                                )

    assert post_cmp.status_code == 200


async def test_create_cmp_user(client, sama_voydet_hr):
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

    post_cmp = await client.post(f"/people/{id}/compiliance",
                                 json={
                                 "person_id": 1,
                                 "record_type": "visa",
                                 "status": "pending",
                                 "issued_date": "2026-12-12",
                                 "expires_date": "2026-12-12",
                                 "notes": None,
                                 "document_url": None
                                 }
                                )

    assert post_cmp.status_code == 401


async def test_get_list_of_cmp(client, sama_voydet_hr):
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
    post_cmp = await client.post(f"/people/{id}/compiliance",
                                     json={
                                     "person_id": 1,
                                     "record_type": "visa",
                                     "status": "pending",
                                     "issued_date": "2026-12-12",
                                     "expires_date": "2026-12-12",
                                     "notes": None,
                                     "document_url": None
                                     },
                                     headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                                    )

    post_cmp = await client.post(f"/people/{id}/compiliance",
                                     json={
                                     "person_id": 1,
                                     "record_type": "visa",
                                     "status": "pending",
                                     "issued_date": "2026-12-12",
                                     "expires_date": "2026-12-12",
                                     "notes": None,
                                     "document_url": None
                                     },
                                     headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                                    )
    response_get = await client.get(f"/people/{id}/compiliance",
                                    headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                                    )

    assert len(response_get.json()) == 2
