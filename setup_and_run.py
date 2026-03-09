"""
Quick Setup and Run Script for Mini SIEM
Automates the entire setup process
"""

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(command, description):
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print("\nPlease create a .env file with:")
        print("MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/security_risk_detection")
        print("SENDER_EMAIL=your-email@gmail.com")
        print("SENDER_PASSWORD=your-app-password")
        return False
    print("✅ .env file found")
    return True

def main():
    print_header("Mini SIEM - Automated Setup")
    
    # Check environment file
    if not check_env_file():
        sys.exit(1)
    
    # Step 1: Generate datasets
    print_header("Step 1: Generating Synthetic Datasets")
    if not run_command(
        "python backend/datasets/generate_datasets.py",
        "Dataset generation"
    ):
        print("⚠️  Dataset generation failed, but continuing...")
    
    # Step 2: Train ML models
    print_header("Step 2: Training ML Models")
    if not run_command(
        "python backend/ml/train_all_models.py",
        "ML model training"
    ):
        print("⚠️  ML training failed, but continuing...")
    
    # Step 3: Instructions for running
    print_header("Setup Complete!")
    print("✅ All setup steps completed successfully!\n")
    print("📋 Next Steps:\n")
    print("1. Start the backend server:")
    print("   uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000\n")
    print("2. In a new terminal, start the frontend:")
    print("   cd frontend")
    print("   npm install  (first time only)")
    print("   npm start\n")
    print("3. Access the dashboard at: http://localhost:3000")
    print("4. API documentation at: http://localhost:8000/docs\n")
    print("🎉 Your Mini SIEM is ready to use!")

if __name__ == "__main__":
    main()
