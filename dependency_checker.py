import sys
import subprocess
import importlib.util
from typing import List, Tuple

def check_and_install_dependencies() -> bool:
    """
    Check for required dependencies and install them if missing
    Returns True if all dependencies are available
    """
    
    required_packages = [
        ('watchdog', 'watchdog>=4.0.0'),
        ('docx', 'python-docx>=1.1.0'),  
        ('requests', 'requests>=2.31.0'),
        ('openai', 'openai==1.35.0'),
        ('colorama', 'colorama>=0.4.6'),
        ('dotenv', 'python-dotenv>=1.0.0'),
        ('lxml', 'lxml>=4.6.0')  # Critical for 100% formatting preservation
    ]
    
    missing_packages = []
    
    print("🔍 Checking dependencies...")
    
    for package_name, pip_name in required_packages:
        if not _is_package_installed(package_name):
            missing_packages.append(pip_name)
            print(f"   ❌ Missing: {package_name}")
        else:
            print(f"   ✅ Found: {package_name}")
    
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing dependencies...")
        
        for package in missing_packages:
            success = _install_package(package)
            if not success:
                print(f"❌ Failed to install {package}")
                print("Please run: pip3 install -r requirements.txt")
                return False
        
        print("✅ All dependencies installed successfully!")
    else:
        print("✅ All dependencies are already installed!")
    
    return True

def _is_package_installed(package_name: str) -> bool:
    """Check if a package is installed"""
    
    # Handle special cases
    package_map = {
        'docx': 'docx',
        'dotenv': 'dotenv',
        'lxml': 'lxml'
    }
    
    import_name = package_map.get(package_name, package_name)
    
    try:
        spec = importlib.util.find_spec(import_name)
        return spec is not None
    except (ImportError, ValueError, ModuleNotFoundError):
        return False

def _install_package(package: str) -> bool:
    """Install a package using pip"""
    try:
        print(f"   📥 Installing {package}...")
        
        # Try pip3 first, then pip
        for pip_cmd in ['pip3', 'pip']:
            try:
                result = subprocess.run(
                    [pip_cmd, 'install', package, '--user'], 
                    capture_output=True, 
                    text=True, 
                    timeout=120
                )
                
                if result.returncode == 0:
                    print(f"   ✅ {package} installed successfully!")
                    return True
                    
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        print(f"   ❌ Failed to install {package}")
        return False
        
    except Exception as e:
        print(f"   ❌ Error installing {package}: {e}")
        return False

def check_advanced_features() -> Tuple[bool, str]:
    """
    Check if advanced XML processing is available
    Returns (available, status_message)
    """
    try:
        import lxml.etree
        return True, "🚀 Advanced XML processing available - 100% formatting preservation enabled!"
    except ImportError:
        return False, "⚠️  Basic formatting only - install 'lxml' for 100% formatting preservation"

if __name__ == "__main__":
    # Test the dependency checker
    success = check_and_install_dependencies()
    advanced_available, message = check_advanced_features()
    
    print(f"\nDependency check: {'✅ Success' if success else '❌ Failed'}")
    print(message)