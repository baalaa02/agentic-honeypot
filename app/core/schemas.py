# TODO: Define request and response schemas

from typing import List, Optional
from pydantic import BaseModel


# -------- Incoming request schemas --------

class Message(BaseModel):
    sender: str            # "scammer" or "user"
    text: str              # message content
    timestamp: str         # ISO-8601 string


class Metadata(BaseModel):
    channel: Optional[str] = None   # SMS / WhatsApp / Email
    language: Optional[str] = None  # English, Tamil, etc.
    locale: Optional[str] = None    # IN, US, etc.


class IncomingRequest(BaseModel):
    message: Message
    conversationHistory: List[Message]
    metadata: Optional[Metadata] = None


# -------- Outgoing response schemas --------

class EngagementMetrics(BaseModel):
    engagementDurationSeconds: int
    totalMessagesExchanged: int


class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str]
    upiIds: List[str]
    phishingLinks: List[str]


class FinalResponse(BaseModel):
    status: str
    scamDetected: bool
    agentResponse: str
    engagementMetrics: EngagementMetrics
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str
