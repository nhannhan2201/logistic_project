import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def train_and_save_model():
    print("⏳ Đang đọc dữ liệu và Feature Engineering...")
    df = pd.read_csv('mk_supply_chain_data.csv')

    # --- FEATURE ENGINEERING ---
    # 1. Chỉ số cảnh báo cạn kho (Âm là thiếu, dương là dư)
    df['stock_health_index'] = df['current_stock_days'] - df['ocean_delay_days']
    
    # 2. Tốc độ tiêu thụ hàng ngày
    df['daily_burn_rate'] = df['order_qty'] / 30
    
    # 3. Cờ khẩn cấp (Boolean biến thành 0/1)
    df['is_critical_shortage'] = (df['stock_health_index'] < 7).astype(int)

    # Khai báo biến X và y
    features = [
        'ocean_delay_days', 'cost_increase_pct', 'current_stock_days', 
        'order_qty', 'stock_health_index', 'daily_burn_rate', 'is_critical_shortage'
    ]
    X = df[features]
    y = df['optimal_air_qty']

    # Chia tập train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("🧠 Đang huấn luyện XGBoost...")
    model = xgb.XGBRegressor(
        n_estimators=200, 
        learning_rate=0.05, 
        max_depth=5, 
        random_state=42
    )
    model.fit(X_train, y_train)

    # Đánh giá độ chính xác
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"📊 Kết quả Đánh giá: Sai số trung bình (MAE) = {mae:.1f} sản phẩm | Độ chính xác (R2) = {r2:.3f}")

    # Lưu mô hình
    model.save_model("xgboost_mk_model.json")
    print("✅ Đã lưu file mô hình: xgboost_mk_model.json")

if __name__ == "__main__":
    train_and_save_model()