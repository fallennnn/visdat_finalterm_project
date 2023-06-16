import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Viridis6
from bokeh.layouts import column
from bokeh.models import Slider, Select

data = pd.read_csv('test.csv')
data.set_index('Year', inplace=True)

island_list = data.Island.unique().tolist()

color_mapper = CategoricalColorMapper(factors=island_list, palette=Viridis6)

source = ColumnDataSource(data={
    'x': data.loc[2020].new_cases,
    'y': data.loc[2020].new_deaths,
    'location': data.loc[2020].Location,
    'island': data.loc[2020].Island
})

# Define the callback function: update_plot
def update_plot():
    # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider
    x = x_select
    y = y_select
    plot_bar = bar_select
    # Label axes of scatter_plot
    scatter_plot.xaxis.axis_label = x
    scatter_plot.yaxis.axis_label = y
    # new data for scatter plot
    new_data = {
        'x': data.loc[yr][x],
        'y': data.loc[yr][y],
        'location': data.loc[yr].Location,
        'island': data.loc[yr].Island
    }
    source.data = new_data
    
    # Add title to scatter_plot: scatter_plot.title.text
    scatter_plot.title.text = 'Scatter plot data for %d' % yr
    
    # Update bar plot
    bar_data = data.loc[yr].groupby('Island')[plot_bar].sum()
    bar_source.data = {
        'island': sorted(data.Island.unique().tolist()),
        'counts': bar_data
    }
    bar_plot.y_range.start = 0
    bar_plot.y_range.end = max(bar_data) * 1.1

    # Add title to bar_plot: bar_plot.title.text
    bar_plot.title.text = 'Bar plot data for %d' % yr
    bar_plot.yaxis.axis_label = plot_bar  # Perbarui label sumbu Y sesuai dengan dropdown

# Add text above the Year slider
st.sidebar.markdown('<h2 style="text-align: center; color: #00BFFF;">VISDAT - Final Term (Interactive Visualization)</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<h3 style="text-align: center; color: #00BFFF;">IF43-PIL-DS02</h3>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="text-align: center; font-size: 14px; color: #FFFFFF;">Reza Donsika Putra (1301201403)</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="text-align: center; font-size: 14px; color: #FFFFFF;">Sawsan Setiady (1301201588)</p>', unsafe_allow_html=True)

# Make a slider object: slider
slider = st.sidebar.slider('Year', 2020, 2022, 2020)

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = st.sidebar.selectbox('Scatter plot (x-axis data)', ['new_cases', 'new_deaths', 'new_recovered', 'new_active_cases'], index=0)

# Create a dropdown Select widget for the y data: y_select
y_select = st.sidebar.selectbox('Scatter plot (y-axis data)', ['new_cases', 'new_deaths', 'new_recovered', 'new_active_cases'], index=1)

# Create a dropdown Select widget for the bar plot data: bar_select
bar_select = st.sidebar.selectbox('Bar plot data', ['new_cases', 'new_deaths', 'new_recovered', 'new_active_cases'], index=0)

# Create the figure: scatter_plot
scatter_plot = figure(title='2020', x_axis_label='New Cases', y_axis_label='New Deaths',
                      sizing_mode='stretch_width', height=400, width=700, tools=[HoverTool(tooltips='@location')])

# Add a circle glyph to the scatter_plot
scatter_plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
                    color=dict(field='island', transform=color_mapper), legend='island')

# Set the legend and axis attributes
scatter_plot.legend.location = 'top_right'

# Create bar plot data source
bar_data = data.loc[2020].groupby('Island')[bar_select].sum()  # Menggunakan bar_select dari dropdown
bar_source = ColumnDataSource(data={
    'island': sorted(data.Island.unique().tolist()),
    'counts': bar_data
})

# Create new CategoricalColorMapper
new_color_mapper = CategoricalColorMapper(factors=island_list, palette=Viridis6)

# Create bar plot
bar_plot = figure(title='Bar Plot', x_axis_label='Island', y_axis_label=bar_select,
                  sizing_mode='stretch_width', height=400, width=700, toolbar_location=None, x_range=sorted(data.Island.unique().tolist()))

bar_plot.vbar(x='island', top='counts', source=bar_source, width=0.8, color=dict(field='island', transform=new_color_mapper))

# Call update_plot when the inputs change
update_plot()

# Add plots to Streamlit app
st.bokeh_chart(scatter_plot)

# Add plots to Streamlit app
st.bokeh_chart(bar_plot)