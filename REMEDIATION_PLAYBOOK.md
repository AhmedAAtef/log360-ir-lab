# Real-World Incident Response Remediation & Containment Playbook

> [!IMPORTANT]
> **SOC OPERATIONAL PLAYBOOK**
> Finding the malicious log entry is only 50% of an Incident Responder's job. This playbook details the exact real-world containment, eradication, and remediation steps required for each stage of the compromise.

---

## 🛡️ Step-by-Step Operational Remediation Actions

### 1. Containment of Password Spraying (Task 1)
* **Real-World Action**: Block threat actor IP at Perimeter Firewall & Disable/Reset compromised AD user accounts.
* **Active Directory PowerShell Command**:
  ```powershell
  # Disable compromised account immediately
  Disable-ADAccount -Identity "a.davis"
  
  # Revoke all active Kerberos TGT tickets
  Purge-KrbTgt -TargetUser "a.davis"
  ```
* **Firewall Rule (Palo Alto / Cisco ASA / Linux iptables)**:
  ```bash
  # Block attacker IP on perimeter firewall
  iptables -A INPUT -s 10.14.22.99 -j DROP
  ```

---

### 2. Eradication of PowerShell C2 Reverse Shell (Task 2)
* **Real-World Action**: Isolate host from the network & terminate malicious PowerShell process tree.
* **Windows Endpoint Isolation PowerShell Command**:
  ```powershell
  # Terminate malicious PowerShell process tree by PID
  Stop-Process -Name "powershell" -Force
  
  # Block outbound connection to C2 IP 10.14.22.99
  New-NetFirewallRule -DisplayName "Block C2 IP 10.14.22.99" -Direction Outbound -RemoteAddress "10.14.22.99" -Action Block
  ```

---

### 3. Removal of Persistence Backdoor Service (Task 3)
* **Real-World Action**: Delete registered malicious Windows service & remove dropped binary from filesystem.
* **Command Prompt (Admin)**:
  ```cmd
  :: Stop the malicious service
  sc.exe stop WinHealthMonitorSvc
  
  :: Delete service registry entry
  sc.exe delete WinHealthMonitorSvc
  
  :: Delete malicious binary payload
  del /f /q "C:\Users\Public\Libraries\svc_host_patch.exe"
  ```

---

### 4. Containment of PsExec Lateral Movement (Task 4)
* **Real-World Action**: Terminate PsExec service on target server & reset compromised Domain Administrator credentials.
* **Domain Controller PowerShell**:
  ```powershell
  # Force immediate Domain Administrator password reset across AD
  Set-ADAccountPassword -Identity "Administrator" -Reset
  
  # Terminate PsExec service on File Server
  Invoke-Command -ComputerName "FILE-SRV01" -ScriptBlock {
      Stop-Service -Name "PSEXESVC" -ErrorAction SilentlyContinue
      sc.exe delete PSEXESVC
  }
  ```

---

### 5. Web Shell Eradication & IIS Hardening (Task 5)
* **Real-World Action**: Delete uploaded webshell file, restart IIS Application Pool, and restrict web upload directory permissions.
* **PowerShell (IIS Server)**:
  ```powershell
  # Delete ASPX web shell payload
  Remove-Item -Path "C:\inetpub\wwwroot\assets\vendors\shell_v2.aspx" -Force
  
  # Restart IIS Application Pool
  Restart-WebAppPool -Name "DefaultAppPool"
  
  # Disable Execution permissions on Uploads folder in IIS
  Set-WebConfigurationProperty -Filter 'system.webServer/handlers' -PSPath 'IIS:\Sites\Default Web Site\assets\vendors' -Name 'accessPolicy' -Value 'Read'
  ```

---

### 6. Ransomware Recovery & Backup Restoration (Task 6)
* **Real-World Action**: Isolate storage server, restore Volume Shadow Copies from offline/immutable backups, and apply YARA rule.
* **Recovery Steps**:
  1. Disconnect `FILE-SRV01` network interface to halt encryption spread.
  2. Restore immutable cloud / VSS backups taken prior to incident timestamp.
  3. Deploy LockBit YARA signature across endpoint EDR to hunt remaining artifacts.
