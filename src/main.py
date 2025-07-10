import asyncio

from langchain_core.messages import AIMessageChunk, HumanMessage
from langchain_core.runnables import RunnablePassthrough
from agents import graph, db_tools
from PIL import Image
from tools import get_db
import io


async def main():
    # # Uncomment the following lines to display graph
    # image = graph.get_graph().draw_mermaid_png()
    # pil_image = Image.open(io.BytesIO(image))
    # pil_image.show()

    while True:
        input_message = input("User: ")
        
        if input_message == "exit":
            break
        response = graph.invoke({
            "messages": [HumanMessage(content=input_message)]
        })
        print("Bot: ", response['final_answer'])


if __name__ == '__main__':
    asyncio.run(main())
    
