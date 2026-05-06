SECTOR_MAP = {
    "finance": "Banking & Financial Services",
    "financial services": "Banking & Financial Services",
    "finances": "Banking & Financial Services",
    "it": "Technology",
    "tech": "Technology",
    "automotive": "Automotive",
    "auto": "Automotive",
    "crypto": "Cryptocurrency"
}


def map_sectors(sectors):
    if not sectors:
        return []

    clean = []

    for s in sectors:
        if not s:
            continue

        key = s.lower().strip()
        mapped = SECTOR_MAP.get(key, s)

        clean.append(mapped)

    return list(set(clean))