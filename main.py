import datetime
import tempfile
import polars as pl
import duckdb
from pathlib import Path

pl.Config(set_ascii_tables=True)

# 1. Create the problematic file for demonstration
file_content = "col_a\tcol_b\tcol_c"
file_path = "test.txt"
with open(file_path, "w", encoding="cp932") as f:
    f.write(file_content)

# 2. Define parameters based on the failing use case
# A non-empty list of columns, as confirmed by debugging
header_list = ['セット親コード', 'セット親年月号', 'セット名', '本体価格', '点数', '冊数', '荷姿', 'NO', '書誌ｺｰﾄﾞ', '年月号・枝', '書名', '構成数', '取引コード']

# Using pl.Utf8 as a representative dtype for reproduction
field_types = {name: pl.Utf8 for name in header_list}

print(f"Attempting to read a single-line file ('{file_path}') with skip_rows=1...")
print(f"Polars version: {pl.__version__}")
print(f"Columns to be created (len: {len(header_list)}): {header_list}")

df = pl.read_csv(
        file_path,
        encoding="cp932",
        separator="\t",
        has_header=False,
        skip_rows=1,
        new_columns=header_list,
        dtypes=field_types,
        raise_if_empty=False, # This should prevent errors on empty data
        quote_char=None,
    )
print("\nSUCCESS: An empty DataFrame was created as expected.")
print(df)
