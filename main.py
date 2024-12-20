import os
import zlib
import cv2
import time
import pyzbar
import pyzbar.pyzbar
import compress
import interpreter

camera = cv2.VideoCapture(0)
while True:
    _, frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)

    W, H = frame.shape

    codes = pyzbar.pyzbar.decode(frame)

    frame = cv2.resize(frame, (500, 500))
    
    cv2.imshow("qr scanner", frame)

    if cv2.waitKey(1) & 0xff == 27:
        cv2.destroyAllWindows()
        break

    if len(codes) != 1:
        continue

    try:
        d = codes[0].data.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f'incorrect qr: {e.__str__()}')
        continue
    if not d:
        continue
    try:
        print(f'qr data: {d}')
        d = compress.decompress(d)
        print(f'qr data: {d}')
    except (ValueError, zlib.error) as e:
        print(f'incorrect qr: {e.__str__()}')
        continue
    try:
        cv2.destroyAllWindows()
        interpreter.interpreter(d, interpreter.State({}, {}, []))
        time.sleep(0.1)
        if os.name != 'nt':
            os.system("bash -c 'read -s -n 1 -p \"Press any key to continue...\"'")
        else:
            os.system("pause")
        exit()
    except Exception:
        pass