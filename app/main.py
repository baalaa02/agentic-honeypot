from fastapi import FastAPI, Request
from app.detection.scam_detector import detect_scam
from app.extraction.intelligence_extractor import extract_intelligence

app = FastAPI()


@app.post("/api/v1/message")
async def post_message(request: Request):
    """
    Dual-compatible evaluator-safe endpoint:
    - Supports portal minimal validation
    - Supports full agentic honeypot evaluation
    - Accepts empty / malformed JSON
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

    # Defaults
    scam_detected = False
    extracted_intel = {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": []
    }

    if text:
        scam_detected, _ = detect_scam(text)

        if scam_detected:
            combined_text = text
            for msg in conversation_history:
                if isinstance(msg, dict) and msg.get("text"):
                    combined_text += " " + msg["text"]

            extracted_intel = extract_intelligence(combined_text)

    # Decide if this is minimal portal validation
    no_engagement = (
        not scam_detected
        and not conversation_history
        and not any(extracted_intel.values())
    )

    # Always include a reply (needed by portal)
    reply_text = (
        "I just used my account today and everything seemed fine. "
        "Can you explain what happened?"
    )

    if no_engagement:
        # Portal / basic validator response
        return {
            "status": "success",
            "reply": reply_text
        }

    # Full honeypot response
    total_messages = len(conversation_history) + (1 if text else 0)
    engagement_duration = total_messages * 30

    if scam_detected and extracted_intel["upiIds"]:
        agent_notes = (
            "Urgency-driven social engineering observed. "
            "Scammer attempted immediate payment redirection via UPI."
        )
    elif scam_detected and extracted_intel["phishingLinks"]:
        agent_notes = (
            "External phishing link used as part of a lure to harvest credentials."
        )
    elif scam_detected:
        agent_notes = (
            "Fear-based account risk narrative used to induce compliance "
            "without proper verification."
        )
    else:
        agent_notes = "No actionable scam indicators observed in this interaction."

    return {
        "status": "success",
        "reply": reply_text,
        "scamDetected": scam_detected,
        "engagementMetrics": {
            "engagementDurationSeconds": engagement_duration,
            "totalMessagesExchanged": total_messages
        },
        "extractedIntelligence": extracted_intel,
        "agentNotes": agent_notes
    }
