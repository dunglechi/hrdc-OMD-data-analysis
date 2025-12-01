"""
Visualization Module for VNPT Telecom Dataset
Creates professional charts with VNPT branding (#0066B2)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# VNPT Brand Colors
VNPT_BLUE = '#0066B2'
VNPT_COLORS = ['#0066B2', '#00A3E0', '#0080C0', '#004D99', '#003366']

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class VNPTVisualizer:
    """Create visualizations for VNPT data analysis"""
    
    def __init__(self, df, stats, output_dir='outputs/charts'):
        """Initialize visualizer"""
        self.df = df
        self.stats = stats
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_all_charts(self):
        """Generate all charts"""
        logger.info("Creating all visualizations...")
        
        charts = {}
        charts['tkc_distribution'] = self.plot_tkc_distribution()
        charts['service_adoption'] = self.plot_service_adoption()
        charts['churn_risk'] = self.plot_churn_risk()
        charts['geographic'] = self.plot_geographic_distribution()
        charts['staff_performance'] = self.plot_staff_performance()
        charts['temporal_trends'] = self.plot_temporal_trends()
        charts['segmentation'] = self.plot_segmentation_matrix()
        
        logger.info(f"Created {len(charts)} charts in {self.output_dir}")
        return charts
    
    def plot_tkc_distribution(self):
        """TKC distribution histogram"""
        logger.info("Creating TKC distribution chart...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        self.df['TOTAL_TKC'].hist(bins=50, color=VNPT_BLUE, edgecolor='white', ax=ax1)
        ax1.set_title('TKC Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Total TKC (VNĐ)')
        ax1.set_ylabel('Number of Customers')
        ax1.axvline(self.df['TOTAL_TKC'].mean(), color='red', linestyle='--', label=f'Mean: {self.df["TOTAL_TKC"].mean():.0f}')
        ax1.legend()
        
        # Segment pie chart
        segment_counts = self.df['TKC_SEGMENT'].value_counts()
        ax2.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%',
                colors=VNPT_COLORS, startangle=90)
        ax2.set_title('TKC Segments', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.output_dir / 'tkc_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved: {output_path}")
        return str(output_path)
    
    def plot_service_adoption(self):
        """Service adoption chart"""
        logger.info("Creating service adoption chart...")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Service adoption bar chart
        service_data = self.df['HAS_SERVICE'].value_counts()
        colors = [VNPT_BLUE if x else '#CCCCCC' for x in service_data.index]
        bars = ax.bar(['With Service', 'No Service'], service_data.values, color=colors, edgecolor='white', linewidth=2)
        
        # Add percentages
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,.0f}\n({height/len(self.df)*100:.1f}%)',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_title('Service Adoption Rate', fontsize=16, fontweight='bold')
        ax.set_ylabel('Number of Customers', fontsize=12)
        ax.set_ylim(0, max(service_data.values) * 1.15)
        
        plt.tight_layout()
        output_path = self.output_dir / 'service_adoption.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved: {output_path}")
        return str(output_path)
    
    def plot_churn_risk(self):
        """Churn risk visualization"""
        logger.info("Creating churn risk chart...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Churn risk distribution
        churn_data = self.df['CHURN_RISK'].value_counts()
        colors = ['#FF4444' if x == 'High' else '#44FF44' for x in churn_data.index]
        ax1.bar(churn_data.index, churn_data.values, color=colors, edgecolor='white', linewidth=2)
        ax1.set_title('Churn Risk Distribution', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Number of Customers')
        
        for i, (idx, val) in enumerate(churn_data.items()):
            ax1.text(i, val, f'{val:,.0f}\n({val/len(self.df)*100:.1f}%)',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Days to expire histogram
        days_to_expire = self.df['DAYS_TO_EXPIRE']
        ax2.hist(days_to_expire[days_to_expire < 100], bins=30, color=VNPT_BLUE, edgecolor='white')
        ax2.axvline(30, color='red', linestyle='--', linewidth=2, label='30-day threshold')
        ax2.set_title('Days to Expiration (<100 days)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Days to Expire')
        ax2.set_ylabel('Number of Customers')
        ax2.legend()
        
        plt.tight_layout()
        output_path = self.output_dir / 'churn_risk.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved: {output_path}")
        return str(output_path)
    
    def plot_geographic_distribution(self):
        """Geographic distribution"""
        logger.info("Creating geographic distribution chart...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Top provinces
        province_counts = self.df['PROVINCE_NAME'].value_counts().head(10)
        bars = ax.barh(range(len(province_counts)), province_counts.values, color=VNPT_BLUE, edgecolor='white')
        ax.set_yticks(range(len(province_counts)))
        ax.set_yticklabels(province_counts.index)
        ax.set_xlabel('Number of Customers', fontsize=12)
        ax.set_title('Top 10 Provinces by Customer Count', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        # Add values
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{width:,.0f}',
                    ha='left', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.output_dir / 'geographic_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved: {output_path}")
        return str(output_path)
    
    def plot_staff_performance(self):
        """Staff performance chart"""
        logger.info("Creating staff performance chart...")
        
        # Top 10 staff by customer count
        staff_stats = self.df[self.df['STAFF_CODE'] != 'UNASSIGNED'].groupby('STAFF_CODE').agg({
            'Phone number': 'count',
            'TOTAL_TKC': 'mean'
        }).sort_values('Phone number', ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(staff_stats))
        bars = ax.bar(x, staff_stats['Phone number'], color=VNPT_BLUE, edgecolor='white', linewidth=2)
        ax.set_xticks(x)
        ax.set_xticklabels(staff_stats.index, rotation=45, ha='right')
        ax.set_ylabel('Number of Customers', fontsize=12)
        ax.set_title('Top 10 Staff by Customer Count', fontsize=14, fontweight='bold')
        
        # Add values
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.output_dir / 'staff_performance.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved: {output_path}")
        return str(output_path)
    
    def plot_temporal_trends(self):
        """Temporal trends chart"""
        logger.info("Creating temporal trends chart...")
        
        # Monthly activations
        self.df['activation_month'] = pd.to_datetime(self.df['DATE_ENTER_ACTIVE']).dt.to_period('M')
        monthly_data = self.df.groupby('activation_month').size()
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        monthly_data.tail(24).plot(kind='line', ax=ax, color=VNPT_BLUE, linewidth=2, marker='o')
        ax.set_title('Customer Activation Trend (Last 24 Months)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('New Activations', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = self.output_dir / 'temporal_trends.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved: {output_path}")
        return str(output_path)
    
    def plot_segmentation_matrix(self):
        """Customer segmentation matrix"""
        logger.info("Creating segmentation matrix...")
        
        # Create pivot table
        pivot = pd.crosstab(self.df['TKC_SEGMENT'], self.df['HAS_SERVICE'], margins=True)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Heatmap
        sns.heatmap(pivot.iloc[:-1, :-1], annot=True, fmt='d', cmap='Blues', 
                    cbar_kws={'label': 'Customer Count'}, ax=ax)
        ax.set_title('Customer Segmentation Matrix', fontsize=14, fontweight='bold')
        ax.set_xlabel('Has Service', fontsize=12)
        ax.set_ylabel('TKC Segment', fontsize=12)
        
        plt.tight_layout()
        output_path = self.output_dir / 'segmentation_matrix.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved: {output_path}")
        return str(output_path)


def main():
    """Main execution"""
    
    logger.info("=" * 80)
    logger.info("VNPT VISUALIZATION GENERATOR")
    logger.info("=" * 80)
    
    # Load data
    df = pd.read_excel(r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\cleaned_data.xlsx")
    
    with open(r"c:\Users\Admin\.gemini\antigravity\playground\zonal-star\data\statistical_analysis.json", 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    # Create visualizer
    visualizer = VNPTVisualizer(df, stats)
    
    # Generate all charts
    charts = visualizer.create_all_charts()
    
    logger.info("=" * 80)
    logger.info(f"✅ Generated {len(charts)} visualizations successfully!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
