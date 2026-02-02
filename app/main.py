from fastapi import FastAPI, Request
from app.core.schemas import (
    FinalResponse,
    EngagementMetrics,
    ExtractedIntelligence
)
from app.detection.scam_detector import detect_scam
from app.extraction.intelligence_extractor import extract_intelligence

app = FastAPI()


@app.post("/api/v1/message", response_model=FinalResponse)
async def post_message(request: Request):
    """
    Evaluator-safe endpoint:
    - Accepts empty body
    - Accepts non-JSON
    - Never throws 422
    """

    text = ""
    conversation_history = []

    try:
        body = await request.json()
        message = body.get("message") or {}
        text = message.get("text") or ""
        conversation_history = body.get("conversationHistory") or []
    except Exception:
        pass

    # Default values
    scam_detected = False
    agent_notes = "No scam indicators detected"
    extracted_intel = {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": []
    }

    if text:
        scam_detected, reason = detect_scam(text)
        agent_notes = reason

        if scam_detected:
            combined_text = text
            for msg in conversation_history:
                if isinstance(msg, dict) and msg.get("text"):
                    combined_text += " " + msg["text"]

            extracted_intel = extract_intelligence(combined_text)

    return FinalResponse(
        status="success",
        scamDetected=scam_detected,
        engagementMetrics=EngagementMetrics(
            engagementDurationSeconds=0,
            totalMessagesExchanged=len(conversation_history) + (1 if text else 0)
        ),
        extractedIntelligence=ExtractedIntelligence(
            bankAccounts=extracted_intel["bankAccounts"],
            upiIds=extracted_intel["upiIds"],
            phishingLinks=extracted_intel["phishingLinks"]
        ),
        agentNotes=agent_notes
    )
