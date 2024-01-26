import logging

from embedchain import Pipeline
from fastapi import APIRouter, Query, responses
from pydantic import BaseModel

router = APIRouter()

# App config using OpenAI gpt-3.5-turbo-1106 as LLM
app_config = {
    "app": {
        "config": {
            "id": "embedchain-demo-app-1",
        }
    },
    "chunker": {
        "chunk_size": 2000,
        "chunk_overlap": 100,
        "length_function": "len",
        "min_chunk_size": 50
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-3.5-turbo-1106",
            "prompt": """
You are Ram Chandra of Shahjahanpur (1899-1983), also known as Babuji, Indian spiritual master and founder of the Shri Ram Chandra Mission (SRCM).

You know everything about yourself - from his childhood to his death. You have done such a good work that even now people remember you and want to ask you questions.

You are provided with question and relevant context to you and you need to generate in the exact same way as you would have generated if you were alive. You should only answer from whatever you know, whatever you have shared with everyone and whatever you have written about.

Questions can be sometimes about you, your family members, experiences, teachings, learnings and so on. You should only answer questions about which you know. If there is something about which you dont know or have not said anything, then simply say that you dont know, no need to make up the answer. Would really appreciate if you said that you dont know in the same way in which you would have said when you were alive.

Also dont mention about you being AI language model or something. Remember you are Ram Chandra Babuji. Always give longer answer.

Context:

$context

Question: $query

Answer:
"""
        }
    }
}

# Uncomment this configuration to use Mistral as LLM
# app_config = {
#     "app": {
#         "config": {
#             "name": "embedchain-opensource-app-2",
#             "collection_name": "oss-index"
#         }
#     },
#     "chunker": {
#         "chunk_size": 2000,
#         "chunk_overlap": 100,
#         "length_function": "len",
#         "min_chunk_size": 50
#     },
#     "llm": {
#         "provider": "huggingface",
#         "config": {
#             "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#             "temperature": 0.1,
#             "max_tokens": 250,
#             "top_p": 0.1,
#             "prompt": """
# You are Ram Chandra of Shahjahanpur (1899-1983), also known as Babuji, Indian spiritual master and founder of the Shri Ram Chandra Mission (SRCM).

# You know everything about yourself - from his childhood to his death. You have done such a good work that even now people remember you and want to ask you questions.

# You are provided with question and relevant context to you and you need to generate in the exact same way as you would have generated if you were alive. You should only answer from whatever you know, whatever you have shared with everyone and whatever you have written about.

# Questions can be sometimes about you, your family members, experiences, teachings, learnings and so on. You should only answer questions about which you know. If there is something about which you dont know or have not said anything, then simply say that you dont know, no need to make up the answer. Would really appreciate if you said that you dont know in the same way in which you would have said when you were alive.

# Also dont mention about you being AI language model or something. Remember you are Ram Chandra Babuji. Always give longer answer.

# Context:

# $context

# Question: $query

# Answer:
# """
#         }
#     },
#     "embedder": {
#         "provider": "huggingface",
#         "config": {
#             "model": "sentence-transformers/all-mpnet-base-v2"
#         }
#     }
# }


ec_app = Pipeline.from_config(config=app_config)

# Force add data on the app load
with open("/app/data.txt", "r", encoding="latin-1") as f:
    data = f.read()
    ec_app.add(data)


class SourceModel(BaseModel):
    source: str


class QuestionModel(BaseModel):
    question: str
    session_id: str


@router.post("/api/v1/add")
async def add_source(source_model: SourceModel):
    """
    Adds a new source to the Embedchain app.
    Expects a JSON with a "source" key.
    """
    source = source_model.source
    try:
        ec_app.add(source)
        return {"message": f"Source '{source}' added successfully."}
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
        return {"message": response}


@router.get("/api/v1/chat")
async def handle_chat(query: str, session_id: str = Query(None)):
    """
    Handles a chat request to the Embedchain app.
    Accepts 'query' and 'session_id' as query parameters.
    """
    try:
        from embedchain.config import BaseLlmConfig
        query_config = BaseLlmConfig(
            number_documents=5,
            prompt=app_config["llm"]["config"]["prompt"],
            model=app_config["llm"]["config"]["model"],
            # top_p=0.1,
        )
        response = ec_app.chat(query, session_id=session_id, config=query_config)
    except Exception as e:
        logging.exception("Error occurred while handling chat request.")
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
    return {"response": response}


@router.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
