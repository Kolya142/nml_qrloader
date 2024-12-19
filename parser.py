from typing import List
from utils import *

def parser(code: str) -> List[Command]:
    cmds = []
    for line_num, line in enumerate(code.split('\n'), start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        sp = []
        context = 0
        s = ''
        i = 0
        while i < len(line):
            c = line[i]
            if context == 1:
                if c == '\\':
                    if i + 1 < len(line):
                        next_char = line[i + 1]
                        if next_char == '\'':
                            s += '\''
                            i += 2
                            continue
                        elif next_char == 'n':
                            s += '\n'
                            i += 2
                            continue
                        elif next_char == '\\':
                            s += '\\'
                            i += 2
                            continue
                        else:
                            s += c
                    else:
                        s += c
                elif c == '\'':
                    sp.append("'" + s + "'")
                    s = ''
                    context = 0
                else:
                    s += c
                i += 1
                continue
            else:
                if c == '\'':
                    context = 1
                    if s:
                        sp.append(s)
                        s = ''
                elif c == ' ':
                    if s:
                        sp.append(s)
                        s = ''
                else:
                    s += c
                i += 1

        if s:
            sp.append(s)
        if sp:
            cmds.append(Command(sp[0], sp[1:]))
    return cmds

if __name__ == '__main__':
    with open("../test.nml", "r", encoding="utf-8") as file:
        code = file.read()
    commands = parser(code)
    for cmd in commands:
        print(cmd)
