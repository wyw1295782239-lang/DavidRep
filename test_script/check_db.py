from utils import util

# 查看Part5表结构
res = util.query("DESCRIBE Part5")
print("Part5表结构:")
for column in res:
    print(column)

# 查看Part5表数据
res = util.query("SELECT * FROM Part5 LIMIT 10")
print("\nPart5表数据:")
for row in res:
    print(row)

# 查看所有表名
res = util.query("SHOW TABLES")
print("\n所有表名:")
for row in res:
    print(row)
