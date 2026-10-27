#!/usr/bin/env python3
"""Draw the last twelve months of contributions in the portfolio's three editions.

almanac.svg is the year as a night sky (coletebou.com), blueprint.svg a plan and profile sheet
(plans.coletebou.com) and shell.svg a terminal session (term.coletebou.com). Standard library only.

    GITHUB_TOKEN=... python3 draw-contributions.py --out assets/contributions
    python3 draw-contributions.py --data calendar.json --out /tmp/editions
"""
import argparse
import datetime as dt
import json
import math
import os
import pathlib
import random
import sys
import urllib.request
from xml.sax.saxutils import escape

LOGIN = "coletebou"
QUERY = """query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar {
  totalContributions weeks { contributionDays { date contributionCount weekday } } } } } }"""
ROMAN = "I II III IV V VI VII VIII IX X XI XII".split()
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
WEEKDAYS = "Sun Mon Tue Wed Thu Fri Sat".split()
GREEK = "αβγ"
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,'Times New Roman',serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
CONDENSED = "'Barlow Condensed','Arial Narrow','Roboto Condensed','Helvetica Neue',Arial,sans-serif"
LETTER = "B612,'Segoe UI','Helvetica Neue',Arial,sans-serif"
DATA = "'B612 Mono','JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
# Every animation keeps the finished drawing as the base style, so a renderer without animation shows it whole.
NO_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def fetch(token):
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    request = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "draw-contributions"})
    with urllib.request.urlopen(request, timeout=60) as response:
        answer = json.load(response)
    if answer.get("errors"):
        sys.exit(f"GitHub GraphQL error: {answer['errors']}")
    return answer


class Day:
    def __init__(self, raw, week):
        self.date = dt.date.fromisoformat(raw["date"])
        self.count = raw["contributionCount"]
        self.level = 0
        self.weekday = raw["weekday"]
        self.week = week


class Year:
    def __init__(self, answer):
        calendar = answer["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        self.total = calendar["totalContributions"]
        self.days = [Day(raw, i) for i, week in enumerate(calendar["weeks"]) for raw in week["contributionDays"]]
        self.weeks = len(calendar["weeks"])
        self.first, self.last = self.days[0].date, self.days[-1].date
        self.max = max(d.count for d in self.days) or 1
        self.active = sum(1 for d in self.days if d.count)
        run = self.longest = 0
        for d in self.days:
            run = run + 1 if d.count else 0
            self.longest = max(self.longest, run)
        # Today may simply not have started yet, so a run that ended yesterday still counts as current.
        tail = self.days[:-1] if not self.days[-1].count else self.days
        self.current = 0
        for d in reversed(tail):
            if not d.count:
                break
            self.current += 1
        self.ranked = sorted((d for d in self.days if d.count), key=lambda d: (-d.count, d.date))
        self.peak = self.ranked[0] if self.ranked else self.days[-1]
        self.per_week = self.total / (len(self.days) / 7)
        # Quartiles of the active days. GitHub's own contributionLevel buckets against the year's maximum,
        # so one very busy month leaves every other day in its first quartile.
        active = sorted(d.count for d in self.days if d.count)
        self.quartiles = [active[len(active) * q // 4] for q in (1, 2, 3)] if active else [0, 0, 0]
        for d in self.days:
            d.level = 0 if not d.count else 1 + sum(d.count > q for q in self.quartiles)

    def brightness(self, day):
        return math.log1p(day.count) / math.log1p(self.max)

    def month_starts(self):
        """(week column, month index) for every month whose first day falls inside the calendar."""
        return [(d.week, d.date.month - 1) for d in self.days if d.date.day == 1]


def moon_phases(first, last):
    """Principal Moon phases between two dates, from Meeus, Astronomical Algorithms ch. 49 (main terms).

    Yields (date, phase) with phase 0 new, 1 first quarter, 2 full, 3 last quarter. Good to well under an hour.
    """
    k = math.floor((first.year + (first.timetuple().tm_yday - 1) / 365.25 - 2000) * 12.3685) - 1
    while True:
        for phase in range(4):
            kk = k + phase / 4
            t = kk / 1236.85
            jde = 2451550.09766 + 29.530588861 * kk + 0.00015437 * t * t
            e = 1 - 0.002516 * t - 0.0000074 * t * t
            m = math.radians(2.5534 + 29.10535670 * kk)
            mp = math.radians(201.5643 + 385.81693528 * kk + 0.0107582 * t * t)
            f = math.radians(160.7108 + 390.67050284 * kk - 0.0016118 * t * t)
            if phase in (0, 2):
                a, b = (-0.40720, 0.17241) if phase == 0 else (-0.40614, 0.17302)
                jde += (a * math.sin(mp) + b * e * math.sin(m) + 0.01608 * math.sin(2 * mp)
                        + 0.01039 * math.sin(2 * f) + 0.00739 * e * math.sin(mp - m) - 0.00514 * e * math.sin(mp + m)
                        + 0.00208 * e * e * math.sin(2 * m) - 0.00111 * math.sin(mp - 2 * f))
            else:
                w = 0.00306 - 0.00038 * e * math.cos(m) + 0.00026 * math.cos(mp)
                jde += (-0.62801 * math.sin(mp) + 0.17172 * e * math.sin(m) - 0.01183 * e * math.sin(mp + m)
                        + 0.00862 * math.sin(2 * mp) + 0.00804 * math.sin(2 * f) + 0.00454 * e * math.sin(mp - m)
                        + 0.00204 * e * e * math.sin(2 * m) - 0.00180 * math.sin(mp - 2 * f)
                        + (w if phase == 1 else -w))
            when = dt.date(1970, 1, 1) + dt.timedelta(days=math.floor(jde - 2440587.5))
            if when > last:
                return
            if when >= first:
                yield when, phase
        k += 1


class Svg:
    def __init__(self, width, height, title, style=""):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
                      f'height="{height}" role="img"><title>{escape(title)}</title>']
        if style:
            self.parts.append(f"<style>{style} {NO_MOTION}</style>")

    def add(self, markup):
        self.parts.append(markup)

    def text(self, x, y, s, size, fill, family, extra=""):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" fill="{fill}" {extra}>'
                 f"{escape(s)}</text>")

    def done(self):
        return "\n".join(self.parts + ["</svg>"]) + "\n"


def stamp(day):
    return f"{day.date.day} {MONTHS[day.date.month - 1]} {day.date.year}"


def almanac(year):
    """The year as a night sky: one star a day, brighter for more work, under the Moon's phases."""
    P = dict(paper="#0b1120", sunk="#080d19", ink="#ede7d8", soft="#c9c2b1", muted="#9c9686", gold="#e6c56d",
             amber="#d6b35c", rule="#ede7d86b")
    W, H, x0, y0, px, py = 1000, 330, 82, 92, 16.3, 17.5
    svg = Svg(W, H, f"{year.total:,} contributions in the last year, drawn as a night sky",
              "@keyframes tw { 50% { opacity: .35; } } .tw { animation: tw 5s ease-in-out infinite; }")
    svg.add(f'<rect width="{W}" height="{H}" fill="{P["paper"]}"/>')
    rnd = random.Random(147)
    for _ in range(90):
        x, y = rnd.uniform(14, W - 14), rnd.uniform(14, H - 14)
        if not (x0 - 30 < x < x0 + year.weeks * px + 12 and 60 < y < 268):
            svg.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.3, 1.1):.2f}" fill="{P["ink"]}" '
                    f'opacity="{rnd.uniform(.12, .5):.2f}"/>')
    svg.add(f'<rect x="9" y="9" width="{W-18}" height="{H-18}" fill="none" stroke="{P["soft"]}" stroke-width="1.2"/>')
    svg.add(f'<rect x="15" y="15" width="{W-30}" height="{H-30}" fill="none" stroke="{P["rule"]}" stroke-width=".6"/>')
    for x, y in ((9, 9), (W - 9, 9), (9, H - 9), (W - 9, H - 9)):
        svg.add(f'<path d="M{x},{y-5} L{x+5},{y} L{x},{y+5} L{x-5},{y} Z" fill="{P["gold"]}"/>')
    svg.add(f'<rect x="{W/2-13}" y="2" width="26" height="18" fill="{P["paper"]}"/>')
    svg.add(f'<path d="M{W/2},2 V20 M{W/2-5.5},7.5 H{W/2+5.5}" stroke="{P["gold"]}" stroke-width="2" stroke-linecap="round"/>')

    span = f"{stamp(year.days[0])} to {stamp(year.days[-1])}".upper()
    svg.text(40, 47, f"EPHEMERIS OF THE YEAR’S WORK · {span}", 11, P["muted"], MONO, 'letter-spacing="1.8"')
    svg.text(W - 40, 48, f"{year.total:,} contributions", 20, P["gold"], SERIF, 'text-anchor="end" font-style="italic"')
    svg.add(f'<line x1="40" y1="60" x2="{W-40}" y2="60" stroke="{P["amber"]}" stroke-width=".8"/>')

    def centre(day):
        jitter = random.Random(day.date.toordinal())
        return (x0 + (day.week + .5) * px + jitter.uniform(-.2, .2) * px,
                y0 + (day.weekday + .5) * py + jitter.uniform(-.2, .2) * py)

    # The Moon's principal phases on their own dates, in a strip above the sky.
    svg.text(x0 - 12, 81, "Moon", 11, P["muted"], SERIF, 'text-anchor="end" font-style="italic"')
    week_of = {d.date: d.week for d in year.days}
    for when, phase in moon_phases(year.first, year.last):
        week = week_of[when]
        cx, cy, r = x0 + (week + .5) * px, 77, 3.6
        if phase == 2:
            svg.add(f'<circle cx="{cx:.1f}" cy="{cy}" r="{r}" fill="{P["ink"]}"/>')
            continue
        svg.add(f'<circle cx="{cx:.1f}" cy="{cy}" r="{r}" fill="{P["sunk"]}" stroke="{P["muted"]}" stroke-width=".8"/>')
        if phase in (1, 3):
            sweep = 1 if phase == 1 else 0
            svg.add(f'<path d="M{cx:.1f},{cy-r} A{r},{r} 0 0 {sweep} {cx:.1f},{cy+r} Z" fill="{P["ink"]}"/>')

    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        svg.text(x0 - 12, y0 + (row + .5) * py + 4, name, 11, P["muted"], SERIF, 'text-anchor="end" font-style="italic"')

    # The year's constellation: each month's brightest day, joined in order.
    brightest = {}
    for d in year.days:
        key = (d.date.year, d.date.month)
        if d.count and (key not in brightest or d.count > brightest[key].count):
            brightest[key] = d
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in (centre(d) for d in sorted(brightest.values(), key=lambda d: d.date)))
    if points:
        svg.add(f'<polyline points="{points}" fill="none" stroke="{P["amber"]}" stroke-width=".7" opacity=".5"/>')

    twinkle = 0
    for d in year.days:
        x, y = centre(d)
        if not d.count:
            svg.add(f'<circle cx="{x0 + (d.week + .5) * px:.1f}" cy="{y0 + (d.weekday + .5) * py:.1f}" r=".55" '
                    f'fill="{P["ink"]}" opacity=".16"/>')
            continue
        b = year.brightness(d)
        r = 1 + 2.5 * b ** 1.2
        colour = P["gold"] if b >= .8 else P["ink"]
        if b >= .8:
            arm = r * 3.4
            svg.add(f'<g class="tw" style="animation-delay:{-(twinkle * 1.7) % 5:.1f}s">'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*2.6:.1f}" fill="{P["gold"]}" opacity=".12"/>'
                    f'<path d="M{x-arm:.1f},{y:.1f} H{x+arm:.1f} M{x:.1f},{y-arm:.1f} V{y+arm:.1f}" '
                    f'stroke="{P["gold"]}" stroke-width=".6" opacity=".85"/></g>')
            twinkle += 1
        svg.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{colour}" opacity="{.4 + .6 * b:.2f}"/>')

    # Bayer letters for the three brightest days, the way a star atlas names its brightest stars.
    placed = []
    for letter, d in zip(GREEK, year.ranked[:3]):
        x, y = centre(d)
        lx, ly = x + 7, y - 6
        if lx > x0 + year.weeks * px - 4:
            lx = x - 7
        if any(abs(lx - px_) < 12 and abs(ly - py_) < 12 for px_, py_ in placed):
            ly += 15
        placed.append((lx, ly))
        anchor = "start" if lx > x else "end"
        svg.text(lx, ly, letter, 12, P["gold"], SERIF, f'font-style="italic" text-anchor="{anchor}"')

    for week, month in year.month_starts():
        svg.text(x0 + (week + .5) * px, y0 + 7 * py + 19, ROMAN[month], 12, P["soft"], SERIF,
                 'text-anchor="middle" letter-spacing=".6"')
    svg.add(f'<line x1="40" y1="246" x2="{W-40}" y2="246" stroke="{P["amber"]}" stroke-width=".8"/>')

    svg.text(40, 270, "MAGNITUDE", 10.5, P["muted"], MONO, 'letter-spacing="1.8"')
    x = 128
    for sample in (1, 10, 100, 1000):
        b = min(1, math.log1p(sample) / math.log1p(year.max))
        svg.add(f'<circle cx="{x}" cy="266" r="{1 + 2.5 * b ** 1.2:.2f}" fill="{P["gold"] if b >= .8 else P["ink"]}" '
                f'opacity="{.4 + .6 * b:.2f}"/>')
        svg.text(x + 8, 270, f"{sample:,}", 10.5, P["muted"], MONO)
        x += 30 + 7 * len(f"{sample:,}")
    peak = year.peak
    alpha = f"α {peak.count:,} ON {stamp(peak).upper()}" if peak.count else "A DARK YEAR"
    svg.text(W - 40, 270, f"{year.active} DAYS LIT · LONGEST RUN {year.longest} DAYS · {alpha}", 10.5, P["muted"],
             MONO, 'text-anchor="end" letter-spacing="1.2"')

    verse = "He telleth the number of the stars; he calleth them all by their names. Psalm 147:4"
    svg.text(W / 2, 303, verse, 15, P["soft"], SERIF,
             'text-anchor="middle" font-style="italic" textLength="520" lengthAdjust="spacing"')
    for side in (-1, 1):
        dx = W / 2 + side * 276
        svg.add(f'<path d="M{dx},295 L{dx+3.5},298.5 L{dx},302 L{dx-3.5},298.5 Z" fill="{P["gold"]}"/>')
    return svg.done()


def blueprint(year):
    """A plan and profile sheet: the days in plan, the running total in profile, on one set of stations."""
    P = dict(desk="#08182d", paper="#123f78", ink="#edf4fd", ink2="#a7bad2", ink3="#4b6e9b", ink4="#2a5387",
             mark="#ffd35c", mark_ink="#1b1400")
    W, H, x0, px = 1000, 420, 84, 13.2
    right = x0 + year.weeks * px
    svg = Svg(W, H, f"{year.total:,} contributions in the last year, drawn as a plan and profile sheet",
              "@keyframes draw { from { stroke-dasharray: 1; stroke-dashoffset: 1; }"
              " to { stroke-dasharray: 1; stroke-dashoffset: 0; } }"
              " .draw { animation: draw 2.6s ease-out .2s backwards; }")
    svg.add(f'<rect width="{W}" height="{H}" fill="{P["desk"]}"/>')
    svg.add(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="{P["paper"]}"/>')
    svg.add("<defs>"
            f'<pattern id="h1" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="5" stroke="{P["ink"]}" stroke-width=".8"/></pattern>'
            f'<pattern id="h2" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<path d="M0,0 V4 M0,0 H4" stroke="{P["ink"]}" stroke-width=".8"/></pattern>'
            f'<pattern id="h3" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<path d="M0,0 V2.6 M0,0 H2.6" stroke="{P["ink"]}" stroke-width=".9"/></pattern>'
            "</defs>")

    # Drawing border with zone marks, numbered right to left and lettered bottom to top like the plan set.
    svg.add(f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{P["ink3"]}" stroke-width=".8"/>')
    svg.add(f'<rect x="26" y="26" width="{W-52}" height="{H-52}" fill="none" stroke="{P["ink"]}" stroke-width="1.4"/>')
    for i in range(8):
        x = 26 + (W - 52) * i / 8
        if i:
            svg.add(f'<path d="M{x:.1f},12 V26 M{x:.1f},{H-26} V{H-12}" stroke="{P["ink3"]}" stroke-width=".8"/>')
        for y in (22.5, H - 15.5):
            svg.text(x + (W - 52) / 16, y, str(8 - i), 9, P["ink2"], DATA, 'text-anchor="middle"')
    for i in range(4):
        y = 26 + (H - 52) * i / 4
        if i:
            svg.add(f'<path d="M12,{y:.1f} H26 M{W-26},{y:.1f} H{W-12}" stroke="{P["ink3"]}" stroke-width=".8"/>')
        for x in (19, W - 19):
            svg.text(x, y + (H - 52) / 8 + 3, "DCBA"[i], 9, P["ink2"], DATA, 'text-anchor="middle"')

    def view_title(x, y, number, name, scale):
        svg.add(f'<circle cx="{x+13}" cy="{y}" r="13" fill="none" stroke="{P["ink"]}" stroke-width="1"/>'
                f'<line x1="{x}" y1="{y}" x2="{x+26}" y2="{y}" stroke="{P["ink"]}" stroke-width=".7"/>')
        svg.text(x + 13, y - 3, number, 9.5, P["ink"], DATA, 'text-anchor="middle"')
        svg.text(x + 13, y + 8.5, "C-102", 5.6, P["ink2"], DATA, 'text-anchor="middle" textLength="19" lengthAdjust="spacingAndGlyphs"')
        svg.text(x + 34, y + 1, name, 17, P["ink"], CONDENSED, 'font-weight="600" letter-spacing="1.2"')
        width = 9.5 * len(name) + 2
        svg.add(f'<line x1="{x+34}" y1="{y+5}" x2="{x+34+width:.0f}" y2="{y+5}" stroke="{P["ink"]}" stroke-width="1.2"/>')
        svg.text(x + 34, y + 17, scale, 8.5, P["ink2"], DATA, 'letter-spacing=".6"')

    # Plan: one cell a day, hatched heavier as the day's count climbs GitHub's quartiles.
    top, py, cell = 58, 13.2, 11
    for week, month in year.month_starts():
        svg.text(x0 + week * px + 1, top - 6, MONTHS[month].upper(), 8.5, P["ink2"], DATA, 'letter-spacing=".6"')
    for row, name in ((1, "MON"), (3, "WED"), (5, "FRI")):
        svg.text(x0 - 8, top + row * py + 8.5, name, 8, P["ink2"], DATA, 'text-anchor="end"')
    marked = {d.date for d in year.ranked[:5]}
    for d in year.days:
        x, y = x0 + d.week * px, top + d.weekday * py
        fill = (P["mark"] if d.date in marked else ("none", "url(#h1)", "url(#h2)", "url(#h3)", P["ink"])[d.level])
        svg.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" fill="{fill}" '
                f'stroke="{P["ink"] if d.level else P["ink3"]}" stroke-width="{.7 if d.level else .5}"/>')
    peak = year.peak
    if peak.count:
        cx, cy = x0 + peak.week * px + cell / 2, top + peak.weekday * py + cell / 2
        ty = top + 7 * py + 17
        left = cx > (x0 + right) / 2
        tx = cx - 14 if left else cx + 14
        svg.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.6" fill="{P["mark_ink"]}"/>'
                f'<path d="M{cx:.1f},{cy:.1f} L{cx:.1f},{ty-3:.1f} L{tx:.1f},{ty-3:.1f}" fill="none" '
                f'stroke="{P["ink"]}" stroke-width=".7"/>')
        svg.text(tx + (-4 if left else 4), ty, f"PEAK DAY: {peak.count:,} EA, {stamp(peak).upper()}", 9, P["ink"], DATA,
                 f'text-anchor="{"end" if left else "start"}" letter-spacing=".5"')
    view_title(x0, top + 7 * py + 30, "1", "PLAN", "DAILY CONTRIBUTIONS · 1 CELL = 1 DAY · HATCH BY QUARTILE")

    # Profile: the running total against a uniform grade, on the plan's own stations.
    ptop, pbot = 222, 330
    step = 10 ** max(0, len(str(max(year.total, 1))) - 1)
    step = max(1, step // 2) if year.total / step < 4 else step
    ceiling = max(step, math.ceil(year.total / step) * step)
    for i in range(0, ceiling + 1, step):
        y = pbot - (pbot - ptop) * i / ceiling
        svg.add(f'<line x1="{x0}" y1="{y:.1f}" x2="{right:.1f}" y2="{y:.1f}" stroke="{P["ink4"] if i else P["ink"]}" '
                f'stroke-width="{.6 if i else 1}"/>')
        svg.text(x0 - 8, y + 3, f"{i:,}", 8, P["ink2"], DATA, 'text-anchor="end"')
    for week in range(0, year.weeks + 1, 4):
        x = x0 + week * px
        svg.add(f'<line x1="{x:.1f}" y1="{ptop}" x2="{x:.1f}" y2="{pbot}" stroke="{P["ink4"]}" stroke-width=".6"/>')
        svg.text(x, pbot + 12, f"{week}+00", 8, P["ink2"], DATA, 'text-anchor="middle"')
    svg.add(f'<rect x="{x0}" y="{ptop}" width="{right-x0:.1f}" height="{pbot-ptop}" fill="none" stroke="{P["ink3"]}" stroke-width=".8"/>')
    running, points = 0, [f"{x0},{pbot}"]
    for d in year.days:
        running += d.count
        points.append(f"{x0 + (d.week + (d.weekday + 1) / 7) * px:.1f},{pbot - (pbot - ptop) * running / ceiling:.1f}")
    end_x, end_y = (float(v) for v in points[-1].split(","))
    svg.add(f'<line x1="{x0}" y1="{pbot}" x2="{end_x:.1f}" y2="{end_y:.1f}" stroke="{P["ink2"]}" stroke-width=".9" '
            f'stroke-dasharray="7 4"/>')
    svg.add(f'<path class="draw" d="M{" L".join(points)}" fill="none" stroke="{P["mark"]}" stroke-width="1.8" '
            f'stroke-linejoin="round" pathLength="1"/>')
    angle = math.degrees(math.atan2(end_y - pbot, end_x - x0))
    mx, my = x0 + (end_x - x0) * .3, pbot + (end_y - pbot) * .3
    svg.text(mx, my - 5, f"UNIFORM GRADE +{year.per_week:,.0f} EA/WK", 8, P["ink2"], DATA,
             f'transform="rotate({angle:.2f} {mx:.1f} {my:.1f})" letter-spacing=".5"')
    svg.text(end_x - 10, end_y + 22, f"{year.total:,}", 10, P["mark"], DATA, 'text-anchor="end" font-weight="bold"')
    view_title(x0, pbot + 32, "2", "PROFILE", "RUNNING TOTAL · STATIONS IN WEEKS")
    svg.text(right, pbot + 49, "So built we the wall … for the people had a mind to work. Neh. 4:6", 9.5, P["ink2"],
             LETTER, 'font-style="italic" text-anchor="end"')

    # Title block.
    tb, tw = right + 22, W - 26 - (right + 22)
    svg.add(f'<rect x="{tb:.1f}" y="26" width="{tw:.1f}" height="{H-52}" fill="none" stroke="{P["ink"]}" stroke-width="1.4"/>')
    rows = [26, 84, 132, 176, 300, 340]
    for y in rows[1:]:
        svg.add(f'<line x1="{tb:.1f}" y1="{y}" x2="{W-26}" y2="{y}" stroke="{P["ink"]}" stroke-width=".8"/>')
    cx = tb + tw / 2
    svg.text(cx, 52, "BADLAND", 22, P["ink"], CONDENSED, 'text-anchor="middle" font-weight="700" letter-spacing="4"')
    svg.text(cx, 70, "COLE TEBOU · CIVIL ENGINEER", 8, P["ink2"], DATA, 'text-anchor="middle" letter-spacing=".5"')
    svg.text(tb + 8, 98, "PROJECT", 7, P["ink2"], DATA, 'letter-spacing=".8"')
    svg.text(tb + 8, 118, "Contributions, last 12 mo.", 12, P["ink"], LETTER)
    svg.text(tb + 8, 146, "SHEET TITLE", 7, P["ink2"], DATA, 'letter-spacing=".8"')
    svg.text(tb + 8, 167, "PLAN & PROFILE", 18, P["ink"], CONDENSED, 'font-weight="600" letter-spacing="1"')
    svg.text(tb + 8, 190, "ESTIMATED QUANTITIES", 7, P["ink2"], DATA, 'letter-spacing=".8"')
    quantities = [("Contributions", "EA", f"{year.total:,}"), ("Days worked", "DAY", f"{year.active}"),
                  ("Longest run", "DAY", f"{year.longest}"), ("Current run", "DAY", f"{year.current}"),
                  ("Peak day", "EA", f"{year.peak.count:,}"), ("Average", "EA/WK", f"{year.per_week:,.0f}")]
    for i, (item, unit, qty) in enumerate(quantities):
        y = 208 + i * 15.5
        svg.text(tb + 8, y, item, 9.5, P["ink"], LETTER)
        svg.text(tb + tw - 62, y, unit, 8, P["ink2"], DATA, 'text-anchor="end"')
        svg.text(tb + tw - 8, y, qty, 9.5, P["ink"], DATA, 'text-anchor="end"')
    svg.text(tb + 8, 315, "ISSUED FOR REVIEW", 8, P["ink"], DATA, 'letter-spacing=".8"')
    svg.text(tb + 8, 330, f"{year.last.isoformat()} · SCALE: GRAPHIC", 8, P["ink2"], DATA, 'letter-spacing=".4"')
    svg.text(tb + 8, 354, "SHEET", 7, P["ink2"], DATA, 'letter-spacing=".8"')
    svg.text(tb + tw - 10, 384, "C-102", 34, P["ink"], CONDENSED, 'text-anchor="end" font-weight="700" letter-spacing="1"')
    return svg.done()


def shell(year):
    """A terminal session that types the command and streams the year's heatmap."""
    P = dict(bg="#080b09", bg2="#101512", rule="#29342c", rule2="#415246", accent="#4ade80", accent2="#31b765",
             amber="#d6b35c", text="#edf3ee", text2="#b7c2ba", muted="#919d94")
    shades = ("#151c17", "#1c4a2d", "#21773e", "#31b765", "#4ade80")
    W, H, x0, px, cell = 1000, 346, 78, 15.6, 12.4
    command = f"contrib {LOGIN} --last 12mo"
    advance = 8.4  # one character of 14px monospace
    typed = .35 + .055 * len(command)
    reveal = typed + .25
    done = reveal + .022 * year.weeks + .3
    svg = Svg(W, H, f"{year.total:,} contributions in the last year, drawn as a terminal session",
              "@keyframes col { from { opacity: 0; } } .col { animation: col .18s ease-out backwards; }"
              " @keyframes line { from { opacity: 0; } } .ln { animation: line .3s ease-out backwards; }"
              " @keyframes blink { 50% { opacity: 0; } } .cur { animation: blink 1.1s steps(1) infinite; }")
    svg.add(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{P["bg"]}" stroke="{P["rule"]}"/>')
    svg.add(f'<path d="M.5,32 V8.5 a8,8 0 0 1 8,-8 H{W-8.5} a8,8 0 0 1 8,8 V32 Z" fill="{P["bg2"]}"/>'
            f'<line x1=".5" y1="32" x2="{W-.5}" y2="32" stroke="{P["rule"]}"/>')
    svg.add(f'<text x="22" y="21" font-family="{MONO}" font-size="12.5"><tspan fill="{P["accent"]}">{LOGIN}@term</tspan>'
            f'<tspan fill="{P["text2"]}">:~</tspan></text>')
    svg.add(f'<text x="{W-22}" y="21" font-family="{MONO}" font-size="12" text-anchor="end" fill="{P["muted"]}">'
            f'edition: almanac · plan set · <tspan fill="{P["accent"]}" text-decoration="underline">terminal</tspan></text>')

    svg.add(f'<text x="22" y="64" font-family="{MONO}" font-size="14" fill="{P["text"]}" xml:space="preserve">'
            f'<tspan fill="{P["accent"]}">$ </tspan>{escape(command)}</text>')
    # Typing: a cover carrying the cursor steps off the command a character at a time, then is removed. It rests
    # off the canvas, so a renderer without animation shows the whole command. SMIL rather than CSS: Chrome stops
    # painting tspans whose CSS animation has finished, so animating each character is unreliable.
    start, wide = 22 + 2 * advance, advance * (len(command) + 1)
    key_times = ";".join(["0"] + [f"{(.35 + .055 * i) / typed:.4f}" for i in range(1, len(command))])
    offsets = ";".join(f"{advance * i:.1f} 0" for i in range(len(command)))
    svg.add(f'<g transform="translate({W} 0)"><animateTransform attributeName="transform" type="translate" '
            f'calcMode="discrete" begin="0s" dur="{typed:.3f}s" keyTimes="{key_times}" values="{offsets}" '
            f'fill="remove"/><rect x="{start:.1f}" y="48" width="{wide:.1f}" height="22" fill="{P["bg"]}"/>'
            f'<rect x="{start:.1f}" y="51" width="{advance}" height="16" fill="{P["accent"]}"/></g>')

    top, py = 100, 15.6
    labels = "".join(f'<text x="{x0 + week * px:.1f}" y="{top - 9}" font-family="{MONO}" font-size="11" '
                     f'fill="{P["muted"]}">{MONTHS[month].lower()}</text>' for week, month in year.month_starts())
    labels += "".join(f'<text x="{x0 - 10}" y="{top + row * py + 10}" font-family="{MONO}" font-size="11" '
                      f'fill="{P["muted"]}" text-anchor="end">{name.lower()}</text>'
                      for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    svg.add(f'<g class="ln" style="animation-delay:{reveal:.2f}s">{labels}</g>')
    columns = [[] for _ in range(year.weeks)]
    for d in year.days:
        colour = P["amber"] if d is year.peak and d.count else shades[d.level]
        columns[d.week].append(f'<rect x="{x0 + d.week * px:.1f}" y="{top + d.weekday * py:.1f}" width="{cell}" '
                               f'height="{cell}" rx="1.5" fill="{colour}"/>')
    for week, cells in enumerate(columns):
        svg.add(f'<g class="col" style="animation-delay:{reveal + .022 * week:.3f}s">{"".join(cells)}</g>')

    legend_x = x0 + year.weeks * px - 5 * 16 - 34
    legend = (f'<text x="{legend_x - 8}" y="{top + 7 * py + 18}" font-family="{MONO}" font-size="11" '
              f'fill="{P["muted"]}" text-anchor="end">less</text>')
    legend += "".join(f'<rect x="{legend_x + i * 16}" y="{top + 7 * py + 8}" width="{cell}" height="{cell}" rx="1.5" '
                      f'fill="{shade}"/>' for i, shade in enumerate(shades))
    legend += (f'<text x="{legend_x + 5 * 16 + 4}" y="{top + 7 * py + 18}" font-family="{MONO}" font-size="11" '
               f'fill="{P["muted"]}">more</text>')
    svg.add(f'<g class="ln" style="animation-delay:{done:.2f}s">{legend}</g>')

    y = top + 7 * py + 44
    peak = year.peak
    lines = [
        f'<tspan fill="{P["accent"]}" font-weight="bold">{year.total:,}</tspan> contributions in the last year',
        f'<tspan fill="{P["text2"]}">{year.active} active days · longest streak {year.longest} · current streak '
        f'{year.current} · peak </tspan><tspan fill="{P["amber"]}">{peak.count:,}</tspan>'
        f'<tspan fill="{P["text2"]}"> on {WEEKDAYS[peak.weekday].lower()} {peak.date.isoformat()}</tspan>',
        f'<tspan fill="{P["muted"]}"># Whatsoever thy hand findeth to do, do it with thy might. Ecclesiastes 9:10</tspan>',
    ]
    for i, line in enumerate(lines):
        svg.add(f'<text class="ln" style="animation-delay:{done + .25 * i:.2f}s" x="22" '
                f'y="{y + i * 22}" font-family="{MONO}" font-size="13.5" fill="{P["text"]}" xml:space="preserve">'
                f"{line}</text>")
    y += len(lines) * 22 + 12
    svg.add(f'<g class="ln" style="animation-delay:{done + .9:.2f}s"><text x="22" y="{y}" font-family="{MONO}" '
            f'font-size="14" fill="{P["accent"]}">$</text>'
            f'<rect class="cur" x="36" y="{y - 12}" width="8.4" height="15" fill="{P["accent"]}"/></g>')
    return svg.done()


EDITIONS = {"almanac": almanac, "blueprint": blueprint, "shell": shell}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=pathlib.Path, required=True, help="directory for the three SVGs")
    parser.add_argument("--data", type=pathlib.Path, help="a saved GraphQL answer instead of asking GitHub")
    parser.add_argument("--save", type=pathlib.Path, help="also write the GraphQL answer here")
    args = parser.parse_args()
    if args.data:
        answer = json.loads(args.data.read_text())
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("Set GITHUB_TOKEN, or pass --data with a saved answer.")
        answer = fetch(token)
    if args.save:
        args.save.write_text(json.dumps(answer))
    year = Year(answer)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, draw in EDITIONS.items():
        (args.out / f"{name}.svg").write_text(draw(year), encoding="utf-8")
    print(f"{year.total:,} contributions, {year.first} to {year.last}: {year.active} active days, "
          f"longest run {year.longest}, current {year.current}, peak {year.peak.count:,} on {year.peak.date}")


if __name__ == "__main__":
    main()
