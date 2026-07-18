# INSTRUCTOR GUIDE - LOG360 V2

> [!CAUTION]
> **CONFIDENTIAL INSTRUCTOR DOCUMENT — DO NOT PUBLISH**
> This document contains the full answer keys to the 25 questions in the LOG360 V2 lab.

## Architecture Notes
The `v2_traffic_generator.py` script automatically spoofs 50 endpoints. It constantly sends background "noise" (successful logons, firewall traffic) and every 60 seconds it injects the entire APT attack sequence via UDP port 514 (Syslog).

## Answer Key

1. **How many total devices are actively forwarding logs to the SIEM?**
   - **Answer**: `50` (The Python script automatically generates 1 DC, 39 Workstations, 5 Web Servers, and 5 DB Servers).
2. **What is the exact hostname of the Primary Domain Controller?**
   - **Answer**: `DC-MEGACORP-01`
3. **Which device (IP Address) is generating the highest volume of dropped firewall traffic?**
   - **Answer**: `10.14.22.99` (The attacker IP).
4. **A web scanner was used against the DMZ. What is the `User-Agent` string of the automated scanner?**
   - **Answer**: `Nuclei/v2.9.1`
5. **The attacker successfully exploited a vulnerability on the web server. What is the CVE number associated with this exploit in the IDS logs?**
   - **Answer**: `CVE-2023-46805`
6. **An uploaded web shell was detected. What is the exact URI path of the malicious script?**
   - **Answer**: `/admin/shell_v2.aspx`
7. **A password spraying attack was launched against Active Directory. What is the Source IP of the attacker?**
   - **Answer**: `10.14.22.99`
8. **Which specific Active Directory user account was successfully compromised during the password spray?**
   - **Answer**: `j.smith`
9. **At what exact timestamp did the successful malicious authentication (Event ID 4624) occur?**
   - **Answer**: *(Dynamic based on when the script runs, e.g., "Oct 11 22:15:30")* - Look for Event ID 4624 for j.smith.
10. **The attacker executed a suspicious encoded PowerShell payload. What destination port did the reverse shell connect to?**
    - **Answer**: `4444`
11. **What is the parent process that launched the malicious `powershell.exe` instance?**
    - **Answer**: `w3wp.exe` (IIS Worker Process)
12. **To establish persistence, the attacker installed a malicious Windows service. What is the name of this service?**
    - **Answer**: `WinRM_SVC_Mgmt`
13. **What is the exact file path of the executable linked to the malicious service?**
    - **Answer**: `C:\Windows\Temp\payload.exe`
14. **The attacker also created a Scheduled Task for persistence. What is the name of the Scheduled Task?**
    - **Answer**: `\Microsoft_Updates_Mgmt`
15. **The attacker pivoted to the File Server using SMB. What was the name of the administrative share accessed?**
    - **Answer**: `C$`
16. **During lateral movement, what binary process name (`Sysmon Event ID 1`) was executed under `services.exe`?**
    - **Answer**: `PSEXESVC.exe`
17. **The attacker attempted to dump credentials from memory. What specific Windows binary was abused to dump the LSASS process?**
    - **Answer**: `procdump.exe`
18. **A DCSync attack was detected in the logs. Which compromised user account requested the directory replication?**
    - **Answer**: `j.smith` (Event ID 4662)
19. **The attacker archived sensitive files for exfiltration. What is the name of the created `.zip` archive?**
    - **Answer**: `backup_2026.zip`
20. **Sensitive data was exfiltrated. What is the Fully Qualified Domain Name (FQDN) of the external command and control (C2) server?**
    - **Answer**: `c2.evil-empire.com`
21. **What protocol was used for the data exfiltration?**
    - **Answer**: `HTTPS` (Port 443)
22. **To cover their tracks, the attacker cleared the Windows Security Event Logs (Event ID 1102). Which compromised user account performed this action?**
    - **Answer**: `j.smith`
23. **The attacker executed ransomware. What exact command-line string was used to delete the Volume Shadow Copies?**
    - **Answer**: `vssadmin.exe Delete Shadows /All /Quiet`
24. **What is the file extension of the encrypted ransomware files?**
    - **Answer**: `.RYUK`
25. **What is the bitcoin address provided in the ransomware note (`readme.txt`)?**
    - **Answer**: `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh`
