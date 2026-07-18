# LOG360 Incident Response Lab V2 - Live Enterprise Challenge

Welcome to the **LOG360 Incident Response Lab V2**!
In this lab, you are investigating a live enterprise environment consisting of **50 endpoint devices** that are actively forwarding real-time telemetry to your LOG360 SIEM. 

An Advanced Persistent Threat (APT) group has breached the MegaCorp network. Your job is to perform a full incident response investigation across the kill chain.

---

## 🎯 Investigation Questions

1. **How many total devices are actively forwarding logs to the SIEM?**
2. **What is the exact hostname of the Primary Domain Controller?**
3. **Which device (IP Address) is generating the highest volume of dropped firewall traffic?**
4. **A web scanner was used against the DMZ. What is the `User-Agent` string of the automated scanner?**
5. **The attacker successfully exploited a vulnerability on the web server. What is the CVE number associated with this exploit in the IDS logs?**
6. **An uploaded web shell was detected. What is the exact URI path of the malicious script?**
7. **A password spraying attack was launched against Active Directory. What is the Source IP of the attacker?**
8. **Which specific Active Directory user account was successfully compromised during the password spray?**
9. **At what exact timestamp did the successful malicious authentication (Event ID 4624) occur?**
10. **The attacker executed a suspicious encoded PowerShell payload. What destination port did the reverse shell connect to?**
11. **What is the parent process that launched the malicious `powershell.exe` instance?**
12. **To establish persistence, the attacker installed a malicious Windows service. What is the name of this service?**
13. **What is the exact file path of the executable linked to the malicious service?**
14. **The attacker also created a Scheduled Task for persistence. What is the name of the Scheduled Task?**
15. **The attacker pivoted to the File Server using SMB. What was the name of the administrative share accessed?**
16. **During lateral movement, what binary process name (`Sysmon Event ID 1`) was executed under `services.exe`?**
17. **The attacker attempted to dump credentials from memory. What specific Windows binary was abused to dump the LSASS process?**
18. **A DCSync attack was detected in the logs. Which compromised user account requested the directory replication?**
19. **The attacker archived sensitive files for exfiltration. What is the name of the created `.zip` archive?**
20. **Sensitive data was exfiltrated. What is the Fully Qualified Domain Name (FQDN) of the external command and control (C2) server?**
21. **What protocol was used for the data exfiltration?**
22. **To cover their tracks, the attacker cleared the Windows Security Event Logs (Event ID 1102). Which compromised user account performed this action?**
23. **The attacker executed ransomware. What exact command-line string was used to delete the Volume Shadow Copies?**
24. **What is the file extension of the encrypted ransomware files?**
25. **What is the bitcoin address provided in the ransomware note (`readme.txt`)?**
