# Báo Cáo Phân Tích Dữ Liệu - VNPT Lào Cai Telecom

## 📊 Tổng Quan Dataset

**File**: Tập TB mục tiêu cả tỉnh.xlsx  
**Kích thước**: 39,928 khách hàng × 15 thuộc tính  
**Dung lượng**: 3.1 MB  
**Ngày phân tích**: 2025-12-01

---

## 📋 Cấu Trúc Dữ Liệu

### Danh Sách Cột (15 columns)

| # | Tên Cột | Kiểu Dữ Liệu | Mô Tả |
|---|----------|--------------|-------|
| 1 | `Donvi` | Text | Đơn vị quản lý |
| 2 | `STAFF_CODE` | Text | Mã nhân viên phụ trách |
| 3 | `Phone number` | Number | Số điện thoại khách hàng |
| 4 | `PROVINCE_CODE_INIT` | Text | Mã tỉnh |
| 5 | `PROVINCE_NAME` | Text | Tên tỉnh |
| 6 | `BTS_NAME` | Text | Tên trạm BTS |
| 7 | `TOTAL_TKC` | Number | Tổng tiền khuyến cáo (VNĐ) |
| 8 | `DATE_ENTER_ACTIVE` | Date | Ngày kích hoạt |
| 9 | `ACCT_EXPIRE_DATE` | Date | Ngày hết hạn tài khoản |
| 10 | `SERVICE_CODE` | Text | Mã dịch vụ |
| 11 | `TIME_START` | Date | Thời gian bắt đầu |
| 12 | `TIME_END` | Date | Thời gian kết thúc |
| 13 | `LIFE_CYCLE_STAT_CD` | Text | Trạng thái vòng đời |
| 14 | `Mục tiêu dùng TKC` | Text | Mục tiêu sử dụng tiền khuyến cáo |
| 15 | `Mục ưu tiên` | Text | Mức độ ưu tiên |

---

## ⚠️ Phân Tích Chất Lượng Dữ Liệu

### Missing Values (Giá Trị Thiếu)

| Cột | Số Lượng Thiếu | Tỷ Lệ (%) | Mức Độ |
|-----|----------------|-----------|---------|
| `SERVICE_CODE` | 30,377 | **76.1%** | 🔴 Nghiêm trọng |
| `TIME_START` | 30,377 | **76.1%** | 🔴 Nghiêm trọng |
| `TIME_END` | 30,377 | **76.1%** | 🔴 Nghiêm trọng |
| `STAFF_CODE` | 340 | 0.9% | 🟡 Trung bình |
| `Donvi` | 182 | 0.5% | 🟢 Thấp |
| `BTS_NAME` | 7 | 0.02% | 🟢 Rất thấp |

**Nhận xét**:
- 3 cột liên quan đến service (SERVICE_CODE, TIME_START, TIME_END) có **76% missing** → Có thể nhiều khách hàng chưa đăng ký dịch vụ cụ thể
- Các cột quan trọng (Phone number, TOTAL_TKC, dates) **KHÔNG có missing values** ✅

### Duplicates (Dữ Liệu Trùng Lặp)

- **Số dòng trùng lặp hoàn toàn**: 0 ✅
- Dataset sạch, không có duplicate records

---

## 📈 Thống Kê Mô Tả

### Phone Number (Số Điện Thoại)
- **Tổng số**: 39,928 khách hàng
- **Phạm vi**: 84,325,050,000 - 84,989,910,000
- **Định dạng**: Tất cả bắt đầu bằng 84 (mã quốc gia Vietnam)

### TOTAL_TKC (Tổng Tiền Khuyến Cáo)
- **Trung bình**: 5,734 VNĐ/khách hàng
- **Trung vị**: 2,595 VNĐ
- **Min**: 0 VNĐ
- **Max**: 20,000 VNĐ
- **Độ lệch chuẩn**: 6,603 VNĐ

**Phân phối**:
- 25% khách hàng: 0 VNĐ (chưa có khuyến cáo)
- 50% khách hàng: ≤ 2,595 VNĐ
- 75% khách hàng: ≤ 10,492 VNĐ

---

## 🎯 Insights & Recommendations

### 1. Missing Data Strategy

**SERVICE_CODE, TIME_START, TIME_END (76% missing)**:
- ✅ **Giữ nguyên** - Đây là dữ liệu hợp lệ (khách hàng chưa có service)
- ✅ Tạo cột mới: `HAS_SERVICE` (Yes/No) để phân loại
- ✅ Phân tích riêng 2 nhóm: có service vs chưa có service

**STAFF_CODE (0.9% missing)**:
- ✅ Điền "UNASSIGNED" cho các khách hàng chưa được assign nhân viên
- ⚠️ Cần review với business: Tại sao có khách hàng chưa có nhân viên phụ trách?

**Donvi (0.5% missing)**:
- ✅ Forward fill hoặc điền theo PROVINCE_NAME

### 2. Data Segmentation Opportunities

**Theo TOTAL_TKC**:
- Segment 1: 0 VNĐ (25% khách hàng) - "No Incentive"
- Segment 2: 1-5,000 VNĐ (25%) - "Low Incentive"
- Segment 3: 5,001-10,000 VNĐ (25%) - "Medium Incentive"
- Segment 4: >10,000 VNĐ (25%) - "High Incentive"

**Theo Service Status**:
- Group A: Có SERVICE_CODE (24% - 9,551 khách hàng)
- Group B: Chưa có SERVICE_CODE (76% - 30,377 khách hàng)

### 3. Trend Analysis Opportunities

**Time-based Analysis**:
- Phân tích theo `DATE_ENTER_ACTIVE`: Xu hướng kích hoạt theo tháng/quý
- Phân tích theo `ACCT_EXPIRE_DATE`: Dự đoán churn risk
- Tính toán `Account Age` = Today - DATE_ENTER_ACTIVE

**Geographic Analysis**:
- Phân bố khách hàng theo `PROVINCE_NAME`
- Phân bố theo `BTS_NAME` (trạm phát sóng)
- Correlation giữa vị trí và TOTAL_TKC

**Staff Performance**:
- Số lượng khách hàng/nhân viên (`STAFF_CODE`)
- Trung bình TOTAL_TKC/nhân viên
- Top performers

---

## 🔧 Quy Trình Xử Lý Đề Xuất

### Phase 1: Data Cleaning ✅
1. ✅ Xử lý missing values theo strategy trên
2. ✅ Tạo derived columns: `HAS_SERVICE`, `ACCOUNT_AGE`, `TKC_SEGMENT`
3. ✅ Chuẩn hóa text fields (trim, uppercase cho codes)
4. ✅ Validate phone numbers (format 84XXXXXXXXX)

### Phase 2: Feature Engineering
1. Tạo `DAYS_TO_EXPIRE` = ACCT_EXPIRE_DATE - Today
2. Tạo `CHURN_RISK` = "High" nếu DAYS_TO_EXPIRE < 30
3. Tạo `CUSTOMER_VALUE_SCORE` dựa trên TOTAL_TKC và account age

### Phase 3: Statistical Analysis
1. Descriptive statistics cho từng segment
2. Correlation analysis (TKC vs Account Age, TKC vs Service)
3. Distribution analysis (histograms, box plots)
4. Outlier detection (customers với TKC = 20,000)

### Phase 4: Visualization & Reporting
1. **Dashboard KPIs**:
   - Total Customers: 39,928
   - Avg TKC: 5,734 VNĐ
   - Service Adoption Rate: 24%
   - Churn Risk Count
   
2. **Charts**:
   - TKC Distribution (histogram)
   - Customers by Province (bar chart)
   - Service Adoption Trend (line chart)
   - Top BTS Stations (bar chart)
   - Staff Performance (scatter plot)

3. **Outputs**:
   - ✅ Excel: Multiple sheets (Raw, Cleaned, Stats, Segments)
   - ✅ PDF: Executive report với charts
   - ✅ Dashboard: Interactive HTML với filters
   - ✅ API: REST endpoints cho integration

---

## 📦 Deliverables

### 1. Cleaned Data (Excel)
- Sheet 1: Cleaned Data (39,928 rows)
- Sheet 2: Summary Statistics
- Sheet 3: Customer Segments
- Sheet 4: Staff Performance
- Sheet 5: Data Quality Report

### 2. PDF Report
- Executive Summary (1 page)
- Data Quality Analysis (2 pages)
- Statistical Insights (3 pages)
- Visualizations (5 pages)
- Recommendations (2 pages)

### 3. Interactive Dashboard
- Overview KPIs
- Customer Segmentation View
- Geographic Distribution Map
- Trend Analysis Charts
- Drill-down capabilities

### 4. API Endpoints
```
GET /api/customers/summary
GET /api/customers/segments
GET /api/customers/by-province
GET /api/staff/performance
GET /api/trends/activation
POST /api/customers/filter
```

---

## ⏱️ Timeline

- **Data Cleaning**: 2 hours
- **Feature Engineering**: 1 hour
- **Statistical Analysis**: 2 hours
- **Visualization**: 2 hours
- **Report Generation**: 2 hours
- **API Development**: 2 hours
- **Testing**: 1 hour

**Total**: ~12 hours

---

## ✅ Next Steps

1. **Review this analysis** - Confirm insights và strategy
2. **Approve implementation plan** - Proceed với development
3. **Execute pipeline** - Run automated processing
4. **Deliver outputs** - Excel, PDF, Dashboard, API
