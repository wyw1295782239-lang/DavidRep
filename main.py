import os
import subprocess

def run_scripts():
    """
    顺序执行爬虫和数据分析脚本
    """
    # 使用虚拟环境中的Python解释器
    python_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Scripts', 'python.exe')
    
    scripts = [
        'data/spider.py',
        'data/data_control.py',
        'data/csv_to_sql.py',
        'data/data_analyse.py'
    ]
    
    for script in scripts:
        print(f"执行脚本: {script}")
        try:
            result = subprocess.run([python_path, script], cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True)
            print(f"脚本 {script} 执行成功")
            print(f"输出: {result.stdout}")
            if result.stderr:
                print(f"错误: {result.stderr}")
        except Exception as e:
            print(f"执行脚本 {script} 时出错: {e}")

if __name__ == "__main__":
    run_scripts()
