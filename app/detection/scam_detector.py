# app/detection/scam_detector.py

from typing import Tuple

# Keyword → tactic mapping
SCAM_PATTERNS = {
    "account will be blocked": "Fear-based account suspension tactic",
    "suspended today": "Fear-based account suspension tactic",
    "bank alert": "Authority impersonation tactic",
    "verify immediately": "Urgency-driven compliance pressure",
    "urgent action": "Urgency-driven compliance pressure",
    "limited time": "Artificial deadline manipulation",
    "confirm now": "Immediate action coercion",
    "share your upi": "Payment redirection attempt via UPI",
    "kyc update": "Fake compliance or KYC update narrative",
    "click the link": "Phishing redirection attempt",
}

def detect_scam(message_text: str) -> Tuple[bool, str]:
    """
    Simple deterministic scam detector.
    Returns:
        scam_detected (bool)
        reason (str)
    """

    if not message_text:
        return False, "Empty message content"

    text = message_text.lower().strip()

    for keyword, tactic in SCAM_PATTERNS.items():
        if keyword in text:
            return True, tactic

    return False, "No scam patterns detected"
