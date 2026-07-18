# ManageEngine LOG360 - V2 Live Enterprise Lab

Welcome to the V2 Lab! This directory contains everything needed to spin up a fully live, 50-endpoint enterprise SIEM environment using Docker and a custom Python Traffic Engine.

## 👨‍🏫 Instructor Guide: How to Start the Lab from Scratch

### Step 1: Start the LOG360 SIEM
1. Open your terminal in this `log360-v2-live` folder.
2. Run the following command to start the ManageEngine SIEM container:
   ```bash
   docker-compose up -d
   ```
3. Wait a minute for the container to initialize, then open your browser and go to `http://localhost:8095` (or your server's IP).
4. **CRITICAL:** Inside the LOG360 UI, go to **Settings > Configuration > Syslog Server** and ensure the Syslog Receiver is enabled on **UDP Port 514**.

### Step 2: Start the Live Traffic Engine
1. Open a second terminal window in this folder.
2. Run the traffic generator:
   ```bash
   python v2_traffic_generator.py
   ```
3. **Leave this script running!** It will instantly begin spoofing 50 devices, pushing continuous background noise (successful logins, firewall traffic) into the SIEM. 
4. Every 2 minutes, it automatically injects the entire 25-step Advanced Persistent Threat (APT) attack sequence into the logs so students can find it.

---

## 🕵️‍♂️ Student Guide: How to Play the Lab

1. Provide your students with the URL to the LOG360 Dashboard (e.g., `http://your-ip:8095`).
2. Give the students the `CHALLENGE_V2.md` file. This is their incident response briefing containing the **25 investigative questions**.
3. Instruct students to use the **Search** and **Dashboards** tabs in LOG360 to hunt for the answers. They will need to filter by Event IDs, IPs, and hostnames to piece the attack together.

---

## 🔑 Answer Key

When the lab is over, you can grade the students using the `INSTRUCTOR_GUIDE_V2.md` file, which contains the exact answers to all 25 questions that the Python script generates.
