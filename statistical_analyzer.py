"""
Statistical Analysis Module for VNPT Telecom Dataset
Performs comprehensive statistical analysis and trend detection
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VNPTStatisticalAnalyzer:
    """Statistical analysis for VNPT telecom customer data"""
    
    def __init__(self, df):
        """Initialize analyzer with cleaned dataframe"""
        self.df = df
        self.stats = {}
        
    def analyze_all(self):
        """Run all statistical analyses"""
        logger.info("Starting comprehensive statistical analysis...")
        
        self.stats['overview'] = self._analyze_overview()
        self.stats['tkc_analysis'] = self._analyze_tkc()
        self.stats['service_analysis'] = self._analyze_service_adoption()
        self.stats['churn_analysis'] = self._analyze_churn_risk()
        self.stats['geographic_analysis'] = self._analyze_geographic()
        self.stats['staff_performance'] = self._analyze_staff_performance()
        self.stats['temporal_trends'] = self._analyze_temporal_trends()
        self.stats['segmentation'] = self._analyze_segmentation()
        
        logger.info("Statistical analysis completed")
        return self.stats
    
    def _analyze_overview(self):
        """Overall dataset statistics"""
        logger.info("Analyzing dataset overview...")
        
        return {
            'total_customers': len(self.df),
            'total_columns': len(self.df.columns),
            'date_range': {
                'earliest_activation': str(self.df['DATE_ENTER_ACTIVE'].min()),
                'latest_activation': str(self.df['DATE_ENTER_ACTIVE'].max()),
                'earliest_expiration': str(self.df['ACCT_EXPIRE_DATE'].min()),
                'latest_expiration': str(self.df['ACCT_EXPIRE_DATE'].max())
            },
            'data_quality': {
                'complete_records': int((~self.df.isnull().any(axis=1)).sum()),
                'records_with_missing': int(self.df.isnull().any(axis=1).sum())
            }
        }
    
    def _analyze_tkc(self):
        """Analyze TOTAL_TKC distribution and statistics"""
        logger.info("Analyzing TKC (Tiền Khuyến Cáo) distribution...")
        
        tkc_col = 'TOTAL_TKC'
        
        analysis = {
            'descriptive_stats': {
                'mean': float(self.df[tkc_col].mean()),
                'median': float(self.df[tkc_col].median()),
                'std': float(self.df[tkc_col].std()),
                'min': float(self.df[tkc_col].min()),
                'max': float(self.df[tkc_col].max()),
                'q25': float(self.df[tkc_col].quantile(0.25)),
                'q75': float(self.df[tkc_col].quantile(0.75))
            },
            'segment_distribution': self.df['TKC_SEGMENT'].value_counts().to_dict(),
            'total_tkc_value': float(self.df[tkc_col].sum()),
            'customers_with_zero_tkc': int((self.df[tkc_col] == 0).sum()),
            'customers_with_max_tkc': int((self.df[tkc_col] == 20000).sum())
        }
        
        return analysis
    
    def _analyze_service_adoption(self):
        """Analyze service adoption patterns"""
        logger.info("Analyzing service adoption...")
        
        has_service = self.df['HAS_SERVICE']
        
        analysis = {
            'adoption_rate': float(has_service.mean()),
            'customers_with_service': int(has_service.sum()),
            'customers_without_service': int((~has_service).sum()),
            'avg_tkc_with_service': float(self.df[has_service]['TOTAL_TKC'].mean()),
            'avg_tkc_without_service': float(self.df[~has_service]['TOTAL_TKC'].mean()),
            'service_codes': self.df[has_service]['SERVICE_CODE'].value_counts().head(10).to_dict()
        }
        
        return analysis
    
    def _analyze_churn_risk(self):
        """Analyze churn risk distribution"""
        logger.info("Analyzing churn risk...")
        
        analysis = {
            'high_risk_count': int((self.df['CHURN_RISK'] == 'High').sum()),
            'high_risk_percentage': float((self.df['CHURN_RISK'] == 'High').mean()),
            'avg_days_to_expire': float(self.df['DAYS_TO_EXPIRE'].mean()),
            'expiring_within_7_days': int((self.df['DAYS_TO_EXPIRE'] < 7).sum()),
            'expiring_within_30_days': int((self.df['DAYS_TO_EXPIRE'] < 30).sum()),
            'already_expired': int((self.df['DAYS_TO_EXPIRE'] < 0).sum())
        }
        
        return analysis
    
    def _analyze_geographic(self):
        """Analyze geographic distribution"""
        logger.info("Analyzing geographic distribution...")
        
        analysis = {
            'provinces': self.df['PROVINCE_NAME'].value_counts().to_dict(),
            'top_bts_stations': self.df['BTS_NAME'].value_counts().head(10).to_dict(),
            'customers_per_province': self.df.groupby('PROVINCE_NAME').agg({
                'Phone number': 'count',
                'TOTAL_TKC': 'mean'
            }).to_dict()
        }
        
        return analysis
    
    def _analyze_staff_performance(self):
        """Analyze staff performance metrics"""
        logger.info("Analyzing staff performance...")
        
        staff_stats = self.df.groupby('STAFF_CODE').agg({
            'Phone number': 'count',
            'TOTAL_TKC': ['mean', 'sum'],
            'HAS_SERVICE': 'mean'
        }).round(2)
        
        staff_stats.columns = ['customer_count', 'avg_tkc', 'total_tkc', 'service_rate']
        staff_stats = staff_stats.sort_values('customer_count', ascending=False)
        
        analysis = {
            'total_staff': len(staff_stats),
            'avg_customers_per_staff': float(staff_stats['customer_count'].mean()),
            'top_performers': staff_stats.head(10).to_dict(),
            'unassigned_customers': int((self.df['STAFF_CODE'] == 'UNASSIGNED').sum())
        }
        
        return analysis
    
    def _analyze_temporal_trends(self):
        """Analyze temporal trends"""
        logger.info("Analyzing temporal trends...")
        
        # Activation trends by month
        self.df['activation_month'] = pd.to_datetime(self.df['DATE_ENTER_ACTIVE']).dt.to_period('M')
        monthly_activations = self.df.groupby('activation_month').size()
        
        # Account age distribution
        age_bins = [0, 365, 730, 1095, 1460, 10000]
        age_labels = ['<1 year', '1-2 years', '2-3 years', '3-4 years', '4+ years']
        self.df['age_category'] = pd.cut(self.df['ACCOUNT_AGE'], bins=age_bins, labels=age_labels)
        
        # Convert Period index to string for JSON serialization
        monthly_activations_dict = {str(k): int(v) for k, v in monthly_activations.tail(12).items()}
        
        analysis = {
            'monthly_activations': monthly_activations_dict,
            'avg_account_age_days': float(self.df['ACCOUNT_AGE'].mean()),
            'account_age_distribution': self.df['age_category'].value_counts().to_dict(),
            'activation_trend': {
                'last_6_months': int(monthly_activations.tail(6).sum()),
                'last_12_months': int(monthly_activations.tail(12).sum())
            }
        }
        
        return analysis
    
    def _analyze_segmentation(self):
        """Analyze customer segmentation"""
        logger.info("Analyzing customer segmentation...")
        
        # Segment by TKC and Service
        segments = self.df.groupby(['TKC_SEGMENT', 'HAS_SERVICE']).agg({
            'Phone number': 'count',
            'TOTAL_TKC': 'mean',
            'CHURN_RISK': lambda x: (x == 'High').mean()
        }).round(2)
        
        segments.columns = ['customer_count', 'avg_tkc', 'churn_risk_rate']
        
        # Convert to JSON-serializable format
        segment_matrix = {}
        for (tkc_seg, has_service), row in segments.iterrows():
            key = f"{tkc_seg}_{'with_service' if has_service else 'no_service'}"
            segment_matrix[key] = {
                'customer_count': int(row['customer_count']),
                'avg_tkc': float(row['avg_tkc']),
                'churn_risk_rate': float(row['churn_risk_rate'])
            }
        
        analysis = {
            'segment_matrix': segment_matrix,
            'high_value_customers': int((
                (self.df['TKC_SEGMENT'] == 'High') & 
                (self.df['HAS_SERVICE'] == True)
            ).sum()),
            'at_risk_high_value': int((
                (self.df['TKC_SEGMENT'] == 'High') & 
                (self.df['CHURN_RISK'] == 'High')
            ).sum())
        }
        
        return analysis
    
    def generate_insights(self):
        """Generate business insights from analysis"""
        logger.info("Generating business insights...")
        
        insights = []
        
        # Service adoption insight
        adoption_rate = self.stats['service_analysis']['adoption_rate']
        if adoption_rate < 0.3:
            insights.append({
                'category': 'Service Adoption',
                'severity': 'High',
                'insight': f'Low service adoption rate ({adoption_rate*100:.1f}%). 76% of customers have no service code.',
                'recommendation': 'Launch targeted campaigns to increase service adoption among existing customers.'
            })
        
        # Churn risk insight
        high_risk_pct = self.stats['churn_analysis']['high_risk_percentage']
        if high_risk_pct > 0.8:
            insights.append({
                'category': 'Churn Risk',
                'severity': 'Critical',
                'insight': f'{high_risk_pct*100:.1f}% of customers are at high churn risk (expiring within 30 days).',
                'recommendation': 'Implement urgent retention campaigns for customers expiring soon.'
            })
        
        # TKC distribution insight
        zero_tkc = self.stats['tkc_analysis']['customers_with_zero_tkc']
        total = self.stats['overview']['total_customers']
        if zero_tkc / total > 0.3:
            insights.append({
                'category': 'TKC Distribution',
                'severity': 'Medium',
                'insight': f'{zero_tkc/total*100:.1f}% of customers have zero TKC value.',
                'recommendation': 'Review TKC allocation strategy to ensure customer engagement.'
            })
        
        # Staff performance insight
        unassigned = self.stats['staff_performance']['unassigned_customers']
        if unassigned > 0:
            insights.append({
                'category': 'Staff Assignment',
                'severity': 'Medium',
                'insight': f'{unassigned} customers are unassigned to any staff member.',
                'recommendation': 'Assign these customers to staff for better account management.'
            })
        
        return insights
    
    def save_results(self, output_path):
        """Save analysis results to JSON"""
        logger.info(f"Saving analysis results to: {output_path}")
        
        # Add insights to stats
        self.stats['insights'] = self.generate_insights()
        
        # Convert any remaining non-serializable objects
        stats_json = json.loads(json.dumps(self.stats, default=str))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats_json, f, ensure_ascii=False, indent=2)
        
        logger.info("Analysis results saved successfully")


def main():
    """Main execution"""
    
    logger.info("=" * 80)
    logger.info("VNPT STATISTICAL ANALYSIS")
    logger.info("=" * 80)
    
    # Load cleaned data
    input_file = r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\cleaned_data.xlsx"
    output_file = r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\statistical_analysis.json"
    
    logger.info(f"Loading cleaned data from: {input_file}")
    df = pd.read_excel(input_file)
    logger.info(f"Loaded {len(df)} records")
    
    # Run analysis
    analyzer = VNPTStatisticalAnalyzer(df)
    stats = analyzer.analyze_all()
    
    # Save results
    analyzer.save_results(output_file)
    
    # Print key metrics
    logger.info("=" * 80)
    logger.info("KEY METRICS")
    logger.info("=" * 80)
    logger.info(f"Total Customers: {stats['overview']['total_customers']:,}")
    logger.info(f"Service Adoption Rate: {stats['service_analysis']['adoption_rate']*100:.1f}%")
    logger.info(f"High Churn Risk: {stats['churn_analysis']['high_risk_percentage']*100:.1f}%")
    logger.info(f"Avg TKC: {stats['tkc_analysis']['descriptive_stats']['mean']:.2f} VNĐ")
    logger.info(f"Avg Account Age: {stats['temporal_trends']['avg_account_age_days']:.0f} days")
    logger.info("=" * 80)
    
    # Print insights
    insights = analyzer.generate_insights()
    logger.info(f"\n{len(insights)} BUSINESS INSIGHTS GENERATED")
    for i, insight in enumerate(insights, 1):
        logger.info(f"\n{i}. [{insight['severity']}] {insight['category']}")
        logger.info(f"   {insight['insight']}")
        logger.info(f"   → {insight['recommendation']}")
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ Statistical analysis completed successfully!")


if __name__ == "__main__":
    main()
