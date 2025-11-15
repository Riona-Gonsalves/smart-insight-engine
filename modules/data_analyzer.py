import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class DataAnalyzer:
    """Simple data analyzer for CSV files"""
    
    def __init__(self, filepath):
        """Initialize with CSV file path"""
        self.filepath = filepath
        self.df = None
        
    def load_data(self):
        """Load CSV file"""
        try:
            self.df = pd.read_csv(self.filepath)
            print(f"✓ Successfully loaded {self.filepath}")
            print(f"  Rows: {len(self.df)}")
            print(f"  Columns: {len(self.df.columns)}")
            return True
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return False
    
    def show_preview(self, rows=5):
        """Show first few rows"""
        if self.df is None:
            print("Please load data first!")
            return
        
        print("\n" + "="*50)
        print("DATA PREVIEW")
        print("="*50)
        print(self.df.head(rows))
    
    def get_info(self):
        """Get basic information"""
        if self.df is None:
            return None
        
        np.info = {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "missing": self.df.isnull().sum().to_dict()
        }
        
        return np.info
        
        print("\n" + "="*50)
        print("DATASET INFO")
        print("="*50)
        print(f"Shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print(f"Data types:\n{self.df.dtypes}")
        print(f"Missing values:\n{self.df.isnull().sum()}")
    
    def get_statistics(self):
        """Get statistical summary"""
        if self.df is None:
            print("Please load data first!")
            return
        
        print("\n" + "="*50)
        print("STATISTICAL SUMMARY")
        print("="*50)
        print(self.df.describe())
    
    def plot_column(self, column_name):
        """Create a simple plot for a column"""
        if self.df is None:
            print("Please load data first!")
            return
        
        if column_name not in self.df.columns:
            print(f"Column '{column_name}' not found!")
            return
        
        # Check if numeric
        if pd.api.types.is_numeric_dtype(self.df[column_name]):
            # Numeric: create histogram
            fig = px.histogram(self.df, x=column_name, 
                             title=f"Distribution of {column_name}")
            fig.show()
        else:
            # Categorical: create bar chart
            value_counts = self.df[column_name].value_counts().head(10)
            fig = px.bar(x=value_counts.index, y=value_counts.values,
                        title=f"Top 10 {column_name}",
                        labels={'x': column_name, 'y': 'Count'})
            fig.show()
            
    def count_missing(self):
        """Count missing values in each column"""
        if self.df is None:
            print("Please load data first!")
            return
        missing = self.df.isnull().sum()
        print("\n" + "="*50)
        print("MISSING VALUES COUNT")
        print("="*50)
        for col, count in missing.items():
            if count > 0:
                print(f"{col}: {count} missing")
    
    def find_max(self, column_name):
        """Find maximum value in a column"""
        if self.df is None:
            print("Please load data first!")
            return
    
        if column_name not in self.df.columns:
            print(f"Column '{column_name}' not found!")
            return
        max_value = self.df[column_name].max()
        max_row = self.df[self.df[column_name] == max_value]
        print(f"\nMaximum {column_name}: {max_value}")
        print("Row with maximum value:")
        print(max_row)

if __name__ == "__main__":
    print("="*60)
    print("SMART INSIGHT ENGINE - WEEK 1 TEST")
    print("="*60)
    
    print("\n📊 Creating sample dataset...")
    
    # Create sample data
    sample_data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 28, 32],
        'Sales': [50000, 75000, 60000, 80000, 70000],
        'Department': ['IT', 'Sales', 'IT', 'Sales', 'Marketing']
    }
    
    # Save to CSV
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv('data/sample_data.csv', index=False)
    print("✓ Sample data created: data/sample_data.csv")
    
    # Now test our analyzer
    print("\n🔍 Testing DataAnalyzer...")
    analyzer = DataAnalyzer('data/sample_data.csv')
    
    # Load data
    if analyzer.load_data():
        # Show preview
        analyzer.show_preview()
        
        # Get info
        analyzer.get_info()
        
        # Get statistics
        analyzer.get_statistics()
        
        # Plot a column
        print("\n📊 Creating visualization...")
        analyzer.plot_column('Sales')
