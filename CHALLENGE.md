# TryHackMe / HackTheBox Challenge Room: ManageEngine LOG360 Incident Response

## 📝 Scenario: Enterprise Intrusion at MegaCorp Domain
Welcome, Security Analyst! You have recently been hired as a Junior SOC Analyst at MegaCorp. 

Late Friday night, an automated alert fired in your **ManageEngine LOG360 SIEM** dashboard. The alert indicated anomalous authentication spikes, malicious process creations, lateral movement, web shell triggers, and volume shadow copy deletion across the internal Active Directory network (`MEGACORP.LOCAL`).

Your objective is to investigate the log repository inside the interactive **LOG360 Console**, reconstruct the attacker's kill chain, answer the incident investigation questions, and stop the ongoing breach!

---

## 🎯 Lab Instructions & Objectives
As a SOC Analyst, you will be using ManageEngine LOG360 to:
1. **Analyze logs** from multiple sources including Active Directory (ADAudit Plus), Windows Sysmon, Web Servers, and Firewalls.
2. **Correlate events** to build a timeline of the attacker's actions.
3. **Map techniques** to the MITRE ATT&CK framework.
4. **Propose remediation steps** to contain the threat.

## 🖥️ How to Submit Answers & Track Progress
To submit your answers, verify flags, unlock hints, and access detailed **ManageEngine LOG360 Search Queries & MITRE ATT&CK Walkthroughs**, open the **[index.html](index.html)** file directly in your web browser!

---

## 📘 Section 1: What is ManageEngine LOG360?
Before starting the investigation, review the **"Section 1: What is ManageEngine LOG360?"** collapsible panel inside `index.html`. It covers:
* What LOG360 is and how it works (6-stage data pipeline)
* Its 5 core integrated modules (EventLog Analyzer, ADAudit Plus, Cloud Security Plus, M365 Security Plus, UEBA/SOAR)
* Its ranking in the **Gartner Magic Quadrant for SIEM (2024 & 2025)**
* Comparison with Splunk, Microsoft Sentinel, IBM QRadar, ELK Stack, and Wazuh

## 📚 Section 2: Learning Resources & Extra Materials
Review the **"Section 2: Learning Resources"** panel for direct links to:
* Official LOG360 product documentation
* LOG360 search query syntax reference guide
* Windows Event ID alert reference
* YouTube video tutorials and walkthroughs
* LOG360 Elevate self-paced training program
* MECPA (ManageEngine Certified Product Associate) certification
* MITRE ATT&CK Enterprise Matrix
* LOG360 PitStop community forum

---

## 🧪 Task 0: LOG360 Search Query Practice (Warm-Up)
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
5. **Filter by Log Source = Sysmon and Severity = CRITICAL. What hostname appears most frequently?**
   * *Answer format: HOSTNAME.DOMAIN*

---

## 🔍 Task 1: Active Directory Password Spray & Account Lockout
A remote threat actor attempted an NTLM password spraying attack targeting multiple user accounts on the Domain Controller.
* **MITRE ATT&CK Mapping**: **[T1110.003 - Password Spraying](https://attack.mitre.org/techniques/T1110/003/)**

### Questions
1. **What is the IP address of the attacker initiating the password spray attack?**
   * *Answer format: X.X.X.X*
2. **Which Windows Event ID in LOG360 indicates a failed logon attempt?**
   * *Answer format: integer*
3. **Which domain user account was locked out (`Event ID 4740`) as a result of the spraying attack?**
   * *Answer format: string*

---

## 💻 Task 2: Suspicious PowerShell Execution & Reverse Shell
Following credential spraying, the attacker executed an encoded PowerShell payload on a workstation.
* **MITRE ATT&CK Mapping**: **[T1059.001 - Command and Scripting Interpreter: PowerShell](https://attack.mitre.org/techniques/T1059/001/)**

### Questions
1. **What is the hostname of the workstation where PowerShell was executed?**
   * *Answer format: HOSTNAME.DOMAIN*
2. **What is the Sysmon Event ID that records Process Creation?**
   * *Answer format: integer*
3. **What destination port was targeted by the outbound PowerShell reverse shell connection (`Sysmon Event ID 3`)?**
   * *Answer format: integer*

---

## ⚙️ Task 3: Privilege Escalation & Persistence via Service Creation
To maintain access, the attacker created a backdoor service running with SYSTEM privileges.
* **MITRE ATT&CK Mapping**: **[T1543.003 - Create or Modify System Process: Windows Service](https://attack.mitre.org/techniques/T1543/003/)**

### Questions
1. **What is the Windows Event ID recorded in System log for new service creation?**
   * *Answer format: integer*
2. **What is the name of the malicious service registered by the attacker?**
   * *Answer format: string*
3. **What is the file path of the executable executed by this new service?**
   * *Answer format: C:\path\to\file.exe*

---

## 🌐 Task 4: Lateral Movement via PsExec
Using stolen Domain Admin credentials, the attacker pivoted from `WKSTN-FIN01` to `FILE-SRV01`.
* **MITRE ATT&CK Mapping**: **[T1021.002 - Remote Services: SMB/Windows Admin Shares](https://attack.mitre.org/techniques/T1021/002/)**

### Questions
1. **What Logon Type in Windows Audit logs (`Event ID 4624`) indicates a Remote Interactive (RDP) logon?**
   * *Answer format: integer*
2. **What binary name (`Sysmon Event ID 1`) was executed under `services.exe` during the PsExec remote execution?**
   * *Answer format: filename.exe*

---

## 🕸️ Task 5: Web Shell Execution on Web Server
The external DMZ web server (`WEB-DMZ01`) was compromised via an uploaded web shell.
* **MITRE ATT&CK Mapping**: **[T1505.003 - Server Software Component: Web Shell](https://attack.mitre.org/techniques/T1505/003/)**

### Questions
1. **What is the exact URI path of the uploaded web shell script?**
   * *Answer format: /path/to/shell.aspx*
2. **What specific User-Agent string was used by the attacker to interact with the web shell?**
   * *Answer format: ToolName/version*
3. **Analyze the PCAP file in Wireshark. What exact command did the attacker send to the web shell?**
   * *Answer format: command string*

---

## 💣 Task 6: Ransomware Execution & Shadow Copy Deletion
Prior to encrypting network files, the attacker executed commands to delete Volume Shadow Copies.
* **MITRE ATT&CK Mapping**: **[T1490 - Inhibit System Recovery](https://attack.mitre.org/techniques/T1490/)**

### Questions
1. **What Windows utility command-line was executed to delete system shadow copies (`vssadmin`)?**
   * *Answer format: string*
2. **What new file extension was appended to the encrypted backup files on the file server?**
   * *Answer format: .EXTENSION*

---

## 🛡️ MITRE ATT&CK Matrix Mapping Reference

| Lab Task | Attack Scenario | MITRE Tactic | MITRE Technique | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | Password Spraying | Credential Access | **[T1110.003](https://attack.mitre.org/techniques/T1110/003/)** | Automated NTLM spraying across AD users |
| **Task 2** | PowerShell Reverse Shell | Execution | **[T1059.001](https://attack.mitre.org/techniques/T1059/001/)** | Base64 encoded PowerShell execution |
| **Task 3** | Persistence Service | Persistence | **[T1543.003](https://attack.mitre.org/techniques/T1543/003/)** | Malicious Windows Service installation |
| **Task 4** | PsExec Pivoting | Lateral Movement | **[T1021.002](https://attack.mitre.org/techniques/T1021/002/)** | Admin share pivoting via PsExec |
| **Task 5** | ASPX Web Shell | Initial Access | **[T1505.003](https://attack.mitre.org/techniques/T1505/003/)** | Web shell deployment on IIS server |
| **Task 6** | Ransomware Shadow Deletion | Impact | **[T1490](https://attack.mitre.org/techniques/T1490/)** | Volume Shadow Copy destruction |
