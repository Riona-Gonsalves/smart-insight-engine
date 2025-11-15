from modules.data_analyzer import DataAnalyzer
import pandas as pd

# Change this to your CSV file path
CSV_FILE = 'data/sales_data_sample.csv'

print("Starting analysis...")
print(f"Looking for file: {CSV_FILE}")

# Try different encodings
encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

for encoding in encodings:
    try:
        print(f"Trying encoding: {encoding}...")
        df = pd.read_csv(CSV_FILE, encoding=encoding)
        print(f"✓ Success with {encoding}!")
        
        # Now use the analyzer
        analyzer = DataAnalyzer(CSV_FILE)
        analyzer.df = df  # Manually set the dataframe
        
        # Show preview
        analyzer.show_preview(10)
        
        # Get info
        analyzer.get_info()
        
        # Get statistics
        analyzer.get_statistics()
        
        #load data
        analyzer.load_data()
        
        #count missing values
        analyzer.count_missing()
        
        #max value of sales
        analyzer.find_max('QUANTITYORDERED')
        
        # Plot
        numeric_cols = analyzer.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            analyzer.plot_column(numeric_cols[0])
        
        break
        
    except UnicodeDecodeError:
        print(f"  ✗ {encoding} didn't work")
        continue
    except Exception as e:
        print(f"  ✗ Error: {e}")
        break

print("\n✅ Analysis complete!")