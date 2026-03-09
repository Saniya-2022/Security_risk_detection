"""
Installation Verification Script for Mini SIEM
Checks all components and dependencies
"""

import os
import sys
import importlib

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check Python version"""
    print("\n🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n🔍 Checking Python dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pymongo',
        'sklearn',
        'joblib',
        'numpy',
        'pandas',
        'faker',
        'pydantic',
        'websockets',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                importlib.import_module('sklearn')
            elif package == 'dotenv':
                importlib.import_module('dotenv')
            else:
                importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed")
        return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔍 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Create .env file with:")
        print("  MONGO_URI=mongodb+srv://...")
        print("  SENDER_EMAIL=your-email@gmail.com")
        print("  SENDER_PASSWORD=your-app-password")
        return False
    
    print("✅ .env file exists")
    
    # Check if variables are set
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['MONGO_URI', 'SENDER_EMAIL', 'SENDER_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var} is set")
        else:
            print(f"  ❌ {var} is missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def check_directory_structure():
    """Check if all required directories exist"""
    print("\n🔍 Checking directory structure...")
    
    required_dirs = [
        'backend',
        'backend/api',
        'backend/datasets',
        'backend/detection',
        'backend/ml',
        'backend/ml/models',
        'backend/security',
        'backend/database',
        'backend/runtime',
        'frontend',
        'frontend/src'
    ]
    
    missing = []
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✅ {directory}")
        else:
            print(f"  ❌ {directory} (missing)")
            missing.append(directory)
    
    if missing:
        print(f"\n❌ Missing directories: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All directories present")
        return True

def check_datasets():
    """Check if datasets are generated"""
    print("\n🔍 Checking datasets...")
    
    datasets = [
        'backend/datasets/email_dataset.csv',
        'backend/datasets/login_dataset.csv',
        'backend/datasets/network_dataset.csv',
        'backend/datasets/malware_dataset.csv'
    ]
    
    missing = []
    for dataset in datasets:
        if os.path.exists(dataset):
            print(f"  ✅ {os.path.basename(dataset)}")
        else:
            print(f"  ❌ {os.path.basename(dataset)} (not generated)")
            missing.append(dataset)
    
    if missing:
        print("\n⚠️  Datasets not generated")
        print("Run: python backend/datasets/generate_datasets.py")
        return False
    else:
        print("\n✅ All datasets generated")
        return True

def check_ml_models():
    """Check if ML models are trained"""
    print("\n🔍 Checking ML models...")
    
    models = [
        'backend/ml/models/phishing_model.pkl',
        'backend/ml/models/phishing_vectorizer.pkl',
        'backend/ml/models/login_model.pkl',
        'backend/ml/models/network_model.pkl',
        'backend/ml/models/malware_model.pkl'
    ]
    
    missing = []
    for model in models:
        if os.path.exists(model):
            print(f"  ✅ {os.path.basename(model)}")
        else:
            print(f"  ❌ {os.path.basename(model)} (not trained)")
            missing.append(model)
    
    if missing:
        print("\n⚠️  ML models not trained")
        print("Run: python backend/ml/train_all_models.py")
        return False
    else:
        print("\n✅ All ML models trained")
        return True

def check_frontend():
    """Check if frontend dependencies are installed"""
    print("\n🔍 Checking frontend...")
    
    if not os.path.exists('frontend/node_modules'):
        print("❌ Frontend dependencies not installed")
        print("Run: cd frontend && npm install")
        return False
    
    print("✅ Frontend dependencies installed")
    return True

def check_mongodb_connection():
    """Test MongoDB connection"""
    print("\n🔍 Testing MongoDB connection...")
    
    try:
        from backend.database.mongo import client
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("Check your MONGO_URI in .env file")
        return False

def main():
    print_header("Mini SIEM - Installation Verification")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Config", check_env_file),
        ("Directory Structure", check_directory_structure),
        ("Datasets", check_datasets),
        ("ML Models", check_ml_models),
        ("Frontend", check_frontend),
        ("MongoDB Connection", check_mongodb_connection)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error checking {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} checks passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("\n🎉 All checks passed! Your Mini SIEM is ready to run!")
        print("\nNext steps:")
        print("1. Start backend: uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000")
        print("2. Start frontend: cd frontend && npm start")
        print("3. Access dashboard: http://localhost:3000")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nQuick fixes:")
        print("- Missing dependencies: pip install -r requirements.txt")
        print("- Missing datasets: python backend/datasets/generate_datasets.py")
        print("- Missing models: python backend/ml/train_all_models.py")
        print("- Missing .env: cp .env.example .env (then edit with your credentials)")
        print("- Frontend deps: cd frontend && npm install")

if __name__ == "__main__":
    main()
