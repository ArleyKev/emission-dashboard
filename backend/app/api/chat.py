from fastapi import APIRouter
from ..schemas import ChatRequest
from ..data_loader import get_data
from ..utils.search_client import search_web
from ..utils.data_answerer import answer_from_data

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
def chat_endpoint(req: ChatRequest):

    user_message = req.message.strip()
    filters = req.filters or {}

    data_answer = answer_from_data(user_message, filters)

    citations = []
    web_answer = ""
    if req.web_fetch:
        results = search_web(user_message, top_k=3)
        for r in results:
            web_answer += f"- {r['title']}: {r['snippet']}\n"
            citations.append({"title": r["title"], "url": r["url"]})
    final = ""
    if data_answer:
        final += f"📊 **Data insights:**\n{data_answer}\n\n"
    if web_answer:
        final += f"🌍 **Web insights:**\n{web_answer}"
    if not final:
        final = "No data or web insights available."

    return {
        "answer": final.strip(),
        "citations": citations
    }
