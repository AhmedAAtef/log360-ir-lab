# ManageEngine LOG360 Incident Response Lab - Student Challenge Guide

Welcome to the LOG360 interactive lab! Below are the details for each of the 6 investigative tasks.

---

## 🎯 Task 0: LOG360 Search Query Practice (Warm-Up)
Before investigating the 6 attack scenarios, complete the warm-up task to practice using the LOG360 SIEM search console.

### Questions
1. **How many total event logs are loaded in the LOG360 repository?**
   * *Answer format: integer*
2. **How many log events have CRITICAL severity?**
   * *Answer format: integer*
3. **What LOG360 module (Log Source) would you use to investigate Active Directory logon failures?**
   * *Answer format: Module_Name*
4. **Search for Event ID `4625`. How many failed logon events appear?**
   * *Answer format: integer*
5. **Search for `vssadmin.exe`. What is the Host name where this was executed?**
   * *Answer format: HOST.DOMAIN.LOCAL*

---

## 🕵️‍♂️ Task 1: Active Directory Password Spraying
The attacker initiated a password spraying attack against Active Directory accounts, resulting in account lockouts.

### Questions
1. **What is the Source IP address used by the attacker to perform the password spraying?**
   * *Answer format: IP Address*
2. **Which user account was successfully locked out due to threshold violations?**
   * *Answer format: username*
3. **What is the precise `sub_status` code in the Event ID 4625 log that indicates a bad password?**
   * *Answer format: 0x00000000*

---

## 🦠 Task 2: Suspicious PowerShell Execution & Reverse Shell
Following credential spraying, the attacker executed an encoded PowerShell payload on a workstation.

### Questions
1. **What destination port was targeted by the outbound PowerShell network connection?**
   * *Answer format: integer*
2. **What parent process launched `powershell.exe` on `WKSTN-FIN01.MEGACORP.LOCAL`?**
   * *Answer format: process.exe*

---

## 🛡️ Task 3: Privilege Escalation & Persistence via Service Creation
The attacker established persistence on the compromised workstation by installing a malicious Windows service.

### Questions
1. **What is the name of the malicious service installed by the attacker?**
   * *Answer format: ServiceName*
2. **What is the exact executable path of the service payload?**
   * *Answer format: C:\path\to\file.exe*

---

## 🚪 Task 4: Lateral Movement via PsExec Pivoting
Using stolen Domain Admin credentials, the attacker pivoted from `WKSTN-FIN01` to file server `FILE-SRV01`.

### Questions
1. **What binary process name (`Sysmon Event ID 1`) was executed under `services.exe` during PsExec remote invocation?**
   * *Answer format: filename.exe*

---

## 🕸️ Task 5: Web Shell Execution on DMZ Web Server
An uploaded ASPX web shell script was executed on DMZ web server `WEB-DMZ01`. A network sensor also captured the interaction.

### Questions
1. **What is the exact URI path of the uploaded web shell script?**
   * *Answer format: /path/to/shell.aspx*
2. **What specific User-Agent string was used by the attacker to interact with the web shell?**
   * *Answer format: ToolName/version*
3. **Analyze the PCAP file in Wireshark. What exact command did the attacker send to the web shell?**
   * *Answer format: command string*

---

## 💣 Task 6: Ransomware Execution & Shadow Copy Deletion
The attacker executed ransomware on the file server and deleted Volume Shadow Copies to prevent recovery.

### Questions
1. **What command-line flag did the attacker use with `vssadmin.exe` to suppress confirmation prompts?**
   * *Answer format: /flag*
2. **What is the file extension of the encrypted ransomware files?**
   * *Answer format: .EXTENSION*

---
Good luck with your investigation!
