import io
import polars as pl

f = io.BytesIO()

pl.LazyFrame({"x": ["foo", "bar"]}).sink_csv(f, include_header=False, quote_style="never", line_terminator="\r\n")

print([c for c in f.getvalue()])
