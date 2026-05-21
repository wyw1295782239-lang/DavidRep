import os

api_key = os.getenv('DASHSCOPE_API_KEY')

if api_key:
    print("✅ 成功！API密钥已找到。")
    # 可以打印密钥的前几位来确认，注意不要泄露完整密钥
    print(f"密钥前缀: {api_key[:8]}...")
else:
    print("❌ 失败！未找到API密钥，请检查环境变量是否设置成功。")