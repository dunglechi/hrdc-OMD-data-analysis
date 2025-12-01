"""
Main Pipeline Orchestrator for VNPT Data Analysis
Runs the complete data processing pipeline from raw data to final outputs
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
import argparse

# Import all modules
from data_cleaner import VNPTDataCleaner
from statistical_analyzer import VNPTStatisticalAnalyzer
from visualization import VNPTVisualizer
from excel_exporter import VNPTExcelExporter

import pandas as pd
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class VNPTDataPipeline:
    """Main orchestrator for VNPT data analysis pipeline"""
    
    def __init__(self, input_file, output_dir='outputs'):
        """Initialize pipeline"""
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_dir = Path('data')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.start_time = datetime.now()
        
    def run_full_pipeline(self):
        """Run complete pipeline"""
        logger.info("=" * 100)
        logger.info("VNPT DATA ANALYSIS PIPELINE - FULL EXECUTION")
        logger.info("=" * 100)
        logger.info(f"Start Time: {self.start_time}")
        logger.info(f"Input File: {self.input_file}")
        logger.info(f"Output Directory: {self.output_dir}")
        logger.info("=" * 100)
        
        try:
            # Step 1: Load raw data
            logger.info("\n[STEP 1/5] Loading raw data...")
            df_raw = pd.read_excel(self.input_file)
            logger.info(f"✓ Loaded {len(df_raw)} records with {len(df_raw.columns)} columns")
            
            # Step 2: Clean data
            logger.info("\n[STEP 2/5] Cleaning data...")
            cleaner = VNPTDataCleaner()
            df_cleaned = cleaner.clean_data(df_raw)
            
            # Save cleaned data
            cleaned_path = self.data_dir / 'cleaned_data.xlsx'
            df_cleaned.to_excel(cleaned_path, index=False)
            logger.info(f"✓ Cleaned data saved: {cleaned_path}")
            
            # Generate cleaning report
            cleaning_report = cleaner.generate_cleaning_report(df_raw, df_cleaned)
            report_path = self.data_dir / 'cleaning_report.json'
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(cleaning_report, f, ensure_ascii=False, indent=2)
            logger.info(f"✓ Cleaning report saved: {report_path}")
            
            # Step 3: Statistical analysis
            logger.info("\n[STEP 3/5] Performing statistical analysis...")
            analyzer = VNPTStatisticalAnalyzer(df_cleaned)
            stats = analyzer.analyze_all()
            
            # Save analysis results
            stats_path = self.data_dir / 'statistical_analysis.json'
            analyzer.save_results(stats_path)
            logger.info(f"✓ Statistical analysis saved: {stats_path}")
            
            # Step 4: Generate visualizations
            logger.info("\n[STEP 4/5] Creating visualizations...")
            visualizer = VNPTVisualizer(df_cleaned, stats, output_dir=self.output_dir / 'charts')
            charts = visualizer.create_all_charts()
            logger.info(f"✓ Generated {len(charts)} charts")
            
            # Step 5: Export outputs
            logger.info("\n[STEP 5/5] Exporting final outputs...")
            
            # Excel export
            excel_exporter = VNPTExcelExporter(
                df_cleaned, 
                stats, 
                output_path=self.output_dir / 'VNPT_Data_Analysis.xlsx'
            )
            excel_file = excel_exporter.export_all()
            logger.info(f"✓ Excel export completed: {excel_file}")
            
            # Generate summary
            self._generate_summary(df_raw, df_cleaned, stats, charts)
            
            # Calculate execution time
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            
            logger.info("\n" + "=" * 100)
            logger.info("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
            logger.info("=" * 100)
            logger.info(f"Execution Time: {duration:.2f} seconds")
            logger.info(f"Output Directory: {self.output_dir.absolute()}")
            logger.info("\nGenerated Files:")
            logger.info(f"  1. Cleaned Data: {cleaned_path}")
            logger.info(f"  2. Statistical Analysis: {stats_path}")
            logger.info(f"  3. Excel Report: {excel_file}")
            logger.info(f"  4. Visualizations: {len(charts)} charts in {self.output_dir / 'charts'}")
            logger.info("=" * 100)
            
            return {
                'status': 'success',
                'duration_seconds': duration,
                'outputs': {
                    'cleaned_data': str(cleaned_path),
                    'statistics': str(stats_path),
                    'excel_report': excel_file,
                    'charts': charts
                }
            }
            
        except Exception as e:
            logger.error(f"\n❌ PIPELINE FAILED: {str(e)}")
            logger.exception("Full traceback:")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def _generate_summary(self, df_raw, df_cleaned, stats, charts):
        """Generate execution summary"""
        summary = {
            'pipeline_execution': {
                'timestamp': str(self.start_time),
                'input_file': str(self.input_file),
                'output_directory': str(self.output_dir)
            },
            'data_summary': {
                'raw_records': len(df_raw),
                'cleaned_records': len(df_cleaned),
                'columns': len(df_cleaned.columns)
            },
            'key_metrics': stats['overview'],
            'insights': stats.get('insights', []),
            'outputs_generated': {
                'excel_sheets': 5,
                'visualizations': len(charts),
                'json_reports': 2
            }
        }
        
        summary_path = self.output_dir / 'pipeline_summary.json'
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✓ Pipeline summary saved: {summary_path}")


def main():
    """Main execution with CLI arguments"""
    
    parser = argparse.ArgumentParser(description='VNPT Data Analysis Pipeline')
    parser.add_argument('--input', '-i', 
                       default='data/raw_data.xlsx',
                       help='Input Excel file path')
    parser.add_argument('--output', '-o',
                       default='outputs',
                       help='Output directory')
    
    args = parser.parse_args()
    
    # Run pipeline
    pipeline = VNPTDataPipeline(args.input, args.output)
    result = pipeline.run_full_pipeline()
    
    # Exit with appropriate code
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == "__main__":
    main()
