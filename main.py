#!/usr/bin/env python3
"""Media Downloader & Converter - by MOHAMED HB"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

AUTHOR = "MOHAMED HB"
PROFILE = "https://github.com/medelhabib213"
VERSION = "1.0.0"

# ---------------------------------------------------------------- Banner
GLYPHS = {
    "M": [r" __  __ ", r"|  \/  |", r"| |\/| |", r"| |  | |", r"|_|  |_|"],
    "O": [r"  ___  ", r" / _ \ ", r"| | | |", r"| |_| |", r" \___/ "],
    "H": [r" _   _ ", r"| | | |", r"| |_| |", r"|  _  |", r"|_| |_|"],
    "A": [r"    _    ", r"   / \   ", r"  / _ \  ", r" / ___ \ ", "/_/   \\_\\"],
    "E": [r" _____ ", r"| ____|", r"|  _|  ", r"| |___ ", r"|_____|"],
    "D": [r" ____  ", r"|  _ \ ", r"| | | |", r"| |_| |", r"|____/ "],
    "B": [r" ____  ", r"| __ ) ", r"|  _ \ ", r"| |_) |", r"|____/ "],
    " ": ["   "] * 5,
}


def build_banner(text: str) -> str:
    rows = [""] * 5
    for ch in text:
        glyph = GLYPHS[ch]
        width = max(len(line) for line in glyph)
        for i in range(5):
            rows[i] += glyph[i].ljust(width)
    return "\n".join(rows)


def print_banner() -> None:
    cyan, green, dim, reset = "\033[96m", "\033[92m", "\033[2m", "\033[0m"
    print(cyan + build_banner(AUTHOR) + reset)
    print(f"{green}  Media Downloader & Converter  v{VERSION}{reset}")
    print(f"{dim}  Author : {AUTHOR}")
    print(f"  Profile: {PROFILE}{reset}\n")


# ---------------------------------------------------------------- Helpers
def check_ffmpeg() -> bool:
    if shutil.which("ffmpeg") is None:
        print("[!] ffmpeg غير مثبت. ثبّته أولاً: https://ffmpeg.org/download.html")
        return False
    return True


def ask(prompt: str, default: str = "") -> str:
    value = input(f"{prompt}" + (f" [{default}]" if default else "") + ": ").strip()
    return value or default


# ---------------------------------------------------------------- Download
def download(url: str, out_dir: Path, audio_only: bool = False,
             audio_fmt: str = "mp3", max_height: int = 1080,
             playlist: bool = False) -> None:
    try:
        import yt_dlp
    except ImportError:
        sys.exit("[!] ثبّت المتطلبات أولاً: pip install -r requirements.txt")

    out_dir.mkdir(parents=True, exist_ok=True)
    opts = {
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "noplaylist": not playlist,
        "restrictfilenames": False,
    }
    if audio_only:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": audio_fmt,
            "preferredquality": "192",
        }]
    else:
        opts["format"] = (f"bestvideo[height<={max_height}]+bestaudio/"
                          f"best[height<={max_height}]/best")
        opts["merge_output_format"] = "mp4"

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    print(f"\n[✓] تم الحفظ في: {out_dir.resolve()}")


# ---------------------------------------------------------------- Convert
def convert(src: Path, target_fmt: str, out_dir: Path) -> None:
    if not src.is_file():
        print(f"[!] الملف غير موجود: {src}")
        return
    if not check_ffmpeg():
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / f"{src.stem}.{target_fmt.lstrip('.')}"
    cmd = ["ffmpeg", "-y", "-i", str(src), str(dst)]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"[✓] تم التحويل: {dst}")
    else:
        print("[!] فشل التحويل.")


# ---------------------------------------------------------------- Menu
def interactive_menu(out_dir: Path) -> None:
    menu = (
        "1) تنزيل فيديو\n"
        "2) تنزيل صوت فقط\n"
        "3) تحويل ملف محلي\n"
        "4) خروج\n"
    )
    while True:
        print(menu)
        choice = ask("اختر رقماً")
        try:
            if choice == "1":
                url = ask("الرابط")
                height = int(ask("أقصى جودة (ارتفاع)", "1080"))
                download(url, out_dir, max_height=height)
            elif choice == "2":
                url = ask("الرابط")
                fmt = ask("الصيغة (mp3/m4a/wav/opus)", "mp3")
                download(url, out_dir, audio_only=True, audio_fmt=fmt)
            elif choice == "3":
                src = Path(ask("مسار الملف"))
                fmt = ask("الصيغة الهدف (mp4/mp3/mkv/wav/gif...)", "mp4")
                convert(src, fmt, out_dir)
            elif choice == "4":
                print("إلى اللقاء!")
                return
            else:
                print("[!] خيار غير صالح.")
        except KeyboardInterrupt:
            print("\n[!] تم الإلغاء.")
        except Exception as exc:  # noqa: BLE001
            print(f"[!] خطأ: {exc}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Media Downloader & Converter")
    parser.add_argument("-u", "--url", help="رابط للتنزيل")
    parser.add_argument("-a", "--audio", action="store_true", help="صوت فقط")
    parser.add_argument("-c", "--convert", help="ملف محلي للتحويل")
    parser.add_argument("-f", "--format", default=None, help="الصيغة الهدف")
    parser.add_argument("-q", "--quality", type=int, default=1080, help="أقصى ارتفاع للفيديو")
    parser.add_argument("--playlist", action="store_true", help="تنزيل قائمة التشغيل كاملة")
    parser.add_argument("-o", "--output", default="downloads", help="مجلد الحفظ")
    args = parser.parse_args()

    print_banner()
    out_dir = Path(args.output)

    if args.url:
        download(args.url, out_dir, audio_only=args.audio,
                 audio_fmt=args.format or "mp3",
                 max_height=args.quality, playlist=args.playlist)
    elif args.convert:
        convert(Path(args.convert), args.format or "mp4", out_dir)
    else:
        interactive_menu(out_dir)


if __name__ == "__main__":
    main()
