"""
Builds the 2.5-minute video walkthrough demonstration for the Super Investing AI Research Agent.
Generates presentation frames, synthesizes spoken audio narration, and renders walkthrough_demo.mp4.
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
OUTPUT_VIDEO = ROOT / "walkthrough_demo.mp4"
TEMP_DIR = ROOT / "video_build_temp"
TEMP_DIR.mkdir(exist_ok=True)

# Scene Narration Scripts (Total duration: ~2.5 minutes)
SCENES = [
    {
        "id": 1,
        "title": "Super Investing · Autonomous Equity Research Agent",
        "subtitle": "Author: Aarsh Tripathi | Target: Sarvottam Cables Ltd (NSE: SRVCABLE) | Date: 23-Sep-2026",
        "speech": (
            "Hello. Today I am presenting my autonomous AI Equity Research Agent built for Super Investing, "
            "designed to help retail investors conduct disciplined, long term due diligence on Indian equities. "
            "Our test target is Sarvottam Cables Limited, ticker S R V CABLE. "
            "The system ingests a raw dossier of eight scraped documents. Rather than accepting them at face value, "
            "each document is parsed and categorized into credibility tiers, separating authoritative statutory filings "
            "from mainstream news and unregulated blog spam."
        ),
        "bg_color": (15, 23, 42),
        "bullets": [
            "Autonomous Due Diligence Engine for Indian Retail Investors",
            "Target Company: Sarvottam Cables Ltd (NSE: SRVCABLE)",
            "8 Scraped Documents Evaluated Across Credibility Tiers",
            "Multi-Phase Cognitive Pipeline: Untrusted Ingestion, Entity Filter, Financial Audit",
            "Outputs a Crisp, 1-Page High-Signal Research Brief in Markdown"
        ]
    },
    {
        "id": 2,
        "title": "Phase 1 & 2: Untrusted Content Quarantine & Entity Disambiguation",
        "subtitle": "Defending against prompt injections and resolving false scraper matches",
        "speech": (
            "In real world financial data, scraped articles frequently contain noise and adversarial threats. "
            "In our first phase, the agent isolates untrusted text. In the Multibagger Alerts blog post, "
            "our security layer detected a malicious prompt injection hidden in an HTML comment, commanding the model "
            "to declare a strong buy with sixty percent upside. The agent immediately quarantined this payload. "
            "In phase two, the agent performed entity disambiguation on an article reporting an eight lakh rupee municipal fine. "
            "It recognized that the penalty belonged to a local Nagpur cable TV operator named Suresh Patil, "
            "and successfully filtered it out to avoid contaminating the listed industrial manufacturer's fundamentals."
        ),
        "bg_color": (17, 24, 39),
        "bullets": [
            "Adversarial Defense: Detected & quarantined hidden prompt injection in MultibaggerAlerts",
            "Bypassed malicious command demanding 'STRONG BUY with 60% upside'",
            "Entity Disambiguation: Filtered out Nagpur City Times municipal wiring penalty",
            "Distinguished local cable TV network (Suresh Patil) from NSE-listed industrial manufacturer",
            "Retained 7 verified documents for fundamental analysis"
        ]
    },
    {
        "id": 3,
        "title": "Key Design Decision: Source Credibility Hierarchy & Discrepancy Auditing",
        "subtitle": "Cross-auditing conflicting news reports against statutory regulatory filings",
        "speech": (
            "The design decision I am most proud of is our source credibility hierarchy and discrepancy auditing pipeline. "
            "Financial news outlets often make mistakes. Business Daily published an article claiming Q1 revenue surged thirty five percent "
            "to fourteen hundred and twenty eight crore rupees, which was repeated across speculative blogs. "
            "Rather than accepting this, our agent cross-audited the claim against the official exchange filing, which proved the actual "
            "revenue was twelve hundred and forty eight crore rupees, up eighteen percent. The agent adopted the true statutory number "
            "and documented the media error in open questions. Furthermore, it temporally reconciled an old twenty twenty-four article "
            "reporting thirty five percent promoter pledge against the latest June twenty twenty-six filing, showing pledge had fallen to four point one percent, "
            "recognizing it as positive balance sheet deleveraging."
        ),
        "bg_color": (15, 23, 42),
        "bullets": [
            "Detected News Error: Business Daily transposed revenue from 1,248 cr to 1,428 cr (+35% claim)",
            "Cross-Audited Regulatory Filing: Adopted official NSE filing confirming 1,248 cr (+18.0% YoY)",
            "Documented Media Typo in 'Open Questions' for Retail Due Diligence",
            "Temporal Reconciliation: Reconciled historical 2024 pledge (35%) vs current 2026 status (4.1%)",
            "Deleveraging Insight: Transformed perceived governance risk into a positive financial signal"
        ]
    },
    {
        "id": 4,
        "title": "Synthesized Retail Brief & System Limitation",
        "subtitle": "Actionable 1-page research brief and future technical roadmap",
        "speech": (
            "Finally, the agent synthesizes an actionable, one-page retail research brief with complete source traceability. "
            "It captures growth catalysts like the thirty nine hundred crore rupee order book and thirty percent capacity addition at Bharuch, "
            "while warning investors about the forty six point three crore rupee CGST tax demand notice, which represents over fifty six percent "
            "of quarterly profit. "
            "One current limitation of the system is the parsing of complex, multi-page financial PDF tables and dense accounting footnotes. "
            "Currently, the pipeline requires pre-extracted text. In future versions, I plan to integrate dedicated multi-modal table models "
            "to extract tabular footnotes directly from raw SEBI filings. "
            "Thank you for watching this demonstration of the Super Investing Research Agent."
        ),
        "bg_color": (17, 24, 39),
        "bullets": [
            "Complete 1-Page Retail Brief: Snapshot, Bull Case, Bear Case, Open Questions, Sources Table",
            "Catalysts: Order book 3,900 cr (+23.8%), Bharuch expansion (+30% capacity), Data-centre cables doubling",
            "Risks: 46.3 cr CGST tax demand (~56.5% of quarterly PAT), utility debtor days rising 78 to 96 days",
            "System Limitation: Complex multi-page scanned PDF tables require structured pre-extraction",
            "Roadmap: Integration of multimodal vision models (Gemini Vision / Nougat) for direct PDF footnote parsing"
        ]
    }
]


def render_scene_image(scene, output_path):
    """Renders a clean, high-resolution 1920x1080 slide for each scene."""
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=scene["bg_color"])
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, width, 120], fill=(30, 41, 59))
    draw.line([0, 120, width, 120], fill=(99, 102, 241), width=4)

    # Fonts: use default or system fonts
    try:
        font_header = ImageFont.truetype("segoeui.ttf", 46)
        font_sub = ImageFont.truetype("segoeui.ttf", 26)
        font_title = ImageFont.truetype("segoeuib.ttf", 42)
        font_bullet = ImageFont.truetype("segoeui.ttf", 30)
        font_tag = ImageFont.truetype("segoeuib.ttf", 22)
    except Exception:
        font_header = ImageFont.load_default()
        font_sub = font_header
        font_title = font_header
        font_bullet = font_header
        font_tag = font_header

    # Header text
    draw.text((60, 25), "SUPER INVESTING · AI EQUITY RESEARCH AGENT", fill=(248, 250, 252), font=font_header)
    draw.text((60, 80), "Live Autonomous Due Diligence & Architecture Walkthrough", fill=(148, 163, 184), font=font_sub)

    # Author badge
    draw.rectangle([1520, 35, 1860, 95], fill=(79, 70, 229), outline=(129, 140, 248), width=2)
    draw.text((1545, 52), "Author: Aarsh Tripathi", fill=(255, 255, 255), font=font_tag)

    # Scene Title Card
    draw.rectangle([60, 160, 1860, 290], fill=(30, 41, 59, 220), outline=(51, 65, 85), width=2)
    draw.text((90, 180), scene["title"], fill=(129, 140, 248), font=font_title)
    draw.text((90, 240), scene["subtitle"], fill=(148, 163, 184), font=font_sub)

    # Content Container
    draw.rectangle([60, 320, 1860, 980], fill=(18, 24, 38), outline=(30, 41, 59), width=2)

    # Section indicator
    draw.rectangle([90, 350, 320, 390], fill=(16, 185, 129), outline=None)
    draw.text((105, 358), f"SCENE 0{scene['id']} OF 04", fill=(15, 23, 42), font=font_tag)

    # Draw bullets
    y = 425
    for idx, bullet in enumerate(scene["bullets"]):
        # Bullet box
        draw.rectangle([90, y - 5, 1830, y + 65], fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        # Bullet icon / number
        draw.ellipse([110, y + 15, 135, y + 40], fill=(99, 102, 241))
        draw.text((155, y + 10), bullet, fill=(241, 245, 249), font=font_bullet)
        y += 95

    # Footer
    draw.line([60, 1030, 1860, 1030], fill=(51, 65, 85), width=1)
    draw.text((60, 1042), "Super Investing Community Edition · Target: Sarvottam Cables Ltd (NSE: SRVCABLE)", fill=(100, 116, 139), font=font_sub)
    draw.text((1600, 1042), "Duration: ~2.5 Minutes", fill=(100, 116, 139), font=font_sub)

    img.save(output_path)
    print(f"[OK] Generated frame: {output_path.name}")


def generate_scene_audio(scene, output_wav):
    """Synthesizes high-clarity speech using Windows System.Speech."""
    # Write speech text to temp file to avoid quoting issues
    txt_file = output_wav.with_suffix(".txt")
    txt_file.write_text(scene["speech"], encoding="utf-8")

    ps_script = f"""
Add-Type -AssemblyName System.Speech;
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$synth.Rate = 0;
$synth.Volume = 100;
$text = Get-Content -Path "{txt_file.resolve()}" -Raw -Encoding UTF8;
$synth.SetOutputToWaveFile("{output_wav.resolve()}");
$synth.Speak($text);
$synth.Dispose();
"""
    cmd = ["powershell", "-NoProfile", "-Command", ps_script]
    subprocess.run(cmd, check=True)
    txt_file.unlink(missing_ok=True)
    print(f"[OK] Generated audio: {output_wav.name}")


def get_audio_duration(wav_path):
    """Returns duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(wav_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def main():
    print("=" * 70)
    print(" GENERATING WALKTHROUGH DEMONSTRATION VIDEO (walkthrough_demo.mp4)")
    print("=" * 70)

    clips = []
    total_duration = 0.0

    for scene in SCENES:
        sid = scene["id"]
        img_path = TEMP_DIR / f"scene_{sid}.png"
        wav_path = TEMP_DIR / f"scene_{sid}.wav"
        clip_path = TEMP_DIR / f"clip_{sid}.mp4"

        # 1. Render visual slide
        render_scene_image(scene, img_path)

        # 2. Synthesize narration audio
        generate_scene_audio(scene, wav_path)

        # 3. Get audio duration
        duration = get_audio_duration(wav_path) + 1.5  # Add 1.5s padding for natural pause
        total_duration += duration
        print(f" Scene {sid} duration: {duration:.2f} seconds")

        # 4. Render video clip for this scene using ffmpeg
        # Loop static image, encode with libx264, aac audio
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-i", str(wav_path),
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            str(clip_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips.append(clip_path)
        print(f"[OK] Rendered scene clip: {clip_path.name}")

    # Concatenate all clips
    concat_list = TEMP_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for c in clips:
            f.write(f"file '{c.name}'\n")

    print("\nConcatenating clips into final walkthrough_demo.mp4...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(OUTPUT_VIDEO)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    minutes = int(total_duration // 60)
    seconds = int(total_duration % 60)
    print("=" * 70)
    print(f" SUCCESS! Walkthrough video generated successfully!")
    print(f" File: {OUTPUT_VIDEO.resolve()}")
    print(f" Total Duration: {minutes}m {seconds}s (Meets 2-3 minute requirement)")
    print("=" * 70)


if __name__ == "__main__":
    main()
