# Kakinmeter — Bionic+ weekly usage widget for Rainmeter

A desktop widget (Rainmeter skin) that shows your **Bionic+ weekly cloud credit
usage**: remaining / limit, a usage bar, and a countdown to the weekly reset —
without opening the app.

Data is read from Bionic's local account cache:

```
%USERPROFILE%\.lmstudio\apps\bionic\.internal\cloud-account.json
```

> ⚠️ That file also contains account-secret material (`ownerKey`). This widget
> reads **only** the usage fields and never displays or logs anything else.
> Treat the file as user-private; do not share it.

## Contents

| File | Role |
| --- | --- |
| `Bionic_cloud.py` | Reads the JSON above, writes `cloud_status.txt` (ASCII `key=value`) next to itself |
| `Kakinmeter.ini` | The Rainmeter skin |
| `cloud_status.txt` | Generated output (auto-created on first run) |

## Setup

1. Install [Rainmeter](https://www.rainmeter.net/) and copy this folder into
   `%USERPROFILE%\AppData\Roaming\Rainmeter\Skins\` (or your custom skins
   folder).
2. Schedule `Bionic_cloud.py` to run periodically with **pythonw.exe** (no
   console window), e.g. every 1 minute via Task Scheduler:
   - Program: `<your python dir>\pythonw.exe`
   - Arguments: `"%USERPROFILE%\AppData\Roaming\Rainmeter\Skins\Kakinmeter\Bionic_cloud.py"`
   - Trigger: at log on, repeat every 1 minute, indefinitely.
   - Or any scheduler you prefer — the script only writes a small text file.
3. In Rainmeter: tray icon → **Refresh all** → load skin
   `Kakinmeter\Kakinmeter`.

### Paths

- The script writes `cloud_status.txt` **next to itself** by default. If you
  keep the skin folder elsewhere, pass the output path as the 2nd argument:
  `pythonw.exe Bionic_cloud.py "<account.json path>" "<cloud_status.txt path>"`.
- The `STATUS_FILE` variable in `Kakinmeter.ini` points to the file inside the
  skin folder (`#CURRENTPATH#`), so the defaults line up when the folder is
  installed as a skin.

## Time zone behavior

The reset timestamp shown on the widget is rendered in **your local time
zone** (parsed from Bionic's `resetsAtIso` UTC value). If the value is ever
missing or already past, the script falls back to the observed schedule:
**every Monday 00:00 UTC**. No region is hardcoded.

## Bar colors

- Purple: normal
- Red: remaining ≤ 20%

## Encoding notes

- The `Kakinmeter.ini` in this repo is plain ASCII (English UI) — Rainmeter
  reads ANSI/ASCII `.ini` files directly. If you customize it with non-ASCII
  text, resave it as **UTF-16LE with BOM and CRLF**.
- `cloud_status.txt` output is 100% ASCII.

## License

Personal use. Provided as-is, no warranty.

© oyasuminet + Bionic Local-LLM agents + GoogleSearch_AI
