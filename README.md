AuthZ Service -- FastAPI Authorization with JWT + SQLite

This project is a lightweight **Authorization (AuthZ) microservice**
built with **FastAPI**.\
It uses **JWT tokens** for authentication and a **SQLite database** to
manage permissions.\
The service answers the core question:

> ❓ **Can this user perform this action on this resource?**


Features

-   ✅ JWT-based authentication (with expiry support)
-   ✅ Permissions stored in SQLite
-   ✅ Role/Policy-Based Access Control with wildcards (`*`)
-   ✅ REST API for permission management
-   ✅ Authorization decision engine (ALLOW / DENY)
-   ✅ Easy to extend for real-world deployments (Auth0, Cognito, Ory,
    etc.)


📂 Project Structure

    .
    ├── auth.py          # JWT issue & validation (with expiry)
    ├── database.py      # SQLite connection & table initialization
    ├── init_db.py       # Seeds the database with sample data
    ├── main.py          # FastAPI app with endpoints
    ├── models.py        # Pydantic request/response models
    ├── permissions.py   # Core authorization logic
    ├── permissions.db   # SQLite database (auto-created)
    ├── requirements.txt # Project dependencies


⚙️ Installation & Setup

1. Clone repository

``` bash
git clone <your-repo-url>
cd <project-folder>


2. Create virtual environment (optional but recommended)

``` bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
3. Install dependencies

``` bash
pip install -r requirements.txt
```

4. Initialize database

``` bash
python init_db.py
```

This creates `permissions.db` and seeds it with sample data.

5. Run the server

``` bash
uvicorn main:app --reload
```


🔑 Authentication

-   Tokens are **JWT (HS256)**, issued via `/token/{user_id}`.
-   Tokens **expire in 2 minutes** (configurable in `auth.py`).

Example:

``` bash
GET /token/user123
→ {"user_id": "user123", "token": "<jwt>"}
```

📡 API Endpoints

1. Health Check

``` http
GET /health
→ {"status": "ok"}
```

2. Generate Token

``` http
GET /token/{user_id}
```

3. Get User Permissions

``` http
/users/{user_id}/permissions
```

4. Add Permission

``` http
POST /permissions
{
  "user_id": "user123",
  "action": "read",
  "resource": "transactions",
  "effect": "allow"
}
```

5. Authorize Request

``` http
POST /authorize
{
  "access_token": "<jwt>",
  "method": "GET",
  "path": "/transactions"
}
```

Response:

``` json
{
  "decision": "ALLOW",
  "user_id": "user123",
  "reason": "User has read permission for transactions",
  "matched_permissions": [
    {"action": "read", "resource": "transactions", "effect": "allow"}
  ]
}
```


🗂️ Permission Model

Permissions are stored in SQLite table `user_permissions`:

  id   user_id    action   resource       effect
  ---- ---------- -------- -------------- --------
  1    user123    read     transactions   allow
  2    user123    write    transactions   allow
  3    user123    delete   transactions   deny
  9    admin789   \*       \*             allow

-   **action**: `read`, `write`, `delete`, `*`
-   **resource**: supports wildcards (e.g., `wallets/*`)
-   **effect**: `allow` or `deny`


⚖️ Decision Logic

1.  Default = **DENY**
2.  Find all matching rules for the user/action/resource
3.  Choose the **most specific match**
4.  If any DENY in that group → **DENY**
5.  Otherwise → **ALLOW**


🛠️ Future Improvements

-   🔑 Use RS256 JWTs with JWKS (Auth0, Cognito, etc.)
-   🔄 Add refresh tokens
-   📊 Admin dashboard for managing permissions
-   🏢 Role-based grouping


👨‍💻 Author

Built with ❤️ using **FastAPI** + **SQLite** + **JWT**.
