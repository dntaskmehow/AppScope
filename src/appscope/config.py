from typing import Optional
from pydantic import BaseModel, Field

class ScopeConfig(BaseModel):
    github_token: Optional[str] = None
    target_org: str
    scan_path: str = "."
    timeout: float = 10.0
