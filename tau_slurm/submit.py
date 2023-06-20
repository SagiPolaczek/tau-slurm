import subprocess


correct = subprocess.run(["dig", "+short", "stackoverflow.com"], check=True, text=True)
