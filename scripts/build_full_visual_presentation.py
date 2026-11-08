#!/usr/bin/env python3
"""
Full Visual Step-by-Step Presentation Builder
Generates:
1. presentation.html & report/presentation.html (Interactive standalone HTML5 deck)
2. report/slides_content.md (Complete markdown transcript with bilingual scripts)
"""

import os
import sys
import json

BASE_DIR = '/mnt/c/Users/ndhs/Works/hcmut-msc-cs/co5173/project'
sys.path.append(os.path.join(BASE_DIR, 'scripts'))

from presentation_data import ALL_SLIDES

def build_html_presentation(slides, output_path):
    slides_json = []
    
    for idx, s in enumerate(slides, 1):
        slides_json.append({
            "num": idx,
            "id": s["id"],
            "section": s["section"],
            "badge": s.get("badge", ""),
            "title": s["title"],
            "subtitle": s["subtitle"],
            "visual_html": s["visual_html"],
            "key_points": s.get("key_points", []),
            "script_en": s["script_en"],
            "script_vi": s["script_vi"]
        })

    # Render template using string replacement to avoid quote escaping issues
    with open('/mnt/c/Users/ndhs/Works/hcmut-msc-cs/co5173/project/scripts/template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    rendered = template.replace('__SLIDES_DATA_PLACEHOLDER__', json.dumps(slides_json, indent=2))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    print(f"Generated HTML slide deck at: {output_path} ({os.path.getsize(output_path)} bytes)")

def build_markdown_report(slides, output_path):
    md_lines = [
        "# CO5173 — Storage Engine Duality: Cassandra (LSM) vs Elasticsearch (Inverted Index)",
        "## Complete 23-Slide Presentation Content & Bilingual Speaker Transcripts",
        "",
        "> **Presentation Pacing:** 23 bite-sized visual slides designed for a 15-minute presentation (~39 seconds per slide).",
        "> **Bilingual Delivery:** Full scripts provided in both English (EN) and Vietnamese (VI).",
        "",
        "---",
        ""
    ]

    for s in slides:
        md_lines.append(f"### Slide {s['id'][-2:]}: {s['title']}")
        md_lines.append(f"**Section:** `{s['section']}` | **Badge:** `{s.get('badge', '')}`  ")
        md_lines.append(f"**Subtitle:** *{s['subtitle']}*  ")
        md_lines.append("")
        md_lines.append("#### Key Points:")
        for kp in s.get("key_points", []):
            md_lines.append(f"- {kp}")
        md_lines.append("")
        md_lines.append("#### Verbatim Spoken Scripts:")
        md_lines.append(f"- **English (EN):** \"{s['script_en']}\"")
        md_lines.append(f"- **Tiếng Việt (VI):** \"{s['script_vi']}\"")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))
    print(f"Generated Markdown report at: {output_path} ({os.path.getsize(output_path)} bytes)")

def main():
    html_target_1 = os.path.join(BASE_DIR, 'presentation.html')
    html_target_2 = os.path.join(BASE_DIR, 'report', 'presentation.html')
    md_target = os.path.join(BASE_DIR, 'report', 'slides_content.md')

    build_html_presentation(ALL_SLIDES, html_target_1)
    build_html_presentation(ALL_SLIDES, html_target_2)
    build_markdown_report(ALL_SLIDES, md_target)
    print("All presentation assets built and synchronized successfully.")

if __name__ == '__main__':
    main()
