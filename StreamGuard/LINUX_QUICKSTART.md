# StreamGuard - Linux Quick Start Guide

Fast setup for Linux users (Ubuntu, Arch, Parrot, etc.)

## 30-Second Setup

```bash
git clone https://github.com/yourusername/StreamGuard.git
cd StreamGuard/StreamGuard
chmod +x setup.sh
./setup.sh
source .venv/bin/activate
cd backend
python app.py
```

Visit: `http://localhost:5000`

---

## Ubuntu/Debian (Recommended)

```bash
# 1. Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

# 2. Clone and setup
git clone https://github.com/yourusername/StreamGuard.git
cd StreamGuard/StreamGuard
chmod +x setup.sh
./setup.sh

# 3. Activate and run
source .venv/bin/activate
cd backend
python app.py
```

---

## Arch Linux

```bash
# 1. Install dependencies
sudo pacman -Sy python python-pip git base-devel

# 2. Clone and setup
git clone https://github.com/yourusername/StreamGuard.git
cd StreamGuard/StreamGuard
chmod +x setup.sh
./setup.sh

# 3. Run
source .venv/bin/activate
cd backend
python app.py
```

---

## Parrot OS

```bash
# 1. Update and install
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git build-essential

# 2. Setup
git clone https://github.com/yourusername/StreamGuard.git
cd StreamGuard/StreamGuard
chmod +x setup.sh
./setup.sh

# 3. Run
source .venv/bin/activate
cd backend
python app.py
```

Perfect for Parrot's security research environment!

---

## Running as a Service (Ubuntu/Debian)

Run StreamGuard automatically on startup:

```bash
# 1. Create service file
sudo nano /etc/systemd/system/streamguard.service
```

Paste this:
```ini
[Unit]
Description=StreamGuard API Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/StreamGuard/StreamGuard
Environment="PATH=$HOME/StreamGuard/StreamGuard/.venv/bin"
ExecStart=$HOME/StreamGuard/StreamGuard/.venv/bin/python backend/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then:
```bash
# 2. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable streamguard
sudo systemctl start streamguard

# 3. Check status
sudo systemctl status streamguard

# View logs
journalctl -u streamguard -f
```

Stop service:
```bash
sudo systemctl stop streamguard
```

---

## Using in Terminal Only (No GUI)

If you don't have a graphical interface:

```bash
# Setup
chmod +x setup.sh
./setup.sh

# Activate environment
source .venv/bin/activate

# Test installation
python test_app.py

# Run server
cd backend
python app.py

# In another terminal, test API
curl http://localhost:5000
curl http://localhost:5000/api/geoip/8.8.8.8
```

---

## Troubleshooting

### "python: command not found"
Use `python3`:
```bash
python3 app.py
python3 test_app.py
```

### "pip: command not found"
Install: `sudo apt install python3-pip` (Ubuntu)

### Virtual environment not activating
```bash
source .venv/bin/activate
# Prompt should show (.venv) prefix
```

### Port 5000 in use
```bash
# Kill other process
lsof -i :5000
kill -9 <PID>

# Or use different port
FLASK_PORT=8000 python app.py
```

### Database errors
Data is in: `~/.streamguard/streamguard.db`

Delete to reset (data will recreate):
```bash
rm -rf ~/.streamguard
```

### Permission issues on setup.sh
```bash
chmod +x setup.sh
```

---

## Testing

```bash
cd backend
python test_app.py
```

Expected: `Ran 17 tests ... OK`

---

## Key Directories

```
StreamGuard/                          # Project root
├── StreamGuard/                      # Main package
│   ├── backend/                      # API code
│   ├── setup.sh                      # Linux setup (run this!)
│   ├── INSTALL.md                    # Detailed installation
│   └── requirements.txt              # Dependencies
└── README.md                         # Main documentation

~/.streamguard/                       # Data directory
├── streamguard.db                    # Database
├── isolation_forest.pkl              # ML model
└── scaler.pkl                        # ML scaler
```

---

## Common Commands

```bash
# Activate environment
source .venv/bin/activate

# Deactivate environment
deactivate

# Run tests
python test_app.py

# Run server
cd backend && python app.py

# Install more packages
pip install <package_name>

# Update packages
pip install --upgrade pip

# View installed packages
pip list
```

---

## Next Steps

1. **Start API**: `python app.py` in backend
2. **Test it**: `curl http://localhost:5000`
3. **Run tests**: `python test_app.py`
4. **Read docs**: See [README.md](README.md) and [INSTALL.md](INSTALL.md)

---

## Need Help?

- Check [INSTALL.md](INSTALL.md) for distro-specific guides
- Run test suite: `python test_app.py`
- Check logs in terminal output
- See API examples in README.md

---

**Made for Linux security professionals and developers** 🐧
