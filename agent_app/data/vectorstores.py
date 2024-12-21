import json
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain_openai.embeddings import OpenAIEmbeddings

from common.config import load_config  # type: ignore

config = load_config()


with open('./agent_app/data/test_event_db.json', 'r', encoding='utf-8') as file:  # noqa
    events = json.load(file)

documents = []

for event in events:
    documents.append(
        Document(
            page_content=event['description'],
            metadata={
                'title': event['title'],
                'url': event['url'],
                'address': event['address']
            }
        )
    )


events_chroma = Chroma.from_documents(
    collection_name='events_db',
    documents=documents,
    embedding=OpenAIEmbeddings(api_key=config.openai.token),
    persist_directory='./agent_app/data/events_chroma'
)
