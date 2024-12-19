import zlib
import qrcode
import base45
import hashlib

def compress(bytecode: bytes) -> str:
    d = base45.b45encode(zlib.compress(bytecode, level=9)).decode()
    h = hashlib.sha1(d.encode('utf-8')).hexdigest()[:10]
    return h + d

def decompress(data: str) -> bytes:
    h = hashlib.sha1(data[10:].encode()).hexdigest()
    if h[:10] != data[:10]:
        raise ValueError("qr program corrupted")
    return zlib.decompress(base45.b45decode(data[10:].encode()))

if __name__ == '__main__':
    data = open('app.nmlx', 'rb').read()
    compressed = compress(data)
    if hashlib.sha1(decompress(compressed)).hexdigest() != hashlib.sha1(data).hexdigest():
        raise Exception("compress algorithm has error")    
    compression_ratio = (1 - len(compressed) / len(base45.b45encode(data))) * 100
    print(f"Compression percentage: {compression_ratio:.2f}%")
    with open("app_qr_source.txt", 'w') as f:
        f.write(compressed)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=3
    )
    qr.add_data(compressed)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("app_qr.png")