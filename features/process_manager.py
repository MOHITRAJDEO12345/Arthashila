import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import platform-independent utilities
from utils.platform_utils import get_cpu_info, get_memory_info, get_process_list

def create_gauge_chart(value, title, max_value=100):
    """Create a gauge chart for displaying values like CPU usage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 24, 'color': 'white'}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#4f8bf9"},
            'bgcolor': "#1a1f2c",
            'borderwidth': 2,
            'bordercolor': "#2d3747",
            'steps': [
                {'range': [0, max_value * 0.5], 'color': 'rgba(79, 139, 249, 0.3)'},
                {'range': [max_value * 0.5, max_value * 0.8], 'color': 'rgba(79, 139, 249, 0.6)'},
                {'range': [max_value * 0.8, max_value], 'color': 'rgba(79, 139, 249, 0.9)'}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="#0e1117",
        font={'color': "white", 'family': "Arial"},
        height=200,
        margin=dict(l=20, r=20, b=20, t=40),
    )
    
    return fig

def get_process_color(cpu_percent):
    """Return color based on CPU usage."""
    if cpu_percent < 5:
        return "#0cce6b"  # Green for low usage
    elif cpu_percent < 25:
        return "#4f8bf9"  # Blue for medium usage
    elif cpu_percent < 60:
        return "#f9a825"  # Orange/Yellow for high usage
    else:
        return "#ff4b4b"  # Red for very high usage

def format_bytes(bytes_value):
    """Format bytes into a readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

# Cache for UI components to reduce re-rendering overhead
@st.cache_data(ttl=5, show_spinner=False)
def create_process_charts(top_processes):
    """Create charts for top processes with caching to reduce rendering overhead"""
    charts = {}
    
    if not top_processes:
        return charts
    
    # CPU Usage Bar Chart
    cpu_df = pd.DataFrame([
        {"Process": f"{p['name']} (PID: {p['pid']})", "CPU (%)": p['cpu_percent']} 
        for p in top_processes
    ])
    
    cpu_fig = px.bar(
        cpu_df,
        x="CPU (%)",
        y="Process",
        orientation='h',
        color="CPU (%)",
        color_continuous_scale=px.colors.sequential.Blues,
        title="CPU Usage by Process"
    )
    cpu_fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300,
        margin=dict(l=0, r=10, t=40, b=0),
    )
    charts['cpu'] = cpu_fig
    
    # Memory Usage Bar Chart
    mem_df = pd.DataFrame([
        {"Process": f"{p['name']} (PID: {p['pid']})", "Memory (MB)": p['memory_mb']} 
        for p in top_processes
    ])
    
    mem_fig = px.bar(
        mem_df,
        x="Memory (MB)",
        y="Process",
        orientation='h',
        color="Memory (MB)",
        color_continuous_scale=px.colors.sequential.Blues,
        title="Memory Usage by Process"
    )
    mem_fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300,
        margin=dict(l=0, r=10, t=40, b=0)
    )
    charts['memory'] = mem_fig
    
    return charts

# Cache gauge charts to reduce rendering overhead
@st.cache_data(ttl=2, show_spinner=False)
def get_gauge_charts(cpu_percent, memory_percent):
    """Create gauge charts with caching to reduce rendering overhead"""
    cpu_fig = create_gauge_chart(cpu_percent, "CPU Usage (%)")
    mem_fig = create_gauge_chart(memory_percent, "Memory Usage (%)")
    return cpu_fig, mem_fig

def process_manager():
    st.title("⚙️ Process Manager")
    st.markdown("Monitor and manage system processes in real-time")
    
    # Current time - update less frequently
    if 'last_time_update' not in st.session_state:
        st.session_state.last_time_update = datetime.now()
        st.session_state.last_time_str = st.session_state.last_time_update.strftime('%Y-%m-%d %H:%M:%S')
    
    # Only update time string every 5 seconds
    current_time = datetime.now()
    if (current_time - st.session_state.last_time_update).total_seconds() > 5:
        st.session_state.last_time_update = current_time
        st.session_state.last_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    st.markdown(f"<div style='color: #888888; margin-bottom: 20px;'>Last updated: {st.session_state.last_time_str}</div>", unsafe_allow_html=True)
    
    # System resource overview using platform-independent utilities
    # Use session state to avoid recalculating these values too frequently
    if 'last_resource_update' not in st.session_state or \
       (current_time - st.session_state.get('last_resource_update', datetime.min)).total_seconds() > 2:
        
        cpu_info = get_cpu_info()
        memory_info = get_memory_info()
        
        # Calculate CPU percent as average of all cores
        cpu_percent = sum(cpu_info["per_core_usage"]) / len(cpu_info["per_core_usage"]) if cpu_info["per_core_usage"] else 0
        memory_percent = memory_info["virtual"]["percent"]
        
        # Store in session state
        st.session_state.cpu_info = cpu_info
        st.session_state.memory_info = memory_info
        st.session_state.cpu_percent = cpu_percent
        st.session_state.memory_percent = memory_percent
        st.session_state.last_resource_update = current_time
    else:
        # Use cached values
        cpu_info = st.session_state.cpu_info
        memory_info = st.session_state.memory_info
        cpu_percent = st.session_state.cpu_percent
        memory_percent = st.session_state.memory_percent
    
    # Get cached gauge charts
    cpu_fig, mem_fig = get_gauge_charts(cpu_percent, memory_percent)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(cpu_fig, use_container_width=True)
    with col2:
        st.plotly_chart(mem_fig, use_container_width=True)
    
    # Process management options
    st.markdown("## 🔍 Process List")
    
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        sort_by = st.selectbox(
            "Sort by",
            options=["CPU Usage (%)", "Memory Usage (MB)", "Process ID", "Process Name"],
            index=0
        )
    
    with filter_col2:
        search_term = st.text_input("Search Process", placeholder="Enter process name...")
    
    # Map sort options to parameters
    sort_map = {
        "CPU Usage (%)": "cpu_percent",
        "Memory Usage (MB)": "memory_mb",
        "Process ID": "pid",
        "Process Name": "name"
    }
    sort_by_param = sort_map.get(sort_by, "cpu_percent")
    
    # Get processes using platform-independent function with caching
    processes = get_process_list(sort_by=sort_by_param, search_term=search_term)
    
    # Display top resource-consuming processes
    top_processes = processes[:5]
    
    # Top processes visualization with caching
    if top_processes:
        st.markdown("### Top Resource-Consuming Processes")
        
        # Get cached charts
        charts = create_process_charts(top_processes)
        
        if 'cpu' in charts:
            st.plotly_chart(charts['cpu'], use_container_width=True)
        
        if 'memory' in charts:
            st.plotly_chart(charts['memory'], use_container_width=True)
    
    # Process list with pagination for better performance
    st.markdown("### All Processes")
    
    if not processes:
        st.info("No processes found matching your criteria.")
    else:
        # Pagination controls to reduce rendering overhead
        total_processes = len(processes)
        items_per_page = 20  # Reduced from 100 to improve performance
        
        # Initialize pagination state if not exists
        if 'process_page' not in st.session_state:
            st.session_state.process_page = 0
            
        # Calculate total pages
        total_pages = (total_processes + items_per_page - 1) // items_per_page
        
        # Pagination controls
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("◀ Previous", disabled=st.session_state.process_page <= 0):
                st.session_state.process_page -= 1
                st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center;'>Page {st.session_state.process_page + 1} of {max(1, total_pages)}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Next ▶", disabled=st.session_state.process_page >= total_pages - 1):
                st.session_state.process_page += 1
                st.rerun()
        
        # Get current page of processes
        start_idx = st.session_state.process_page * items_per_page
        end_idx = min(start_idx + items_per_page, total_processes)
        current_page_processes = processes[start_idx:end_idx]
        
        # Display processes for current page only
        for i, proc in enumerate(current_page_processes):
            with st.container():
                # Calculate color based on CPU usage
                cpu_color = get_process_color(proc['cpu_percent'])
                
                with st.expander(f"{proc['name']} (PID: {proc['pid']})", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Process Name:** {proc['name']}")
                        st.markdown(f"**PID:** {proc['pid']}")
                        st.markdown(f"**User:** {proc['username']}")
                        st.markdown(f"**Status:** {proc['status']}")
                        st.markdown(f"**Started:** {proc['create_time']}")
                    
                    with col2:
                        # CPU Usage
                        st.markdown("**CPU Usage**")
                        st.progress(min(proc['cpu_percent'] / 100, 1.0))
                        st.markdown(f"<div style='text-align: right; color: {cpu_color};'>{proc['cpu_percent']:.2f}%</div>", unsafe_allow_html=True)
                        
                        # Memory Usage - calculate percentage more efficiently
                        st.markdown("**Memory Usage**")
                        # Use cached memory info from session state
                        total_memory_mb = memory_info["virtual"]["total"] / (1024 * 1024)
                        memory_percent = min(proc['memory_mb'] / total_memory_mb * 100, 100) if total_memory_mb > 0 else 0
                        st.progress(memory_percent / 100)
                        st.markdown(f"<div style='text-align: right;'>{proc['memory_mb']:.2f} MB</div>", unsafe_allow_html=True)
                        
                        # Terminate process button - use unique key based on page and index
                        button_key = f"terminate_{proc['pid']}_{st.session_state.process_page}_{i}"
                        if st.button("Terminate Process", key=button_key):
                            try:
                                process = psutil.Process(proc['pid'])
                                process.terminate()
                                st.success(f"Process {proc['name']} (PID: {proc['pid']}) terminated successfully!")
                                time.sleep(0.5)  # Reduced sleep time
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error terminating process: {str(e)}")
    
    # Auto refresh option with configurable interval
    st.markdown("---")
    refresh_col1, refresh_col2 = st.columns([1, 3])
    with refresh_col1:
        auto_refresh = st.checkbox("Auto Refresh")
    
    with refresh_col2:
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval (seconds)", min_value=2, max_value=30, value=5, step=1)
            time.sleep(refresh_interval)
            st.rerun()
        else:
            st.slider("Refresh Interval (seconds)", min_value=2, max_value=30, value=5, step=1, disabled=True)