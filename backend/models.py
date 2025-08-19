from pydantic import BaseModel, Field

class AuthRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2/JWT access token")
    method: str = Field(..., description="HTTP method (GET/POST/PUT/PATCH/DELETE)")
    path: str = Field(..., description="API path, e.g., /wallets/wallet-789/transactions")

class PermissionIn(BaseModel):
    user_id: str
    action: str  # read | write | delete | *
    resource: str
    effect: str  # allow | deny
