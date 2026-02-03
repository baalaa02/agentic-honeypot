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

    bank_accounts_raw = BANK_ACCOUNT_REGEX.findall(text)
    upi_ids_raw = UPI_REGEX.findall(text)
    phishing_links_raw = PHISHING_LINK_REGEX.findall(text)

    # Normalize bank accounts: remove spaces/dashes, keep realistic lengths
    bank_accounts = []
    for acc in bank_accounts_raw:
        cleaned = acc.replace(" ", "").replace("-", "")
        if 9 <= len(cleaned) <= 18:
            bank_accounts.append(cleaned)

    # Normalize UPI IDs
    upi_ids = [u.strip() for u in upi_ids_raw]

    # Normalize phishing links
    phishing_links = []
    for link in phishing_links_raw:
        normalized = link.lower().rstrip(".,)]}")
        phishing_links.append(normalized)

    # Deduplicate + deterministic ordering
    bank_accounts = sorted(set(bank_accounts))
    upi_ids = sorted(set(upi_ids))
    phishing_links = sorted(set(phishing_links))

    return {
        "bankAccounts": bank_accounts,
        "upiIds": upi_ids,
        "phishingLinks": phishing_links
    }
