import re
import pandas as pd
from ..data_loader import get_data

def answer_from_data(message, filters=None):
    year_match = re.search(r"\b(20\d{2})\b", message or "")
    year = int(year_match.group(1)) if year_match else None

    sectors = ["Agriculture", "Buildings", "Energy", "Industry", "Transport"]
    detected_sector = None
    for s in sectors:
        if s.lower() in (message or "").lower():
            detected_sector = s
            break

    df = get_data().copy()

    if filters:
        if 'start_year' in filters and filters['start_year'] is not None:
            df = df[df['year'] >= int(filters['start_year'])]
        if 'end_year' in filters and filters['end_year'] is not None:
            df = df[df['year'] <= int(filters['end_year'])]
        if 'sector' in filters and filters['sector']:
            df = df[df['sector'] == filters['sector']]
        if 'region' in filters and filters['region']:
            df = df[df['region'] == filters['region']]

    if 'emissions_tCO2e' in df.columns:
        df['emissions_tCO2e'] = pd.to_numeric(df['emissions_tCO2e'], errors='coerce').fillna(0)
    wide_sectors = [c for c in df.columns if c not in ('year','sector','industry','region','emissions_tCO2e')]
    if wide_sectors:
        if year:
            row = df[df['year'] == year]
            if row.empty:
                return f"No data available for {year}."
            if detected_sector:
                try:
                    val = int(float(row.iloc[0].get(detected_sector, 0)))
                    return f"{detected_sector} emissions in {year}: {val:,} tCO2e."
                except Exception:
                    return f"{detected_sector} emissions in {year}: {row.iloc[0].get(detected_sector, 0)} tCO2e."
            else:
                vals = row.iloc[0].to_dict()
                vals.pop('year', None)
                lines = []
                for k, v in vals.items():
                    try:
                        num = int(float(v))
                        lines.append(f"- {k}: {num:,} tCO2e")
                    except Exception:
                        lines.append(f"- {k}: {v} tCO2e")
                return f"Emissions in {year}:\n" + "\n".join(lines)
        if detected_sector:
            series = df[['year', detected_sector]]
            lines = [f"{detected_sector} emissions across years:"]
            for _, r in series.iterrows():
                try:
                    num = int(float(r[detected_sector]))
                    lines.append(f"- {int(r['year'])}: {num:,} tCO2e")
                except Exception:
                    lines.append(f"- {int(r['year'])}: {r[detected_sector]}")
            return "\n".join(lines)
        return ""

    if year:
        dfy = df[df['year'] == year]
        if dfy.empty:
            return f"No data available for {year}."
        if detected_sector:
            total = int(dfy[dfy['sector'] == detected_sector]['emissions_tCO2e'].sum())
            return f"{detected_sector} emissions in {year}: {total:,} tCO2e."
        else:
            by_sector = dfy.groupby('sector', as_index=False)['emissions_tCO2e'].sum()
            lines = []
            for _, row in by_sector.iterrows():
                try:
                    val = int(row['emissions_tCO2e'])
                    lines.append(f"- {row['sector']}: {val:,} tCO2e")
                except Exception:
                    lines.append(f"- {row['sector']}: {row['emissions_tCO2e']} tCO2e")
            return f"Emissions in {year}:\n" + "\n".join(lines)

    if detected_sector:
        series = df[df['sector'] == detected_sector].groupby('year', as_index=False)['emissions_tCO2e'].sum().sort_values('year')
        lines = [f"{detected_sector} emissions across years:"]
        for _, row in series.iterrows():
            try:
                val = int(row['emissions_tCO2e'])
                lines.append(f"- {int(row['year'])}: {val:,} tCO2e")
            except Exception:
                lines.append(f"- {int(row['year'])}: {row['emissions_tCO2e']}")
        return "\n".join(lines)

    return ""