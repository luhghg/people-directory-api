# People Directory API

An internal company people directory: stores data about employees and serves it on request, but shows a different set of fields depending on the requester's role — and logs every access to restricted data.

## Idea

A plain CRUD directory is something almost anyone can build. The point of this project is what happens on top of the CRUD: the same endpoint, `GET /people/{id}`, returns a different set of fields depending on who called it. A regular employee (`viewer`) sees only open data — name, job title, department, work email. An HR administrator (`hr_admin`) sees everything, including date of birth, home address, and national ID. Every time an `hr_admin` accesses those restricted fields, it is recorded in an audit log — who looked at whose data, and which specific fields were read or changed.

Separately, data about a person as an employee (`Person`) and a login account (`User`) are deliberately kept as two different entities, connected by an optional one-to-one relationship. `Person` exists for anyone who has ever been an employee, even someone terminated, even someone who never had access to this system. `User` exists only for those who actually need access. `Person` knows nothing about the authorization mechanism: the link between the two lives on `User`, not the other way around.

## Example: one endpoint, two different responses

`GET /people/{id}` with a regular user's token:

```json
{
  "first_name": "Ivan",
  "last_name": "Hulin",
  "work_email": "ivan.hulin@example.com",
  "phone": 987654321,
  "photo_url": "https://example.com/photo.jpg"
}
```

The same request, the same `id`, with an hr_admin token:

```json
{
  "id": 5,
  "first_name": "Ivan",
  "last_name": "Hulin",
  "work_email": "ivan.hulin@example.com",
  "phone": 987654321,
  "photo_url": "https://example.com/photo.jpg",
  "date_of_birth": "1990-02-09",
  "home_adress": "Fabryczna 333",
  "national_id": 12345
}
```

The second request additionally creates a record in `AuditLog`: who looked, whose record it was, and which restricted fields were shown.

## Data model

- **User** — a login account: email, password hash, role (`viewer` / `manager` / `hr_admin`), an optional link to a `Person`.
- **Person** — an employee record: open fields (first name, last name, work email, phone, photo, status) and restricted ones (date of birth, home address, national ID).
- **Employment** — job history: a single `Person` can have several records at once and over time (transfers, promotions). Salary lives here rather than on `Person`, because it changes together with the job title — which automatically produces a history of salary changes. `manager_id` points to a `Person`, not a `User`, because "who your manager is" is a fact about employment, not about whether that manager has a login account.
- **Classification** — formal employment status (full time / part time / contractor / intern) and grade, also kept as history, several records per person.
- **ComplianceRecord** — records of formal requirements (NDA, background check, certifications, visa) — a person can have several records of different types at the same time.
- **AuditLog** — insert-only, no updates or deletes: who accessed whose data, which fields were read or changed, with IP address and timestamp.

The user's role is not stored in the token itself — it is read from the database on every request, so that a role change or an account being deactivated takes effect immediately, without waiting for the token to be reissued.

## Tech stack

- FastAPI
- PostgreSQL
- SQLAlchemy (async) + asyncpg
- Alembic for migrations
- Argon2 for password hashing
- JWT (PyJWT) for authorization
- Docker / Docker Compose
- pytest + pytest-asyncio + httpx (ASGI transport)

## Endpoints

```
POST   /auth/register
POST   /auth/login

GET    /people                        list, search, filters, pagination
POST   /people                        hr_admin only
GET    /people/{id}                   fields returned depend on role
PATCH  /people/{id}                   hr_admin only

GET    /people/{id}/employments
POST   /people/{id}/employments

GET    /people/{id}/classifications
POST   /people/{id}/classifications

GET    /people/{id}/compliance
POST   /people/{id}/compliance

GET    /audit-logs                    hr_admin only
```

Full interactive documentation is available at `/docs` once the app is running (Swagger UI).

## Running the project

1. Copy `.env.example` to `.env` and fill in the values (Postgres connection details, `SECRET_KEY`, token expiry time).
2. Start the stack:

```
docker compose up -d --build
```

The `web` container waits for the database to be ready and applies Alembic migrations on startup. The app will be available at `http://localhost:8080`, documentation at `http://localhost:8080/docs`.

## Tests

```
pytest
```

The test suite uses a separate test database and sends real HTTP requests to the application (via `httpx.AsyncClient` with an ASGI transport, without opening a network port). Covered: authentication, role-based field visibility, access being denied for unauthenticated and non-hr_admin requests, an audit log entry being created (or not) depending on whether restricted fields were shown, and multiple-record history for Employment/Classification/ComplianceRecord.

## Not implemented

Updating and deleting Employment/Classification/ComplianceRecord records, changing roles through the API (roles are assigned directly in the database), token refresh and revocation.

