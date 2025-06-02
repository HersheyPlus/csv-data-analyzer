import os
from src.loader import load_data_csv
from src.cleaner import clean_data, filter_columns
from src.analyzer import (
    decode_categorical_data,
    analyze_events_overview,
    team_performance_analysis,
    player_performance_analysis,
    location_analysis,
    disciplinary_analysis,
    time_analysis,
    generate_summary_report
)
from src.visualizer import create_dashboard, plot_shot_map

def main():
    # Load data
    print("Loading data...")
    df = load_data_csv('events.csv')
    
    # Define columns to keep
    columns_to_keep = [
        "id_event",
        "time",
        "event_type",
        "side",
        "event_team",
        "opponent",
        "player",
        "shot_place",
        "shot_outcome",
        "is_goal",
        "location",
        "bodypart",
        "assist_method",
        "situation",
        "fast_break"
    ]
    
    # Filter and clean data
    print("\nFiltering and cleaning data...")
    df_filtered = filter_columns(df, columns_to_keep)
    df_cleaned = clean_data(df_filtered)
    
    # Decode categorical data ONCE
    print("Decoding categorical data...")
    df_final = decode_categorical_data(df_cleaned)
    
    print("Original data shape:", df.shape)
    print("Filtered and cleaned data shape:", df_cleaned.shape)
    print("Final decoded data shape:", df_final.shape)
    
    # Generate analyses
    print("\n" + "="*50)
    print("RUNNING ANALYSES")
    print("="*50)
    
    # Overview analysis
    print("\n1. Overview Analysis:")
    overview = analyze_events_overview(df_final)
    for key, value in overview.items():
        if isinstance(value, dict) and len(value) > 5:
            print(f"  {key}: {dict(list(value.items())[:3])}... ({len(value)} total)")
        else:
            print(f"  {key}: {value}")
    
    # Team performance
    print("\n2. Team Performance:")
    team_stats = team_performance_analysis(df_final)
    if not team_stats.empty:
        print(team_stats.head())
    else:
        print("  No team data available")
    
    # Player performance (top 10)
    print("\n3. Top Players:")
    player_stats = player_performance_analysis(df_final)
    if not player_stats.empty:
        print(player_stats.head(10))
    else:
        print("  No player data available")
    
    # Location analysis
    print("\n4. Location Analysis:")
    location_stats = location_analysis(df_final)
    for category, data in location_stats.items():
        print(f"  {category}:")
        for item, count in list(data.items())[:5]:
            print(f"    {item}: {count}")
    
    # Disciplinary analysis
    print("\n5. Disciplinary Analysis:")
    discipline_stats = disciplinary_analysis(df_final)
    for key, value in discipline_stats.items():
        if isinstance(value, dict) and len(value) > 3:
            print(f"  {key}: {dict(list(value.items())[:3])}")
        else:
            print(f"  {key}: {value}")
    
    # Time analysis
    print("\n6. Time Analysis:")
    time_stats = time_analysis(df_final)
    for category, data in time_stats.items():
        print(f"  {category}:")
        if isinstance(data, dict):
            for period, events in data.items():
                print(f"    {period}: {events}")
        else:
            print(f"    {data}")
    
    # Generate and save comprehensive report
    print("\n" + "="*50)
    print("GENERATING REPORTS & VISUALIZATIONS")
    print("="*50)
    
    try:
        # Import the new functions
        from src.analyzer import save_report_to_file, save_data_exports
        
        # Save detailed report to file
        report_path = save_report_to_file(df_final)
        print(f"✅ Detailed report saved to: {report_path}")
        
        # Save data exports
        exported_files = save_data_exports(df_final)
        print(f"✅ Data exports saved:")
        for file_type, path in exported_files.items():
            print(f"   {file_type}: {path}")
        
        # Create visualization dashboard
        print(f"\n📈 Creating visualization dashboard...")
        plot_paths = create_dashboard(df_final)
        print(f"✅ Visualizations saved:")
        for plot_path in plot_paths:
            print(f"   📊 {os.path.basename(plot_path)}")
        
        
        # Display summary in console
        print("\n" + "="*50)
        print("SUMMARY REPORT PREVIEW")
        print("="*50)
        summary = generate_summary_report(df_final)
        print(summary[:1000] + "..." if len(summary) > 1000 else summary)
        print(f"\nFull report available at: {report_path}")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
        print("Displaying summary in console only:")
        summary = generate_summary_report(df_final)
        print(summary)

if __name__ == "__main__":
    main()