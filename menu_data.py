from datetime import datetime
DRINK_MENU= {
    "珍珠奶茶": 65,
    "四季春青茶": 40,
    "芋頭鮮奶": 80,
    "冬瓜檸檬": 55
}

drink_list = list(DRINK_MENU.keys())

def calculate_drink_revenue(orders, menu_data):
    revenue_total = {}
    for drink, price in orders:
        if drink not in revenue_total:
            revenue_total[drink] = price
        else:
            revenue_total[drink] += price
    return revenue_total

def generate_drink_report(orders, menu_data):
    totalprice = calculate_drink_revenue(orders, menu_data)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"\n--- 今日飲料店銷售總營收報表 ---(時間: {current_time})\n"
    for drink, price in totalprice.items():
        report += f"品項: {drink} | 總營業額: {price} 元\n"
    return report