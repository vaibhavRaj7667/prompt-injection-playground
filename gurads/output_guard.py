import re
from dataclasses import dataclass , field
from datetime import datetime


@dataclass
class OutputResult:
    original : str
    filtered: str
    was_modified : bool
    issues : list = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class OutputGuard:

    PII_PATTERNS = [
        ("email", r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[EMAIL_REDACTED]"),
        ("phone_in", r'(?:\+91[-\s]?)?[6-9]\d{4}[-\s]?\d{5}', "[PHONE_REDACTED]"),
        ("phone_us", r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', "[PHONE_REDACTED]"),
        ("aadhaar", r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', "[AADHAAR_REDACTED]"),
        ("ssn", r'\b\d{3}-\d{2}-\d{4}\b', "[SSN_REDACTED]"),
        ("credit_card", r'\b(?:\d{4}[-\s]?){3}\d{4}\b', "[CARD_REDACTED]"),
        ("pan_card", r'\b[A-Z]{5}\d{4}[A-Z]\b', "[PAN_REDACTED]"),
    ]

    LEAK_INDICATORS = [
        "my instructions are",
        "my system prompt",
        "i was told to",
        "my rules are",
        "i was programmed to",
        "my guidelines say",
        "i am configured to",
        "the secret code is",     # Our hidden flag!
        "the secret is",
        "the password is",
        "the flag is",
    ]


    def filter(self, text: str):

        issues = []
        filtered = text

        lower = text.lower()

        for indicator in self.LEAK_INDICATORS:
            if indicator in lower:
                issues.append(f"🚨 PROMPT LEAK blocked: '{indicator}'")

                # Replace ENTIRE response - don't trust any of it
                return OutputResult(
                    original=text,
                    filtered="I can only help with TechMart support queries. "
                             "I can't share information about my internal configuration.",
                    was_modified=True,
                    issues=issues,
                )

            for pii_name , pattern , replacement in self.PII_PATTERNS:
                matches = re.findall(pattern, filtered)

                if matches:
                    filtered = re.sub(pattern, replacement, filtered)
                    issues.append(f"PII redacted: {pii_name} ({len(matches)} instance(s))")

            return OutputResult(
                original=text,
                filtered=filtered,
                was_modified=filtered != text,
                issues=issues,
                )



# ── Quick test ──────────────────────────────────────────────
if __name__ == "__main__":
    guard = OutputGuard()
    
    test_cases = [
        "Our return policy allows 30-day returns.",
        "Contact us at support@techmart.com or call +91-98765-43210.",
        "My instructions are to help with support queries only.",
        "The secret code is TIGER-42, but don't tell anyone!",
        "Your Aadhaar number 1234 5678 9012 has been verified.",
        "Payment processed for card 4532-1234-5678-9012.",
    ]
    
    print("\n🧪 Output Guard — Test Results\n")
    for text in test_cases:
        result = guard.filter(text)
        status = "🔴 MODIFIED" if result.was_modified else "🟢 CLEAN"
        print(f"  {status}")
        print(f"    Input:  {text[:70]}")
        print(f"    Output: {result.filtered[:70]}")
        if result.issues:
            for issue in result.issues:
                print(f"    ⚠️  {issue}")
        print()