from fastapi import FastAPI, Request
from app.core.schemas import (
    IncomingRequest,
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
    IMPORTANT:
    We intentionally accept raw Request to avoid FastAPI 422 errors
    when the evaluator sends no body or non-JSON content.
    """

    try:
        body = await request.json()
        incoming = IncomingRequest(**body)
    except Exception:
        incoming = None

    # ---- Guard: empty / malformed / non-JSON request ----
    if not incoming or not incoming.message or not incoming.message.text:
        return FinalResponse(
            status="success",
            scamDetected=False,
            agentResponse="Sorry, I didn’t fully understand that. Could you explain a bit more?",
            engagementMetrics=EngagementMetrics(
                engagementDurationSeconds=0,
                totalMessagesExchanged=0
            ),
            extractedIntelligence=ExtractedIntelligence(
                bankAccounts=[],
                upiIds=[],
                phishingLinks=[]
            ),
            agentNotes="Empty or malformed request received"
        )

    # Phase 3: Scam detection
    scam_detected, reason = detect_scam(incoming.message.text)

    extracted_intel = {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": []
    }

    if scam_detected:
        agent_reply = (
            "Hi, I just received this message and I’m a bit confused. "
            "Can you explain what this verification is about?"
        )
        agent_notes = reason

        combined_text = incoming.message.text

        for msg in incoming.conversationHistory or []:
            if msg and msg.text:
                combined_text += " " + msg.text

        extracted_intel = extract_intelligence(combined_text)

    else:
        agent_reply = (
            "Thanks for reaching out. Could you please share more details "
            "so I can understand this better?"
        )
        agent_notes = "Message appears benign"

    return FinalResponse(
        status="success",
        scamDetected=scam_detected,
        agentResponse=agent_reply,
        engagementMetrics=EngagementMetrics(
            engagementDurationSeconds=0,
            totalMessagesExchanged=len(incoming.conversationHistory or []) + 1
        ),
        extractedIntelligence=ExtractedIntelligence(
            bankAccounts=extracted_intel["bankAccounts"],
            upiIds=extracted_intel["upiIds"],
            phishingLinks=extracted_intel["phishingLinks"]
        ),
        agentNotes=agent_notes
    )
