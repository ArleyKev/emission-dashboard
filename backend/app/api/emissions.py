from fastapi import APIRouter, Query
from ..data_loader import get_data
from ..utils.aggregator import aggregate_time_series, breakdown_by_industry

router = APIRouter(prefix="/emissions", tags=["emissions"])

@router.get("/sectors")
def list_sectors():
    df = get_data()
    sectors = df['sector'].unique().tolist()
    mapping = {}
    for s in sectors:
        mapping[s] = df[df['sector']==s]['industry'].unique().tolist()
    return {"sectors": mapping}

@router.get("/")
def get_emissions(start_year: int = Query(None), end_year: int = Query(None), sector: str = Query(None), region: str = Query(None)):
    df = get_data()
    ts = aggregate_time_series(df, start_year, end_year, sector, region)
    return {"time_series": ts}

@router.get("/breakdown")
def get_breakdown(year: int, sector: str):
    df = get_data()
    out = breakdown_by_industry(df, year, sector)
    return {"breakdown": out}
