# ManageEngine LOG360 Incident Response Lab

«اللَّهُمَّ انْفَعْنَا بِمَا عَلَّمْتَنَا، وَعَلِّمْنَا مَا يَنْفَعُنَا، وَزِدْنَا عِلْمًا»
إن كان هناك توفيق وتمام فمن الله وحده، وإن كان هناك تقصير فمني ومن الشيطان.

---

Welcome to the **ManageEngine LOG360 Incident Response Learning Lab**! Designed specifically for cybersecurity instructors and SOC students, this lab replicates TryHackMe and HackTheBox style interactive learning environments.

---

## 🚀 Deployment Options

### Option 1: Standalone Browser (Quickest & Easiest)
No Docker or Kubernetes required! To work with this lab, you must first download the files to your own computer.

**Step 1:** Download the project from GitHub. You can either use Git to clone the repository or download the ZIP file:
```bash
# To clone using Git:
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```
*(If you downloaded the ZIP file instead, extract it and open the extracted folder).*

**Step 2:** Open the interactive dashboard directly in your web browser. Simply double-click the **`index.html`** file in your file explorer, or run it from the command line:
```bash
# Open directly in your browser
start index.html  # On Windows
open index.html   # On macOS
```

---

### Option 2: Run with Docker Compose
To deploy the lab container stack (Web Portal + Syslog Collector + Attack Log Generator):
```bash
# Clone or navigate to lab directory
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME

# Start containers in detached mode
docker compose up -d

# Access the web app in your browser at:
http://localhost:8080
```

To stop the Docker lab:
```bash
docker compose down -v
```

---

### Option 3: Deploy to Kubernetes (Minikube / K3s / Cloud K8s)
Deploy the lab to a Kubernetes cluster using raw manifests:
```bash
# Create namespace & deploy lab
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check running pod status
kubectl get pods -n log360-lab

# Access via NodePort (Default: http://<NODE-IP>:30080)
```

---

### Option 4: Deploy using Helm Chart
Deploy the lab via Helm:
```bash
# Install Helm release
helm install log360-lab ./k8s/helm -n log360-lab --create-namespace

# Uninstall Helm release
helm uninstall log360-lab -n log360-lab
```

---

## 📂 Project Structure
```
log360-ir-lab/
├── index.html                 # Main THM/HTB-Style Interactive Web App
├── CHALLENGE.md               # Student Room Guide & Investigation Tasks
├── README.md                  # Lab Documentation & Quickstart
├── docker-compose.yml         # Multi-container Docker orchestration
├── generator/
│   └── log_generator.py       # Attack Log Generator & Syslog Streamer
└── k8s/                       # Kubernetes Manifests & Helm Chart
    ├── namespace.yaml
    ├── configmap.yaml
    ├── deployment.yaml
    ├── service.yaml
    └── helm/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
```

---

## 🛡️ License & Educational Use
Created for cybersecurity instructors, university professors, and security analysts to train hands-on SOC incident response skills. Free for educational and non-commercial training.

---
**Created by Ahmed Atef**
