import subprocess
import sys

git_path = r"C:\Users\Lenovo\AppData\Local\Programs\Git\bin\git.exe"
args = sys.argv[1:]

result = subprocess.run([git_path] + args, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
