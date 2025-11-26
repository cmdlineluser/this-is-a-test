import io
import polars as pl

pl.LazyFrame({"x": ["foo", "bar"]}).sink_csv("1.csv", include_header=False, quote_style="never", line_terminator="\r\n")

print([c for c in open("1.csv", "rb")])
