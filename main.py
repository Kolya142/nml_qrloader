import base64
import os
import time
import zlib
import compress
import subprocess


CAMERAFILE = "/dev/video0"

if os.name != 'nt':
    process = subprocess.Popen(['zbarcam', CAMERAFILE], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
else:
    process = subprocess.Popen(['start', 'zbarcam', CAMERAFILE], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)



while True:
    time.sleep(0.5)
    print("scanning")
    try:
        d = process.stdout.readline().decode('utf-8').strip()
    except UnicodeDecodeError as e:
        print(f'incorrect qr: {e.__str__()}')
        continue
    if not d:
        continue
    if d.startswith("QR-Code:"):
        try:
            d = d.split("QR-Code:")[1].strip()
            print(f'qr data: {d}')
            d = compress.decompress(d)
        except (ValueError, zlib.error) as e:
            print(f'incorrect qr: {e.__str__()}')
            continue
        try:
            with open("app1.nmlx", 'wb') as f1:
                f1.write(d)
            process.kill()
            os.system(f"python3 interpreter.py byte app1.nmlx")
            exit()
        except Exception:
            pass