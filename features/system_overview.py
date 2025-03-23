import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import get_size
from utils.platform_utils import get_system_info, get_cpu_info, get_memory_info, get_disk_info

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

def system_overview():
    st.title("🖥️ System Overview")
    st.markdown("View detailed information about your system hardware and software")
    
    # Current time
    st.markdown(f"<div style='color: #888888; margin-bottom: 20px;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
    
    # Quick Stats in cards using platform-independent utilities
    col1, col2, col3 = st.columns(3)
    
    # Get system metrics using platform-independent functions
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    
    # Calculate CPU percent as average of all cores
    cpu_percent = sum(cpu_info["per_core_usage"]) / len(cpu_info["per_core_usage"]) if cpu_info["per_core_usage"] else 0
    memory_percent = memory_info["virtual"]["percent"]
    disk_percent = disk_info[0]["percent"] if disk_info else 0
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="text-align: center; color: #4f8bf9;">CPU Usage</h3>
            <div style="font-size: 2.5rem; text-align: center; font-weight: bold;">{:.1f}%</div>
        </div>
        """.format(cpu_percent), unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="text-align: center; color: #4f8bf9;">Memory Usage</h3>
            <div style="font-size: 2.5rem; text-align: center; font-weight: bold;">{:.1f}%</div>
        </div>
        """.format(memory_percent), unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="card">
            <h3 style="text-align: center; color: #4f8bf9;">Disk Usage</h3>
            <div style="font-size: 2.5rem; text-align: center; font-weight: bold;">{:.1f}%</div>
        </div>
        """.format(disk_percent), unsafe_allow_html=True)
    
    # Gauge charts for visual representation using platform-independent metrics
    col1, col2 = st.columns(2)
    
    with col1:
        cpu_fig = create_gauge_chart(cpu_percent, "CPU Usage (%)")
        st.plotly_chart(cpu_fig, use_container_width=True)
    
    with col2:
        mem_fig = create_gauge_chart(memory_percent, "Memory Usage (%)")
        st.plotly_chart(mem_fig, use_container_width=True)
    
    # System Information using platform-independent utilities
    with st.expander("📋 System Information", expanded=True):
        col1, col2 = st.columns(2)
        
        # Get system info using platform-independent function
        sys_info = get_system_info()
        
        with col1:
            st.markdown("#### 🖥️ Hardware")
            hardware_info = [
                ["System", sys_info["system"]],
                ["Node Name", sys_info["node"]],
                ["Machine", sys_info["machine"]],
                ["Processor", sys_info["processor"]]
            ]
            
            for prop, value in hardware_info:
                st.markdown(f"**{prop}:** {value}")
        
        with col2:
            st.markdown("#### 💾 Software")
            software_info = [
                ["OS Release", sys_info["release"]],
                ["OS Version", sys_info["version"]],
                ["Python Version", sys_info["python_version"]],
                ["Platform", sys_info["platform"]]
            ]
            
            for prop, value in software_info:
                st.markdown(f"**{prop}:** {value}")
    
    # CPU Information using platform-independent utilities
    with st.expander("⚡ CPU Information", expanded=True):
        st.markdown("#### CPU Details")
        
        # Get CPU info using platform-independent function
        cpu_details = get_cpu_info()
        
        col1, col2 = st.columns(2)
        
        with col1:
            cpu_core_info = [
                ["Physical Cores", str(cpu_details["physical_cores"])],
                ["Total Cores", str(cpu_details["total_cores"])],
            ]
            
            for prop, value in cpu_core_info:
                st.markdown(f"**{prop}:** {value}")
                
        with col2:
            freq_info = [
                ["Max Frequency", f"{cpu_details['max_frequency']:.2f} MHz" if cpu_details['max_frequency'] else "N/A"],
                ["Min Frequency", f"{cpu_details['min_frequency']:.2f} MHz" if cpu_details['min_frequency'] else "N/A"],
                ["Current Frequency", f"{cpu_details['current_frequency']:.2f} MHz" if cpu_details['current_frequency'] else "N/A"],
            ]
            
            for prop, value in freq_info:
                st.markdown(f"**{prop}:** {value}")
        
        # CPU Usage per core
        st.markdown("#### Per-Core Usage")
        cpu_percents = cpu_details["per_core_usage"]
        
        if cpu_percents:
            cols = st.columns(4)
            for i, (col, percent) in enumerate(zip(cols * (len(cpu_percents) // 4 + 1), cpu_percents)):
                with col:
                    st.markdown(f"**Core {i}**")
                    st.progress(percent / 100)
                    st.markdown(f"<div style='text-align: center;'>{percent}%</div>", unsafe_allow_html=True)
        else:
            st.info("Per-core CPU usage information is not available on this platform.")

    # Memory Information using platform-independent utilities
    with st.expander("🧠 Memory Information", expanded=True):
        # Get memory info using platform-independent function
        mem_info = get_memory_info()
        virtual_mem = mem_info["virtual"]
        swap_mem = mem_info["swap"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### RAM Usage")
            memory_info = [
                ["Total", get_size(virtual_mem["total"])],
                ["Available", get_size(virtual_mem["available"])],
                ["Used", get_size(virtual_mem["used"])],
                ["Percentage", f"{virtual_mem['percent']}%"]
            ]
            
            for prop, value in memory_info:
                st.markdown(f"**{prop}:** {value}")
                
            # RAM Usage Breakdown
            ram_fig = go.Figure()
            ram_fig.add_trace(go.Pie(
                labels=["Used", "Available"],
                values=[virtual_mem["used"], virtual_mem["available"]],
                hole=.4,
                marker_colors=["#4f8bf9", "#1a1f2c"]
            ))
            ram_fig.update_layout(
                title_text="RAM Usage Breakdown",
                paper_bgcolor="#0e1117",
                plot_bgcolor="#0e1117",
                font={'color': "white"},
                height=300
            )
            st.plotly_chart(ram_fig, use_container_width=True)
            
        with col2:
            st.markdown("#### Swap Memory")
            swap_info = [
                ["Total", get_size(swap_mem["total"])],
                ["Free", get_size(swap_mem["free"])],
                ["Used", get_size(swap_mem["used"])],
                ["Percentage", f"{swap_mem['percent']}%"]
            ]
            
            for prop, value in swap_info:
                st.markdown(f"**{prop}:** {value}")
                
            # Swap Usage Breakdown
            swap_fig = go.Figure()
            swap_fig.add_trace(go.Pie(
                labels=["Used", "Free"],
                values=[swap_mem["used"], swap_mem["free"]],
                hole=.4,
                marker_colors=["#4f8bf9", "#1a1f2c"]
            ))
            swap_fig.update_layout(
                title_text="Swap Usage Breakdown",
                paper_bgcolor="#0e1117",
                plot_bgcolor="#0e1117",
                font={'color': "white"},
                height=300
            )
            st.plotly_chart(swap_fig, use_container_width=True)
    
    # Disk Information using platform-independent utilities
    with st.expander("💽 Disk Information", expanded=True):
        st.markdown("#### Disk Partitions")
        
        # Get disk info using platform-independent function
        partitions = get_disk_info()
        
        if not partitions:
            st.info("No disk partitions could be accessed on this system.")
        
        for i, partition in enumerate(partitions):
            st.markdown(f"**Partition {i+1}: {partition['mountpoint']}**")
            st.markdown(f"**Device:** {partition['device']}")
            st.markdown(f"**File System:** {partition['fstype']}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Size", get_size(partition['total']))
            col2.metric("Used", get_size(partition['used']))
            col3.metric("Free", get_size(partition['free']))
            
            st.progress(partition['percent'] / 100)
            st.markdown(f"<div style='text-align: right;'>{partition['percent']}% used</div>", unsafe_allow_html=True)
            st.markdown("---")