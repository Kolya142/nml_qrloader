from parser import *

@dataclasses.dataclass
class State:
    variables: Dict[str, int]
    functions: Dict[str, Tuple[List[Command], bool]]

def tt(v: str) -> bytes:
    return int.to_bytes(len(v), 1)+v.encode()

def compiler(commands: List[Command], state: State) -> bytes:
    f = None
    fc = []
    tf = []
    bytecode = bytearray()
    
    for i, cmd in enumerate(commands):
        if f:
            tf.append(i)
            if cmd.fn == 'ret':
                state.functions[f] = (fc.copy(), False)
                fc = []
                f = None
                continue
            fc.append(cmd)
            continue
        if cmd.fn == 'def' and not f:
            tf.append(i)
            f = cmd.args[0]
            fc = []
            state.functions[f] = ([], False)
            continue

    for f in state.functions:
        c = state.functions[f]
        if not c[1]:
            state.functions[f] = (state.functions[f][0], True)
            x = compiler(state.functions[f][0], state)
            x = b'\x02'+tt(f)+int.to_bytes(len(x), 3)+compiler(state.functions[f][0], state)
            bytecode.extend(x)

    for i, cmd in enumerate(commands):
        if i in tf:
            continue
        if cmd.fn in state.functions:
            bytecode.append(0x00)
            bytecode.extend(tt(cmd.fn))
            continue
        match cmd.fn:
            case 'loop':
                f = cmd.args[0]
                op = cmd.args[1]
                t = cmd.args[2]
                fn = cmd.args[3]
                bytecode.append(0x01)
                bytecode.extend(tt(f))
                bytecode.extend(tt(t))
                if op == 'lower':
                    bytecode.append(0x01)
                if op == 'bigger':
                    bytecode.append(0x02)
                if op == 'lower_eq':
                    bytecode.append(0x03)
                if op == 'bigger_eq':
                    bytecode.append(0x04)
                if op == 'eq':
                    bytecode.append(0x05)
                if op == 'ieq':
                    bytecode.append(0x06)
                bytecode.extend(tt(fn))
            case _:
                bytecode.append(0x03)
                bytecode.extend(tt(cmd.fn))
                bytecode.extend(tt(cmd.args[0]))
    return bytes(bytecode)
                    
if __name__ == '__main__':
    print(compiler(parser(open('../test.nml').read()), State({}, {})))