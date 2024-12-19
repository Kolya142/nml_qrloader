from typing import List, Dict, Tuple
import dataclasses

def parse_int(s: str) -> int:
    if s.startswith('0x'):
        return int(s[2:], 16)
    if s.startswith('0b'):
        return int(s[2:], 2)
    if s.startswith('\''):
        i = 0
        for c in s[1:][:-1]:
            i |= ord(c)
            i <<= 8
        return i
    i = float(s)
    if i % 1 == 0:
        return int(i)
    return i

def int_to_str(i: int) -> str:
    s = ''
    while True:
        s += chr(i & 0xff)
        i >>= 8
        if i == 0:
            break
    return s[::-1]

@dataclasses.dataclass
class Command:
    fn: str
    args: List[str]