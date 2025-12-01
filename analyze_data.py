"""
Data Analysis Script - Initial Exploration
Analyzes Excel file structure and generates comprehensive data profile
"""

import pandas as pd
import sys
import json
from pathlib import Path

# File path - read from workspace
excel_file = r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\raw_data.xlsx"

if not Path(excel_file).exists():
    print(f"❌ Không tìm thấy file: {excel_file}")
    sys.exit(1)

print(f"📁 Đang phân tích file: {excel_file}\n")

def analyze_excel_structure():
    """Analyze Excel file structure and data quality"""
    
    print("=" * 80)
    print("PHÂN TÍCH CẤU TRÚC FILE EXCEL")
    print("=" * 80)
    
    try:
        # Read all sheets
        excel_file_obj = pd.ExcelFile(excel_file)
        print(f"\n📊 Số lượng sheets: {len(excel_file_obj.sheet_names)}")
        print(f"📋 Tên các sheets: {excel_file_obj.sheet_names}")
        
        analysis_results = {}
        
        for sheet_name in excel_file_obj.sheet_names:
            print(f"\n{'=' * 80}")
            print(f"SHEET: {sheet_name}")
            print(f"{'=' * 80}")
            
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Basic info
            print(f"\n📏 Kích thước: {df.shape[0]} rows × {df.shape[1]} columns")
            print(f"\n📝 Tên các cột:")
            for i, col in enumerate(df.columns, 1):
                print(f"  {i}. {col}")
            
            # Data types
            print(f"\n🔤 Kiểu dữ liệu:")
            print(df.dtypes.to_string())
            
            # Missing values
            print(f"\n❌ Giá trị thiếu:")
            missing = df.isnull().sum()
            missing_pct = (missing / len(df) * 100).round(2)
            missing_df = pd.DataFrame({
                'Số lượng': missing,
                'Tỷ lệ (%)': missing_pct
            })
            print(missing_df[missing_df['Số lượng'] > 0].to_string())
            
            # Duplicates
            duplicates = df.duplicated().sum()
            print(f"\n🔄 Số dòng trùng lặp: {duplicates}")
            
            # Sample data
            print(f"\n📄 Dữ liệu mẫu (5 dòng đầu):")
            print(df.head().to_string())
            
            # Descriptive statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                print(f"\n📈 Thống kê mô tả (cột số):")
                print(df[numeric_cols].describe().to_string())
            
            # Store results
            analysis_results[sheet_name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'missing_values': missing.to_dict(),
                'duplicates': int(duplicates),
                'numeric_columns': list(numeric_cols)
            }
        
        # Save analysis results to JSON
        output_path = Path("c:/Users/Admin/.gemini/antigravity/playground/zonal-star/data/analysis_results.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n\n✅ Kết quả phân tích đã được lưu tại: {output_path}")
        
        return analysis_results
        
    except FileNotFoundError:
        print(f"❌ KHÔNG TÌM THẤY FILE: {excel_file}")
        print("Vui lòng kiểm tra lại đường dẫn!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ LỖI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    analyze_excel_structure()
