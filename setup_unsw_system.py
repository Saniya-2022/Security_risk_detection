"""
UNSW-NB15 Intrusion Detection System Setup Script
Automates installation, training, and system startup
"""
import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def run_command(command, description):
    """Run shell command with error handling"""
    print(f"▶️ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def check_dataset_files():
    """Check if UNSW-NB15 dataset files exist"""
    dataset_dir = Path('backend/datasets')
    training_file = dataset_dir / 'UNSW_NB15_training-set.csv'
    testing_file = dataset_dir / 'UNSW_NB15_testing-set.csv'
    
    if not training_file.exists() or not testing_file.exists():
        print("\n⚠️ UNSW-NB15 Dataset Not Found!")
        print("\n📥 Please download the dataset:")
        print("   1. Visit: https://research.unsw.edu.au/projects/unsw-nb15-dataset")
        print("   2. Download:")
        print("      - UNSW_NB15_training-set.csv")
        print("      - UNSW_NB15_testing-set.csv")
        print(f"   3. Place files in: {dataset_dir.absolute()}")
        print("\n❌ Cannot proceed without dataset files.")
        return False
    
    print("✅ Dataset files found")
    return True

def main():
    """Main setup process"""
    print_header("UNSW-NB15 INTRUSION DETECTION SYSTEM - SETUP")
    
    # Step 1: Check Python version
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        return
    
    # Step 2: Check dataset files
    print_header("STEP 1: Checking Dataset Files")
    if not check_dataset_files():
        return
    
    # Step 3: Install dependencies
    print_header("STEP 2: Installing Dependencies")
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    ):
        print("⚠️ Some packages may have failed. Continuing...")
    
    # Step 4: Train ML models
    print_header("STEP 3: Training ML Models")
    print("⏳ This may take 5-15 minutes depending on your hardware...")
    if not run_command(
        f"{sys.executable} backend/ml/train_unsw_models.py",
        "Training Random Forest, Logistic Regression, and XGBoost"
    ):
        print("❌ Model training failed. Please check errors above.")
        return
    
    # Step 5: Setup complete
    print_header("✅ SETUP COMPLETE!")
    
    print("📋 Next Steps:")
    print("\n1. Configure MongoDB Atlas:")
    print("   - Edit .env file")
    print("   - Add your MONGODB_URI")
    print("\n2. Configure Email (optional):")
    print("   - Edit .env file")
    print("   - Add SMTP settings for email alerts")
    print("\n3. Start the system:")
    print("   - Backend:  uvicorn backend.api.main_unsw:app --reload --host 0.0.0.0 --port 8000")
    print("   - Frontend: cd frontend && npm start")
    print("\n4. Access the dashboard:")
    print("   - Open: http://localhost:3000")
    print("   - API Docs: http://localhost:8000/docs")
    
    print("\n" + "="*70)
    print("🎉 Ready to detect intrusions!")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
