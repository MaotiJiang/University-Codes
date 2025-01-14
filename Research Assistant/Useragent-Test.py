from fake_useragent import UserAgent

# Instantiate UserAgent class
ua = UserAgent()

# Generate a list of random User-Agents
user_agents = [ua.random for _ in range(1000)]  # 生成1000个User-Agent

print(user_agents[:30])  # 打印前5个


