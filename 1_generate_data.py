import pandas as pd
import numpy as np

def generate_mock_data(n_samples=10000):
    print("⏳ Đang khởi tạo dữ liệu mô phỏng chuỗi cung ứng MK...")
    np.random.seed(42)

    # 1. Các biến đầu vào (Inputs)
    # Trễ từ 0 đến 45 ngày (bao gồm mốc 15 ngày của đề)
    ocean_delay_days = np.random.randint(0, 45, n_samples)
    
    # Phí biển tăng từ 0% đến 50% (bao gồm mốc 20% của đề)
    cost_increase_pct = np.random.uniform(0.0, 0.50, n_samples)
    
    # Tồn kho hiện tại đủ bán trong 2 đến 28 ngày
    current_stock_days = np.random.randint(2, 28, n_samples)
    
    # Lượng hàng cần giao (Mix giữa 20,000 của US-E và 13,773 của UK)
    order_qty = np.random.choice([20000, 13773], n_samples)

    # 2. Logic tạo nhãn (Ground Truth) để huấn luyện AI
    # Tính nhu cầu bán mỗi ngày (Burn rate)
    daily_demand = order_qty / 30 
    
    # Rule an toàn kho: Tồn kho phải chịu được (Số ngày trễ + 7 ngày buffer an toàn)
    required_stock_days = ocean_delay_days + 7 
    deficit_days = np.maximum(0, required_stock_days - current_stock_days)
    
    # Lượng hàng cơ bản cần bay để bù đắp số ngày thiếu hụt
    base_air_qty = deficit_days * daily_demand

    # Thêm độ nhiễu ngẫu nhiên (noise) mô phỏng thực tế vận hành
    noise = np.random.normal(0, 300, n_samples)
    optimal_air_qty = np.clip(base_air_qty + noise, 0, order_qty).astype(int)

    # 3. Xuất file
    df = pd.DataFrame({
        'ocean_delay_days': ocean_delay_days,
        'cost_increase_pct': cost_increase_pct,
        'current_stock_days': current_stock_days,
        'order_qty': order_qty,
        'optimal_air_qty': optimal_air_qty
    })

    df.to_csv('mk_supply_chain_data.csv', index=False)
    print("✅ Đã tạo xong file: mk_supply_chain_data.csv")

if __name__ == "__main__":
    generate_mock_data()