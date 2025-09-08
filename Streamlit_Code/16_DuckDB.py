import duckdb
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'name': ['A', 'B', 'C'],
    'score': [90, 85, 88]
})

# Query with DuckDB
result = duckdb.query("SELECT name, score FROM df WHERE score > 85").to_df()
print(result)