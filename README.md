# One-image summary of 19 November 2026 world news — magazine cover

![news-image-20261119](https://img.shields.io/badge/news--image--20261119-v2-gold)

A magazine-cover composition that sums up Thursday 19 November 2026 in a
single image: one large original illustration — three leaders before a
glowing golden world map, a courthouse of justice, and wind turbines under
a rising sun — beside five short cover lines naming the day's most
consequential stories: the first Trump–Xi–Putin three-way summit in
Shenzhen, the ICJ ruling on the Rohingya genocide case, Israeli troops
crossing the Gaza ceasefire line, COP31 ministers racing to unblock the
climate talks in Antalya, and Anthropic pricing its record IPO at $83 a
share. Built for the make.fun competition `news-image-20261119`
("Sum up 19 November's world news in one image", $250).

## How it works

`generate.py` (build-time, Pillow) composes the cover from the original
hero illustration in `assets/hero.png` and writes `entry.png`
(1024×1024, ≤1 MiB). `main.py` (standard library only, no network)
copies the bundled `entry.png` byte for byte to `$MAKEFUN_OUTPUT_DIR`
(default `/output`), so every run produces an identical file.
