#!/usr/bin/env python3
"""
Script pour tester les requirements et détecter les conflits.
"""
import subprocess
import sys

def test_requirements(filename):
    """Test l'installation d'un fichier requirements."""
    print(f"🔍 Testing {filename}...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--dry-run', '-r', filename
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {filename} - SUCCESS")
            return True
        else:
            print(f"❌ {filename} - FAILED")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ {filename} - ERROR: {e}")
        return False

def main():
    """Test tous les fichiers requirements."""
    files = [
        'requirements.txt',
        'requirements-flexible.txt', 
        'requirements-minimal.txt'
    ]
    
    print("🚀 GreenCart Requirements Checker")
    print("=" * 40)
    
    results = {}
    for file in files:
        results[file] = test_requirements(file)
        print()
    
    print("📊 SUMMARY:")
    print("=" * 40)
    for file, success in results.items():
        status = "✅ OK" if success else "❌ FAILED"
        print(f"{file}: {status}")
    
    if any(results.values()):
        print("\n🎉 At least one requirements file works!")
        return 0
    else:
        print("\n💥 All requirements files failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())