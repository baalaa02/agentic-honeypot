from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None

class IncomingRequest(BaseModel):
    message: Message
    conversationHistory: List[Message] = Field(default_factory=list)
    metadata: Optional[Metadata] = None

    class Config:
        extra = "ignore"


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
