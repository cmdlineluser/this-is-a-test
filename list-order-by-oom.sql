set preserve_insertion_order = false;

copy (
  with
    dates as (select unnest(generate_series(date '2010-01-01', date '2015-12-01', interval '1 day')) as days),
    ids   as (select unnest(generate_series(1, 500_000)) as id)
  from dates, ids
  select
    id,
    date: days::date,
    value: random()
) to 'output.parquet';

from 'output.parquet'
select
    first(columns(*)),
    list(value order by date)
group by id
order by id, date;
