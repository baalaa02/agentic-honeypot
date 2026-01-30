# TODO: Implement intelligence extraction logic

# app/extraction/intelligence_extractor.py

import re
from typing import Dict, List

BANK_ACCOUNT_REGEX = re.compile(
    r'\b(?:\d[ -]?){9,18}\b'
)

UPI_REGEX = re.compile(
    r'\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b'
)

PHISHING_LINK_REGEX = re.compile(
    r'\bhttps?://[^\s<>"]+|www\.[^\s<>"]+\b',
    re.IGNORECASE
)


def extract_intelligence(text: str) -> Dict[str, List[str]]:
    """
    Extracts scam-related intelligence from text using deterministic patterns.
    """

    bank_accounts = BANK_ACCOUNT_REGEX.findall(text)
    upi_ids = UPI_REGEX.findall(text)
    phishing_links = PHISHING_LINK_REGEX.findall(text)

    # Normalize results
    bank_accounts = list(set([b.replace(" ", "").replace("-", "") for b in bank_accounts]))
    upi_ids = list(set(upi_ids))
    phishing_links = list(set(phishing_links))

    return {
        "bankAccounts": bank_accounts,
        "upiIds": upi_ids,
        "phishingLinks": phishing_links
    }
