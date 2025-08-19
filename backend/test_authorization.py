import json
from main import app
from fastapi.testclient import TestClient
from init_db import seed
from auth import issue_demo_token

client = TestClient(app)

def setup_module(_):
    seed()

def authz(token, method, path):
    return client.post("/authorize", json={
        "access_token": token,
        "method": method,
        "path": path
    })

def test_allow_user123_read_transactions():
    t = issue_demo_token("user123")
    r = authz(t, "GET", "/transactions")
    assert r.status_code == 200
    assert r.json()["decision"] == "ALLOW"

def test_deny_user123_delete_transactions_nested():
    t = issue_demo_token("user123")
    r = authz(t, "DELETE", "/transactions/txn-456")
    assert r.json()["decision"] == "DENY"

def test_allow_user456_wallet789_txns_read():
    t = issue_demo_token("user456")
    r = authz(t, "GET", "/wallets/wallet-789/transactions")
    assert r.json()["decision"] == "ALLOW"

def test_allow_user789_write_any_wallet_txn():
    t = issue_demo_token("user789")
    r = authz(t, "POST", "/wallets/wallet-456/transactions/txn-999")
    assert r.json()["decision"] == "ALLOW"

def test_deny_user456_write_wallet789_txns():
    t = issue_demo_token("user456")
    r = authz(t, "POST", "/wallets/wallet-789/transactions")
    assert r.json()["decision"] == "DENY"

def test_allow_admin789_global_delete():
    t = issue_demo_token("admin789")
    r = authz(t, "DELETE", "/accounts/acc-123/settings")
    assert r.json()["decision"] == "ALLOW"
