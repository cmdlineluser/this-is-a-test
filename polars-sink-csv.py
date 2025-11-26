import polars as pl
import requests
from pathlib import Path

url = "https://raw.githubusercontent.com/leanhdung1994/files/main/processedStep1_enwiktionary_namespace_0_43.ndjson"

outNdjson = Path("wiktionary.ndjson")
outTxt = Path("wiktionary.txt")

# Download
resp = requests.get(url)
resp.raise_for_status()

# Save
with open(outNdjson, "wb") as f:
    f.write(resp.content)

# Read with Polars
lf = pl.scan_ndjson(outNdjson)
lf.select("html").sink_csv(outTxt,
                           include_header=False,
                           maintain_order=True,
                           quote_style="never",
                           line_terminator="\r\n")

with open(outNdjson, "rb") as f:
  for row in f:
    print(repr(row[-10:]))
