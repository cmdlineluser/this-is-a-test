import urllib.request
import zipfile
import sys
import os
import polars as pl

url = "https://github.com/user-attachments/files/22982158/polars_bug_data_before_panic.zip"

file_name, response = urllib.request.urlretrieve(url)

content = zipfile.ZipFile(file_name).open("polars_bug_data_before_panic.parquet").read()

buf = io.BytesIO(content)
pdf = pl.read_parquet(buf)

print(f"Polars {pl.__version__} | Python {sys.version.split()[0]}")

"""
# Check data file exists
data_file = 'polars_bug_data_before_panic.parquet'
if not os.path.exists(data_file):
    print(f"ERROR: {data_file} not found")
    print("This file should be included with the bug report.")
    sys.exit(1)

# Load data
print(f"Loading {data_file}...")
pdf = pl.read_parquet(data_file)
"""

print(f"Loaded {len(pdf)} rows, {pdf['window_id'].n_unique()} groups\n")

# Run the aggregation that triggers panic
print("Running group_by().agg() - will panic at group 95...")

try:
    # EXACT aggregation that causes Polars to panic
    shape_stats_native = pdf.group_by('window_id', maintain_order=True).agg([
        # Multimodality detection with shift
        (
            (pl.col('volume') > pl.col('volume').shift(1).fill_null(float('-inf'))) & 
            (pl.col('volume') > pl.col('volume').shift(-1).fill_null(float('-inf')))
        ).sum().alias('multimodality_raw'),

        # Entropy calculation
        (
            -(pl.when(pl.col('pdf') > 0)
              .then(pl.col('pdf') * pl.col('pdf').log())
              .otherwise(0))
        ).sum().alias('entropy'),

        # POC width
        (pl.col('volume') >= pl.col('volume').max() * 0.5).sum().alias('poc_width'),

        # Tailing upper - CRITICAL: nested filter + quantile + first
        pl.when(pl.len() > 1)
            .then(
                pl.col('volume')
                .filter(pl.col('price_bin_center') >= pl.col('price_bin_center').quantile(0.9))
                .sum() / pl.col('total_volume').first().clip(lower_bound=1e-9)
            )
            .otherwise(pl.lit(0.0))
            .alias('tailing_upper'),

        # Tailing lower - CRITICAL: nested filter + quantile + first
        pl.when(pl.len() > 1)
            .then(
                pl.col('volume')
                .filter(pl.col('price_bin_center') <= pl.col('price_bin_center').quantile(0.1))
                .sum() / pl.col('total_volume').first().clip(lower_bound=1e-9)
            )
            .otherwise(pl.lit(0.0))
            .alias('tailing_lower'),

        # Volume above/below value area
        pl.col('volume').filter(pl.col('price_bin_center') > pl.col('vah').first()).sum().alias('volume_above_va'),
        pl.col('volume').filter(pl.col('price_bin_center') < pl.col('val').first()).sum().alias('volume_below_va'),
        pl.col('poc_bias').first().alias('poc_bias'),

        # Statistical moments - CRITICAL: multiple pow() operations
        pl.col('total_volume').first().alias('_sum_vol'),
        (pl.col('price_bin_center') * pl.col('volume')).sum().alias('_m1_num'),
        (pl.col('price_bin_center').pow(2) * pl.col('volume')).sum().alias('_m2_num'),
        (pl.col('price_bin_center').pow(3) * pl.col('volume')).sum().alias('_m3_num'),
        (pl.col('price_bin_center').pow(4) * pl.col('volume')).sum().alias('_m4_num'),
        
    ]).with_columns([
        # Derived: mean
        (pl.col('_m1_num') / pl.col('_sum_vol')).alias('mean'),
    ]).with_columns([
        # Derived: variance
        ((pl.col('_m2_num') / pl.col('_sum_vol')) - pl.col('mean').pow(2)).alias('variance'),
    ]).with_columns([
        # Derived: skewness
        pl.when(pl.col('variance') < 1e-9)
            .then(0.0)
            .otherwise(
                (
                    (pl.col('_m3_num') / pl.col('_sum_vol')) -
                    3 * pl.col('mean') * (pl.col('_m2_num') / pl.col('_sum_vol')) +
                    2 * pl.col('mean').pow(3)
                ) / pl.col('variance').pow(1.5)
            )
            .alias('skewness'),
        
        # Derived: kurtosis
        pl.when(pl.col('variance') < 1e-9)
            .then(3.0)
            .otherwise(
                (
                    (pl.col('_m4_num') / pl.col('_sum_vol')) -
                    4 * pl.col('mean') * (pl.col('_m3_num') / pl.col('_sum_vol')) +
                    6 * pl.col('mean').pow(2) * (pl.col('_m2_num') / pl.col('_sum_vol')) -
                    3 * pl.col('mean').pow(4)
                ) / pl.col('variance').pow(2)
            )
            .alias('kurtosis'),
    ])
    
    # Success - bug fixed
    print(f"SUCCESS! Aggregation completed. Result: {shape_stats_native.shape}")
    
except Exception as e:
    print(f"\nPANIC OCCURRED: {type(e).__name__}: {e}")
    print("\nExpected error: 'index: 95 out of bounds for len: 1'")
    print("Location: crates\\polars-core\\src\\chunked_array\\mod.rs:517:9")
    print("\nBUG CONFIRMED - Polars panics at group 95 with 100+ groups")
    raise

