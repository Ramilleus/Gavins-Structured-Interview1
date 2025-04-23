from preswald import connect, get_df, query, table, text,sidebar,separator
import pandas as pd

sidebar(defaultopen = True)

def stringify_timestamps(df): # Created this function to handle "ERROR - Error creating table component: RenderBuffer failed to compute hash: can not serialize 'Timestamp' object" 
    return df.copy().map(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)

connect()

# Load and fix main dataframe
df = get_df("CropYield_csv")
df = stringify_timestamps(df)

# Filtered data
sql = "SELECT region,crop_type,harvest_date,total_days,yield_kg_per_hectare FROM CropYield_csv WHERE yield_kg_per_hectare > 2000"
filtered_df = query(sql, "CropYield_csv")
filtered_df = stringify_timestamps(filtered_df)

# UI
text("# My Data Analysis App")
table(filtered_df, title="Filtered Data")

separator()

table(df)

separator()

from preswald import slider, table 
threshold = slider("Threshold", min_val=1, max_val=10000, default=5000)
table(df[df["yield_kg_per_hectare"] > threshold], title="Dynamic Data View")

from preswald import plotly
import plotly.express as px

fig = px.scatter(df, x="total_days", y="yield_kg_per_hectare", color="farm_id")
plotly(fig)