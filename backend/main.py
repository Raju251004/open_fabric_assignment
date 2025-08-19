from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from database import init_tables, db
from models import AuthRequest, PermissionIn
from auth import extract_user, issue_demo_token
from permissions import method_to_action, normalize_path, decide

app = FastAPI(title="AuthZ Service", version="1.0.0")

# CORS for local frontend (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # e.g. ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_tables()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/token/{user_id}")
def token(user_id: str):
    """
    Helper endpoint to mint demo tokens (HS256).
    In real deployments, tokens come from Auth0/Cognito/Ory.
    """
    return {"user_id": user_id, "token": issue_demo_token(user_id)}

@app.get("/users/{user_id}/permissions")
def get_user_permissions(user_id: str) -> List[Dict[str, Any]]:
    with db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, user_id, action, resource, effect
            FROM user_permissions
            WHERE user_id = ?
            ORDER BY id ASC
        """, (user_id,))
        rows = cur.fetchall()
    return [
        {"id": r[0], "user_id": r[1], "action": r[2], "resource": r[3], "effect": r[4]}
        for r in rows
    ]

@app.post("/permissions")
def add_permission(p: PermissionIn):
    if p.effect.lower() not in {"allow", "deny"}:
        raise HTTPException(status_code=400, detail="effect must be 'allow' or 'deny'")
    if p.action.lower() not in {"read", "write", "delete", "*"}:
        raise HTTPException(status_code=400, detail="action must be read|write|delete|*")

    with db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_permissions (user_id, action, resource, effect)
            VALUES (?, ?, ?, ?)
        """, (p.user_id, p.action.lower(), p.resource, p.effect.lower()))
        conn.commit()
        new_id = cur.lastrowid

    return {"id": new_id, "message": "permission added"}

@app.post("/authorize")
def authorize(req: AuthRequest):
    """
    Core endpoint from the spec.
    - Validates token (extracts user_id)
    - Maps method -> action
    - Normalizes path to resource
    - Applies precedence rules and returns decision
    """
    user_id = extract_user(req.access_token)
    action = method_to_action(req.method)
    if not action:
        raise HTTPException(status_code=400, detail="Unsupported HTTP method")

    resource = normalize_path(req.path)
    decision, matched = decide(user_id, action, resource)

    return {
        "decision": decision,
        "user_id": user_id,
        "reason": (
            f"User has {action} permission for {resource}"
            if decision == "ALLOW" else "Permission denied"
        ),
        "matched_permissions": matched
    }