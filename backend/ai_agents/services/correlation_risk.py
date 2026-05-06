def calculate_correlation_risk(sector_exposure):

    correlated_pairs = [
        ("Energy", "Economy"),
        ("Banking & Financial Services", "Economy"),
        ("Technology", "Semiconductors")
    ]

    risk_flags = []

    for s1, s2 in correlated_pairs:
        if s1 in sector_exposure and s2 in sector_exposure:
            combined = sector_exposure[s1] + sector_exposure[s2]

            if combined > 50:
                risk_flags.append({
                    "pair": f"{s1} + {s2}",
                    "combined_exposure": combined,
                    "risk": "High"
                })

    return risk_flags