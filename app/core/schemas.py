from pydantic import BaseModel, Field
from typing import List, Optional


# -------- Incoming request schemas --------

class Message(BaseModel):
    sender: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        extra = "ignore"


class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None

    class Config:
        extra = "ignore"


class IncomingRequest(BaseModel):
    message: Optional[Message] = None
    conversationHistory: Optional[List[Message]] = Field(default_factory=list)
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
