"""
detector.py
-----------
Nijam's core detection logic: combines the transparent rule-based red-flag
checks (rules.py) with the ML text classifier (classifier.py) into a
single risk score and a plain-language explanation.

The goal is to give an elderly user or their family a simple verdict —
"Likely Safe", "Be Careful", or "High Risk" — along with the *specific
reasons*, rather than a confusing raw number, so the tool can genuinely
be understood and trusted.

Usage (CLI):
    python -m nijam.detector "Your account will be blocked, share your OTP now"

Usage (as a library):
    from nijam.detector import analyze_message
    result = analyze_message("some text")
"""

import sys

from .rules import evaluate_rules
from .classifier import load_model, predict_scam_probability

# Weight given to the rule-based score vs the ML model score when combining
RULE_WEIGHT = 0.45
ML_WEIGHT = 0.55

# Max rule score used to normalize rule_score into 0-1 range. Set below the
# theoretical maximum (sum of all weights) so that matching 2-3 strong rules
# already pushes the normalized score close to 1, rather than needing every
# rule to fire at once.
MAX_RULE_SCORE = 8


def analyze_message(text: str, model=None) -> dict:
    """
    Analyze a message and return a dict with:
      - risk_score: float 0-1 (higher = more likely a scam)
      - verdict: "Likely Safe" | "Be Careful" | "High Risk"
      - reasons: list of plain-language explanations
      - ml_probability: raw ML model score
      - rule_score: raw matched-rule weight sum
    """
    if model is None:
        model = load_model()

    rule_score, matched_rules = evaluate_rules(text)
    normalized_rule_score = min(rule_score / MAX_RULE_SCORE, 1.0)

    ml_probability = predict_scam_probability(text, model=model)

    combined = RULE_WEIGHT * normalized_rule_score + ML_WEIGHT * ml_probability

    if combined >= 0.55:
        verdict = "High Risk"
    elif combined >= 0.3:
        verdict = "Be Careful"
    else:
        verdict = "Likely Safe"

    reasons = [explanation for _, explanation in matched_rules]
    if not reasons and combined >= 0.3:
        reasons.append(
            "The wording of this message is similar to patterns seen in "
            "known scam messages."
        )

    return {
        "risk_score": round(combined, 3),
        "verdict": verdict,
        "reasons": reasons,
        "ml_probability": round(ml_probability, 3),
        "rule_score": rule_score,
    }


def print_report(text: str, result: dict):
    print("=" * 60)
    print(f"Message: {text}")
    print("-" * 60)
    print(f"Verdict: {result['verdict']}  (risk score: {result['risk_score']})")
    if result["reasons"]:
        print("Why this message was flagged:")
        for reason in result["reasons"]:
            print(f"  - {reason}")
    else:
        print("No red flags detected.")
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print('Usage: python -m nijam.detector "message text here"')
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    model = load_model()
    result = analyze_message(text, model=model)
    print_report(text, result)


if __name__ == "__main__":
    main()
