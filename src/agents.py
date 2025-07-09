from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from datatypes import CustomerSupportState, UserIntent
from tools import get_logger, get_llm
import sys
from prompts import (
    supervisor_prompt
)


logger = get_logger(__name__)
llm = get_llm("llama3.2")


#region Agents
k_supervisor_agent = "supervisor_agent"
async def supervisor_agent(state: CustomerSupportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    assert state['user_query'] is not None, "There's nothing to ask the supervisor"

    response = llm.with_structured_output(UserIntent).invoke(supervisor_prompt.invoke({"input": state['user_query']}))
    logger.info(f"Supervisor response: {response}")
    return {"user_intent": response}


k_product_support_agent = "product_support_agent"
def product_support_agent(state: CustomerSupportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    return {"resolution": "resolved"}


k_order_support_agent = "order_support_agent"
def order_support_agent(state: CustomerSupportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    return {"resolution": "resolved"}


k_human_proxy_agent = "human_proxy_agent"
def human_proxy_agent(state: CustomerSupportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    return {"resolution": "resolved"}

#endregion

def route_to_agent(state: CustomerSupportState):
    
    if state.get('resolution') is not None:
        return END

    intent = state.get('user_intent')

    if intent is None:
        return k_human_proxy_agent
    

    if intent.user_intent == "PRODUCT ENQUIRY":
        return k_product_support_agent
    
    elif intent.user_intent == "ORDER":
        return k_order_support_agent
    
    elif intent.user_intent == "HUMANHELP":
        return k_human_proxy_agent
    
    
    return k_human_proxy_agent


#region Graph

graph_builder = StateGraph(CustomerSupportState)
graph_builder.add_node(k_supervisor_agent, supervisor_agent)
graph_builder.add_node(k_product_support_agent, product_support_agent)
graph_builder.add_node(k_order_support_agent, order_support_agent)
graph_builder.add_node(k_human_proxy_agent, human_proxy_agent)


graph_builder.add_edge(START, k_supervisor_agent)
graph_builder.add_conditional_edges(k_supervisor_agent, route_to_agent)
graph_builder.add_conditional_edges(k_product_support_agent, route_to_agent)
graph_builder.add_conditional_edges(k_order_support_agent, route_to_agent)
graph_builder.add_conditional_edges(k_human_proxy_agent, route_to_agent)

graph = graph_builder.compile()

#endregion