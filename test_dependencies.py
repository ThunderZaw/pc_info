"""
Quick Test Script - Verify all dependencies are installed
"""

import sys

print("=" * 70)
print(" " * 20 + "DEPENDENCY CHECK")
print("=" * 70)
print()

# Check Python version
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print()

# Check required modules
required_modules = {
    'psutil': 'System and process utilities',
    'wmi': 'Windows Management Instrumentation',
    'platform': 'Platform identification (built-in)',
    'socket': 'Network interface (built-in)',
    'winreg': 'Windows Registry access (built-in)',
    'ctypes': 'C library access (built-in)'
}

print("Checking required modules...")
print("-" * 70)

all_good = True
for module, description in required_modules.items():
    try:
        __import__(module)
        print(f"✓ {module:20s} - {description}")
    except ImportError:
        print(f"✗ {module:20s} - MISSING! ({description})")
        all_good = False

print("-" * 70)
print()

if all_good:
    print("SUCCESS! All dependencies are installed.")
    print("You can now run the System Information Collector.")
else:
    print("WARNING! Some dependencies are missing.")
    print("Please run: pip install -r requirements.txt")

print()
print("Press Enter to exit...")
input()
