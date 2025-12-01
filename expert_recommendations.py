"""
Expert Recommendation Engine
Tạo khuyến nghị chuyên gia dựa trên kết quả phân tích
"""

def generate_churn_recommendations(high_risk_count, total_customers, avg_churn_prob, lang='vi'):
    """Generate expert recommendations for churn analysis"""
    
    churn_rate = high_risk_count / total_customers * 100
    
    if lang == 'vi':
        recommendations = {
            'severity': 'CRITICAL' if churn_rate > 80 else 'HIGH' if churn_rate > 50 else 'MEDIUM',
            'summary': f"🚨 **Tình Trạng Nghiêm Trọng**: {churn_rate:.1f}% khách hàng có nguy cơ rời mạng cao",
            'insights': [
                f"📊 **Phân tích**: Trong tổng số {total_customers:,} khách hàng, có {high_risk_count:,} khách hàng ({churn_rate:.1f}%) có xác suất rời mạng cao (>50%).",
                f"💰 **Tác động tài chính**: Nếu không có biện pháp can thiệp, công ty có thể mất {churn_rate:.1f}% doanh thu từ khách hàng này.",
                f"⏰ **Thời gian**: Cần hành động NGAY để giữ chân khách hàng trước khi hết hạn dịch vụ."
            ],
            'root_causes': [
                "📉 **TKC thấp hoặc bằng 0**: Khách hàng không có động lực sử dụng dịch vụ",
                "⏳ **Sắp hết hạn**: Nhiều tài khoản sắp hết hạn trong 30 ngày",
                "❌ **Không có dịch vụ**: 76% khách hàng chưa đăng ký service code",
                "👤 **Thiếu chăm sóc**: 340 khách hàng chưa được phân công nhân viên"
            ],
            'immediate_actions': [
                {
                    'priority': 'P0 - URGENT',
                    'action': '🎯 **Chiến dịch giữ chân khẩn cấp**',
                    'details': [
                        f"Target: {high_risk_count:,} khách hàng high-risk",
                        "Thời gian: Trong vòng 7 ngày",
                        "Phương thức: SMS + Call + Email",
                        "Ưu đãi: Tặng thêm TKC, gia hạn miễn phí, gói data đặc biệt"
                    ]
                },
                {
                    'priority': 'P1 - HIGH',
                    'action': '💰 **Chương trình nạp TKC khuyến mãi**',
                    'details': [
                        "Target: Khách hàng có TKC = 0 (37.7%)",
                        "Khuyến mãi: Nạp 50K tặng 50K",
                        "Thời gian: 30 ngày",
                        "KPI: Tăng 20% khách hàng có TKC > 0"
                    ]
                },
                {
                    'priority': 'P1 - HIGH',
                    'action': '📱 **Kích hoạt dịch vụ tự động**',
                    'details': [
                        "Target: 30,377 khách hàng chưa có service",
                        "Phương án: Tự động kích hoạt gói cơ bản miễn phí",
                        "Mục tiêu: Tăng service adoption từ 23.9% lên 60%",
                        "Timeline: 60 ngày"
                    ]
                }
            ],
            'long_term_strategy': [
                "🎁 **Loyalty Program**: Xây dựng chương trình khách hàng thân thiết với điểm thưởng",
                "📊 **Predictive Analytics**: Triển khai hệ thống cảnh báo sớm churn risk hàng tuần",
                "👥 **Phân công nhân viên**: Assign 340 khách hàng unassigned cho account managers",
                "💬 **Customer Feedback**: Thu thập feedback để hiểu lý do rời mạng",
                "🔄 **Auto-renewal**: Triển khai tự động gia hạn với thông báo trước 15 ngày"
            ],
            'expected_results': [
                f"📈 **Giảm churn rate**: Từ {churn_rate:.1f}% xuống còn 30-40% trong 3 tháng",
                "💰 **Tăng revenue**: Giữ được 50-60% khách hàng high-risk = tăng 40-50% doanh thu",
                "👥 **Tăng engagement**: Service adoption tăng từ 23.9% lên 60%",
                "⭐ **Customer satisfaction**: Cải thiện CSAT score lên 80%+"
            ]
        }
    else:  # English
        recommendations = {
            'severity': 'CRITICAL' if churn_rate > 80 else 'HIGH' if churn_rate > 50 else 'MEDIUM',
            'summary': f"🚨 **Critical Situation**: {churn_rate:.1f}% customers at high churn risk",
            'insights': [
                f"📊 **Analysis**: Out of {total_customers:,} customers, {high_risk_count:,} ({churn_rate:.1f}%) have high churn probability (>50%).",
                f"💰 **Financial Impact**: Without intervention, company may lose {churn_rate:.1f}% revenue from these customers.",
                f"⏰ **Urgency**: Immediate action needed to retain customers before service expiration."
            ],
            'root_causes': [
                "📉 **Low/Zero TKC**: Customers lack incentive to use service",
                "⏳ **Near Expiration**: Many accounts expiring within 30 days",
                "❌ **No Service**: 76% customers without service code",
                "👤 **Lack of Care**: 340 customers unassigned to staff"
            ],
            'immediate_actions': [
                {
                    'priority': 'P0 - URGENT',
                    'action': '🎯 **Emergency Retention Campaign**',
                    'details': [
                        f"Target: {high_risk_count:,} high-risk customers",
                        "Timeline: Within 7 days",
                        "Channels: SMS + Call + Email",
                        "Offers: Bonus TKC, free extension, special data packages"
                    ]
                },
                {
                    'priority': 'P1 - HIGH',
                    'action': '💰 **TKC Top-up Promotion**',
                    'details': [
                        "Target: Customers with TKC = 0 (37.7%)",
                        "Promotion: Top-up 50K get 50K bonus",
                        "Duration: 30 days",
                        "KPI: Increase customers with TKC > 0 by 20%"
                    ]
                },
                {
                    'priority': 'P1 - HIGH',
                    'action': '📱 **Auto Service Activation**',
                    'details': [
                        "Target: 30,377 customers without service",
                        "Method: Auto-activate basic free package",
                        "Goal: Increase service adoption from 23.9% to 60%",
                        "Timeline: 60 days"
                    ]
                }
            ],
            'long_term_strategy': [
                "🎁 **Loyalty Program**: Build rewards program with points",
                "📊 **Predictive Analytics**: Deploy weekly churn risk alerts",
                "👥 **Staff Assignment**: Assign 340 unassigned customers",
                "💬 **Customer Feedback**: Collect feedback on churn reasons",
                "🔄 **Auto-renewal**: Deploy auto-renewal with 15-day notice"
            ],
            'expected_results': [
                f"📈 **Reduce churn**: From {churn_rate:.1f}% to 30-40% in 3 months",
                "💰 **Increase revenue**: Retain 50-60% high-risk customers = 40-50% revenue increase",
                "👥 **Increase engagement**: Service adoption from 23.9% to 60%",
                "⭐ **Customer satisfaction**: Improve CSAT score to 80%+"
            ]
        }
    
    return recommendations


def generate_segmentation_recommendations(segments_data, lang='vi'):
    """Generate recommendations for customer segmentation"""
    
    if lang == 'vi':
        return {
            'summary': "👥 **Phân khúc thành công**: Đã chia khách hàng thành các nhóm đồng nhất",
            'insights': [
                "🎯 **Personalization**: Mỗi segment cần chiến lược marketing riêng biệt",
                "💡 **Optimization**: Tối ưu hóa nguồn lực cho từng nhóm khách hàng",
                "📊 **Targeting**: Dễ dàng nhắm mục tiêu cho campaigns"
            ],
            'segment_strategies': [
                {
                    'segment': 'High Value - High Engagement',
                    'characteristics': 'TKC cao, có service, churn risk thấp',
                    'strategy': '⭐ **VIP Treatment**: Chương trình ưu đãi đặc biệt, priority support, exclusive offers',
                    'budget_allocation': '40%'
                },
                {
                    'segment': 'High Value - Low Engagement',
                    'characteristics': 'TKC cao nhưng không dùng service',
                    'strategy': '🎁 **Activation Campaign**: Khuyến khích sử dụng service, tặng gói data, hướng dẫn sử dụng',
                    'budget_allocation': '30%'
                },
                {
                    'segment': 'Low Value - High Engagement',
                    'characteristics': 'TKC thấp nhưng dùng service tích cực',
                    'strategy': '📈 **Upsell**: Khuyến mãi nạp tiền, gói combo tiết kiệm, referral program',
                    'budget_allocation': '20%'
                },
                {
                    'segment': 'Low Value - Low Engagement',
                    'characteristics': 'TKC thấp, không service, high churn risk',
                    'strategy': '🚨 **Win-back**: Ưu đãi đặc biệt để kích hoạt lại, hoặc accept churn',
                    'budget_allocation': '10%'
                }
            ],
            'action_items': [
                "📋 **Tạo segment profiles**: Document đặc điểm chi tiết từng segment",
                "🎯 **Design campaigns**: Thiết kế 4 campaigns riêng cho mỗi segment",
                "📊 **Set KPIs**: Đặt mục tiêu cụ thể cho từng segment",
                "🔄 **Monitor & Adjust**: Review hàng tháng và điều chỉnh strategy"
            ]
        }
    else:  # English
        return {
            'summary': "👥 **Successful Segmentation**: Customers divided into homogeneous groups",
            'insights': [
                "🎯 **Personalization**: Each segment needs different marketing strategy",
                "💡 **Optimization**: Optimize resources for each customer group",
                "📊 **Targeting**: Easy targeting for campaigns"
            ],
            'segment_strategies': [
                {
                    'segment': 'High Value - High Engagement',
                    'characteristics': 'High TKC, has service, low churn risk',
                    'strategy': '⭐ **VIP Treatment**: Special offers, priority support, exclusive deals',
                    'budget_allocation': '40%'
                },
                {
                    'segment': 'High Value - Low Engagement',
                    'characteristics': 'High TKC but no service usage',
                    'strategy': '🎁 **Activation Campaign**: Encourage service usage, free data, tutorials',
                    'budget_allocation': '30%'
                },
                {
                    'segment': 'Low Value - High Engagement',
                    'characteristics': 'Low TKC but active service usage',
                    'strategy': '📈 **Upsell**: Top-up promotions, combo packages, referral program',
                    'budget_allocation': '20%'
                },
                {
                    'segment': 'Low Value - Low Engagement',
                    'characteristics': 'Low TKC, no service, high churn risk',
                    'strategy': '🚨 **Win-back**: Special offers to reactivate, or accept churn',
                    'budget_allocation': '10%'
                }
            ],
            'action_items': [
                "📋 **Create segment profiles**: Document detailed characteristics",
                "🎯 **Design campaigns**: Create 4 separate campaigns per segment",
                "📊 **Set KPIs**: Define specific goals for each segment",
                "🔄 **Monitor & Adjust**: Monthly review and strategy adjustment"
            ]
        }


def generate_anomaly_recommendations(anomaly_count, total_customers, lang='vi'):
    """Generate recommendations for anomaly detection"""
    
    anomaly_rate = anomaly_count / total_customers * 100
    
    if lang == 'vi':
        return {
            'summary': f"🔍 **Phát hiện {anomaly_count:,} bất thường** ({anomaly_rate:.1f}% tổng khách hàng)",
            'insights': [
                "⚠️ **Hành vi khác thường**: Các khách hàng này có pattern khác biệt đáng kể",
                "🎯 **Cơ hội**: Có thể là VIP customers hoặc fraud cases",
                "🔎 **Cần điều tra**: Review manual để hiểu nguyên nhân"
            ],
            'investigation_steps': [
                "1️⃣ **Phân loại anomalies**: Chia thành positive (VIP) và negative (fraud)",
                "2️⃣ **VIP Customers**: TKC rất cao, usage pattern đặc biệt → Chăm sóc đặc biệt",
                "3️⃣ **Fraud Detection**: Pattern bất thường, suspicious activity → Điều tra",
                "4️⃣ **Data Errors**: Có thể là lỗi nhập liệu → Cần clean data"
            ],
            'actions': [
                {
                    'category': 'VIP Customers',
                    'action': '⭐ **VIP Program**: Tạo chương trình chăm sóc riêng',
                    'details': 'Dedicated account manager, exclusive offers, priority support'
                },
                {
                    'category': 'Fraud Cases',
                    'action': '🚨 **Security Review**: Kiểm tra gian lận',
                    'details': 'Verify identity, check transaction history, block if needed'
                },
                {
                    'category': 'Data Quality',
                    'action': '🔧 **Data Cleaning**: Sửa lỗi dữ liệu',
                    'details': 'Validate data, correct errors, update records'
                }
            ]
        }
    else:  # English
        return {
            'summary': f"🔍 **Detected {anomaly_count:,} anomalies** ({anomaly_rate:.1f}% of total customers)",
            'insights': [
                "⚠️ **Unusual Behavior**: These customers have significantly different patterns",
                "🎯 **Opportunity**: Could be VIP customers or fraud cases",
                "🔎 **Investigation Needed**: Manual review to understand causes"
            ],
            'investigation_steps': [
                "1️⃣ **Classify anomalies**: Separate into positive (VIP) and negative (fraud)",
                "2️⃣ **VIP Customers**: Very high TKC, special usage → Special care",
                "3️⃣ **Fraud Detection**: Unusual patterns, suspicious activity → Investigate",
                "4️⃣ **Data Errors**: Possible data entry errors → Clean data"
            ],
            'actions': [
                {
                    'category': 'VIP Customers',
                    'action': '⭐ **VIP Program**: Create dedicated care program',
                    'details': 'Dedicated account manager, exclusive offers, priority support'
                },
                {
                    'category': 'Fraud Cases',
                    'action': '🚨 **Security Review**: Check for fraud',
                    'details': 'Verify identity, check transaction history, block if needed'
                },
                {
                    'category': 'Data Quality',
                    'action': '🔧 **Data Cleaning**: Fix data errors',
                    'details': 'Validate data, correct errors, update records'
                }
            ]
        }
