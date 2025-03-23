# Arthashila — Pillar of Purpose

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Streamlit-1.24.0+-red.svg" alt="Streamlit 1.24.0+">
</div>

## 🔍 Overview

Arthashila ("Pillar of Purpose") is a comprehensive system monitoring and task management application built with Streamlit. It provides real-time insights into system resources, process management, performance metrics, and battery usage, along with productivity features like task planning and team collaboration tools.

## ✨ Features

### 📊 System Overview
- Real-time monitoring of CPU, memory, and disk usage
- Detailed system information display including OS, processor, and memory specifications
- Clean visualization of system metrics using modern UI components

### 🔄 Process Management
- View and manage running processes
- Terminate unresponsive applications
- Monitor process resource consumption
- Process priority management

### 📈 Performance Graphs
- Historical tracking of system resource usage
- Interactive charts for CPU, memory, and disk metrics
- Timeline visualization for system performance analysis

### 🔋 Battery Management
- Real-time battery status monitoring
- Remaining time estimation
- Power-saving tips and recommendations
- Battery usage statistics

### 📝 Task Planning
- Create, manage, and prioritize tasks
- Set due dates and task categories
- Progress tracking and completion status
- Task filtering and organization

### 👥 Team Collaboration Tools
- Messaging and communication features
- Shared task management
- Team coordination tools
- Activity tracking and updates

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Option 1: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Arthashila.git
cd Arthashila
```

### Option 2: Install Dependencies Directly

Install the required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Start the application:
```bash
streamlit run main.py
```

The application will launch in your default web browser, typically at http://localhost:8501.

## 📁 Project Structure

```
Arthashila/
├── main.py                 # Main application entry point
├── requirements.txt        # Project dependencies
├── setup.py                # Package installation configuration
├── README.md               # Project documentation
├── features/               # Feature modules
│   ├── __init__.py         # Package initialization
│   ├── system_overview.py  # System monitoring functionality
│   ├── process_manager.py  # Process management tools
│   ├── performance_graphs.py  # Performance visualization
│   ├── battery_management.py  # Battery monitoring tools
│   ├── task_planning.py    # Task planning functionality
│   └── collaboration_tools.py  # Team collaboration features
└── utils/                  # Utility functions and helpers
    ├── __init__.py         # Package initialization
    ├── helpers.py          # Helper functions
    └── visualization.py    # Visualization utilities
```

## 🧩 Architecture

Arthashila follows a modular architecture where each feature is implemented as a separate module within the `features` package. The main application (`main.py`) provides the UI framework and navigation, while the individual feature modules implement specific functionality.

Key components:
- **Main App**: Handles navigation, styling, and routing to feature modules
- **Feature Modules**: Self-contained implementations of specific features
- **Utils**: Shared utility functions used across multiple features

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please ensure your code follows the project's coding style and includes appropriate documentation.

## 📚 Documentation

Each module and function in the codebase is documented with docstrings following the Google Python Style Guide. To generate the documentation locally, you can use tools like Sphinx.

## 📋 Requirements

- Python 3.7+
- streamlit>=1.24.0
- streamlit-option-menu>=0.3.2
- psutil>=5.9.0
- plotly>=5.13.0
- tabulate>=0.9.0

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- Arthashila Team

## 🔗 Links

- [GitHub Repository](https://github.com/yourusername/Arthashila)
- [Report Issues](https://github.com/yourusername/Arthashila/issues) 
