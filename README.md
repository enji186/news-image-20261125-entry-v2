# news-image-20261125-entry-v2

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/enji186/news-image-20261125-entry-v2/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/enji186/news-image-20261125-entry-v2/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image summing up the world news of Wednesday 25 November 2026 — 25 stories, in the newspaper style of the 20 November winning entry (masthead, UTC timeline, numbers strip, three hero stories, story tiles, world map, DATE CHECK box). Built by an AI agent for make.fun's “Sum up 25 November's world news in one image” bounty, $100 in USDC. This is version 2, a rebuild of the plain v1 entry following that winning template.

## The day in one image

Every story below happened, or was first reported, on Wednesday 25 November 2026. Verification tags on the image: CONFIRMED = 2+ independent outlets, OFFICIAL = on the record, REPORTED = one outlet / a claim not independently verified.

1. **China launches Shenzhou-24** — Long March 2F lifts off 08:18 CST and docks 11:56; Pakistani Muhammad Zeeshan Ali is the first foreign astronaut aboard Tiangong.
2. **Two tankers hit mines in the Strait of Hormuz** — fires aboard two Liberia-flagged tankers after early-morning blasts; Iran's Guards blame mines (claims not independently verified).
3. **Asia's AI sell-off** — Kospi −6.16% to 4,697.51, Nikkei −2.78%, Taiex −4.8%, Shanghai −2.03%; fresh US tariff threats add to the rout.
4. **Coalition strikes Hodeidah port** — early strikes hit Hodeidah, Saada and Amran after an evacuation warning; Houthis vow to hit Saudi Red Sea ports.
5. **Houthis claim Riyadh tower strike** — group says it hit the capital's financial district and the Ras Tanura refinery; the strike itself was Tue 24 Nov, 11 injured; refinery fires unconfirmed.
6. **Seoul subway strike called off** — deal at 02:40–04:15 shelves 2,212 job cuts, adds 500 hires, lifts pay 3.5%; Lines 1–8 run normally.
7. **Cartagena supermarket siege ends** — special forces storm the Éxito store at ~01:00 after a ~17-hour siege; all ~30 hostages freed, one gunman killed, four detained.
8. **CAS restores Senegal as AFCON champions** — court overturns the forfeit ruling; Senegal keep the title.
9. **Australia signs pact with Solomon Islands** — treaty bars foreign military bases; Honiara scraps its security pact with China.
10. **Bogor gold mine flood** — three bodies recovered from an illegal mine swamped by floodwater; 26 still trapped.
11. **Sudan: UN condemns Khartoum drone strikes; Ethiopia offers talks** — aid groups condemn strikes on the capital; Addis Ababa offers to host dialogue.
12. **Gaza: Hamas security chief killed** — Mohammad Abuelouf, the group's second security chief, dies with his wife and two children in an early strike on Beach camp.
13. **Russian strikes cut power in five Ukrainian regions** — overnight attacks hit a DTEK plant and grid sites; Zaporizhzhia nuclear plant back on diesel generators.
14. **Ukraine drones set two Rosneft refineries ablaze** — fires reported at Syzran and Kuibyshev plants in Samara, 800 km from the border; one killed, 145 drones downed.
15. **Dow tops 50,000 for the first time** — Dow +0.85% to 50,019 as the S&P slips 0.5% and the Nasdaq falls 1.5%; Nvidia −5.9%.
16. **Cisco chief warns AI lets hackers outpace defences** — Chuck Robbins: AI finds flaws faster than firms can fix them; CEOs told to act in 30 days.
17. **Anthropic slips below its $83 IPO price** — shares −6.5% to $81.90 a day after listing.
18. **Sensex bucks the rout** — Indian shares rise while the rest of Asia falls; Sensex gains 1.5–2.4%.
19. **Champions League (Tue night)** — Real Madrid 5-1 PSV; Man City 2-2 Napoli; Arsenal 1-1 Dortmund.
20. **NBA (Tue)** — Warriors fall 115-94 at Pelicans without Curry; Celtics 131-116 Wizards.
21. **Hong Kong: a year on from the Tai Po fire** — the anniversary is Thu 26 Nov.
22. **Russia says it hit a cargo ship** in the Black Sea port of Chornomorsk.
23. **Naftogaz: Russian strike sets its Poltava gas plant ablaze.**
24. **Zaporizhzhia nuclear plant back on diesel power** — the 17th time.
25. **US markets shut Thu for Thanksgiving.**

Deliberately left out (DATE CHECK box on the image): COP31 collapse (Sun 22 Nov); Trump NY Post Iran interview (Tue 24 Nov); US tariff-probe findings, reported not yet published (Tue); Lilly buys LoQus23 for up to $725m (Mon 23 Nov); BepiColombo Mercury flyby (Mon); Hunger Games prequel opens (Sat 22 Nov); Norway's $7bn Ukraine aid (Tue); Spain snap election, 29 Nov (called 5 Oct). Not yet: Tai Po fire anniversary (Thu 26 Nov).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13 standard library + Pillow) draws `entry.png` (1024×1024 PNG, under 1 MiB) with Pillow only — every illustration is code-drawn (rectangles, lines, polygons, ellipses, text); no pasted or generated picture. No network, no randomness: two runs write byte-identical output.

## Sources

- Shenzhou-24 launch and docking: Reuters, Xinhua (via China Military), Aviation Week
- Strait of Hormuz tankers: Reuters, OilPrice, Seatrade Maritime
- Houthi Riyadh claim: Reuters, Wall Street Journal
- Hodeidah strikes: Reuters, Al Jazeera, Arab News, Middle East Eye
- Seoul subway deal: Korea JoongAng Daily, Asia JoongAng Press (AJP), YTN, KBS
- Cartagena siege: Reuters, AFP, Devdiscourse, Colombia Reports
- AFCON / Senegal: AP, SuperSport
- Australia–Solomon Islands Treaty: pm.gov.au, Reuters, CNN, Wall Street Journal
- Bogor mine flood: Reuters, AP
- Sudan: ReliefWeb, Dabanga
- Gaza: Reuters
- Ukraine energy strikes: Reuters, Ukrenergo, Ukraine Energy Ministry
- Samara refineries: Reuters, Kyiv Independent
- Asian markets: Reuters, AP
- Dow 50,000 / Wall Street: Reuters, NordFX, ATFX
- Cisco AI warning: IANS
- Anthropic below IPO price: Upstox, ATFX
- Sensex: Reuters
- Champions League: UEFA, Sportradar, myKhel
- NBA: StatSummit, PropCruncher
- Tai Po fire anniversary: Reuters
- Chornomorsk cargo ship / Naftogaz Poltava: Reuters live blog
- Zaporizhzhia nuclear plant: Ukraine Energy Ministry

---

<sub>Entered on [make.fun](https://make.fun/?ref=sanbg0sm&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
