import csv, random
years = list(range(2015, 2026))
sectors = {
  "Energy": ["Power plants","Oil & Gas"],
  "Transport": ["Aviation","Road","Shipping"],
  "Industry": ["Steel","Cement","Chemicals"],
  "Agriculture": ["Livestock","Crop burning"],
  "Buildings": ["Residential","Commercial"]
}
with open("emissions_fake.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["year","sector","industry","region","emissions_tCO2e"])
    for y in years:
        for s, inds in sectors.items():
            for ind in inds:
                base = random.uniform(0.5, 2.0) * (1_000_000 if s=="Energy" else 200_000)
                trend = (y-2015) * random.uniform(-0.03, 0.05)
                val = max(1000, int(base * (1 + trend) * random.uniform(0.9, 1.15)))
                w.writerow([y, s, ind, "Global", val])
print("emissions_fake.csv created")
