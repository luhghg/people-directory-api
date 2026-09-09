
async def test_create_emp_hr(client, sama_voydet_hr):

    id = 1
    manager_id = 2
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

    post_manager = await client.post(
                f"/people/",
                json={
                    "first_name": "Bobr",
                    "last_name": "Kurva",
                    "work_email": "bobrkurva123@gmai.com",
                    "phone": 98746573,
                    "photo_url": "https://djeiuceiu",
                    "date_of_birth": "2000-12-12",
                    "home_adress": "Oleha Vsevoloda 44",
                    "national_id": 1,
                },
                headers={"Authorization": f"Bearer {sama_voydet_hr}"},
            )

    response = await client.post(f"/people/{id}/employments",
                                 json={
                                       "person_id": 1,
                                       "job_title": "DevOps",
                                       "department": "engineering",
                                       "manager_id": manager_id,
                                       "start_date": "2025-12-12",
                                       "end_date": "2026-12-12",
                                       "is_current": True,
                                       "salary": 1000.50,
                                       "currency": "UAH"
                                      },
                                      headers={"Authorization": f"Bearer {sama_voydet_hr}"})

    assert response.status_code == 200


async def test_create_emp_user(client, sama_voydet_hr):

    id = 1
    manager_id = 2
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

    post_manager = await client.post(
                f"/people/",
                json={
                    "first_name": "Bobr",
                    "last_name": "Kurva",
                    "work_email": "bobrkurva123@gmai.com",
                    "phone": 98746573,
                    "photo_url": "https://djeiuceiu",
                    "date_of_birth": "2000-12-12",
                    "home_adress": "Oleha Vsevoloda 44",
                    "national_id": 1,
                },
                headers={"Authorization": f"Bearer {sama_voydet_hr}"},
            )

    response = await client.post(f"/people/{id}/employments",
                                 json={
                                       "person_id": 1,
                                       "job_title": "DevOps",
                                       "department": "engineering",
                                       "manager_id": manager_id,
                                       "start_date": "2025-12-12",
                                       "end_date": "2026-12-12",
                                       "is_current": True,
                                       "salary": 1000.50,
                                       "currency": "UAH"
                                      }
                                      )
    assert response.status_code == 401


async def test_many_zapisey(client, sama_voydet_hr):

    id = 1
    manager_id = 2
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

    post_manager = await client.post(
                f"/people/",
                json={
                    "first_name": "Bobr",
                    "last_name": "Kurva",
                    "work_email": "bobrkurva123@gmai.com",
                    "phone": 98746573,
                    "photo_url": "https://djeiuceiu",
                    "date_of_birth": "2000-12-12",
                    "home_adress": "Oleha Vsevoloda 44",
                    "national_id": 1,
                },
                headers={"Authorization": f"Bearer {sama_voydet_hr}"},
            )

    response = await client.post(f"/people/{id}/employments",
                                 json={
                                       "person_id": 1,
                                       "job_title": "DevOps",
                                       "department": "engineering",
                                       "manager_id": manager_id,
                                       "start_date": "2025-12-12",
                                       "end_date": "2026-12-12",
                                       "is_current": True,
                                       "salary": 1000.50,
                                       "currency": "UAH"
                                      },
                                      headers={"Authorization": f"Bearer {sama_voydet_hr}"})

    response_dwa = await client.post(f"/people/{id}/employments",
                                     json={
                                           "person_id": 1,
                                           "job_title": "Clown",
                                           "department": "hr",
                                           "manager_id": manager_id,
                                           "start_date": "2025-12-12",
                                           "end_date": "2026-12-12",
                                           "is_current": True,
                                           "salary": 100.50,
                                           "currency": "UAH"
                                          },
                                          headers={"Authorization": f"Bearer {sama_voydet_hr}"})

    response_get = await client.get(f"/people/{id}/employments",
                                    headers={"Authorization": f"Bearer {sama_voydet_hr}"}
                                   )

    assert len(response_get.json()) == 2
