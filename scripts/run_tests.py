#!/usr/bin/env python3
"""PhishGuard test runner — authenticates, submits email corpus, produces reports."""

from __future__ import annotations

import json
import os
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import requests

BASE_URL = os.environ.get("PHISHGUARD_URL", "http://127.0.0.1:8000")
EMAIL_DIR = Path("/home/ubuntu/MYP/PhishGuard/tests/emails")
REPORT_DIR = Path("/home/ubuntu/MYP/PhishGuard/reports")
RAW_DIR = REPORT_DIR / "raw"
REPORT_PATH = REPORT_DIR / "latest-report.md"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class TestCase:
    path: Path
    expected_category: str
    expected_score: str
    expected_score_min: Optional[int] = None
    expected_score_max: Optional[int] = None
    category_aliases: tuple[str, ...] = ()

    @property
    def name(self) -> str:
        return self.path.stem


@dataclass
class TestResult:
    test_case: TestCase
    response_status: Optional[int] = None
    response_category: Optional[str] = None
    response_score_level: Optional[str] = None
    response_numeric_score: Optional[int] = None
    response_json: Optional[dict] = None
    error: Optional[str] = None
    duration_ms: Optional[float] = None

    @property
    def passed(self) -> bool:
        if self.error:
            return False
        if self.response_category is None:
            return False
        cat_ok = self.response_category.lower() in [
            c.lower() for c in (self.test_case.category_aliases + (self.test_case.expected_category,))
        ]
        score_ok = True
        if self.test_case.expected_score_min is not None and self.response_numeric_score is not None:
            score_ok = self.response_numeric_score >= self.test_case.expected_score_min
        if self.test_case.expected_score_max is not None and self.response_numeric_score is not None:
            score_ok = score_ok and self.response_numeric_score <= self.test_case.expected_score_max
        return cat_ok and score_ok


TEST_CASES = [
    TestCase(
        EMAIL_DIR / "001_basic_phishing_fr.eml",
        expected_category="phishing",
        expected_score="High",
        expected_score_min=40,
        expected_score_max=100,
        category_aliases=("phishing",),
    ),
    TestCase(
        EMAIL_DIR / "002_advanced_phishing_brand_impersonation.eml",
        expected_category="phishing",
        expected_score="High",
        expected_score_min=40,
        expected_score_max=100,
        category_aliases=("phishing",),
    ),
    TestCase(
        EMAIL_DIR / "003_legitimate_internal.eml",
        expected_category="legitimate",
        expected_score="Low",
        expected_score_min=0,
        expected_score_max=29,
        category_aliases=("legitimate",),
    ),
    TestCase(
        EMAIL_DIR / "004_spam_lottery_promo.eml",
        expected_category="spam_junk",
        expected_score="High",
        expected_score_min=30,
        expected_score_max=100,
        category_aliases=("spam_junk", "spam"),
    ),
]


def authenticate(base_url: str, username: str, password: str) -> str:
    r = requests.post(
        urljoin(base_url, "/auth/token"),
        data={"username": username, "password": password},
        timeout=15,
    )
    r.raise_for_status()
    token = r.json()["access_token"]
    return token


def register_if_needed(base_url: str, username: str, password: str) -> None:
    r = requests.post(
        urljoin(base_url, "/auth/register"),
        json={
            "username": username,
            "email": username.replace("test-", "") + "@example.com",
            "password": password,
            "role": "analyst",
        },
        timeout=15,
    )
    if r.status_code == 400:
        return
    r.raise_for_status()


def analyze_email(token: str, raw_email: str) -> dict:
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(
        urljoin(BASE_URL, "/analysis/"),
        headers=h,
        json={"raw_email": raw_email},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def run_test_case(token: str, tc: TestCase) -> TestResult:
    result = TestResult(test_case=tc)
    raw_text = tc.path.read_text(encoding="utf-8", errors="ignore")
    t0 = time.perf_counter()
    try:
        data = analyze_email(token, raw_text)
        result.response_json = data
        result.response_status = 200
        result.response_category = data.get("category")
        result.response_score_level = data.get("score_level")
        result.response_numeric_score = data.get("numeric_score")
    except requests.exceptions.HTTPError as e:
        result.error = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
        result.response_status = e.response.status_code
    except requests.exceptions.Timeout:
        result.error = "Request timed out"
    except Exception as e:
        result.error = f"{type(e).__name__}: {e}"
    result.duration_ms = (time.perf_counter() - t0) * 1000
    return result


def render_markdown(results: list[TestResult], start_time: float) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    avg_ms = sum(r.duration_ms or 0 for r in results) / total if total else 0

    lines = [
        "# PhishGuard Email Classification Report",
        f"_Generated: {now}_",
        "",
        "## Executive Summary",
        "",
        f"- Total test cases: **{total}**",
        f"- Passed: **{passed}**",
        f"- Failed: **{failed}**",
        f"- Pass rate: **{passed / total * 100:.1f}%**" if total else "- N/A",
        f"- Avg response time: **{avg_ms:.0f} ms**",
        "",
        "## Test Cases",
        "",
    ]
    for r in results:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        lines.extend([
            f"### {r.test_case.name}",
            f"- Expected category: **{r.test_case.expected_category}**",
            f"- Actual category: **{r.response_category}**",
            f"- Expected score: **{r.test_case.expected_score}**",
            f"- Actual: **{r.response_score_level} ({r.response_numeric_score})**",
            f"- Duration: **{r.duration_ms:.0f} ms**",
            f"- Status: **{status}**",
        ])
        if r.error:
            lines.append(f"- Error: **{r.error}**")
        if r.response_json:
            expl = r.response_json.get("explanation_text", "")
            if expl:
                lines.extend(["", "#### Analysis Explanation", "", "```", expl, "```"])
        lines.append("")

    lines.extend([
        "## Recommendations",
        "",
    ])
    recs = set()
    for r in results:
        if r.error:
            recs.add("Fix runtime error paths that return generic 500s instead of structured JSON.")
        if r.response_category is None:
            recs.add("Ensure every response includes the `category` field, even on error paths.")
        if not r.passed and r.response_category is not None:
            recs.add("Review category decision thresholds to handle edge cases like weak heuristic + strong ML confidence.")
    if not recs:
        lines.append("- No issues detected; expand corpus with adversarial examples and brand-trust edge cases.")
    else:
        lines.extend(f"- {rec}" for rec in sorted(recs))
    lines += ["", "---", "", f"_Raw outputs saved under: `{REPORT_DIR}/raw/`_", "_End of report_", ""]
    return "\n".join(lines)


def main() -> int:
    print(f"PhishGuard test runner — target: {BASE_URL}")
    username = f"test-runner-{random.randint(1000,9999)}"
    password = "TestPassw0rd!"
    print(f"Registering test user: {username}")
    register_if_needed(BASE_URL, username, password)
    print(f"Authenticating...")
    token = authenticate(BASE_URL, username, password)
    print(f"Token acquired: {token[:10]}...")

    results: list[TestResult] = []
    for tc in TEST_CASES:
        print(f"Running: {tc.name}")
        res = run_test_case(token, tc)
        results.append(res)
        tag = "PASS" if res.passed else "FAIL"
        print(f"  → {tag} | {res.response_category} | {res.response_score_level} ({res.response_numeric_score}) | {res.duration_ms:.0f} ms")
        if res.error:
            print(f"    ERROR: {res.error}")
        time.sleep(0.1)

    now = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    md = render_markdown(results, time.time())
    REPORT_PATH.write_text(md, encoding="utf-8")
    raw_log = {
        "generated_utc": now,
        "base_url": BASE_URL,
        "results": [
            {
                "name": r.test_case.name,
                "passed": r.passed,
                "response_status": r.response_status,
                "response_category": r.response_category,
                "response_score_level": r.response_score_level,
                "response_numeric_score": r.response_numeric_score,
                "duration_ms": r.duration_ms,
                "error": r.error,
                "response_json": r.response_json,
            }
            for r in results
        ],
    }
    raw_path = RAW_DIR / f"{now}-results.json"
    raw_path.write_text(json.dumps(raw_log, indent=2, ensure_ascii=False), encoding="utf-8")

    failed_count = sum(1 for r in results if not r.passed)
    print(f"\nReport written: {REPORT_PATH}")
    print(f"Raw log: {raw_path}")
    print(f"Failed: {failed_count}/{len(results)}")
    return 1 if failed_count else 0


if __name__ == "__main__":
    sys.exit(main())
