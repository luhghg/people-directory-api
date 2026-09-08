async def test_hr_reading_forbiddn_fields(client, sama_voydet_hr):

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
                headers={"Authorization": f"Bearer {sama_voydet_hr}"})

    response = await client.get(
            f"/people/{id}",
            headers={"Authorization": f"Bearer {sama_voydet_hr}"},
    )

    audit = await client.get("/audit-logs/",
                             headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                            )

    au = audit.json()
    dictionary = au[0]

    assert "date_of_birth" in dictionary["field_name"]
    assert "home_adress" in dictionary["field_name"]
    assert "national_id" in dictionary["field_name"]




async def test_user_reading_forbiddn_fields(client, sama_voydet_hr, sama_voydet):

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
                headers={"Authorization": f"Bearer {sama_voydet_hr}"})

    response = await client.get(
            f"/people/{id}",
            headers={"Authorization": f"Bearer {sama_voydet}"},
    )

    audit = await client.get("/audit-logs/",
                             headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                            )

    au = audit.json()


    assert au == []
