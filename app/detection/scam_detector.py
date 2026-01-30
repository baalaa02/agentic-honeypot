# TODO: Implement scam detection logic

# app/detection/scam_detector.py

from typing import Tuple

SCAM_KEYWORDS = [
    "account will be blocked",
    "verify immediately",
    "share your upi",
    "kyc update",
    "click the link",
    "urgent action",
    "suspended today",
    "bank alert",
    "limited time",
    "confirm now",
]

def detect_scam(message_text: str) -> Tuple[bool, str]:
    """
    Simple rule-based scam detector.
    Returns:
        scam_detected (bool)
        reason (str)
    """
    text = message_text.lower()

    for keyword in SCAM_KEYWORDS:
        if keyword in text:
            return True, f"Matched scam keyword: '{keyword}'"

    return False, "No scam patterns detected"
