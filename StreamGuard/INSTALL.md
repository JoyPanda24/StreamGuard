# StreamGuard - Installation Guide

Complete setup instructions for Windows, Linux, and macOS.

## Quick Start

### Windows
```bash
git clone https://github.com/yourusername/StreamGuard.git
cd StreamGuard/StreamGuard
setup.bat
```

### Linux/Mac
```bash
git clone https://github.com/yourusername/StreamGuard.git
cd StreamGuard/StreamGuard
chmod +x setup.sh
./setup.sh
```

---

## Detailed Installation by OS

### Windows

#### Prerequisites
- Windows 7 or later
- Internet connection

#### Steps

1. **Install Python 3.10+**
   - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Verify installation:
   ```bash
   python --version
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/StreamGuard.git
   cd StreamGuard/StreamGuard
   ```

3. **Run Setup Script**
   ```bash
   setup.bat
   ```

4. **Start Development Server**
   ```bash
   .venv\Scripts\activate.bat
   cd backend
   python app.py
   ```

---

### Ubuntu / Debian / Linux Mint

#### Prerequisites
- Ubuntu 18.04+ or Debian 10+
- sudo access

#### Steps

1. **Install Python and Dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv build-essential git
   ```

2. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/StreamGuard.git
   cd StreamGuard/StreamGuard
   ```

4. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

5. **Start Development Server**
   ```bash
   source .venv/bin/activate
   cd backend
   python app.py
   ```

#### Troubleshooting

- **ModuleNotFoundError for pip**: Run `sudo apt install python3-pip`
- **Permission denied**: Run `chmod +x setup.sh` before executing

---

### Fedora / RHEL / CentOS

#### Prerequisites
- Fedora 30+, RHEL 8+, or CentOS 8+
- sudo access

#### Steps

1. **Install Python and Dependencies**
   ```bash
   sudo dnf install -y python3 python3-pip git
   sudo dnf groupinstall -y "Development Tools"
   ```

2. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/StreamGuard.git
   cd StreamGuard/StreamGuard
   ```

4. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

5. **Start Development Server**
   ```bash
   source .venv/bin/activate
   cd backend
   python app.py
   ```

---

### Arch Linux / Manjaro / Garuda

#### Prerequisites
- Arch Linux or Arch-based distro
- sudo access (if not running as root)

#### Steps

1. **Install Python and Dependencies**
   ```bash
   sudo pacman -S python python-pip git base-devel
   ```

2. **Verify Installation**
   ```bash
   python --version
   pip --version
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/StreamGuard.git
   cd StreamGuard/StreamGuard
   ```

4. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

5. **Start Development Server**
   ```bash
   source .venv/bin/activate
   cd backend
   python app.py
   ```

---

### Parrot OS / Kali Linux

#### Prerequisites
- Parrot OS 5.0+ or Kali Linux 2021+
- sudo access

#### Steps

1. **Update System**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Python and Dependencies**
   ```bash
   sudo apt install -y python3 python3-pip python3-venv build-essential git
   ```

3. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/StreamGuard.git
   cd StreamGuard/StreamGuard
   ```

5. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

6. **Start Development Server**
   ```bash
   source .venv/bin/activate
   cd backend
   python app.py
   ```

#### Note
Parrot OS is perfect for security research. StreamGuard's threat detection features integrate well with Parrot's security tools.

---

### macOS

#### Prerequisites
- macOS 10.12+
- Internet connection

#### Steps

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python3 git
   ```

3. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/StreamGuard.git
   cd StreamGuard/StreamGuard
   ```

5. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

6. **Start Development Server**
   ```bash
   source .venv/bin/activate
   cd backend
   python app.py
   ```

---

## Manual Setup (All Platforms)

If you prefer to set up manually without scripts:

### 1. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate.bat

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cd backend
cp .env.example .env
# Edit .env as needed
```

### 4. Run Application
```bash
python app.py
```

---

## Verifying Installation

### Check Python Installation
```bash
python --version  # Windows
python3 --version  # Linux/Mac
```

### Check Virtual Environment
```bash
# If activated correctly, your prompt should show (.venv)
which python  # Linux/Mac
where python  # Windows
```

### Run Tests
```bash
cd backend
python test_app.py
```

Expected output:
```
Ran 17 tests in 0.019s
OK
```

---

## Common Issues

### Issue: "Python not found"
**Solution**: Add Python to PATH
- **Windows**: Reinstall Python with "Add Python to PATH" checked
- **Linux**: Python3 should be in PATH by default
- **Mac**: Install via Homebrew: `brew install python3`

### Issue: "pip: command not found"
**Solution**: Install pip
```bash
# Ubuntu/Debian
sudo apt install python3-pip

# Fedora
sudo dnf install python3-pip

# Arch
sudo pacman -S python-pip

# Mac
brew install python3
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Activate virtual environment and reinstall
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
```

### Issue: "Permission denied" on setup.sh
**Solution**: Make script executable
```bash
chmod +x setup.sh
./setup.sh
```

### Issue: Database not found
**Solution**: Automatic - database creates on first run
- Windows: `~/StreamGuardDB/streamguard.db`
- Linux/Mac: `~/.streamguard/streamguard.db`

---

## Uninstallation

### Remove StreamGuard
```bash
# Windows
rmdir /s StreamGuard

# Linux/Mac
rm -rf StreamGuard
```

### Remove Data
```bash
# Windows
rmdir /s %USERPROFILE%\StreamGuardDB

# Linux/Mac
rm -rf ~/.streamguard
```

---

## Getting Help

If you encounter issues:

1. Check that all prerequisites are installed
2. Ensure you're in the correct directory
3. Verify Python version (3.10+)
4. Run setup script again
5. Check test suite: `python test_app.py`

---

## Next Steps

After successful installation:

1. **Start Server**
   ```bash
   cd backend
   python app.py
   ```

2. **Test API**
   ```bash
   curl http://localhost:5000
   ```

3. **Run Tests**
   ```bash
   python test_app.py
   ```

4. **Read Main README**
   See [README.md](README.md) for API documentation and features

---

## Environment Configuration

Edit `backend/.env` for custom settings:

```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

Default data locations:
- **Windows**: `C:\Users\{username}\StreamGuardDB`
- **Linux**: `/home/{username}/.streamguard`
- **Mac**: `/Users/{username}/.streamguard`

---
