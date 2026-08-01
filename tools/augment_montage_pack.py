#!/usr/bin/env python3
"""Augment the base Kenney SFX build with verified CC0 packs and rebuild navigation."""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import urllib.parse
import zipfile
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path.cwd()
WORK = ROOT / "_work"
PACK = WORK / "МОНТАЖНЫЙ_SFX_ПАК_RU"
AUDIO = PACK / "01_ЗВУКИ_WAV"
CATALOG = PACK / "02_КАТАЛОГ_И_ПОИСК"
PLAYLISTS = PACK / "03_БЫСТРЫЕ_ПОДБОРКИ"
LICENSES = PACK / "04_ИСТОЧНИКИ_И_ЛИЦЕНЗИИ"
LISTING = PACK / "05_ОФОРМЛЕНИЕ_PLAYEROK"
DOWNLOADS = WORK / "extra_downloads"
EXTRACT = WORK / "extra_extract"
TEMP = WORK / "extra_wav"
OUT = ROOT / "dist"
UA = {"User-Agent": "Mozilla/5.0 MontagePackBuilder/2.0"}
AUDIO_EXT = {".wav", ".ogg", ".mp3", ".flac", ".aif", ".aiff", ".m4a"}

CATEGORIES = [
    "01_ПЕРЕХОДЫ_ВУШИ_СВИПЫ",
    "02_УДАРЫ_ИМПАКТЫ",
    "03_КЛИКИ_ИНТЕРФЕЙС_UI",
    "04_КАМЕРА_ФОТО_МЕХАНИЗМЫ",
    "05_ГЛИТЧ_ЦИФРА_ТЕХНО",
    "06_SCI_FI_ТЕХНОЛОГИИ",
    "07_ИГРОВЫЕ_БОЕВЫЕ",
    "08_FOLEY_ПРЕДМЕТЫ_ШАГИ",
    "09_РЕТРО_АРКАДА",
    "10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ",
    "11_КАЗИНО_НАГРАДЫ",
    "12_АТМОСФЕРА_ВОДА_ОКРУЖЕНИЕ",
    "13_ХОРРОР_ДЖАМПСКЕЙРЫ",
    "14_ДЖИНГЛЫ_МУЗЫКАЛЬНЫЕ_ЗАСТАВКИ",
    "15_РАЗНОЕ",
]

# title, source page, direct archive or None (discover on Kenney), default category, source kind
SOURCES = [
    (
        "Owlish Media Sound Effects",
        "https://opengameart.org/content/sound-effects-pack",
        "https://opengameart.org/sites/default/files/Owlish%20Media%20Sound%20Effects.zip",
        "08_FOLEY_ПРЕДМЕТЫ_ШАГИ",
        "OpenGameArt",
    ),
    (
        "Swishes Sound Pack",
        "https://opengameart.org/content/swishes-sound-pack",
        "https://opengameart.org/sites/default/files/swishes.zip",
        "01_ПЕРЕХОДЫ_ВУШИ_СВИПЫ",
        "OpenGameArt",
    ),
    (
        "Sound Effects Pack 2",
        "https://opengameart.org/content/sound-effects-pack-2",
        "https://opengameart.org/sites/default/files/Sound%20effects%20Pack%202.zip",
        "09_РЕТРО_АРКАДА",
        "OpenGameArt",
    ),
    (
        "RPG Sound Pack",
        "https://opengameart.org/content/rpg-sound-pack",
        "https://opengameart.org/sites/default/files/rpg_sound_pack.zip",
        "07_ИГРОВЫЕ_БОЕВЫЕ",
        "OpenGameArt",
    ),
    (
        "Horror Hit Soundpack 1",
        "https://opengameart.org/content/horror-hit-soundpack-1",
        "https://opengameart.org/sites/default/files/horror_hit_soundpack_1.zip",
        "13_ХОРРОР_ДЖАМПСКЕЙРЫ",
        "OpenGameArt",
    ),
    (
        "Kenney Voiceover Pack",
        "https://kenney.nl/assets/voiceover-pack",
        None,
        "10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ",
        "Kenney",
    ),
    (
        "Kenney Music Jingles",
        "https://kenney.nl/assets/music-jingles",
        None,
        "14_ДЖИНГЛЫ_МУЗЫКАЛЬНЫЕ_ЗАСТАВКИ",
        "Kenney",
    ),
]


def run(args: list[str], capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        check=False,
    )


def clean(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-zА-Яа-яЁё_-]+", "_", value.replace(" ", "_"))
    return re.sub(r"_+", "_", value).strip("_")[:100] or "sound"


def discover_kenney_zip(page: str) -> str:
    response = requests.get(page, headers=UA, timeout=60)
    response.raise_for_status()
    text = response.text
    soup = BeautifulSoup(text, "html.parser")
    candidates: list[str] = []
    for tag in soup.find_all(True):
        for value in tag.attrs.values():
            values = value if isinstance(value, list) else [value]
            for item in values:
                if isinstance(item, str) and ".zip" in item.lower():
                    candidates.append(urllib.parse.urljoin(page, html.unescape(item).replace("\\/", "/")))
    for pattern in (
        r'https?://[^"\'<>\s]+?\.zip(?:\?[^"\'<>\s]*)?',
        r'/media/pages/assets/[^"\'<>\s]+?\.zip(?:\?[^"\'<>\s]*)?',
    ):
        candidates.extend(urllib.parse.urljoin(page, item) for item in re.findall(pattern, text, re.I))
    for candidate in sorted(set(candidates), key=lambda x: (0 if "kenney.nl/media/" in x else 1, len(x))):
        try:
            probe = requests.get(candidate, headers=UA, timeout=90, stream=True)
            first = next(probe.iter_content(8), b"")
            if probe.ok and (first.startswith(b"PK") or "zip" in probe.headers.get("content-type", "").lower()):
                return probe.url
        except requests.RequestException:
            continue
    raise RuntimeError("прямая ZIP-ссылка не найдена")


def download(url: str, destination: Path) -> None:
    with requests.get(url, headers=UA, timeout=300, stream=True) as response:
        response.raise_for_status()
        with destination.open("wb") as output:
            for chunk in response.iter_content(1024 * 1024):
                if chunk:
                    output.write(chunk)
    if destination.stat().st_size < 100:
        raise RuntimeError("пустой архив")


def safe_extract(archive: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            resolved = (target / member.filename).resolve()
            if target.resolve() not in resolved.parents and resolved != target.resolve():
                raise RuntimeError("опасный путь внутри ZIP")
        zf.extractall(target)


def choose_audio(root: Path) -> list[Path]:
    priority = {".wav": 0, ".flac": 1, ".aiff": 2, ".aif": 2, ".ogg": 3, ".mp3": 4, ".m4a": 5}
    groups: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in AUDIO_EXT:
            key = str(path.relative_to(root).with_suffix("")).lower()
            groups.setdefault(key, []).append(path)
    return [sorted(group, key=lambda p: priority.get(p.suffix.lower(), 9))[0] for group in groups.values()]


def duration(path: Path) -> float:
    result = run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        capture=True,
    )
    try:
        return float(result.stdout.strip())
    except (TypeError, ValueError):
        return 0.0


def convert_wav(source: Path, destination: Path) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    result = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-vn",
            "-ar",
            "48000",
            "-c:a",
            "pcm_s16le",
            str(destination),
        ],
        capture=True,
    )
    return result.returncode == 0 and destination.exists() and destination.stat().st_size > 100


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def category(default: str, value: str) -> str:
    text = value.lower().replace("\\", "/")
    rules = [
        ("13_ХОРРОР_ДЖАМПСКЕЙРЫ", ["horror", "scary", "jumpscare", "terror", "scream"]),
        ("14_ДЖИНГЛЫ_МУЗЫКАЛЬНЫЕ_ЗАСТАВКИ", ["jingle", "music", "intro", "outro", "fanfare"]),
        ("01_ПЕРЕХОДЫ_ВУШИ_СВИПЫ", ["whoosh", "woosh", "swoosh", "swish", "sweep", "swipe", "transition", "flyby", "passby", "riser"]),
        ("04_КАМЕРА_ФОТО_МЕХАНИЗМЫ", ["camera", "shutter", "photo", "mechanic", "machine", "gear", "lever", "clock", "typewriter"]),
        ("02_УДАРЫ_ИМПАКТЫ", ["impact", "hit", "slam", "thud", "punch", "kick", "crash", "break", "explosion", "boom", "smash"]),
        ("03_КЛИКИ_ИНТЕРФЕЙС_UI", ["interface", "ui/", "click", "button", "tap", "select", "confirm", "cancel", "toggle", "menu", "notification", "rollover"]),
        ("12_АТМОСФЕРА_ВОДА_ОКРУЖЕНИЕ", ["ambient", "ambience", "atmos", "water", "rain", "wind", "river", "ocean", "roomtone"]),
        ("08_FOLEY_ПРЕДМЕТЫ_ШАГИ", ["foley", "foot", "step", "door", "paper", "cloth", "fabric", "wood", "metal", "glass", "ceramic", "stone", "drop", "rustle"]),
        ("10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ", ["voice", "human", "breath", "laugh", "cough", "synth", "robot", "speech", "alarm", "signal", "beep"]),
        ("11_КАЗИНО_НАГРАДЫ", ["coin", "card", "dice", "chip", "casino", "win", "jackpot", "reward", "1up", "powerup", "power-up"]),
        ("05_ГЛИТЧ_ЦИФРА_ТЕХНО", ["glitch", "digital", "computer", "technology", "teleport", "error"]),
        ("06_SCI_FI_ТЕХНОЛОГИИ", ["sci-fi", "scifi", "laser", "space", "engine", "energy"]),
        ("09_РЕТРО_АРКАДА", ["retro", "8-bit", "8bit", "arcade", "blip", "jump", "lose"]),
        ("07_ИГРОВЫЕ_БОЕВЫЕ", ["rpg", "battle", "weapon", "sword", "spell", "monster", "beast", "ogre", "slime", "shoot"]),
    ]
    for result, words in rules:
        if any(word in text for word in words):
            return result
    return default if default in CATEGORIES else "15_РАЗНОЕ"


def load_existing() -> tuple[list[dict[str, str]], set[str]]:
    csv_path = CATALOG / "СПИСОК_ВСЕХ_ЗВУКОВ.csv"
    rows: list[dict[str, str]] = []
    if csv_path.exists():
        with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
    hashes = {sha256(path) for path in AUDIO.rglob("*.wav")}
    return rows, hashes


def rebuild_navigation(rows: list[dict[str, str]], source_records: list[dict[str, str]]) -> None:
    rows.sort(key=lambda row: (CATEGORIES.index(row["Категория"]) if row["Категория"] in CATEGORIES else 999, row["Название"].lower()))
    for index, row in enumerate(rows, 1):
        row["№"] = str(index)

    for category_name in CATEGORIES:
        folder = AUDIO / category_name
        folder.mkdir(parents=True, exist_ok=True)
        if not any(folder.iterdir()):
            folder.rmdir()

    with (CATALOG / "СПИСОК_ВСЕХ_ЗВУКОВ.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["№", "Категория", "Название", "Длительность", "Источник", "Путь"])
        writer.writeheader()
        writer.writerows(rows)

    data = [
        {
            "c": row["Категория"],
            "n": row["Название"],
            "d": row["Длительность"],
            "s": row["Источник"],
            "u": urllib.parse.quote("../../" + row["Путь"], safe="/._-"),
        }
        for row in rows
    ]
    options = "".join(
        f"<option>{html.escape(category_name)}</option>"
        for category_name in CATEGORIES
        if any(row["Категория"] == category_name for row in rows)
    )
    page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Каталог SFX</title><style>
    *{{box-sizing:border-box}}body{{margin:0;background:#090a0e;color:#fff;font:15px Arial,sans-serif}}header{{position:sticky;top:0;z-index:2;padding:18px 22px;background:#090a0ef4;border-bottom:1px solid #272b35}}h1{{margin:0 0 12px}}input,select{{min-width:260px;padding:12px;margin:4px;background:#151821;color:#fff;border:1px solid #363c49;border-radius:10px}}main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px;padding:20px}}article{{padding:14px;background:#12151c;border:1px solid #292e3a;border-radius:14px}}audio{{width:100%;margin-top:10px}}small{{color:#a9b2c3}}#count{{margin-left:10px;color:#ffc857}}@media(max-width:620px){{input,select{{width:100%;min-width:0}}}}
    </style></head><body><header><h1>Монтажный SFX-пак RU</h1><input id="query" placeholder="Поиск: whoosh, click, horror..."><select id="category"><option value="">Все категории</option>{options}</select><b id="count"></b></header><main id="grid"></main><script>
    const sounds={json.dumps(data, ensure_ascii=False)},grid=document.querySelector('#grid'),query=document.querySelector('#query'),category=document.querySelector('#category'),count=document.querySelector('#count');
    function render(){{const term=query.value.toLowerCase();const visible=sounds.filter(item=>(!category.value||item.c===category.value)&&(!term||(item.n+' '+item.c+' '+item.s).toLowerCase().includes(term)));count.textContent='Найдено: '+visible.length;grid.innerHTML=visible.map(item=>`<article><b>${{item.n}}</b><br><small>${{item.c}} • ${{item.d}} сек. • ${{item.s}}</small><audio controls preload="none" src="${{item.u}}"></audio></article>`).join('')}}
    query.oninput=category.onchange=render;render();</script></body></html>'''
    (CATALOG / "ОТКРЫТЬ_КАТАЛОГ.html").write_text(page, encoding="utf-8")

    sets = {
        "01_SHORTS_REELS": ["01_ПЕРЕХОДЫ_ВУШИ_СВИПЫ", "02_УДАРЫ_ИМПАКТЫ", "03_КЛИКИ_ИНТЕРФЕЙС_UI"],
        "02_ИГРОВАЯ_НАРЕЗКА": ["07_ИГРОВЫЕ_БОЕВЫЕ", "09_РЕТРО_АРКАДА", "11_КАЗИНО_НАГРАДЫ"],
        "03_ТЕХНО_ГЛИТЧ": ["05_ГЛИТЧ_ЦИФРА_ТЕХНО", "06_SCI_FI_ТЕХНОЛОГИИ"],
        "04_МЕМНЫЙ_МОНТАЖ": ["10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ", "11_КАЗИНО_НАГРАДЫ", "09_РЕТРО_АРКАДА"],
        "05_ХОРРОР": ["13_ХОРРОР_ДЖАМПСКЕЙРЫ", "12_АТМОСФЕРА_ВОДА_ОКРУЖЕНИЕ", "02_УДАРЫ_ИМПАКТЫ"],
        "06_СПОКОЙНЫЙ_FOLEY": ["08_FOLEY_ПРЕДМЕТЫ_ШАГИ", "12_АТМОСФЕРА_ВОДА_ОКРУЖЕНИЕ"],
    }
    for playlist_name, category_names in sets.items():
        selected = [row for row in rows if row["Категория"] in category_names][:120]
        (PLAYLISTS / f"{playlist_name}.m3u8").write_text(
            "#EXTM3U\n" + "\n".join("../" + row["Путь"] for row in selected) + "\n",
            encoding="utf-8",
        )

    count = len(rows)
    per_category: dict[str, int] = {}
    for row in rows:
        per_category[row["Категория"]] = per_category.get(row["Категория"], 0) + 1
    category_lines = "\n".join(f"• {name}: {amount}" for name, amount in per_category.items())

    source_text = [
        "ИСТОЧНИКИ И ЛИЦЕНЗИИ",
        "",
        "В пак включены только библиотеки, которые на официальных страницах источников обозначены как Creative Commons CC0 1.0.",
        "CC0: https://creativecommons.org/publicdomain/zero/1.0/",
        "",
    ]
    for record in source_records:
        source_text.extend(
            [
                record["title"],
                f'Площадка: {record["kind"]}',
                f'Страница: {record["page"]}',
                f'Архив: {record["archive"]}',
                f'Добавлено после конвертации и удаления точных дублей: {record["added"]}',
                "Лицензия на странице источника: CC0 1.0",
                "",
            ]
        )
    (LICENSES / "ИСТОЧНИКИ_И_ЛИЦЕНЗИИ.txt").write_text("\n".join(source_text), encoding="utf-8")
    with (LICENSES / "РЕЕСТР_ИСТОЧНИКОВ.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["title", "kind", "page", "archive", "added"])
        writer.writeheader()
        writer.writerows(source_records)

    (PACK / "ОТКРОЙ_МЕНЯ.txt").write_text(
        f'''МОНТАЖНЫЙ SFX-ПАК RU\n\nВнутри: {count} уникальных звуков WAV, приведённых к 48 kHz.\n\n1. Звуки: 01_ЗВУКИ_WAV\n2. Каталог с поиском и прослушиванием: 02_КАТАЛОГ_И_ПОИСК/ОТКРЫТЬ_КАТАЛОГ.html\n3. Быстрые подборки: 03_БЫСТРЫЕ_ПОДБОРКИ\n4. Источники и лицензии: 04_ИСТОЧНИКИ_И_ЛИЦЕНЗИИ\n\nРАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ:\n{category_lines}\n\nНикаких EXE, BAT, установщиков, макросов или взломанных плагинов.\n''',
        encoding="utf-8",
    )
    (LISTING / "НАЗВАНИЕ_ТОВАРА.txt").write_text(
        f"🔥 {count}+ ЗВУКОВ ДЛЯ МОНТАЖА | WAV + РУССКИЙ КАТАЛОГ | АВТОВЫДАЧА\n",
        encoding="utf-8",
    )
    (LISTING / "ОПИСАНИЕ_ТОВАРА.txt").write_text(
        f'''🔥 МОЩНЫЙ SFX-ПАК ДЛЯ МОНТАЖА — {count} УНИКАЛЬНЫХ ЗВУКОВ\n\nНе свалка из случайных файлов: архив приведён к единому WAV 48 kHz, очищен от точных дублей и разложен по понятным русским категориям.\n\nВНУТРИ:\n• {count} готовых звуков WAV;\n• переходы и свипы, импакты, клики, glitch, sci-fi, игровые эффекты, Foley, ретро, голоса, атмосфера, хоррор и джинглы;\n• офлайн HTML-каталог с поиском и прослушиванием;\n• быстрые подборки для Shorts/Reels, игровой нарезки, техно, мемов, хоррора и спокойного Foley;\n• CSV-список, реестр источников и лицензии.\n\nПодходит для CapCut, Premiere Pro, After Effects, DaVinci Resolve, Vegas Pro, Filmora и других редакторов.\n\n✅ Только проверенные CC0-библиотеки с официальных страниц Kenney и OpenGameArt.\n✅ Без EXE, BAT, взломанных плагинов и установщиков.\n⚡ Автовыдача сразу после оплаты.\n\nВажно: это цифровой набор звуков, а не программа или подписка.\n''',
        encoding="utf-8",
    )


def main() -> None:
    if not PACK.exists():
        raise SystemExit("Сначала должен быть собран базовый пакет")
    for folder in (DOWNLOADS, EXTRACT, TEMP):
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
    for category_name in CATEGORIES:
        (AUDIO / category_name).mkdir(parents=True, exist_ok=True)

    rows, seen = load_existing()
    source_records: list[dict[str, str]] = []
    # Preserve already included Kenney records from the base build when possible.
    old_registry = LICENSES / "ИСТОЧНИКИ_И_ЛИЦЕНЗИИ.txt"
    if old_registry.exists():
        old_text = old_registry.read_text(encoding="utf-8", errors="replace")
        pattern = re.compile(
            r"(Kenney [^\n]+)\nСтраница: ([^\n]+)\nАрхив: ([^\n]+)\nДобавлено: (\d+)", re.M
        )
        for title, page, archive, added in pattern.findall(old_text):
            source_records.append({"title": title, "kind": "Kenney", "page": page, "archive": archive, "added": added})

    next_number = max([int(row.get("№", 0) or 0) for row in rows] + [0]) + 1
    failures: list[str] = []
    for source_index, (title, page, archive_url, default_category, kind) in enumerate(SOURCES, 1):
        print(f"\n=== {title} ===", flush=True)
        slug = clean(title).lower()
        try:
            resolved_url = archive_url or discover_kenney_zip(page)
            archive = DOWNLOADS / f"{source_index:02d}_{slug}.zip"
            download(resolved_url, archive)
            extracted = EXTRACT / f"{source_index:02d}_{slug}"
            safe_extract(archive, extracted)

            license_folder = LICENSES / f"extra_{source_index:02d}_{slug}"
            license_folder.mkdir(parents=True, exist_ok=True)
            for candidate in extracted.rglob("*"):
                if (
                    candidate.is_file()
                    and any(key in candidate.name.lower() for key in ("license", "licence", "credit", "readme", "attribution"))
                    and candidate.stat().st_size < 2_000_000
                ):
                    try:
                        shutil.copy2(candidate, license_folder / clean(candidate.name))
                    except OSError:
                        pass

            added = 0
            for audio_index, source in enumerate(choose_audio(extracted), 1):
                seconds = duration(source)
                if seconds <= 0.01 or seconds > 180:
                    continue
                relative = str(source.relative_to(extracted))
                chosen_category = category(default_category, relative)
                temp_wav = TEMP / f"{source_index:02d}_{audio_index:05d}_{clean(source.stem)}.wav"
                if not convert_wav(source, temp_wav):
                    continue
                digest = sha256(temp_wav)
                if digest in seen:
                    temp_wav.unlink(missing_ok=True)
                    continue
                seen.add(digest)
                filename = f"{next_number:04d}_{slug}_{clean(source.stem)}.wav"
                destination = AUDIO / chosen_category / filename
                shutil.move(temp_wav, destination)
                rows.append(
                    {
                        "№": str(next_number),
                        "Категория": chosen_category,
                        "Название": clean(source.stem).replace("_", " "),
                        "Длительность": f"{seconds:.2f}",
                        "Источник": title,
                        "Путь": destination.relative_to(PACK).as_posix(),
                    }
                )
                next_number += 1
                added += 1
            source_records.append(
                {"title": title, "kind": kind, "page": page, "archive": resolved_url, "added": str(added)}
            )
            print(f"Добавлено: {added}", flush=True)
        except Exception as error:  # keep useful pack even if one source temporarily fails
            failures.append(f"{title}: {error}")
            print(f"FAILED: {title}: {error}", flush=True)

    if len(rows) < 800:
        raise SystemExit(f"Сборка недостаточно полная: только {len(rows)} звуков; ошибки: {failures}")

    rebuild_navigation(rows, source_records)
    if failures:
        (LICENSES / "НЕ_ВКЛЮЧЕНО.txt").write_text("\n".join(failures) + "\n", encoding="utf-8")

    archive_base = OUT / "МОНТАЖНЫЙ_SFX_ПАК_RU"
    existing = archive_base.with_suffix(".zip")
    existing.unlink(missing_ok=True)
    shutil.make_archive(str(archive_base), "zip", root_dir=WORK, base_dir=PACK.name)
    print(f"DONE: {len(rows)} WAV; ZIP {existing.stat().st_size / 1024 / 1024:.1f} MB", flush=True)


if __name__ == "__main__":
    main()
