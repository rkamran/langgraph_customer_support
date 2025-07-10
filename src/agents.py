import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, START, END
from datatypes import CustomerSupportState, UserIntent, DBquery
from tools import get_logger, get_llm, get_db
import sys
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.types import Command
from prompts import (
    supervisor_agent_prompt, 
    sql_query_agent_prompt,     
    response_agent_prompt
)

from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,    
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool,
)

logger = get_logger(__name__)
llm = get_llm("gemma3")

db: SQLDatabase = get_db()
db_tools = SQLDatabaseToolkit(db=db, llm=llm).get_tools()


#region Agents
k_supervisor_agent = "supervisor_agent"
def supervisor_agent(state: CustomerSupportState) -> Command:
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    
    assert state['messages'] is not None, "There's nothing to ask the supervisor"    
    user_query = state.get("messages", [])[-1].content
    
    structured_llm = llm.with_structured_output(UserIntent)
    prompt = ChatPromptTemplate.from_template(supervisor_agent_prompt)
    response = (prompt | structured_llm).invoke({"user_query": user_query})

    if response.intent in ["general", "human_escalation"]:
        return Command(
            goto=END,
            update={"additional_info": "transferred to customer support human agent"}
        )

    return Command(
        goto=k_query_generation_agent,
        update={"user_intent": response.intent, "user_query": user_query}
    )


k_query_generation_agent = "query_generation_agent"
def query_generation_agent(state: CustomerSupportState) -> Command:
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    
    prompt = ChatPromptTemplate.from_template(sql_query_agent_prompt)    
    schema = RunnablePassthrough.assign(schema=lambda _: InfoSQLDatabaseTool(db=db).invoke("orders, products"))

    query = None
    results = None
    
    retry_count = state.get("retry", 1)

    llm_with_structured_output = llm.with_structured_output(DBquery)

    while retry_count < 3:      
        retry_count += 1    
        try:
            response = (schema | prompt | llm_with_structured_output).invoke({
                "dialect": f"{db.dialect}",
                "user_query": state['user_query'], 
                "available_tables": db.get_usable_table_names()
            })
            query = response.query    
            logger.info(f"Query: {query}")
            # Doesn't work consistently
            # QuerySQLCheckerTool(db=db, llm=llm).invoke(query)
            results = QuerySQLDatabaseTool(db=db, llm=llm).invoke(query)
            logger.info(f"Results: {results}")
            return Command(
                goto=k_response_agent,
                update={"db_query": query, "query_result": f"{results}"}
            )
        except Exception as e:
            logger.error(e)            
            query = None
            results = None
            if retry_count == 3:
                return Command(
                    goto=k_response_agent,
                    update={
                        "additional_info": "transferred to customer support human agent",
                        "retry": retry_count - 1
                    }
                )



k_response_agent = "response_agent"
def response_agent(state: CustomerSupportState) -> Command:
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    prompt = ChatPromptTemplate.from_template(response_agent_prompt)

    response = (prompt | llm).invoke({
        "user_query": state['user_query'],         
        "additional_info": state.get("query_result", state.get("additional_info", ""))
    })

    return Command(
        goto=END,
        update={"final_answer": response.content}
    )


# k_human_proxy_agent = "human_proxy_agent"
# def human_proxy_agent(state: CustomerSupportState):
#     logger.info(f"Running {sys._getframe(0).f_code.co_name}")

#endregion


#region Graph

graph_builder = StateGraph(CustomerSupportState)
graph_builder.add_node(k_supervisor_agent, supervisor_agent)
graph_builder.add_node(k_query_generation_agent, query_generation_agent)
graph_builder.add_node(k_response_agent, response_agent)

graph_builder.add_edge(START, k_supervisor_agent)

graph = graph_builder.compile()

#endregion