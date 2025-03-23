"""
Visualization Utilities Module for SimpleRTOS

This module provides visualization functions used throughout the SimpleRTOS application.
It encapsulates Plotly chart creation functions with consistent styling and formatting.
"""

import plotly.graph_objects as go

# Define the exported functions
__all__ = ["create_line_chart", "create_bar_chart"]

def create_line_chart(data, title, x_label, y_label):
    """
    Create a line chart using Plotly with consistent styling.
    Optimized for better performance with larger datasets.
    
    This function generates a line chart with the SimpleRTOS theme styling applied,
    including dark background, appropriate colors, and consistent font styling.
    
    Parameters:
        data (list of tuples): Data points as [(x1, y1), (x2, y2), ...] pairs
        title (str): Title of the chart
        x_label (str): Label for the x-axis
        y_label (str): Label for the y-axis
    
    Returns:
        plotly.graph_objects.Figure: A fully configured Plotly figure object
        
    Example:
        >>> data = [(1, 10), (2, 15), (3, 13), (4, 17)]
        >>> fig = create_line_chart(data, "Sample Metrics", "Time", "Value")
        >>> st.plotly_chart(fig)
    """
    # Performance optimization: Only process if we have data
    if not data:
        # Return empty figure with message if no data
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            paper_bgcolor="#222222",
            plot_bgcolor="#333333",
            font=dict(color="#FFFFFF"),
            annotations=[dict(
                text="No data available",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                font=dict(color="#FFFFFF", size=14)
            )]
        )
        return fig
    
    # Performance optimization: Downsample data if there are too many points
    # Only keep at most 100 points to improve rendering performance
    if len(data) > 100:
        # Simple downsampling by taking every nth point
        step = len(data) // 100
        data = data[::step]
    
    # Extract x and y values from data tuples
    x_values = [t for t, _ in data]
    y_values = [v for _, v in data]
    
    # Create the figure with Scatter trace - optimize for performance
    fig = go.Figure(
        data=go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",  # Only show lines, not markers for better performance
            line=dict(color="blue", width=2),
            fill="tozeroy",  # Fill area between line and x-axis
            fillcolor="rgba(0, 0, 255, 0.1)",  # Light blue fill
        )
    )
    
    # Update layout with consistent styling
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        paper_bgcolor="#222222",  # Dark background for the chart paper
        plot_bgcolor="#333333",   # Dark background for the plotting area
        font=dict(color="#FFFFFF"), # White text for better contrast
        # Optimize layout for performance
        autosize=True,
        margin=dict(l=50, r=30, b=50, t=50),
        hovermode="closest"
    )
    
    return fig


def create_bar_chart(categories, values, title, x_label, y_label):
    """
    Create a bar chart using Plotly with consistent styling.
    Optimized for better performance with larger datasets.
    
    This function generates a bar chart with the SimpleRTOS theme styling applied,
    including dark background, appropriate colors, and consistent font styling.
    
    Parameters:
        categories (list): List of category labels for the x-axis
        values (list): List of numeric values corresponding to each category
        title (str): Title of the chart
        x_label (str): Label for the x-axis
        y_label (str): Label for the y-axis
    
    Returns:
        plotly.graph_objects.Figure: A fully configured Plotly figure object
        
    Example:
        >>> categories = ["Category A", "Category B", "Category C"]
        >>> values = [20, 35, 15]
        >>> fig = create_bar_chart(categories, values, "Sample Distribution", "Categories", "Count")
        >>> st.plotly_chart(fig)
    """
    # Performance optimization: Only process if we have data
    if not categories or not values or len(categories) == 0 or len(values) == 0:
        # Return empty figure with message if no data
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            paper_bgcolor="#222222",
            plot_bgcolor="#333333",
            font=dict(color="#FFFFFF"),
            annotations=[dict(
                text="No data available",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                font=dict(color="#FFFFFF", size=14)
            )]
        )
        return fig
    
    # Performance optimization: Limit the number of bars to display
    # If there are too many categories, only show the top N by value
    max_bars = 20  # Maximum number of bars to display for performance
    if len(categories) > max_bars:
        # Create pairs of categories and values
        pairs = list(zip(categories, values))
        # Sort by value in descending order
        pairs.sort(key=lambda x: x[1], reverse=True)
        # Take only the top max_bars items
        pairs = pairs[:max_bars]
        # Unzip the pairs back into separate lists
        categories, values = zip(*pairs)
    
    # Create the figure with Bar trace - optimize for performance
    fig = go.Figure(
        data=go.Bar(
            x=categories,
            y=values,
            marker_color="blue",  # Use blue for the bars
            opacity=0.8,          # Slight transparency
            hoverinfo="x+y"       # Simplified hover info for better performance
        )
    )
    
    # Update layout with consistent styling and performance optimizations
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        paper_bgcolor="#222222",  # Dark background for the chart paper
        plot_bgcolor="#333333",   # Dark background for the plotting area
        font=dict(color="#FFFFFF"), # White text for better contrast
        bargap=0.2,               # Gap between bars
        # Optimize layout for performance
        autosize=True,
        margin=dict(l=50, r=30, b=50, t=50),
        hovermode="closest"
    )
    
    return fig
