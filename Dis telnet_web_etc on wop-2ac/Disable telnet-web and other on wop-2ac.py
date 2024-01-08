import pexpect


def disable_telnet(ap_ip):
    s = pexpect.spawn(f"ssh -oHostKeyAlgorithms=+ssh-dss admin@{ap_ip}")
    is_key_known = s.expect(
        [r"\(yes\/no\/\[fingerprint\]\)\?", pexpect.TIMEOUT, pexpect.EOF], timeout=3
    )
    if is_key_known == 0:
        print(f"Adding ssh host {ap_ip} key to known")
        s.sendline("yes")
    match = s.expect(["assword:", pexpect.TIMEOUT, pexpect.EOF], timeout=3)
    if match != 0:
        print(f"{ap_ip} TIMEOUT or EOF Error")
        return False
    s.sendline("password")
    s.expect("#")
    s.sendline("set telnet status down")
    s.expect("#")
    s.sendline("set web-server http-status down")
    s.expect("#")
    s.sendline("set web-server https-status down")
    s.expect("#")
    s.sendline("remove basic-rate all")
    s.expect("#")
    s.sendline("remove supported-rate all")
    s.expect("#")
    s.sendline("add basic-rate wlan0 rate 6,12,24")
    s.expect("#")
    s.sendline("add supported-rate wlan0 rate 6,9,12,18,24,36,48,54")
    s.expect("#")
    s.sendline("add basic-rate wlan1 rate 1,2,5.5,11")
    s.expect("#")
    s.sendline("add supported-rate wlan1 rate 1,2,5.5,6,9,11,12,18,24,36,48,54")
    s.expect("#")
    s.sendline("set rrm rrm-service up")
    s.expect("#")
    s.sendline("set rrm rrm-service-url ws://172.19.5.6:8099/apb/rrm")
    s.expect("#")
    s.sendline("save-running")
    s.expect("#", timeout=10)
    s.sendline("exit")
    try:
        s.close()
    except Exception:
        pass
    print(f"{ap_ip} Success")
    return True


with open("ap_list.txt", "r") as f:
    ap_list = f.read().split("\n")
    ap_list.pop(-1)

for ap_ip in ap_list:
    disable_telnet(ap_ip)
