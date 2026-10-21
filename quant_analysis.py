from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. ЗАДАЕМ ИСХОДНЫЕ ЗНАЧЕНИЯ (реальные базовые цены товаров)
# Теперь это не случайные числа, а конкретные стартовые цены
initial_products_data = {
    "iPhone 18 Pro": 1199.00,
    "Samsung Galaxy S26 Ultra": 1299.00,
    "Sony WH-1000XM6": 399.00,
    "MacBook Pro 16": 2499.00,
}

np.random.seed(42)  # Фиксируем генератор для стабильности графика
dates = [datetime(2026, 10, 20) + timedelta(days=i) for i in range(30)]

data = []
for product, base_price in initial_products_data.items():
  current_price = base_price

  for i, date in enumerate(dates):
    # Точная настройка поведения цен по дням таймлайна:
    # Дни 0–17: Обычные небольшие колебания рынка (шум)
    if i < 18:
      current_price = base_price * np.random.uniform(0.99, 1.01)

    # Дни 18–24 (накануне Черной Пятницы): Искусственное завышение цены магазином (+10-15%)
    elif 18 <= i < 25:
      current_price = base_price * np.random.choice([1.0, 1.12, 1.15])

    # День 25 (Black Friday): Реальная скидка или фейковая (сравниваем с завышенной)
    elif i == 25:
      current_price = base_price * np.random.choice(
          [0.80, 0.90]
      )  # Честная или слабая скидка

    # Дни 26–27: Небольшой отскок после пятницы
    elif 26 <= i < 28:
      current_price = base_price * 0.95

    # День 28 (Cyber Monday): Максимальное падение цен
    elif i == 28:
      current_price = base_price * 0.75

    # День 29: Возврат к средним значениям
    else:
      current_price = base_price * 0.92

    # Заявленная магазином «перечеркнутая» старая цена (strikethrough)
    strikethrough_price = round(base_price * 1.25, 2)

    data.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Product": product,
        "Current_Price": round(current_price, 2),
        "Strikethrough_Price": strikethrough_price,
    })

df = pd.DataFrame(data)
df.to_csv("simulated_black_friday_data.csv", index=False)
print("📊 Исторический датасет на основе исходных цен успешно создан!")

# 2. РАСЧЕТ QUANT МЕТРИК
print("\n--- QUANTITATIVE METRICS REPORT ---")

summary_results = []
for product in initial_products_data.keys():
  prod_df = df[df["Product"] == product].reset_index(drop=True)

  # Базовая цена = среднее за первые 14 дней (до начала маркетинговых войн)
  baseline_price = prod_df.loc[:14, "Current_Price"].mean()

  # Цена в Черную Пятницу (день 25)
  bf_price = prod_df.loc[25, "Current_Price"]

  # Волатильность (стандартное отклонение за 14 дней)
  price_volatility = prod_df.loc[:14, "Current_Price"].std()

  # True Discount (%) = насколько цена в пятницу ниже честной базы, а не нарисованной
  true_discount = ((baseline_price - bf_price) / baseline_price) * 100

  # Markup Flag: поднималась ли цена выше нормы за неделю до распродажи
  pre_bf_max = prod_df.loc[18:24, "Current_Price"].max()
  markup_flag = 1 if pre_bf_max > baseline_price * 1.05 else 0

  summary_results.append({
      "Product": product,
      "Baseline Price (\$)": round(baseline_price, 2),
      "Black Friday Price (\$)": round(bf_price, 2),
      "True Discount (%)": round(true_discount, 2),
      "Pre-Event Volatility": round(price_volatility, 2),
      "Markup Flag (1/0)": markup_flag,
  })

df_metrics = pd.DataFrame(summary_results)
print(df_metrics.to_string(index=False))

# 3. ВИЗУАЛИЗАЦИЯ И СОХРАНЕНИЕ ГРАФИКА
plt.figure(figsize=(12, 6))

for product in initial_products_data.keys():
  prod_data = df[df["Product"] == product]
  plt.plot(
      pd.to_datetime(prod_data["Date"]),
      prod_data["Current_Price"],
      marker="o",
      markersize=3,
      label=product,
  )

plt.axvline(
    pd.to_datetime("2026-11-14"),
    color="red",
    linestyle="--",
    alpha=0.7,
    label="Black Friday",
)
plt.axvline(
    pd.to_datetime("2026-11-17"),
    color="purple",
    linestyle="--",
    alpha=0.7,
    label="Cyber Monday",
)

plt.title(
    "Retail Price Dynamics & Event-Driven Anomalies (Custom Baseline Data)",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price (USD)", fontsize=12)
plt.legend(loc="upper left")
plt.grid(True, linestyle=":", alpha=0.6)

plt.savefig("price_dynamics_report.png", dpi=300, bbox_inches="tight")
print(
    "\n✅ График успешно обновлен и сохранен как `price_dynamics_report.png`!"
)
plt.show()