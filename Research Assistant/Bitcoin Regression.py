import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
import warnings

# 忽略未来警告
warnings.simplefilter(action='ignore', category=FutureWarning)

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

# 6. 计算滚动波动率（7天窗口），仅在至少有7天数据时计算
data['volatility'] = data.groupby('token_id')['price_return'] \
                         .rolling(window=7, min_periods=7) \
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

# 11. 深入分析 'volatility' 的 NaN 原因
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

# 12. 创建事件的虚拟变量
# 定义所有七个事件及其日期
events = {
    'China_Crypto_Ban': pd.to_datetime('2021-09-24'),  #所有币
    'Crypto_Market_Crash': pd.to_datetime('2022-05-19'),
    'Ethereum_Merge': pd.to_datetime('2022-09-15'),  #只影响ETH ETH Treat 其他币看作control
    'FTX_Collapse': pd.to_datetime('2022-11-11'),    #before and after (无control)

    
    'SEC_Crackdown': pd.to_datetime('2023-04-01'),  # 假设日期
    # 移除 'NFT_Scams_Hacks' 以避免多重共线性
    'Alternative_Blockchains_L2': pd.to_datetime('2022-03-01')
}

# 为每个事件创建一个虚拟变量，表示事件后（含当天）为1，否则为0
for event_name, event_date in events.items():
    panel_data[event_name] = np.where(panel_data['date'] >= event_date.date(), 1, 0)

# 13. 设置多级索引
panel_data['date'] = pd.to_datetime(panel_data['date'])
panel_data.set_index(['token_id', 'date'], inplace=True)

# 14. 构建自变量和因变量
X = panel_data[['trading_volume'] + list(events.keys())]
y = panel_data['volatility']

# 15. 检查并处理 missing values in X and y
# 确保 X 和 y 没有缺失值，并且索引对齐
X = X.dropna()
y = y.dropna()
X, y = X.align(y, join='inner', axis=0)  # 添加 axis=0

# 16. 使用 PanelOLS 进行回归分析
model = PanelOLS(y, X, entity_effects=True)
results = model.fit()
print("\n回归分析结果:")
print(results)

# 17. 可视化回归系数（仅事件的系数）
# 提取事件的系数和置信区间
event_coeffs = results.params[list(events.keys())]
conf = results.conf_int().loc[list(events.keys())]
conf['coef'] = event_coeffs

# 绘制条形图
plt.figure(figsize=(14, 8))
sns.pointplot(x=conf.index, y='coef', data=conf, join=False, capsize=0.2)
plt.errorbar(conf.index, conf['coef'], 
             yerr=[conf['coef'] - conf['lower'], conf['upper'] - conf['coef']], 
             fmt='none', c='b', capsize=5)
plt.axhline(0, color='red', linestyle='--')
plt.title('DID 模型中事件的回归系数')
plt.xlabel('事件')
plt.ylabel('系数')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()















