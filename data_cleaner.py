"""
Data Cleaning Module for VNPT Telecom Dataset
Handles missing values, creates derived columns, validates data integrity
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import yaml
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VNPTDataCleaner:
    """Data cleaning pipeline for VNPT telecom customer data"""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize cleaner with configuration"""
        self.config = self._load_config(config_path)
        self.today = datetime.now()
        
    def _load_config(self, config_path):
        """Load configuration from YAML file"""
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self._default_config()
    
    def _default_config(self):
        """Default configuration"""
        return {
            'missing_value_strategy': {
                'SERVICE_CODE': 'keep_null',
                'TIME_START': 'keep_null',
                'TIME_END': 'keep_null',
                'STAFF_CODE': 'UNASSIGNED',
                'Donvi': 'forward_fill',
                'BTS_NAME': 'UNKNOWN_BTS'
            },
            'tkc_bins': [0, 1, 5000, 10000, 20000],
            'tkc_labels': ['None', 'Low', 'Medium', 'High'],
            'churn_risk_days': 30
        }
    
    def clean_data(self, df):
        """Main cleaning pipeline"""
        logger.info(f"Starting data cleaning for {len(df)} records...")
        
        df_clean = df.copy()
        
        # Step 1: Handle missing values
        df_clean = self._handle_missing_values(df_clean)
        
        # Step 2: Standardize text fields
        df_clean = self._standardize_text_fields(df_clean)
        
        # Step 3: Validate phone numbers
        df_clean = self._validate_phone_numbers(df_clean)
        
        # Step 4: Create derived columns
        df_clean = self._create_derived_columns(df_clean)
        
        # Step 5: Validate data integrity
        df_clean = self._validate_data_integrity(df_clean)
        
        logger.info(f"Data cleaning completed. Final records: {len(df_clean)}")
        return df_clean
    
    def _handle_missing_values(self, df):
        """Handle missing values according to strategy"""
        logger.info("Handling missing values...")
        
        strategy = self.config['missing_value_strategy']
        
        # SERVICE_CODE, TIME_START, TIME_END: Keep null (valid missing)
        # Already null, no action needed
        
        # STAFF_CODE: Fill with UNASSIGNED
        if 'STAFF_CODE' in df.columns:
            missing_count = df['STAFF_CODE'].isnull().sum()
            if missing_count > 0:
                df['STAFF_CODE'] = df['STAFF_CODE'].fillna(strategy['STAFF_CODE'])
                logger.info(f"Filled {missing_count} missing STAFF_CODE with '{strategy['STAFF_CODE']}'")
        
        # Donvi: Forward fill
        if 'Donvi' in df.columns:
            missing_count = df['Donvi'].isnull().sum()
            if missing_count > 0:
                df['Donvi'] = df['Donvi'].fillna(method='ffill')
                # If still null after ffill, use PROVINCE_NAME
                still_missing = df['Donvi'].isnull().sum()
                if still_missing > 0:
                    df['Donvi'] = df['Donvi'].fillna(df['PROVINCE_NAME'])
                logger.info(f"Filled {missing_count} missing Donvi values")
        
        # BTS_NAME: Fill with UNKNOWN_BTS
        if 'BTS_NAME' in df.columns:
            missing_count = df['BTS_NAME'].isnull().sum()
            if missing_count > 0:
                df['BTS_NAME'] = df['BTS_NAME'].fillna(strategy['BTS_NAME'])
                logger.info(f"Filled {missing_count} missing BTS_NAME with '{strategy['BTS_NAME']}'")
        
        return df
    
    def _standardize_text_fields(self, df):
        """Standardize text fields"""
        logger.info("Standardizing text fields...")
        
        # Trim whitespace from all text columns
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]
        
        # Uppercase for code columns
        code_columns = ['STAFF_CODE', 'PROVINCE_CODE_INIT', 'SERVICE_CODE', 'LIFE_CYCLE_STAT_CD']
        for col in code_columns:
            if col in df.columns:
                df[col] = df[col].str.upper() if df[col].dtype == 'object' else df[col]
        
        logger.info("Text standardization completed")
        return df
    
    def _validate_phone_numbers(self, df):
        """Validate phone number format"""
        logger.info("Validating phone numbers...")
        
        if 'Phone number' in df.columns:
            # Convert to string for validation
            df['Phone number'] = df['Phone number'].astype(str)
            
            # Check format: should be 84XXXXXXXXX (11 digits starting with 84)
            invalid_phones = df[~df['Phone number'].str.match(r'^84\d{9}$')]
            
            if len(invalid_phones) > 0:
                logger.warning(f"Found {len(invalid_phones)} invalid phone numbers")
                # Add validation flag
                df['PHONE_VALID'] = df['Phone number'].str.match(r'^84\d{9}$')
            else:
                logger.info("All phone numbers are valid")
                df['PHONE_VALID'] = True
            
            # Convert back to int64 for valid phones
            df['Phone number'] = pd.to_numeric(df['Phone number'], errors='coerce')
        
        return df
    
    def _create_derived_columns(self, df):
        """Create derived columns for analysis"""
        logger.info("Creating derived columns...")
        
        # HAS_SERVICE: Boolean flag (check if SERVICE_CODE column exists)
        if 'SERVICE_CODE' in df.columns:
            df['HAS_SERVICE'] = ~df['SERVICE_CODE'].isnull()
            logger.info(f"HAS_SERVICE: {df['HAS_SERVICE'].sum()} customers with service ({df['HAS_SERVICE'].mean()*100:.1f}%)")
        else:
            logger.warning("SERVICE_CODE column not found, skipping HAS_SERVICE creation")
            df['HAS_SERVICE'] = False  # Default to False if column doesn't exist
        
        # ACCOUNT_AGE: Days since activation
        if 'DATE_ENTER_ACTIVE' in df.columns:
            df['DATE_ENTER_ACTIVE'] = pd.to_datetime(df['DATE_ENTER_ACTIVE'], errors='coerce')
            df['ACCOUNT_AGE'] = (self.today - df['DATE_ENTER_ACTIVE']).dt.days
            logger.info(f"ACCOUNT_AGE: Mean = {df['ACCOUNT_AGE'].mean():.0f} days")
        else:
            logger.warning("DATE_ENTER_ACTIVE column not found, skipping ACCOUNT_AGE creation")
        
        # DAYS_TO_EXPIRE: Days until expiration
        if 'ACCT_EXPIRE_DATE' in df.columns:
            df['ACCT_EXPIRE_DATE'] = pd.to_datetime(df['ACCT_EXPIRE_DATE'], errors='coerce')
            df['DAYS_TO_EXPIRE'] = (df['ACCT_EXPIRE_DATE'] - self.today).dt.days
            logger.info(f"DAYS_TO_EXPIRE: Mean = {df['DAYS_TO_EXPIRE'].mean():.0f} days")
        else:
            logger.warning("ACCT_EXPIRE_DATE column not found, skipping DAYS_TO_EXPIRE creation")
            df['DAYS_TO_EXPIRE'] = 999  # Default to high value if column doesn't exist
        
        # CHURN_RISK: High if expiring within threshold
        if 'DAYS_TO_EXPIRE' in df.columns:
            churn_threshold = self.config['churn_risk_days']
            df['CHURN_RISK'] = df['DAYS_TO_EXPIRE'].apply(
                lambda x: 'High' if pd.notna(x) and x < churn_threshold else 'Low'
            )
            high_risk_count = (df['CHURN_RISK'] == 'High').sum()
            logger.info(f"CHURN_RISK: {high_risk_count} customers at high risk ({high_risk_count/len(df)*100:.1f}%)")
        else:
            logger.warning("DAYS_TO_EXPIRE not available, skipping CHURN_RISK creation")
            df['CHURN_RISK'] = 'Low'  # Default to Low
        
        # TKC_SEGMENT: Categorize by TOTAL_TKC
        if 'TOTAL_TKC' in df.columns:
            bins = self.config['tkc_bins']
            labels = self.config['tkc_labels']
            df['TKC_SEGMENT'] = pd.cut(
                df['TOTAL_TKC'], 
                bins=bins, 
                labels=labels,
                include_lowest=True
            )
            logger.info(f"TKC_SEGMENT distribution:\n{df['TKC_SEGMENT'].value_counts()}")
        else:
            logger.warning("TOTAL_TKC column not found, skipping TKC_SEGMENT creation")
            df['TKC_SEGMENT'] = 'None'  # Default segment
        
        return df
    
    def _validate_data_integrity(self, df):
        """Validate data integrity and business rules"""
        logger.info("Validating data integrity...")
        
        # Check for negative TOTAL_TKC
        if 'TOTAL_TKC' in df.columns:
            negative_tkc = (df['TOTAL_TKC'] < 0).sum()
            if negative_tkc > 0:
                logger.warning(f"Found {negative_tkc} records with negative TOTAL_TKC")
        
        # Check date logic: DATE_ENTER_ACTIVE should be before ACCT_EXPIRE_DATE
        if 'DATE_ENTER_ACTIVE' in df.columns and 'ACCT_EXPIRE_DATE' in df.columns:
            invalid_dates = df[df['DATE_ENTER_ACTIVE'] > df['ACCT_EXPIRE_DATE']]
            if len(invalid_dates) > 0:
                logger.warning(f"Found {len(invalid_dates)} records with invalid date logic")
        
        # Check for future activation dates
        if 'DATE_ENTER_ACTIVE' in df.columns:
            future_dates = df[df['DATE_ENTER_ACTIVE'] > self.today]
            if len(future_dates) > 0:
                logger.warning(f"Found {len(future_dates)} records with future activation dates")
        
        logger.info("Data integrity validation completed")
        return df
    
    def generate_cleaning_report(self, df_original, df_cleaned):
        """Generate cleaning report"""
        report = {
            'original_records': len(df_original),
            'cleaned_records': len(df_cleaned),
            'records_removed': len(df_original) - len(df_cleaned),
            'missing_values_handled': {},
            'derived_columns_created': [
                'HAS_SERVICE', 'ACCOUNT_AGE', 'DAYS_TO_EXPIRE', 
                'CHURN_RISK', 'TKC_SEGMENT', 'PHONE_VALID'
            ],
            'data_quality_metrics': {
                'service_adoption_rate': f"{df_cleaned['HAS_SERVICE'].mean()*100:.1f}%",
                'avg_account_age_days': f"{df_cleaned['ACCOUNT_AGE'].mean():.0f}",
                'high_churn_risk_pct': f"{(df_cleaned['CHURN_RISK']=='High').mean()*100:.1f}%",
                'avg_tkc': f"{df_cleaned['TOTAL_TKC'].mean():.2f}"
            }
        }
        
        # Calculate missing values handled
        for col in df_original.columns:
            orig_missing = df_original[col].isnull().sum()
            clean_missing = df_cleaned[col].isnull().sum() if col in df_cleaned.columns else 0
            if orig_missing > 0:
                report['missing_values_handled'][col] = {
                    'original': int(orig_missing),
                    'remaining': int(clean_missing),
                    'filled': int(orig_missing - clean_missing)
                }
        
        return report


def main():
    """Main execution function"""
    
    # File paths
    input_file = r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\raw_data.xlsx"
    output_file = r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\cleaned_data.xlsx"
    report_file = r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\cleaning_report.json"
    
    logger.info("=" * 80)
    logger.info("VNPT DATA CLEANING PIPELINE")
    logger.info("=" * 80)
    
    # Load data
    logger.info(f"Loading data from: {input_file}")
    df_original = pd.read_excel(input_file)
    logger.info(f"Loaded {len(df_original)} records with {len(df_original.columns)} columns")
    
    # Initialize cleaner
    cleaner = VNPTDataCleaner()
    
    # Clean data
    df_cleaned = cleaner.clean_data(df_original)
    
    # Generate report
    report = cleaner.generate_cleaning_report(df_original, df_cleaned)
    
    # Save cleaned data
    logger.info(f"Saving cleaned data to: {output_file}")
    df_cleaned.to_excel(output_file, index=False)
    
    # Save report
    import json
    logger.info(f"Saving cleaning report to: {report_file}")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Print summary
    logger.info("=" * 80)
    logger.info("CLEANING SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Original records: {report['original_records']}")
    logger.info(f"Cleaned records: {report['cleaned_records']}")
    logger.info(f"Records removed: {report['records_removed']}")
    logger.info(f"\nData Quality Metrics:")
    for metric, value in report['data_quality_metrics'].items():
        logger.info(f"  {metric}: {value}")
    logger.info("=" * 80)
    logger.info("✅ Data cleaning completed successfully!")
    

if __name__ == "__main__":
    main()
