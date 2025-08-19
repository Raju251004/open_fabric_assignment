from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

# DEMO secret. In production, replace with RS256 + JWKS validation.
ALGORITHM = "HS256"
SECRET = "dev-secret-change-me"

# Token lifetime (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 2

def extract_user(token: str) -> str:
    """
    Decode JWT and return subject (user_id).
    Token must contain 'sub'.
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Token missing 'sub'")
        return sub
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def issue_demo_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)
