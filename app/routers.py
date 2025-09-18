from fastapi import APIRouter, HTTPException, Request
from .schemas import ChatRequest, ChatResponse


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, request: Request) -> ChatResponse:
    last = payload.messages[-1]

    if last.type == "text":
        text = last.content.strip()

        if text == "ping":
            return ChatResponse(message="pong", base_random_keys=None, member_random_keys=None)

        if text.lower().startswith("return base random key:"):
            value = text.split(":", 1)[1].strip()
            if not value:
                raise HTTPException(status_code=400, detail="empty base key")
            return ChatResponse(message=None, base_random_keys=[value], member_random_keys=None)

        if text.lower().startswith("return member random key:"):
            value = text.split(":", 1)[1].strip()
            if not value:
                raise HTTPException(status_code=400, detail="empty member key")
            return ChatResponse(message=None, base_random_keys=None, member_random_keys=[value])

        # Stage 1: map query to a single base_random_key using retrieval
        rk = request.app.state.retrieval.search_one(text)
        if rk:
            resp = ChatResponse(message=None, base_random_keys=[rk], member_random_keys=None)
            request.app.state.log_chat(payload.chat_id, payload.model_dump(), resp.model_dump())
            return resp

    # default safe reply for stage 0
    resp = ChatResponse(message="unsupported request for stage 0", base_random_keys=None, member_random_keys=None)
    request.app.state.log_chat(payload.chat_id, payload.model_dump(), resp.model_dump())
    return resp


