import plotly.express as px

# Create a sample figure
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

# Save the figure as an HTML file
fig.write_html("index.html")
