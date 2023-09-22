import subprocess

# コマンドとコマンドライン引数をリストで指定
command = ["./procon-server_win.exe", "-c", "sample.conf.txt"]

# コマンドを実行
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"コマンドエラー：{e}")
except FileNotFoundError:
    print("ファイルが見つかりません")
