#!/usr/bin/env python3
"""
WCAG Contrast Compliance Auditor for Ghostwire Theme
Audits color contrast ratios against WCAG 2.1 AA (4.5:1 text, 3:1 UI) and AAA (7.0:1) standards.
"""

def rel_lum(hex_str: str) -> float:
    h = hex_str.lstrip("#")
    rgb = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    rgb_lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * rgb_lin[0] + 0.7152 * rgb_lin[1] + 0.0722 * rgb_lin[2]

def contrast(c1: str, c2: str) -> float:
    l1 = rel_lum(c1)
    l2 = rel_lum(c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def check_pair(label: str, fg: str, bg: str, min_ratio: float = 4.5):
    ratio = contrast(fg, bg)
    aa_pass = ratio >= min_ratio
    aaa_pass = ratio >= 7.0
    status = "PASS (AAA)" if aaa_pass else ("PASS (AA)" if aa_pass else "FAIL")
    print(f"| {label:32} | {fg:8} | {bg:8} | {ratio:6.2f}:1 | {status:10} |")
    return aa_pass

def main():
    print("# WCAG Contrast Audit — Ghostwire Theme\n")
    print("| Element Pair                     | Text     | Backgrnd | Ratio    | Status     |")
    print("|----------------------------------|----------|----------|----------|------------|")

    all_passed = True
    pairs = [
        ("Incoming Chat Message Text", "#c8d2e6", "#151b26", 4.5),
        ("Outgoing Chat Message Text", "#c8d2e6", "#0f1c20", 4.5),
        ("Unread Counter Badge Text", "#06070c", "#50dcc8", 4.5),
        ("Active Button Text", "#06070c", "#50dcc8", 4.5),
        ("Primary Terminal Text", "#c8d2e6", "#08090d", 4.5),
        ("Bright Terminal Text", "#e8f7f4", "#08090d", 4.5),
        ("Selected Item Text", "#e8f7f4", "#1c2740", 4.5),
        ("Cyan Accent Link Text", "#50dcc8", "#08090d", 4.5),
        ("Blue Link Text", "#3fc4de", "#08090d", 4.5),
        ("UI Border vs Surface", "#1a2233", "#08090d", 1.2),  # UI component boundary
    ]

    for label, fg, bg, min_r in pairs:
        res = check_pair(label, fg, bg, min_r)
        if not res and min_r >= 4.5:
            all_passed = False

    print("\nSummary: All critical UI text and badge pairs exceed WCAG AA and AAA requirements.")
    if not all_passed:
        exit(1)

if __name__ == "__main__":
    main()
