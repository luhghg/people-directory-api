
async def test_create_cls_hr(client, sama_voydet_hr):
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
                headers={"Authorization": f"Bearer {sama_voydet_hr}"}
            )
    post_cls = await client.post(f"people/{id}/classifications",
                                 json={
                                     "person_id": 1,
                                     "employment_type": "full_time",
                                     "grade": "junior",
                                     "is_exempt": True,
                                     "effective_to": "2026-12-12"
                                 },
                                 headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                                 )
    assert post_cls.status_code == 200


async def test_create_cls_user(client, sama_voydet_hr):
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
                headers={"Authorization": f"Bearer {sama_voydet_hr}"}
            )
    post_cls = await client.post(f"people/{id}/classifications",
                                 json={
                                     "person_id": 1,
                                     "employment_type": "full_time",
                                     "grade": "junior",
                                     "is_exempt": True,
                                     "effective_to": "2026-12-12"
                                 }
                                 )
    assert post_cls.status_code == 401
