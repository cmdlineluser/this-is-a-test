import datetime
import tempfile
import polars as pl
import duckdb
from pathlib import Path

pl.Config(set_ascii_tables=True)

expected = {'date_of_birth': [datetime.date(1887, 1, 11), datetime.date(1887, 1, 11), datetime.date(1889, 1, 11), datetime.date(1886, 1, 12), datetime.date(1889, 1, 13), datetime.date(1886, 1, 15), datetime.date(1888, 1, 17), datetime.date(1889, 1, 18), datetime.date(1885, 1, 18), datetime.date(1880, 1, 2)]}

with tempfile.TemporaryDirectory() as tmp_dir:

    filename = Path(tmp_dir) / "1.xlsx"

    (pl.from_repr("""
    ┌────────────────┐
    │ date_of_birth  │
    │ ---            │
    │ str            │
    ╞════════════════╡
    │ 1/11/1887      │
    │ 1/11/1887      │
    │ 1/11/1889      │
    │ 1/12/1886      │
    │ 1/13/1889      │
    │ 1/15/1886      │
    │ 1/17/1888      │
    │ 1/18/1889      │
    │ 1/18/1885      │
    │ 1/2/1880       │    
    └────────────────┘
    """)
    .with_columns(pl.col.date_of_birth.str.to_date("%m/%d/%Y"))
    .write_excel(filename))

    df = pl.read_excel(filename)

    assert df.to_dict(as_series=False) == expected
    print(df)

    csv_file = Path(tmp_dir) / "1.csv"
    csv_file.write_text("""ID,Name,Age
1,John,28
2,Jane,35,California,USA
3,Emily,22
4,Michael,40,Australia,Melbourne""")

    try:
        print(pl.read_csv(csv_file))
    except:
        print("[ERROR]:", "pl.read_csv()")
    
    print(duckdb.read_csv(str(csv_file)))
