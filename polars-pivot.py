import os
os.environ["POLARS_MAX_THREADS"] = "8"
import polars as pl
import numpy as np
import datetime

# Parameters
n_codes = 400
n_timestamps = 100_000
n_rows = n_codes * n_timestamps  # 40,000,000

# Generate unique timestamps
base = datetime.datetime(2019, 1, 1)
datetimes = np.array([base + datetime.timedelta(minutes=i) for i in range(n_timestamps)], dtype="datetime64[ns]")

# Generate codes
codes = np.array([f"COD{i:03d}" for i in range(n_codes)], dtype="object")

# Repeat and tile to create a full dataset
code_col = np.repeat(codes, n_timestamps)
datetime_col = np.tile(datetimes, n_codes)

# Two random float columns
v1 = np.random.randn(n_rows).astype(np.float32)
v2 = np.random.randn(n_rows).astype(np.float32)

# Build the Polars DataFrame
df = pl.DataFrame({
    "code": code_col,
    "datetime": datetime_col,
    "v1": v1,
    "v2": v2,
})
print(df)
pivoted = df.pivot(
    index="datetime",
    on="code",
    values="v1", 
    maintain_order=True,
    sort_columns=True
)
print(pivoted.shape)import os
#os.environ["POLARS_MAX_THREADS"] = "8"
import polars as pl
import numpy as np
import datetime

# Parameters
n_codes = 400
n_timestamps = 100_000
n_rows = n_codes * n_timestamps  # 40,000,000

# Generate unique timestamps
base = datetime.datetime(2019, 1, 1)
datetimes = np.array([base + datetime.timedelta(minutes=i) for i in range(n_timestamps)], dtype="datetime64[ns]")

# Generate codes
codes = np.array([f"COD{i:03d}" for i in range(n_codes)], dtype="object")

# Repeat and tile to create a full dataset
code_col = np.repeat(codes, n_timestamps)
datetime_col = np.tile(datetimes, n_codes)

# Two random float columns
v1 = np.random.randn(n_rows).astype(np.float32)
v2 = np.random.randn(n_rows).astype(np.float32)

# Build the Polars DataFrame
df = pl.DataFrame({
    "code": code_col,
    "datetime": datetime_col,
    "v1": v1,
    "v2": v2,
})
print(df)
pivoted = df.pivot(
    index="datetime",
    on="code",
    values="v1", 
    maintain_order=True,
    sort_columns=True
)
print(pivoted.shape)
