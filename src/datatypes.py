
from typing import  Annotated, List, Literal, TypedDict
from langchain_core.messages import BaseMessage
from pydantic import BaseModel



class UserIntent(BaseModel):
    intent: Literal["product_enquiry", "order_status", "human_escalation", "general"]


class DBquery(BaseModel):
    query: str


class CustomerSupportState(TypedDict):
    user_intent: Literal["product_enquiry", "order_status", "human_escalation", "general"]
    user_query: str
    db_query: str
    query_result: str
    final_answer: str
    retry: int
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
