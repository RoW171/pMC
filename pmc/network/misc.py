__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-02"
__version__ = "0.0.1"

from socket import gethostbyname, gethostname, inet_aton
from subprocess import call, Popen, PIPE


def hostname(): return gethostbyname(gethostname())


def valid_ip(address):
    try: inet_aton(address)
    except (OSError,): return False
    else: return True


def ping(address): return call(['ping', '-n', '1', address], stdout=PIPE, stderr=PIPE, shell=False) == 0


def pingTime(address):
    out, err, = Popen(['ping', address], stdout=PIPE, stderr=PIPE, shell=False).communicate()
    if err != bytes(): return None
    ms = out.decode('iso-8859-1').replace('ms\r\n', '').split(' = ')[-1]
    if ms.isdigit(): return int(ms)
    else: return None


if __name__ == '__main__': pass
