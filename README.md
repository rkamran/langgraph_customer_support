
### **Problem 2: Interactive RAG-Based Customer Support Bot**

This problem requires you to build a sophisticated customer support bot that uses a database as its primary knowledge source. The bot must handle multi-turn conversations, understand user intent, escalate to a human agent when necessary, and log its interactions for future analysis.

---

### **Problem Description**

You are tasked with building "CircuitHelper," an AI customer support bot for an e-commerce company that sells electronics. The bot will assist users with product inquiries, order status questions, and troubleshooting common issues.

The core challenge is to make the bot retrieve information directly from a structured database, providing specific and accurate answers based on real-time data. It must also be able to handle evolving conversations, ask clarifying questions, and decide when a problem is too complex for it to solve.

### **Core Functional Requirements**

1.  **Intent Recognition:** The bot must first determine the user's intent. The primary intents are:
    * **Product Inquiry:** User asks about product details (e.g., "What are the specs of the 'CyberGamer X1' laptop?", "Do you have any 4K monitors?").
    * **Order Status:** User asks about an existing order (e.g., "Where is my order #12345?", "When will my package arrive?").
    * **Troubleshooting:** User has a problem with a product (e.g., "My new headphones won't connect to Bluetooth.").
    * **Human Escalation:** User explicitly asks to speak to a person (e.g., "talk to an agent").

2.  **RAG from a Database:**
    * The bot's knowledge **must** come from a **PostgreSQL** database. You will need to create and populate a simple database with at least these three tables:
        * `products`: with columns like `product_id`, `product_name`, `description`, `specs` (JSONB), `price`, and `stock_quantity`.
        * `orders`: with columns like `order_id`, `customer_id`, `order_date`, `status` (e.g., 'Processing', 'Shipped', 'Delivered'), and `tracking_number`.
        * `troubleshooting_guides`: with columns like `guide_id`, `product_category`, `issue_description`, and `solution_steps`.
    * The bot must be able to translate a user's natural language query into a **SQL query** to fetch the relevant information from these tables.

3.  **Dynamic, Multi-Turn Conversation:** The bot must maintain the context of the conversation.
    * **Clarification:** If a query is ambiguous (e.g., "Tell me about the laptop"), the bot should ask for more specific information (e.g., "Certainly! Which laptop model are you interested in?").
    * **Follow-up Questions:** If a user asks a follow-up question ("How much RAM does it have?"), the bot should know the conversation is still about the previously mentioned product.

4.  **Human Escalation Logic:** The bot needs a "safety valve." It must decide when it's unable to help and should escalate to a human agent. This decision must be triggered if:
    * The user explicitly asks for an agent.
    * A database query fails to find an answer after **two** attempts.

5.  **Interaction Logging:** Every conversation (including user queries, bot responses, generated SQL queries, and the final outcome) must be logged into a separate `interaction_logs` table in the PostgreSQL database.

### **Agent & Graph Design**

You will need a team of agents orchestrated by LangGraph to manage this workflow. A recommended structure is:

* **Router Agent:** The entry point. This agent's only job is to classify the user's intent and route the conversation to the appropriate specialist or to the escalation path.
* **SQL Query Agent:** A specialized agent that takes a user's question and the conversation history, and its only job is to generate a valid SQL query.
* **Database Agent:** A simple node that executes the SQL query against the database and returns the results. It should also catch any errors.
* **Response Generation Agent:** Takes the structured data retrieved from the database and formulates a natural, human-readable response.
* **Escalation Agent:** A final node that informs the user they are being transferred to a human agent.

Your graph must have **conditional edges** leading from the `Router Agent` to the `SQL Query Agent` or the `Escalation Agent`. Another conditional edge is required after the `Database Agent` to check if the query returned results. If not, the graph should loop back to ask a clarifying question or, after a set number of retries, route to the `Escalation Agent`.

### **Technical Stack and Constraints**

* **Orchestration:** **Langgraph**. The state object must track the conversation history, current user intent, a retry counter, and any data retrieved from the database.
* **Database:** **PostgreSQL**. This is a firm requirement. You are responsible for the schema, dummy data, and query logic.
* **Text-to-SQL:** You must build a component that converts natural language to SQL. Leverage LangChain's built-in functionalities for this, such as `create_sql_query_chain`.
* **Caching:** **Redis**. You must cache the **final generated answers**. If two users ask the exact same question (e.g., "What is the price of the CyberGamer X1?"), the answer for the second user should be served from the cache to reduce redundant LLM and DB calls.
* **Interface:** A command-line interface (CLI) is sufficient to demonstrate the interactive conversation.

### **Your Task**

1.  **Database Setup:** Design and create the PostgreSQL schema with the four required tables. Populate them with varied dummy data (at least 5-10 rows per table).
2.  **RAG Tooling:** Create the core tool/chain that converts a user's question into a SQL query.
3.  **Langgraph Design:** Define the `State` object and the agent nodes. The most important part is designing the **conditional logic** for routing based on intent and for handling database lookup failures and retries.
4.  **Agent and Graph Implementation:** Write the Python code for the agents and wire them together in the LangGraph graph according to your design.
5.  **Application Logic:** Build the main application loop that simulates a chat session, passes user input to your graph, manages state across turns, and logs the entire interaction to the database.