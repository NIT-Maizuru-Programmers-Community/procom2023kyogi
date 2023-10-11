import subprocess

# コマンドとコマンドライン引数をリストで指定
command = ["https://procon34system.kosen.work/server?token=maizuru98a2309fded8fd535faf506029733e9e3d030aae3c46c7c5ee8193690"]

# コマンドを実行
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"コマンドエラー：{e}")
except FileNotFoundError:
    print("ファイルが見つかりません")
