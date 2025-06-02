import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List
import os
from datetime import datetime

# Set style for consistent plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def setup_plot_directory():
    """Create output/plot directory if it doesn't exist"""
    plot_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'plots')
    os.makedirs(plot_dir, exist_ok=True)
    return plot_dir

def save_plot(fig, filename: str, plot_dir: str = None):
    """Save plot with timestamp and proper formatting"""
    if plot_dir is None:
        plot_dir = setup_plot_directory()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if not filename.endswith('.png'):
        filename = f"{filename}_{timestamp}.png"
    else:
        filename = f"{filename[:-4]}_{timestamp}.png"
    
    filepath = os.path.join(plot_dir, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return filepath

def plot_event_distribution(df: pd.DataFrame) -> str:
    """
    Create bar chart of event type distribution
    
    Args:
        df: DataFrame with event_type_label column
        
    Returns:
        Path to saved plot
    """
    if 'event_type_label' not in df.columns:
        raise ValueError("DataFrame must have 'event_type_label' column")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    event_counts = df['event_type_label'].value_counts()
    
    bars = ax.bar(range(len(event_counts)), event_counts.values, 
                  color=sns.color_palette("viridis", len(event_counts)))
    
    ax.set_xlabel('Event Types', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Event Types', fontsize=14, fontweight='bold', pad=20)
    
    # Rotate labels and add values on bars
    ax.set_xticks(range(len(event_counts)))
    ax.set_xticklabels(event_counts.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return save_plot(fig, 'event_distribution')

def plot_team_performance(df: pd.DataFrame) -> str:
    """
    Create team performance comparison chart
    
    Args:
        df: DataFrame with team performance data
        
    Returns:
        Path to saved plot
    """
    from src.analyzer import team_performance_analysis
    
    team_stats = team_performance_analysis(df)
    if team_stats.empty:
        raise ValueError("No team performance data available")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Team Performance Analysis', fontsize=16, fontweight='bold')
    
    # Goals scored
    team_stats['goals_scored'].plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Goals Scored by Team', fontweight='bold')
    ax1.set_ylabel('Goals')
    ax1.tick_params(axis='x', rotation=45)
    
    # Total shots
    if 'total_shots' in team_stats.columns:
        team_stats['total_shots'].plot(kind='bar', ax=ax2, color='lightcoral')
        ax2.set_title('Total Shots by Team', fontweight='bold')
        ax2.set_ylabel('Shots')
        ax2.tick_params(axis='x', rotation=45)
    
    # Shooting accuracy
    if 'shooting_accuracy' in team_stats.columns:
        team_stats['shooting_accuracy'].plot(kind='bar', ax=ax3, color='lightgreen')
        ax3.set_title('Shooting Accuracy by Team (%)', fontweight='bold')
        ax3.set_ylabel('Accuracy %')
        ax3.tick_params(axis='x', rotation=45)
    
    # Conversion rate
    if 'conversion_rate' in team_stats.columns:
        team_stats['conversion_rate'].plot(kind='bar', ax=ax4, color='gold')
        ax4.set_title('Goal Conversion Rate by Team (%)', fontweight='bold')
        ax4.set_ylabel('Conversion %')
        ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return save_plot(fig, 'team_performance')

def plot_goals_heatmap(df: pd.DataFrame) -> str:
    """
    Create heatmap of goals by location and body part
    
    Args:
        df: DataFrame with location and bodypart labels
        
    Returns:
        Path to saved plot
    """
    if 'is_goal' not in df.columns:
        raise ValueError("DataFrame must have 'is_goal' column")
    
    goals_df = df[df['is_goal'] == 1]
    
    if goals_df.empty:
        raise ValueError("No goals found in dataset")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Goals by location heatmap
    if 'location_label' in goals_df.columns and 'bodypart_label' in goals_df.columns:
        crosstab = pd.crosstab(goals_df['location_label'], goals_df['bodypart_label'])
        sns.heatmap(crosstab, annot=True, fmt='d', cmap='YlOrRd', ax=ax1)
        ax1.set_title('Goals by Location and Body Part', fontweight='bold')
        ax1.set_xlabel('Body Part')
        ax1.set_ylabel('Location')
    
    # Goals by situation heatmap
    if 'situation_label' in goals_df.columns and 'assist_method_label' in goals_df.columns:
        crosstab2 = pd.crosstab(goals_df['situation_label'], goals_df['assist_method_label'])
        sns.heatmap(crosstab2, annot=True, fmt='d', cmap='Blues', ax=ax2)
        ax2.set_title('Goals by Situation and Assist Method', fontweight='bold')
        ax2.set_xlabel('Assist Method')
        ax2.set_ylabel('Situation')
    
    plt.tight_layout()
    return save_plot(fig, 'goals_heatmap')

def plot_time_analysis(df: pd.DataFrame) -> str:
    """
    Create time-based analysis plots
    
    Args:
        df: DataFrame with time column
        
    Returns:
        Path to saved plot
    """
    if 'time' not in df.columns:
        raise ValueError("DataFrame must have 'time' column")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Time-Based Event Analysis', fontsize=16, fontweight='bold')
    
    # Create time bins
    df_time = df.copy()
    df_time['time_bin'] = pd.cut(df_time['time'], 
                                bins=[0, 15, 30, 45, 60, 75, 90, float('inf')],
                                labels=['0-15', '15-30', '30-45', '45-60', '60-75', '75-90', '90+'])
    
    # Events by time period
    time_events = df_time['time_bin'].value_counts().sort_index()
    time_events.plot(kind='bar', ax=ax1, color='steelblue')
    ax1.set_title('Events by Time Period', fontweight='bold')
    ax1.set_ylabel('Number of Events')
    ax1.set_xlabel('Time Period (minutes)')
    ax1.tick_params(axis='x', rotation=0)
    
    # Goals by time period
    if 'is_goal' in df_time.columns:
        goals_time = df_time[df_time['is_goal'] == 1]['time_bin'].value_counts().sort_index()
        goals_time.plot(kind='bar', ax=ax2, color='crimson')
        ax2.set_title('Goals by Time Period', fontweight='bold')
        ax2.set_ylabel('Number of Goals')
        ax2.set_xlabel('Time Period (minutes)')
        ax2.tick_params(axis='x', rotation=0)
    
    # Timeline of goals
    if 'is_goal' in df_time.columns:
        goals_timeline = df_time[df_time['is_goal'] == 1]['time']
        ax3.scatter(goals_timeline, [1]*len(goals_timeline), alpha=0.6, s=100, color='red')
        ax3.set_xlim(0, 95)
        ax3.set_ylim(0.5, 1.5)
        ax3.set_xlabel('Match Time (minutes)')
        ax3.set_title('Goal Timeline', fontweight='bold')
        ax3.set_yticks([])
        ax3.grid(True, alpha=0.3)
    
    # Event intensity over time
    time_histogram = df_time['time'].hist(bins=20, ax=ax4, color='orange', alpha=0.7)
    ax4.set_title('Event Intensity Over Time', fontweight='bold')
    ax4.set_xlabel('Match Time (minutes)')
    ax4.set_ylabel('Number of Events')
    
    plt.tight_layout()
    return save_plot(fig, 'time_analysis')

def plot_player_performance(df: pd.DataFrame, top_n: int = 10) -> str:
    """
    Create player performance visualizations
    
    Args:
        df: DataFrame with player data
        top_n: Number of top players to show
        
    Returns:
        Path to saved plot
    """
    from src.analyzer import player_performance_analysis
    
    player_stats = player_performance_analysis(df)
    if player_stats.empty:
        raise ValueError("No player performance data available")
    
    # Get top players by goals
    top_players = player_stats.head(top_n)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Top {top_n} Player Performance Analysis', fontsize=16, fontweight='bold')
    
    # Goals scored
    player_names = [f"{idx[0]}\n({idx[1]})" for idx in top_players.index]
    ax1.bar(range(len(top_players)), top_players['goals'], color='gold')
    ax1.set_title('Goals Scored', fontweight='bold')
    ax1.set_ylabel('Goals')
    ax1.set_xticks(range(len(top_players)))
    ax1.set_xticklabels(player_names, rotation=45, ha='right')
    
    # Add value labels
    for i, v in enumerate(top_players['goals']):
        ax1.text(i, v + 0.1, str(int(v)), ha='center', fontweight='bold')
    
    # Shots taken (if available)
    if 'shots_taken' in top_players.columns:
        ax2.bar(range(len(top_players)), top_players['shots_taken'], color='skyblue')
        ax2.set_title('Shots Taken', fontweight='bold')
        ax2.set_ylabel('Shots')
        ax2.set_xticks(range(len(top_players)))
        ax2.set_xticklabels(player_names, rotation=45, ha='right')
    
    # Conversion rate (if available)
    if 'conversion_rate' in top_players.columns:
        ax3.bar(range(len(top_players)), top_players['conversion_rate'], color='lightgreen')
        ax3.set_title('Conversion Rate (%)', fontweight='bold')
        ax3.set_ylabel('Conversion %')
        ax3.set_xticks(range(len(top_players)))
        ax3.set_xticklabels(player_names, rotation=45, ha='right')
    
    # Goals vs Shots scatter plot
    if 'shots_taken' in top_players.columns:
        ax4.scatter(top_players['shots_taken'], top_players['goals'], 
                   s=100, alpha=0.7, color='purple')
        ax4.set_xlabel('Shots Taken')
        ax4.set_ylabel('Goals Scored')
        ax4.set_title('Goals vs Shots Efficiency', fontweight='bold')
        
        # Add player labels to points
        for i, (shots, goals) in enumerate(zip(top_players['shots_taken'], top_players['goals'])):
            player_name = top_players.index[i][0][:10]  # Truncate long names
            ax4.annotate(player_name, (shots, goals), xytext=(5, 5), 
                        textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    return save_plot(fig, f'top_{top_n}_players')

def plot_disciplinary_analysis(df: pd.DataFrame) -> str:
    """
    Create disciplinary analysis visualizations
    
    Args:
        df: DataFrame with disciplinary data
        
    Returns:
        Path to saved plot
    """
    if 'event_type_label' not in df.columns:
        raise ValueError("DataFrame must have 'event_type_label' column")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Disciplinary Analysis', fontsize=16, fontweight='bold')
    
    # Card distribution
    card_events = df[df['event_type_label'].isin(['Yellow card', 'Red card', 'Second yellow card'])]
    if not card_events.empty:
        card_counts = card_events['event_type_label'].value_counts()
        colors = ['yellow', 'red', 'orange']
        ax1.pie(card_counts.values, labels=card_counts.index, autopct='%1.1f%%', 
                colors=colors[:len(card_counts)])
        ax1.set_title('Card Distribution', fontweight='bold')
    
    # Cards by team
    if 'event_team' in card_events.columns and not card_events.empty:
        team_cards = card_events.groupby('event_team')['event_type_label'].count().sort_values(ascending=True)
        team_cards.plot(kind='barh', ax=ax2, color='coral')
        ax2.set_title('Total Cards by Team', fontweight='bold')
        ax2.set_xlabel('Number of Cards')
    
    # Fouls over time
    fouls = df[df['event_type_label'] == 'Foul']
    if not fouls.empty and 'time' in fouls.columns:
        fouls['time_bin'] = pd.cut(fouls['time'], 
                                  bins=[0, 15, 30, 45, 60, 75, 90, float('inf')],
                                  labels=['0-15', '15-30', '30-45', '45-60', '60-75', '75-90', '90+'])
        foul_time = fouls['time_bin'].value_counts().sort_index()
        foul_time.plot(kind='bar', ax=ax3, color='darkred')
        ax3.set_title('Fouls by Time Period', fontweight='bold')
        ax3.set_ylabel('Number of Fouls')
        ax3.tick_params(axis='x', rotation=0)
    
    # Cards vs Fouls by team
    if 'event_team' in df.columns:
        team_fouls = df[df['event_type_label'] == 'Foul'].groupby('event_team').size()
        team_cards_count = card_events.groupby('event_team').size() if not card_events.empty else pd.Series()
        
        # Align indices
        teams = list(set(team_fouls.index.tolist() + team_cards_count.index.tolist()))
        fouls_aligned = [team_fouls.get(team, 0) for team in teams]
        cards_aligned = [team_cards_count.get(team, 0) for team in teams]
        
        x = np.arange(len(teams))
        width = 0.35
        
        ax4.bar(x - width/2, fouls_aligned, width, label='Fouls', color='lightcoral')
        ax4.bar(x + width/2, cards_aligned, width, label='Cards', color='gold')
        ax4.set_title('Fouls vs Cards by Team', fontweight='bold')
        ax4.set_xlabel('Teams')
        ax4.set_ylabel('Count')
        ax4.set_xticks(x)
        ax4.set_xticklabels(teams, rotation=45)
        ax4.legend()
    
    plt.tight_layout()
    return save_plot(fig, 'disciplinary_analysis')

def create_dashboard(df: pd.DataFrame) -> List[str]:
    """
    Create complete visualization dashboard
    
    Args:
        df: Cleaned and decoded DataFrame
        
    Returns:
        List of paths to saved plots
    """
    saved_plots = []
    plot_dir = setup_plot_directory()
    
    print("Creating visualization dashboard...")
    
    try:
        # Event distribution
        print("  📊 Creating event distribution plot...")
        saved_plots.append(plot_event_distribution(df))
        
        # Team performance
        print("  🏆 Creating team performance plots...")
        saved_plots.append(plot_team_performance(df))
        
        # Goals heatmap
        print("  🎯 Creating goals heatmap...")
        saved_plots.append(plot_goals_heatmap(df))
        
        # Time analysis
        print("  ⏰ Creating time analysis plots...")
        saved_plots.append(plot_time_analysis(df))
        
        # Player performance
        print("  👤 Creating player performance plots...")
        saved_plots.append(plot_player_performance(df, top_n=10))
        
        # Disciplinary analysis
        print("  🟨 Creating disciplinary analysis plots...")
        saved_plots.append(plot_disciplinary_analysis(df))
        
        print(f"✅ Dashboard created! {len(saved_plots)} plots saved to: {plot_dir}")
        
    except Exception as e:
        print(f"❌ Error creating plot: {e}")
    
    return saved_plots

def plot_shot_map(df: pd.DataFrame) -> str:
    """
    Create a shot map visualization (simplified field representation)
    
    Args:
        df: DataFrame with shot data
        
    Returns:
        Path to saved plot
    """
    if 'event_type_label' not in df.columns:
        raise ValueError("DataFrame must have 'event_type_label' column")
    
    shots_df = df[df['event_type_label'] == 'Attempt']
    
    if shots_df.empty:
        raise ValueError("No shots found in dataset")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create simplified field zones based on location labels
    location_coords = {
        'Centre of the box': (0.5, 0.3),
        'Left side of the box': (0.3, 0.3),
        'Right side of the box': (0.7, 0.3),
        'Penalty spot': (0.5, 0.2),
        'Left side of the six yard box': (0.4, 0.1),
        'Right side of the six yard box': (0.6, 0.1),
        'Very close range': (0.5, 0.05),
        'Outside the box': (0.5, 0.5),
        'Long range': (0.5, 0.7),
        'Left wing': (0.2, 0.4),
        'Right wing': (0.8, 0.4),
    }
    
    # Plot shots
    for _, shot in shots_df.iterrows():
        location = shot.get('location_label', 'Unknown')
        is_goal = shot.get('is_goal', 0)
        
        if location in location_coords:
            x, y = location_coords[location]
            # Add some random jitter to avoid overlapping
            x += np.random.normal(0, 0.02)
            y += np.random.normal(0, 0.02)
            
            color = 'red' if is_goal else 'blue'
            size = 100 if is_goal else 50
            alpha = 0.8 if is_goal else 0.5
            
            ax.scatter(x, y, c=color, s=size, alpha=alpha)
    
    # Draw simplified field
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    
    # Add field elements
    from matplotlib.patches import Rectangle
    
    # Goal area
    goal_area = Rectangle((0.4, 0), 0.2, 0.1, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(goal_area)
    
    # Penalty area
    penalty_area = Rectangle((0.25, 0), 0.5, 0.35, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(penalty_area)
    
    ax.set_title('Shot Map (Goals in Red, Shots in Blue)', fontweight='bold', fontsize=14)
    ax.set_xlabel('Field Width')
    ax.set_ylabel('Distance from Goal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return save_plot(fig, 'shot_map')