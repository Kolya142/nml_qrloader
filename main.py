import os
import time


CAMERAFILE = "/dev/video0"

os.system(f"zbarcam {CAMERAFILE} > data &")


while True:
    time.sleep(0.5)
    print("scanning")
    with open("data") as f:
        d = f.read()
        if not d:
            continue
        if d.startswith("QR-Code:"):
            d = d[len("QR-Code:"):]
            print(d)
            try:
                with open("data1", 'w') as f1:
                    f1.write(d)
                os.system(f"cat data1 | python3 interpreter.py b64 _")
            except Exception:
                pass
    with open('data', 'w') as f:
        f.write('')