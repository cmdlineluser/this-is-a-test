import polars as pl
import requests
from pathlib import Path

url = "https://raw.githubusercontent.com/leanhdung1994/files/main/processedStep1_enwiktionary_namespace_0_43.ndjson"

# Read with Polars
lf = pl.scan_ndjson(url)
lf.select("html").sink_csv("1.csv",
                           include_header=False,
                           maintain_order=True,
                           quote_style="never",
                           line_terminator="\r\n")

with open("1.csv", "rb") as f:
  for row in f:
    print(repr(row[-10:]))
