import pandas as pd
from typing import Dict

# Event type mappings from dictionary
EVENT_TYPES = {
    0: "Announcement", 1: "Attempt", 2: "Corner", 3: "Foul", 4: "Yellow card",
    5: "Second yellow card", 6: "Red card", 7: "Substitution", 8: "Free kick won",
    9: "Offside", 10: "Hand ball", 11: "Penalty conceded", 12: "Key Pass",
    13: "Failed through ball", 14: "Sending off", 15: "Own goal"
}

SHOT_OUTCOMES = {
    1: "On target", 2: "Off target", 3: "Blocked", 4: "Hit the bar"
}

LOCATIONS = {
    1: "Attacking half", 2: "Defensive half", 3: "Centre of the box",
    4: "Left wing", 5: "Right wing", 6: "Difficult angle and long range",
    7: "Difficult angle on the left", 8: "Difficult angle on the right",
    9: "Left side of the box", 10: "Left side of the six yard box",
    11: "Right side of the box", 12: "Right side of the six yard box",
    13: "Very close range", 14: "Penalty spot", 15: "Outside the box",
    16: "Long range", 17: "More than 35 yards", 18: "More than 40 yards"
}

BODY_PARTS = {1: "right foot", 2: "left foot", 3: "head"}
ASSIST_METHODS = {0: "None", 1: "Pass", 2: "Cross", 3: "Headed pass", 4: "Through ball"}
SITUATIONS = {1: "Open play", 2: "Set piece", 3: "Corner", 4: "Free kick"}
SIDES = {1: "Home", 2: "Away"}


def decode_categorical_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Decode numerical categories to human-readable labels
    
    Args:
        df: DataFrame with encoded categorical columns
        
    Returns:
        DataFrame with decoded categorical columns
    """
    df_decoded = df.copy()
    
    # Decode categorical columns
    if 'event_type' in df_decoded.columns:
        df_decoded['event_type_label'] = df_decoded['event_type'].map(EVENT_TYPES)
    
    if 'shot_outcome' in df_decoded.columns:
        df_decoded['shot_outcome_label'] = df_decoded['shot_outcome'].map(SHOT_OUTCOMES)
        
    if 'location' in df_decoded.columns:
        df_decoded['location_label'] = df_decoded['location'].map(LOCATIONS)
        
    if 'bodypart' in df_decoded.columns:
        df_decoded['bodypart_label'] = df_decoded['bodypart'].map(BODY_PARTS)
        
    if 'assist_method' in df_decoded.columns:
        df_decoded['assist_method_label'] = df_decoded['assist_method'].map(ASSIST_METHODS)
        
    if 'situation' in df_decoded.columns:
        df_decoded['situation_label'] = df_decoded['situation'].map(SITUATIONS)
    
    if 'side' in df_decoded.columns:
        df_decoded['side_label'] = df_decoded['side'].map(SIDES)
    
    return df_decoded


def analyze_events_overview(df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive event analysis using human-readable labels
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        Dictionary with analysis results
    """
    stats = {
        'total_events': len(df),
        'unique_teams': df['event_team'].nunique() if 'event_team' in df.columns else 0,
        'unique_players': df['player'].nunique() if 'player' in df.columns else 0,
        'total_goals': df['is_goal'].sum() if 'is_goal' in df.columns else 0,
    }
    
    # Home vs Away breakdown with labels
    if 'side_label' in df.columns:
        stats['home_vs_away'] = df['side_label'].value_counts().to_dict()
    
    # Event type breakdown with labels
    if 'event_type_label' in df.columns:
        stats['event_breakdown'] = df['event_type_label'].value_counts().to_dict()
    
    # Shot analysis using labels
    if 'event_type_label' in df.columns:
        shot_events = df[df['event_type_label'] == 'Attempt']
        if not shot_events.empty:
            stats['shot_analysis'] = {
                'total_shots': len(shot_events),
                'shots_on_target': len(shot_events[shot_events['shot_outcome_label'] == 'On target']) if 'shot_outcome_label' in shot_events.columns else 0,
                'conversion_rate': round((shot_events['is_goal'].sum() / len(shot_events)) * 100, 2) if 'is_goal' in shot_events.columns else 0
            }
            
            # Shot outcome breakdown
            if 'shot_outcome_label' in shot_events.columns:
                stats['shot_outcome_breakdown'] = shot_events['shot_outcome_label'].value_counts().to_dict()
    
    return stats


def team_performance_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze team performance metrics with readable labels
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        DataFrame with team performance stats
    """
    if 'event_team' not in df.columns:
        return pd.DataFrame()
    
    # Basic team stats
    team_stats = df.groupby('event_team').agg({
        'is_goal': 'sum',
        'id_event': 'count'
    }).rename(columns={'is_goal': 'goals_scored', 'id_event': 'total_events'})
    
    # Shot-specific analysis using labels
    if 'event_type_label' in df.columns:
        shots_df = df[df['event_type_label'] == 'Attempt']
        if not shots_df.empty:
            shot_stats = shots_df.groupby('event_team').agg({
                'id_event': 'count',
                'is_goal': 'sum'
            }).rename(columns={
                'id_event': 'total_shots',
                'is_goal': 'goals_from_shots'
            })
            
            # Count shots on target using labels
            if 'shot_outcome_label' in shots_df.columns:
                shots_on_target = shots_df[shots_df['shot_outcome_label'] == 'On target'].groupby('event_team').size()
                shot_stats['shots_on_target'] = shots_on_target
            
            # Calculate percentages
            shot_stats['shooting_accuracy'] = ((shot_stats['shots_on_target'] / shot_stats['total_shots']) * 100).round(2)
            shot_stats['conversion_rate'] = ((shot_stats['goals_from_shots'] / shot_stats['total_shots']) * 100).round(2)
            
            # Merge with team stats
            team_stats = team_stats.merge(shot_stats, left_index=True, right_index=True, how='left')
    
    # Fill NaN values with 0
    team_stats = team_stats.fillna(0)
    return team_stats


def player_performance_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze individual player performance with readable data
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        DataFrame with player performance stats
    """
    if 'player' not in df.columns:
        return pd.DataFrame()
    
    # Basic player stats
    player_stats = df.groupby(['player', 'event_team']).agg({
        'is_goal': 'sum',
        'id_event': 'count'
    }).rename(columns={'is_goal': 'goals', 'id_event': 'total_events'})
    
    # Shot analysis for players using labels
    if 'event_type_label' in df.columns:
        shots_df = df[df['event_type_label'] == 'Attempt']
        if not shots_df.empty:
            player_shots = shots_df.groupby(['player', 'event_team']).agg({
                'id_event': 'count',
                'is_goal': 'sum'
            }).rename(columns={
                'id_event': 'shots_taken',
                'is_goal': 'goals_scored'
            })
            
            # Count shots on target using labels
            if 'shot_outcome_label' in shots_df.columns:
                shots_on_target = shots_df[shots_df['shot_outcome_label'] == 'On target'].groupby(['player', 'event_team']).size()
                player_shots['shots_on_target'] = shots_on_target
            
            # Calculate conversion rate
            player_shots['conversion_rate'] = ((player_shots['goals_scored'] / player_shots['shots_taken']) * 100).round(2)
            
            # Merge with player stats
            player_stats = player_stats.merge(player_shots, left_index=True, right_index=True, how='left')
    
    # Fill NaN values and sort by goals
    player_stats = player_stats.fillna(0)
    return player_stats.sort_values('goals', ascending=False)


def location_analysis(df: pd.DataFrame) -> Dict:
    """
    Analyze goal scoring by location and situation using labels
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        Dictionary with location-based analysis
    """
    if 'is_goal' not in df.columns:
        return {}
    
    goals_df = df[df['is_goal'] == 1]
    
    if goals_df.empty:
        return {}
    
    analysis = {}
    
    # Goals by location using labels
    if 'location_label' in goals_df.columns:
        analysis['goals_by_location'] = goals_df['location_label'].value_counts().to_dict()
    
    # Goals by body part using labels
    if 'bodypart_label' in goals_df.columns:
        analysis['goals_by_bodypart'] = goals_df['bodypart_label'].value_counts().to_dict()
    
    # Goals by situation using labels
    if 'situation_label' in goals_df.columns:
        analysis['goals_by_situation'] = goals_df['situation_label'].value_counts().to_dict()
    
    # Goals by assist method using labels
    if 'assist_method_label' in goals_df.columns:
        analysis['goals_by_assist'] = goals_df['assist_method_label'].value_counts().to_dict()
    
    # Goals by side (home/away) using labels
    if 'side_label' in goals_df.columns:
        analysis['goals_by_side'] = goals_df['side_label'].value_counts().to_dict()
    
    return analysis


def disciplinary_analysis(df: pd.DataFrame) -> Dict:
    """
    Analyze cards and fouls using readable labels
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        Dictionary with disciplinary stats
    """
    if 'event_type_label' not in df.columns:
        return {}
    
    # Card and foul events using labels
    cards_df = df[df['event_type_label'].isin(['Yellow card', 'Second yellow card', 'Red card'])]
    fouls_df = df[df['event_type_label'] == 'Foul']
    
    analysis = {
        'total_fouls': len(fouls_df),
        'yellow_cards': len(df[df['event_type_label'] == 'Yellow card']),
        'red_cards': len(df[df['event_type_label'] == 'Red card']),
        'second_yellow_cards': len(df[df['event_type_label'] == 'Second yellow card']),
        'total_cards': len(cards_df)
    }
    
    # Team discipline breakdown
    if 'event_team' in df.columns and not cards_df.empty:
        team_cards = cards_df.groupby('event_team')['event_type_label'].count().sort_values(ascending=False)
        analysis['most_cards_by_team'] = team_cards.to_dict()
        
        # Card type breakdown by team
        card_breakdown = cards_df.groupby(['event_team', 'event_type_label']).size().unstack(fill_value=0)
        analysis['card_breakdown_by_team'] = card_breakdown.to_dict()
    
    # Foul breakdown by team
    if 'event_team' in df.columns and not fouls_df.empty:
        team_fouls = fouls_df.groupby('event_team').size().sort_values(ascending=False)
        analysis['most_fouls_by_team'] = team_fouls.to_dict()
    
    return analysis


def time_analysis(df: pd.DataFrame) -> Dict:
    """
    Analyze events by time periods
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        Dictionary with time-based analysis
    """
    if 'time' not in df.columns:
        return {}
    
    analysis = {}
    
    # Define time periods
    df_time = df.copy()
    df_time['time_period'] = pd.cut(df_time['time'], 
                                   bins=[0, 15, 30, 45, 60, 75, 90, float('inf')],
                                   labels=['0-15min', '15-30min', '30-45min', '45-60min', '60-75min', '75-90min', '90+min'])
    
    # Events by time period
    if 'event_type_label' in df_time.columns:
        time_events = df_time.groupby(['time_period', 'event_type_label']).size().unstack(fill_value=0)
        analysis['events_by_time_period'] = time_events.to_dict()
    
    # Goals by time period
    if 'is_goal' in df_time.columns:
        goals_by_time = df_time[df_time['is_goal'] == 1]['time_period'].value_counts().sort_index()
        analysis['goals_by_time_period'] = goals_by_time.to_dict()
    
    return analysis


def generate_summary_report(df: pd.DataFrame) -> str:
    """
    Generate a comprehensive text summary report
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        String with formatted summary report
    """
    from datetime import datetime
    
    overview = analyze_events_overview(df)
    team_stats = team_performance_analysis(df)
    location_stats = location_analysis(df)
    discipline_stats = disciplinary_analysis(df)
    time_stats = time_analysis(df)
    
    report = []
    report.append("=" * 70)
    report.append("FOOTBALL MATCH ANALYSIS REPORT")
    report.append("=" * 70)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    
    # Overview section
    report.append(f"\n📊 MATCH OVERVIEW:")
    report.append(f"{'Total Events:':<20} {overview['total_events']:>10}")
    report.append(f"{'Total Teams:':<20} {overview['unique_teams']:>10}")
    report.append(f"{'Total Players:':<20} {overview['unique_players']:>10}")
    report.append(f"{'Total Goals:':<20} {overview['total_goals']:>10}")
    
    # Home vs Away
    if 'home_vs_away' in overview:
        report.append(f"\n🏠 HOME vs AWAY:")
        for side, count in overview['home_vs_away'].items():
            report.append(f"{'  ' + side + ':':<20} {count:>10} events")
    
    # Event breakdown
    if 'event_breakdown' in overview:
        report.append(f"\n⚽ EVENT BREAKDOWN (Top 10):")
        for event, count in sorted(overview['event_breakdown'].items(), key=lambda x: x[1], reverse=True)[:10]:
            report.append(f"{'  ' + event + ':':<25} {count:>8}")
    
    # Shot analysis
    if 'shot_analysis' in overview:
        shot_data = overview['shot_analysis']
        report.append(f"\n🎯 SHOOTING ANALYSIS:")
        report.append(f"{'  Total Shots:':<20} {shot_data['total_shots']:>10}")
        report.append(f"{'  Shots on Target:':<20} {shot_data['shots_on_target']:>10}")
        report.append(f"{'  Conversion Rate:':<20} {shot_data['conversion_rate']:>9}%")
        
        if 'shot_outcome_breakdown' in overview:
            report.append(f"\n  Shot Outcome Details:")
            for outcome, count in overview['shot_outcome_breakdown'].items():
                report.append(f"{'    ' + outcome + ':':<22} {count:>8}")
    
    # Team Performance
    if not team_stats.empty:
        report.append(f"\n🏆 TEAM PERFORMANCE:")
        report.append(f"{'Team':<15} {'Goals':<8} {'Shots':<8} {'Accuracy':<10} {'Conv.Rate':<10}")
        report.append("-" * 55)
        for team, stats in team_stats.head().iterrows():
            goals = int(stats.get('goals_scored', 0))
            shots = int(stats.get('total_shots', 0))
            accuracy = f"{stats.get('shooting_accuracy', 0):.1f}%" if shots > 0 else "N/A"
            conv_rate = f"{stats.get('conversion_rate', 0):.1f}%" if shots > 0 else "N/A"
            report.append(f"{team:<15} {goals:<8} {shots:<8} {accuracy:<10} {conv_rate:<10}")
    
    # Location analysis
    if location_stats:
        if 'goals_by_location' in location_stats:
            report.append(f"\n📍 TOP SCORING LOCATIONS:")
            for location, goals in list(location_stats['goals_by_location'].items())[:5]:
                report.append(f"{'  ' + location + ':':<35} {goals:>5} goals")
        
        if 'goals_by_bodypart' in location_stats:
            report.append(f"\n🦵 GOALS BY BODY PART:")
            for bodypart, goals in location_stats['goals_by_bodypart'].items():
                report.append(f"{'  ' + bodypart + ':':<20} {goals:>5} goals")
        
        if 'goals_by_situation' in location_stats:
            report.append(f"\n⚡ GOALS BY SITUATION:")
            for situation, goals in location_stats['goals_by_situation'].items():
                report.append(f"{'  ' + situation + ':':<20} {goals:>5} goals")
    
    # Time analysis
    if time_stats and 'goals_by_time_period' in time_stats:
        report.append(f"\n⏰ GOALS BY TIME PERIOD:")
        for period, goals in time_stats['goals_by_time_period'].items():
            report.append(f"{'  ' + period + ':':<15} {goals:>5} goals")
    
    # Discipline summary
    if discipline_stats:
        report.append(f"\n🟨 DISCIPLINE SUMMARY:")
        report.append(f"{'  Total Fouls:':<20} {discipline_stats.get('total_fouls', 0):>8}")
        report.append(f"{'  Yellow Cards:':<20} {discipline_stats.get('yellow_cards', 0):>8}")
        report.append(f"{'  Red Cards:':<20} {discipline_stats.get('red_cards', 0):>8}")
        report.append(f"{'  Total Cards:':<20} {discipline_stats.get('total_cards', 0):>8}")
        
        if 'most_cards_by_team' in discipline_stats:
            report.append(f"\n  Most Disciplined Teams (Fewest Cards):")
            sorted_teams = sorted(discipline_stats['most_cards_by_team'].items(), key=lambda x: x[1])
            for team, cards in sorted_teams[:3]:
                report.append(f"{'    ' + team + ':':<20} {cards:>5} cards")
    
    report.append("\n" + "=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)
    
    return "\n".join(report)


def save_report_to_file(df: pd.DataFrame, filename: str = None) -> str:
    """
    Generate and save comprehensive report to output/summaries directory
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        filename: Optional custom filename
        
    Returns:
        Path to saved report file
    """
    import os
    from datetime import datetime
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'summaries')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"match_analysis_report_{timestamp}.txt"
    
    # Ensure .txt extension
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    file_path = os.path.join(output_dir, filename)
    
    # Generate and save report
    report_content = generate_summary_report(df)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return file_path


def save_data_exports(df: pd.DataFrame) -> Dict[str, str]:
    """
    Export processed data and analysis results to output directory
    
    Args:
        df: Cleaned events DataFrame (should be pre-decoded)
        
    Returns:
        Dictionary with paths to saved files
    """
    import os
    from datetime import datetime
    
    # Create output directories
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'summaries')
    os.makedirs(data_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    saved_files = {}
    
    # Save processed data
    processed_file = os.path.join(data_dir, f"processed_events_{timestamp}.csv")
    df.to_csv(processed_file, index=False)
    saved_files['processed_data'] = processed_file
    
    # Save team analysis
    team_stats = team_performance_analysis(df)
    if not team_stats.empty:
        team_file = os.path.join(data_dir, f"team_analysis_{timestamp}.csv")
        team_stats.to_csv(team_file)
        saved_files['team_analysis'] = team_file
    
    # Save player analysis
    player_stats = player_performance_analysis(df)
    if not player_stats.empty:
        player_file = os.path.join(data_dir, f"player_analysis_{timestamp}.csv")
        player_stats.to_csv(player_file)
        saved_files['player_analysis'] = player_file
    
    return saved_files