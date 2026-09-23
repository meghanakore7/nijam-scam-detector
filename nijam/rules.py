"""
rules.py
--------
A transparent, human-readable rule-based layer that flags common patterns
used in scams targeting elderly people (fake bank alerts, lottery scams,
"grandchild in trouble" scams, urgency/fear tactics, requests for OTP/PIN,
etc.)

This is deliberately kept separate from the ML model (classifier.py) so
that Nijam can always explain *why* a message was flagged in plain
language — important for elderly users and their families to trust and
understand the tool, not just get a black-box "risky" label.
"""

import re

# Each rule: (name, regex pattern, human-readable explanation, weight)
RULES = [
    (
        "otp_pin_request",
        r"\b(otp|pin|cvv|password|net ?banking)\b",
        "Asks you to share an OTP, PIN, CVV or password — banks and "
        "government agencies never ask for these over SMS or call.",
        3,
    ),
    (
        "urgency_pressure",
        r"\b(urgent|immediately|right now|today only|expire[sd]?|blocked|"
        r"suspend(ed)?|disconnect(ed)?|avoid (arrest|fine|loss))\b",
        "Creates urgency or fear to pressure you into acting fast without "
        "thinking it through.",
        2,
    ),
    (
        "money_transfer_request",
        r"\b(send|transfer|pay).{0,20}\b(rs\.?|rupees|inr|amount|fee)\b",
        "Directly asks you to send or transfer money.",
        3,
    ),
    (
        "prize_lottery",
        r"\b(won|winner|lottery|prize|lucky draw|kbc|kaun banega)\b",
        "Claims you have won a prize or lottery you never entered.",
        3,
    ),
    (
        "family_emergency",
        r"\b(grandson|granddaughter|this is your (son|daughter|grandson|"
        r"granddaughter)|new number|do not tell anyone|don't tell anyone|"
        r"accident|hospital admission)\b",
        "Pretends to be a family member in urgent trouble, often asking "
        "you to keep it secret — a classic pressure tactic.",
        3,
    ),
    (
        "suspicious_link",
        r"(click (this|here|the)|download this app|http\S+)",
        "Asks you to click a link or download an app from an unknown "
        "source.",
        2,
    ),
    (
        "authority_impersonation",
        r"\b(rbi|income tax|police department|government account|"
        r"investigation|arrest warrant)\b",
        "Pretends to be a bank, government body or police to sound "
        "official and scare you.",
        2,
    ),
]


def evaluate_rules(text: str):
    """
    Run all rules against a message and return:
      - rule_score: sum of weights of matched rules
      - matched: list of (name, explanation) for matched rules
    """
    text_lower = text.lower()
    matched = []
    rule_score = 0

    for name, pattern, explanation, weight in RULES:
        if re.search(pattern, text_lower):
            matched.append((name, explanation))
            rule_score += weight

    return rule_score, matched
