import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# 1. 读取 Parquet 文件
data = pd.read_parquet(r'D:\dataset for RA\train0.parquet', engine='pyarrow')

# 2. 转换 'tx_timestamp' 为 datetime 并提取日期
data['tx_timestamp'] = pd.to_datetime(data['tx_timestamp'], errors='coerce')
data = data.dropna(subset=['tx_timestamp'])  # 删除无法转换的行
data['date'] = data['tx_timestamp'].dt.date

# 3. 按 'token_id' 和 'date' 排序
data = data.sort_values(by=['token_id', 'date'])

# 4. 计算滞后价格和价格回报
data['usd_price_shifted'] = data.groupby('token_id')['usd_price'].shift(1)
data['price_return'] = (data['usd_price'] - data['usd_price_shifted']) / data['usd_price_shifted']

# 5. 删除 'usd_price_shifted' 为 NaN 或 0 的行
data = data.dropna(subset=['usd_price_shifted', 'price_return'])
data = data[data['usd_price_shifted'] != 0]

# 6. 计算滚动波动率（7天窗口），允许少于7天计算
data['volatility'] = data.groupby('token_id')['price_return'] \
                         .rolling(window=7, min_periods=1) \
                         .std() \
                         .reset_index(level=0, drop=True)

# 7. 计算每日交易量
daily_volume = data.groupby(['token_id', 'date'])['usd_price'].sum().reset_index(name='trading_volume')

# 8. 删除重复项并保留每个 'token_id' 和 'date' 的最后一个 'volatility'
data_unique = data.groupby(['token_id', 'date']).agg({'volatility': 'last'}).reset_index()
daily_volume_unique = daily_volume.groupby(['token_id', 'date']).agg({'trading_volume': 'sum'}).reset_index()

# 9. 合并数据
panel_data = pd.merge(
    data_unique,
    daily_volume_unique,
    on=['token_id', 'date'],
    how='inner'
)

# 10. 检查 'volatility' 列中的 NaN 数量
num_nan_volatility = panel_data['volatility'].isna().sum()
total_rows = panel_data.shape[0]
print(f"Volatility 中 NaN 的数量: {num_nan_volatility}，占比: {num_nan_volatility / total_rows:.2%}")

# 检查是否所有 'volatility' 都是 NaN
if panel_data['volatility'].isna().all():
    print("所有 'volatility' 值都是 NaN")
else: 
    print("有部分 'volatility' 值是 NaN")

# 11. 深入分析 'volatility' 的 NaN 原因（可选）
if num_nan_volatility > 0:
    # 计算每个 'token_id' 的交易记录数
    group_counts = data.groupby('token_id').size().reset_index(name='count')
    
    # 找出交易记录少于7条的 'token_id'
    tokens_less_7 = group_counts[group_counts['count'] < 7]
    num_tokens_less_7 = tokens_less_7.shape[0]
    total_tokens = group_counts.shape[0]
    print(f"交易记录少于7条的 'token_id' 数量: {num_tokens_less_7}，占比: {num_tokens_less_7 / total_tokens:.2%}")
    
    # 示例查看部分 'token_id'
    print(f"交易记录少于7条的 'token_id' 示例:\n{tokens_less_7.head()}")

# 12. 进行回归分析（仅使用非NaN 'volatility' 数据）
# 删除 'volatility' 中的 NaN 值
regression_data = panel_data.dropna(subset=['volatility', 'trading_volume'])

# 检查回归数据的基本信息
print(f"\n回归分析使用的观测数量: {regression_data.shape[0]}")
print(regression_data[['volatility', 'trading_volume']].describe())

# 进行线性回归
formula = 'volatility ~ trading_volume'
model = smf.ols(formula=formula, data=regression_data).fit()
print("\n回归分析结果:")
print(model.summary())

