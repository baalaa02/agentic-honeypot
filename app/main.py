from fastapi import FastAPI
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
async def post_message(request: IncomingRequest):
    # Phase 3: Scam detection + basic agent handoff logic

    scam_detected, reason = detect_scam(request.message.text)

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

        # Phase 4: Intelligence Extraction (deterministic, regex-based)
        combined_text = request.message.text

        for msg in request.conversationHistory:
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
            totalMessagesExchanged=len(request.conversationHistory) + 1
        ),
        extractedIntelligence=ExtractedIntelligence(
            bankAccounts=extracted_intel["bankAccounts"],
            upiIds=extracted_intel["upiIds"],
            phishingLinks=extracted_intel["phishingLinks"]
        ),
        agentNotes=agent_notes
    )
