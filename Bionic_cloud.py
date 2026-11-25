#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Kakinmeter reader — writes Bionic+ weekly cloud credit status to a plain
ASCII key=value file for the Rainmeter skin.

Data source : %USERPROFILE%\.lmstudio\apps\bionic\.internal\cloud-account.json
Output      : cloud_status.txt next to this script (override: argv[2])
Output is 100% ASCII to avoid any encoding issues with Rainmeter.

Weekly reset time is taken from the file's `resetsAtIso` (UTC) and shown in
the *local* timezone. If the value is missing or in the past, the fallback
assumes the observed schedule: every Monday 00:00 UTC.
"""
import os, json, sys, datetime

DEFAULT_JSON = os.path.expandvars(r"%USERPROFILE%\.lmstudio\apps\bionic\.internal\cloud-account.json")
DEFAULT_OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cloud_status.txt")

UTC = datetime.timezone.utc

def next_monday_utc(now_utc):
    """Observed reset schedule: every Monday 00:00 UTC."""
    days_ahead = (0 - now_utc.weekday()) % 7  # Monday == 0
    target = now_utc.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=days_ahead)
    if target <= now_utc:
        target += datetime.timedelta(days=7)
    return target

def extract(jpath):
    remaining = limit = pct = 0
    reset_iso = None
    try:
        with open(jpath, encoding="utf-8") as f:
            d = json.load(f)
        payload = d.get("payload", {}) or {}
        for lim in payload.get("limits", []) or []:
            w = lim.get("weekly", {}) or {}
            remaining = int(w.get("remainingMicrocredits", "0"))
            limit = int(w.get("limitMicrocredits", "0"))
            reset_iso = w.get("resetsAtIso")
            break
        if limit:
            pct = round(remaining / limit * 100, 2)
    except Exception as e:
        print("ERROR: %s" % e, file=sys.stderr)

    now_local = datetime.datetime.now().astimezone()

    target_local = None
    if reset_iso:
        try:
            dt_utc = datetime.datetime.fromisoformat(reset_iso.replace("Z", "+00:00"))
            if dt_utc > datetime.datetime.now(UTC):
                target_local = dt_utc.astimezone()
        except Exception:
            pass

    # Fallback (value missing or already past): next Monday 00:00 UTC
    if target_local is None:
        now_utc = datetime.datetime.now(UTC)
        target_local = next_monday_utc(now_utc).astimezone()

    delta = target_local - now_local
    total_sec = max(0, int(delta.total_seconds()))
    r_day  = total_sec // 86400
    r_hour = (total_sec % 86400) // 3600
    r_min  = (total_sec % 3600) // 60
    reset_str = target_local.strftime("%Y-%m-%d %H:%M")

    return remaining, limit, pct, reset_str, r_day, r_hour, r_min

def main():
    jpath = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JSON
    out   = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT
    remaining, limit, pct, reset_str, r_day, r_hour, r_min = extract(jpath)

    with open(out, "w", encoding="utf-8") as f:
        f.write("title=Bionic Cloud Credits\n")
        f.write("plan=Bionic+\n")
        f.write("pct=%s\n" % pct)
        f.write("rem=%s\n" % remaining)
        f.write("limit=%s\n" % limit)
        f.write("reset=%s\n" % reset_str)
        f.write("r_day=%s\n" % r_day)
        f.write("r_hour=%s\n" % r_hour)
        f.write("r_min=%s\n" % r_min)

if __name__ == "__main__":
    main()
