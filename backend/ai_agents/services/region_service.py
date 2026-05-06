def classify_region(region_text):
    if not region_text:
        return "GLOBAL"

    region_text = region_text.lower()

    india_keywords = ["india", "indian", "mumbai", "nse", "bse"]

    for k in india_keywords:
        if k in region_text:
            return "INDIA"

    return "GLOBAL"