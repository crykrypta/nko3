import logging

from pydantic import BaseModel
from typing import Literal

from langchain.prompts import ChatPromptTemplate

from langgraph.types import Command
from langgraph.graph import END

from langchain_openai.chat_models import ChatOpenAI

from agent_app.data.vectorstores import events_chroma   # type: ignore
# from agent_app.data.vectorstores import cc_chroma       # type: ignore

from agent_app.utils.state import AgentState            # type: ignore
from common.config import load_config                   # type: ignore

# ------------------- MODULE CONFIG -------------------
# Логирование
logger = logging.getLogger(__name__)
# Переменные окружения
config = load_config()


# ------------------- SUPERVIZOR NODE -------------------
# --- STRUCTURED OUTPUT
class Router(BaseModel):
    """Структурирует вывод супервизора"""
    next: Literal['events', 'company_consult', 'FINISH']


# --- SYSTEM PROMPT
supervizor_system_prompt = """You are a supervisor AI responsible for directing users based on their needs.  # noqa
Your task is to analyze the user's input and decide the next step. 

- If the user expresses interest in registering for an event, your response should be 'events'.
- If the user seeks information or consultation about the company, your response should be 'company_consult'.
- If the interaction should be concluded, your response should be 'FINISH'.

Provide your response in a structured format as specified."""
# --- LLM
llm = ChatOpenAI(model="gpt-4o-mini",
                 temperature=0,
                 api_key=config.openai.token)


# --- NODE
def supervizor(state: AgentState):
    """Решает какой узел будет следующим"""
    # Собираем сообщения в один список
    messages = [
        {"role": "system", "content": supervizor_system_prompt},
    ] + state["messages"]

    response = llm.with_structured_output(Router).invoke(messages)

    next_node = response["next"]
    if next_node == "FINISH":
        next_node = END

    return Command(goto=next_node)   # type: ignore


# ------------------- EVENT REGISTRATION NODE -------------------
# --- NODE
def event_registration(state: AgentState):
    """Регистрация на мероприятие"""
    query = state["messages"][-1].content
    events = events_chroma.similarity_search(query, k=1)  # type: ignore
    event = events[0]

    description = event.page_content
    title = event.metadata['title']
    url = event.metadata['url']

    # --- SYSTEM PROMPT
    event_system = """Вы — консультант в Telegram чате, задача которого — направлять пользователей к регистрации на мероприятия.
Супервизор перед тобой уже определил, что пользователь хочет зарегистрироваться на мероприятие.
Ответь на вопрос пользователя, и используй предоставленные данные о мероприятии, чтобы создать сообщение с приглашением на регистрацию.
Учитывай форматизацию чата Telegram при формировании сообщения.

- Используйте название мероприятия, чтобы привлечь внимание пользователя.
- Включите описание мероприятия, чтобы дать пользователю представление о том, чего ожидать.
- Предоставьте ссылку для регистрации, чтобы пользователь мог легко зарегистрироваться.
Ваш ответ должен быть в виде структурированного сообщения, которое включает все эти элементы."""  # noqa
    # --- LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=config.openai.token)  # noqa

    prompt = ChatPromptTemplate.from_messages([
        ("system", event_system),
        ("user", "Мероприятие: {title}\nОписание: {description}\nСсылка: {url}\nВопрос пользователя: {query}"),  # noqa
    ])

    chain = prompt | llm

    response = chain.invoke(
        {
            "title": title,
            "description": description,
            "url": url,
            "query": query
        }
    )
    return Command(update={"messages": [response]}, goto=END)  # type: ignore


# ------------------- COMPANY CONSULT NODE -------------------
# --- NODE
def company_consult(state: AgentState):
    """Консультация по компании"""
    query = state["messages"][-1].content
    # docs = cc_chroma.similarity_search(query, k=3)  # type: ignore

    # --- SYSTEM PROMPT
    company_consult_system = """Вы — консультант в Telegram чате, задача которого — отвечать на вопросы пользователей о компании."""  # noqa
    prompt = ChatPromptTemplate.from_messages([
        ("system", company_consult_system),
        ("user", "Вопрос пользователя: {query}"),  # noqa
    ])

    # --- LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=config.openai.token)  # noqa
    chain = prompt | llm
    response = chain.invoke({"query": query})

    return Command(update={"messages": [response]}, goto=END)  # type: ignore
