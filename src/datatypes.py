
from itertools import product
from typing import List, Literal, Optional, TypedDict
from unittest.mock import Base
from pydantic import BaseModel


class UserIntent(BaseModel):
    user_intent: Literal["PRODUCT", "ORDER", "HUMANHELP", "OTHER"]
    product_name: Optional[str]
    order_number: Optional[str]    


class CustomerSupportState(TypedDict):
    user_intent: UserIntent
    user_query: str
    followups: List[str]
    case_id: str
    resolution: str
    escalte: bool