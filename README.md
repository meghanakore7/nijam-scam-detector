# Nijam — Scam Detection for the Elderly

*"Nijam" means "truth" — helping elderly users tell what's real from what's a trap.*

## The Problem

Scam calls and messages targeting elderly people are everywhere — fake
lottery wins, "your bank account will be blocked" threats, impersonated
grandchildren asking for urgent money, fake government notices. These
scams work because they lean on **urgency, fear, and trust** — exactly
the pressure points that make even careful people freeze up and act
without thinking.

Elderly users are disproportionately targeted because they're often less
familiar with digital fraud patterns, more trusting of anything that
"sounds official," and less likely to have someone nearby to double-check
a suspicious message with in the moment.

## The Solution

Nijam is a lightweight scam-message detector that analyzes a text
message (SMS, WhatsApp, or transcribed call) and gives a **simple,
explainable verdict**:

- ✅ **Likely Safe**
- ⚠️ **Be Careful**
- 🚫 **High Risk**

along with **plain-language reasons** — not just a score, but *why* it
was flagged, in language a non-technical person can immediately
understand and act on ("This message asks you to share your OTP — real
banks never ask for this").

### How it works

Nijam combines two layers:

1. **Rule-based red flags** (`nijam/rules.py`) — a transparent set of
   patterns for well-known scam tactics: requests for OTP/PIN, urgency
   and fear language, impersonated family members, prize/lottery claims,
   suspicious links, and authority impersonation (fake police/RBI/income
   tax messages). This layer is fully explainable — every flag has a
   plain-English reason attached.

2. **A lightweight ML text classifier** (`nijam/classifier.py`) — a
   TF-IDF + Naive Bayes model trained on a sample set of scam vs.
   legitimate messages (`data/messages.csv`), which can catch scam-like
   *phrasing* even when it doesn't match an exact rule keyword.

The two scores are combined into one risk score and verdict
(`nijam/detector.py`).

> **Note on the dataset:** `data/messages.csv` is a small, illustrative
> sample of common Indian elder-scam patterns (fake KBC lottery wins,
> fake bank/RBI alerts, "grandson in trouble" messages, etc.) written for
> this prototype. A real deployment would need a much larger, more
> diverse dataset built with proper consent and privacy safeguards —
> this repo demonstrates the approach and pipeline, not a
> production-ready model.

## Target Audience

- **Primary:** Elderly individuals (60+) who receive scam SMS/WhatsApp
  messages and calls, especially those managing digital banking or
  UPI payments with limited prior exposure to online fraud tactics.
- **Secondary:** Family members and caregivers who want a quick way to
  double-check a message their elderly parent or grandparent forwards to
  them, saying "is this real?"

## Social Issue & Impact

Financial scams targeting the elderly cause real harm — not just money
lost, but the erosion of trust, independence, and confidence in using
digital services at all, which pushes some elderly users to disengage
from banking apps and digital payments entirely.

Nijam's goal isn't to replace human judgment but to **slow the moment
down** — giving an elderly user (or the family member they text) a fast,
understandable second opinion before they act, at exactly the moment a
scammer is counting on them acting fast.

## Project Structure

```
nijam/
├── data/
│   └── messages.csv          # sample labeled dataset (scam / legit)
├── nijam/
│   ├── rules.py               # transparent rule-based red-flag checks
│   ├── classifier.py          # TF-IDF + Naive Bayes ML classifier
│   └── detector.py            # combines both, CLI entry point
├── try_it.py                  # simple interactive tester
├── requirements.txt
└── README.md
```

## Running it

Install dependencies:

```bash
pip install -r requirements.txt
```

Check a single message from the command line:

```bash
python -m nijam.detector "Congratulations! You have won Rs 25,00,000. Share your OTP to claim."
```

Or try messages interactively:

```bash
python try_it.py
```

Example output:

```
============================================================
Message: Your bank account will be blocked today, click this link
and enter your PIN immediately
------------------------------------------------------------
Verdict: High Risk  (risk score: 0.817)
Why this message was flagged:
  - Asks you to share an OTP, PIN, CVV or password — banks and
    government agencies never ask for these over SMS or call.
  - Creates urgency or fear to pressure you into acting fast
    without thinking it through.
  - Asks you to click a link or download an app from an unknown
    source.
============================================================
```

## Possible Extensions

- A WhatsApp bot or simple mobile app wrapper so elderly users (or their
  family) can forward a suspicious message directly and get an instant
  verdict.
- Voice-call transcription + real-time analysis for phone scam calls,
  not just text.
- A much larger, crowdsourced, consented dataset of real scam messages
  (in regional languages too — Telugu, Hindi, etc.) to make the ML layer
  far more robust.
- Family "alert" mode — optionally notify a trusted family member when a
  High Risk message is detected.

## Author

Pedhodha — CSE student, built for a Tech for Social Good hackathon
submission.
