from fastapi import APIRouter, HTTPException
from .schemas import ChatRequest, ChatResponse


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
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

    # default safe reply for stage 0
    return ChatResponse(message="unsupported request for stage 0", base_random_keys=None, member_random_keys=None)


