# Cybersecurity Portfolio Quick Start

## 🚀 Quick Access to Your Portfolio Automation

Your cybersecurity portfolio automation is now easily accessible from the main Cybersecurity folder!

## 📋 How to Run Portfolio Automation

### **Option 1: Python Script (Recommended)**
```bash
cd /Users/stephenmiller/Desktop/Cybersecurity
python3 run_portfolio.py
```

### **Option 2: Shell Script**
```bash
cd /Users/stephenmiller/Desktop/Cybersecurity
./portfolio.sh
```

### **Option 3: Direct Access**
```bash
cd /Users/stephenmiller/Desktop/Cybersecurity/Portfolio
python3 add_document.py
```

## 🎯 What These Scripts Do

Both scripts will:
1. **Check** that your portfolio is properly set up
2. **Navigate** to the Portfolio directory
3. **Launch** the automated document manager
4. **Guide you** through adding new documents

## 📁 File Structure

```
Cybersecurity/
├── run_portfolio.py          # Python runner script
├── portfolio.sh              # Shell runner script
├── PORTFOLIO_QUICK_START.md  # This file
└── Portfolio/                # Your organized portfolio
    ├── add_document.py       # Main automation tool
    ├── index.html            # Interactive web portfolio
    ├── README.md             # Portfolio overview
    └── [all your projects and documentation]
```

## 🎯 **Quick Commands**

### **Add a New Document**
```bash
# From Cybersecurity folder
python3 run_portfolio.py

# Or
./portfolio.sh
```

### **View Your Portfolio**
```bash
# Open the interactive web portfolio
open Portfolio/index.html

# Or visit online
open https://pianomansjpm.github.io/cybersecurity-portfolio
```

### **Update Portfolio on GitHub**
```bash
cd Portfolio
git add .
git commit -m "Update portfolio"
git push origin main
```

## 🛠️ **Troubleshooting**

### **Script won't run**
```bash
# Make sure scripts are executable
chmod +x run_portfolio.py
chmod +x portfolio.sh

# Try running with Python explicitly
python3 run_portfolio.py
```

### **Portfolio not found**
- Ensure you're in the `/Users/stephenmiller/Desktop/Cybersecurity` folder
- Check that the `Portfolio` directory exists

### **Permission errors**
```bash
# Fix permissions
chmod +x run_portfolio.py
chmod +x portfolio.sh
```

## 🎉 **Benefits**

- **Quick access**: Run from anywhere in the Cybersecurity folder
- **Error checking**: Scripts verify everything is set up correctly
- **Consistent experience**: Same interface regardless of how you run it
- **Easy maintenance**: Simple commands for portfolio management

## 🚀 **Pro Tips**

1. **Use the Python script** (`run_portfolio.py`) for the most reliable experience
2. **Keep the Cybersecurity folder** as your main workspace
3. **Run scripts from the Cybersecurity folder** for best results
4. **Check your portfolio regularly** at https://pianomansjpm.github.io/cybersecurity-portfolio

Your portfolio automation is now just one command away! 🛡️ 