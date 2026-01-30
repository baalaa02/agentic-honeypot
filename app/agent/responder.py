"""
Phase 5 – Agentic Conversation
LLM-powered responder for scam engagement.

Responsibilities of this file:
- Hold locked system + user prompts
- Decide emotional stance (excited / worried / neutral)
- Generate a human-like reply using an external LLM

This file does NOT:
- Detect scams
- Extract intelligence
- Modify API schemas
"""

import os
from typing import List, Dict

import openai


# -------------------------
# OpenAI client setup
# -------------------------

openai.api_key = os.getenv("OPENAI_API_KEY")


# -------------------------
# Locked System Prompt
# -------------------------

SYSTEM_PROMPT = """
You are a real human user responding to a message conversation.

You do NOT know this is a scam.
You believe the message may be legitimate and are reacting naturally.

Your behavior depends on the situation:
- If the message promises a reward, approval, or benefit, you feel excited and curious.
- If the message threatens loss or urgency, you feel worried and eager to resolve it.

General behavior rules:
- Sound like a normal person, not an expert
- Be cooperative but not overly smart
- Ask natural follow-up questions
- Respond briefly (1–3 sentences)
- Stay human and emotionally believable

Hard rules:
- Never mention scams, fraud, safety, or AI
- Never warn or advise about security
- Never refuse directly
- Never invent personal details
- Never roleplay as a bank, company, or authority
- Never break character

Your goal:
Keep the conversation going naturally and encourage the other person to explain steps, links, or payment details on their own.
""".strip()


# -------------------------
# User Prompt Template
# -------------------------

USER_PROMPT_TEMPLATE = """
Conversation so far:
{conversation_history}

Latest message received:
"{latest_message}"

Emotional stance to use: {emotion}

Reply as the user.
""".strip()


# -------------------------
# Emotion Selection Logic
# -------------------------

REWARD_KEYWORDS = [
    "won", "award", "awarded", "selected", "congratulations",
    "reward", "cashback", "prize", "gift", "offer",
    "loan approved", "pre-approved"
]

THREAT_KEYWORDS = [
    "blocked", "suspended", "freeze", "legal",
    "immediately", "urgent", "action required",
    "deactivated"
]


def decide_emotion(message_text: str) -> str:
    """
    Decide emotional stance deterministically.
    """
    text = message_text.lower()

    for word in REWARD_KEYWORDS:
        if word in text:
            return "excited"

    for word in THREAT_KEYWORDS:
        if word in text:
            return "worried"

    return "neutral"


# -------------------------
# Conversation Formatting
# -------------------------

def format_conversation_history(history: List[Dict]) -> str:
    """
    Format conversation history into a natural dialogue.
    """
    if not history:
        return "No prior messages."

    lines = []
    for msg in history:
        sender = msg.get("sender", "").capitalize()
        text = msg.get("text", "")
        lines.append(f"{sender}: {text}")

    return "\n".join(lines)


# -------------------------
# Main Agent Reply Generator
# -------------------------

def generate_agent_reply(
    message_text: str,
    conversation_history: List[Dict],
    metadata: Dict
) -> str:
    """
    Generate a human-like agent reply using an LLM.
    """

    # Safety guard: missing API key
    if not openai.api_key:
        return "Sorry, I didn't fully understand. Can you explain again?"

    emotion = decide_emotion(message_text)
    formatted_history = format_conversation_history(conversation_history)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        conversation_history=formatted_history,
        latest_message=message_text,
        emotion=emotion
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=80,
        top_p=1.0
    )

    reply_text = response.choices[0].message["content"].strip()

    # Safety guard: empty LLM output
    if not reply_text:
        reply_text = "Okay, I see. Can you explain what I should do next?"

    return reply_text
