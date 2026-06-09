"""
Task 3 — Convert toan bo file trong data/landing/ thanh Markdown.

Su dung MarkItDown cua Microsoft cho PDF/DOCX.
Xu ly JSON (bai bao) bang cach extract content_markdown.

Output luu vao data/standardized/ giu nguyen cau truc thu muc.
"""

import json
from pathlib import Path

from markitdown import MarkItDown

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs():
    """Convert PDF/DOCX files trong data/landing/legal/ sang markdown."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not legal_dir.exists():
        print("  [WARN] Thu muc legal/ chua ton tai")
        return

    md = MarkItDown()

    for filepath in legal_dir.iterdir():
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"  Converting: {filepath.name}")
            try:
                result = md.convert(str(filepath))
                output_path = output_dir / f"{filepath.stem}.md"
                output_path.write_text(result.text_content, encoding="utf-8")
                print(f"    [OK] Saved: {output_path.name} ({len(result.text_content)} chars)")
            except Exception as e:
                print(f"    [ERR] Loi convert {filepath.name}: {e}")


def convert_news_articles():
    """Convert JSON crawled articles trong data/landing/news/ sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not news_dir.exists():
        print("  [WARN] Thu muc news/ chua ton tai")
        return

    for filepath in news_dir.iterdir():
        if filepath.suffix.lower() == ".json":
            print(f"  Converting: {filepath.name}")
            try:
                data = json.loads(filepath.read_text(encoding="utf-8"))
                output_path = output_dir / f"{filepath.stem}.md"

                # Them metadata header
                header = f"# {data.get('title', 'Unknown')}\n\n"
                header += f"**Source:** {data.get('url', 'N/A')}\n"
                header += f"**Crawled:** {data.get('date_crawled', 'N/A')}\n\n---\n\n"

                content = header + data.get("content_markdown", "")
                output_path.write_text(content, encoding="utf-8")
                print(f"    [OK] Saved: {output_path.name} ({len(content)} chars)")
            except Exception as e:
                print(f"    [ERR] Loi convert {filepath.name}: {e}")
        elif filepath.suffix.lower() in (".html", ".txt", ".md"):
            print(f"  Copying: {filepath.name}")
            try:
                content = filepath.read_text(encoding="utf-8")
                output_path = output_dir / f"{filepath.stem}.md"
                output_path.write_text(content, encoding="utf-8")
                print(f"    [OK] Saved: {output_path.name}")
            except Exception as e:
                print(f"    [ERR] Loi copy {filepath.name}: {e}")


def convert_all():
    """Convert toan bo files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown (MarkItDown)")
    print("=" * 50)

    print("\n--- Legal Documents ---")
    convert_legal_docs()

    print("\n--- News Articles ---")
    convert_news_articles()

    # Count output files
    md_files = list(OUTPUT_DIR.rglob("*.md"))
    print(f"\n[DONE] Tong cong {len(md_files)} file markdown tai {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()
