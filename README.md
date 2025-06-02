# ⚽ Football Match Analysis Pipeline

A comprehensive Python-based analytics pipeline for processing and analyzing football match event data. This project provides data cleaning, statistical analysis, visualization, and automated reporting capabilities for football performance analysis.

## 🚀 Features

### 📊 **Data Processing**
- **CSV Data Loading** with validation and error handling
- **Data Cleaning** - Remove duplicates, handle missing values, filter columns
- **Categorical Decoding** - Convert numerical codes to human-readable labels
- **Data Validation** - Ensure data integrity throughout the pipeline

### 📈 **Advanced Analytics**
- **Match Overview** - Total events, teams, players, goals
- **Team Performance** - Shooting accuracy, conversion rates, discipline records
- **Player Analysis** - Individual performance metrics and rankings
- **Location Analysis** - Goal patterns by field position, body part, situation
- **Time Analysis** - Event distribution across match periods
- **Disciplinary Analysis** - Cards and fouls breakdown

### 📊 **Professional Visualizations**
- **Event Distribution** charts
- **Team Performance** comparison dashboards
- **Goals Heatmaps** by location and method
- **Time-based Analysis** plots
- **Player Performance** rankings
- **Shot Maps** with field visualization
- **Disciplinary Statistics** breakdowns

### 📋 **Automated Reporting**
- **Comprehensive Text Reports** with professional formatting
- **CSV Data Exports** for further analysis
- **Timestamped Output Files** for version control
- **Dashboard Visualizations** saved as high-resolution images

## 👇 Dowload Dataset
[Kaggle](https://www.kaggle.com/datasets/secareanualin/football-events)

## 🏗️ Project Structure

```
.
├── data/
│   ├── raw/                    # Raw CSV files
│   └── processed/              # Cleaned data outputs
├── output/
│   ├── plot/                   # Generated visualizations
│   └── summaries/              # Reports and analysis exports
├── notebooks/
│   └── demo.ipynb             # Jupyter notebook demos
├── src/
│   ├── __init__.py
│   ├── analyzer.py            # Core analysis functions
│   ├── loader.py              # Data loading utilities
│   ├── cleaner.py             # Data cleaning functions
│   ├── visualizer.py          # Plotting and visualization
│   ├── exporter.py            # Data export utilities
│   └── utils.py               # Helper functions
├── main.py                    # Main execution pipeline
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. **Clone the repository**
```bash
git clone <repository-url>
cd football-analysis-pipeline
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Required Packages
```
pandas
matplotlib
seaborn
numpy
```

## 📊 Data Format

### Input Data Requirements
Place your CSV file in `data/raw/events.csv` with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `id_event` | int | Unique event identifier |
| `time` | int | Match time in minutes |
| `event_type` | int | Event type code (see dictionary) |
| `side` | int | Home (1) or Away (2) |
| `event_team` | str | Team name |
| `opponent` | str | Opponent team name |
| `player` | str | Player name |
| `shot_place` | int | Shot location code |
| `shot_outcome` | int | Shot result code |
| `is_goal` | int | Goal flag (1/0) |
| `location` | int | Field location code |
| `bodypart` | int | Body part used code |
| `assist_method` | int | Assist type code |
| `situation` | int | Play situation code |
| `fast_break` | int | Fast break flag (1/0) |

### Data Dictionary
The system uses the following code mappings (automatically decoded):

**Event Types:**
- 0: Announcement, 1: Attempt, 2: Corner, 3: Foul, 4: Yellow card, etc.

**Locations:**
- 1: Attacking half, 2: Defensive half, 3: Centre of the box, etc.

**Body Parts:**
- 1: Right foot, 2: Left foot, 3: Head

*Full dictionary available in `dictionary.txt`*

## 🚀 Usage

### Run
```bash
python main.py
```

### What It Does
1. **Loads** data from `data/raw/events.csv`
2. **Cleans** and filters the data
3. **Decodes** categorical variables
4. **Performs** comprehensive analysis
5. **Generates** visualizations and reports
6. **Saves** outputs to respective directories

### Customization
Modify `main.py` to:
- **Change input file** name or path
- **Select specific columns** to analyze
- **Adjust analysis parameters**
- **Configure output formats**

### Advanced Usage
```python
from src.loader import load_data_csv
from src.analyzer import analyze_events_overview, team_performance_analysis
from src.visualizer import plot_team_performance

# Load and analyze specific data
df = load_data_csv('your_file.csv')
overview = analyze_events_overview(df)
plot_team_performance(df)
```

## 📈 Output Files

### Reports (`output/summaries/`)
- **`match_analysis_report_YYYYMMDD_HHMMSS.txt`** - Comprehensive text report
- **`processed_events_YYYYMMDD_HHMMSS.csv`** - Cleaned data with decoded labels
- **`team_analysis_YYYYMMDD_HHMMSS.csv`** - Team performance metrics
- **`player_analysis_YYYYMMDD_HHMMSS.csv`** - Player statistics

### Visualizations (`output/plot/`)
- **`event_distribution_YYYYMMDD_HHMMSS.png`** - Event type breakdown
- **`team_performance_YYYYMMDD_HHMMSS.png`** - Team comparison dashboard
- **`goals_heatmap_YYYYMMDD_HHMMSS.png`** - Goal pattern analysis
- **`time_analysis_YYYYMMDD_HHMMSS.png`** - Temporal event distribution
- **`top_10_players_YYYYMMDD_HHMMSS.png`** - Player performance rankings
- **`disciplinary_analysis_YYYYMMDD_HHMMSS.png`** - Cards and fouls analysis
- **`shot_map_YYYYMMDD_HHMMSS.png`** - Field position shot visualization

## 🔧 Configuration

### Custom Analysis Parameters
Modify these in the respective modules:

**Data Cleaning (`src/cleaner.py`):**
```python
# Customize missing value handling
fill_na_cols = {'player': 'Unknown', 'location': 0}
dropna_cols = ['event_type', 'time']
```

**Visualization (`src/visualizer.py`):**
```python
# Adjust plot parameters
figsize=(15, 10)
dpi=300
top_n_players=15
```

### Adding New Analysis Functions
1. Create function in `src/analyzer.py`
2. Add visualization in `src/visualizer.py`
3. Update `main.py` pipeline

