"""
Train Multiple ML Models on UNSW-NB15 Dataset
Compares Random Forest, Logistic Regression, and XGBoost
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import joblib
from pathlib import Path
import time

from datasets.unsw_loader import UNSWDatasetLoader

class UNSWModelTrainer:
    """Train and evaluate multiple ML models"""
    
    def __init__(self):
        self.loader = UNSWDatasetLoader()
        self.models = {}
        self.results = {}
        self.model_dir = Path('backend/ml/models')
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def train_all_models(self):
        """Train Random Forest, Logistic Regression, and XGBoost"""
        print("="*60)
        print("UNSW-NB15 ML MODEL TRAINING")
        print("="*60)
        
        # Load training data
        print("\n📂 Loading training dataset...")
        train_df = self.loader.load_dataset('UNSW_NB15_training-set.csv')
        
        # Preprocess
        print("\n🔧 Preprocessing data...")
        train_df = self.loader.preprocess_data(train_df, fit_encoders=True)
        X_train, y_train, attack_types_train = self.loader.prepare_training_data(train_df)
        
        print(f"✅ Training samples: {len(X_train)}")
        print(f"✅ Features: {len(self.loader.feature_columns)}")
        print(f"✅ Attack samples: {sum(y_train)}, Normal samples: {len(y_train) - sum(y_train)}")
        
        # Handle class imbalance with SMOTE
        print("\n⚖️ Balancing classes with SMOTE...")
        smote = SMOTE(random_state=42, k_neighbors=5)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        print(f"✅ Balanced samples: {len(X_train_balanced)}")
        
        # Load test data
        print("\n📂 Loading test dataset...")
        test_df = self.loader.load_dataset('UNSW_NB15_testing-set.csv')
        test_df = self.loader.preprocess_data(test_df, fit_encoders=False)
        X_test, y_test, attack_types_test = self.loader.prepare_test_data(test_df)
        print(f"✅ Test samples: {len(X_test)}")
        
        # Train models
        print("\n" + "="*60)
        print("TRAINING MODELS")
        print("="*60)
        
        # 1. Random Forest
        print("\n🌲 Training Random Forest...")
        start = time.time()
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=10,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        rf_model.fit(X_train_balanced, y_train_balanced)
        rf_time = time.time() - start
        self.models['random_forest'] = rf_model
        print(f"✅ Random Forest trained in {rf_time:.2f}s")
        
        # 2. Logistic Regression
        print("\n📊 Training Logistic Regression...")
        start = time.time()
        lr_model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            n_jobs=-1,
            solver='saga'
        )
        lr_model.fit(X_train_balanced, y_train_balanced)
        lr_time = time.time() - start
        self.models['logistic_regression'] = lr_model
        print(f"✅ Logistic Regression trained in {lr_time:.2f}s")
        
        # 3. XGBoost
        print("\n🚀 Training XGBoost...")
        start = time.time()
        xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=10,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        )
        xgb_model.fit(X_train_balanced, y_train_balanced)
        xgb_time = time.time() - start
        self.models['xgboost'] = xgb_model
        print(f"✅ XGBoost trained in {xgb_time:.2f}s")
        
        # Evaluate all models
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        for model_name, model in self.models.items():
            print(f"\n📈 Evaluating {model_name.upper()}...")
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            
            self.results[model_name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'training_time': rf_time if model_name == 'random_forest' else (lr_time if model_name == 'logistic_regression' else xgb_time)
            }
            
            print(f"  Accuracy:  {accuracy*100:.2f}%")
            print(f"  Precision: {precision*100:.2f}%")
            print(f"  Recall:    {recall*100:.2f}%")
            print(f"  F1-Score:  {f1*100:.2f}%")
        
        # Select best model
        best_model_name = max(self.results, key=lambda x: self.results[x]['accuracy'])
        best_accuracy = self.results[best_model_name]['accuracy']
        
        print("\n" + "="*60)
        print("BEST MODEL SELECTION")
        print("="*60)
        print(f"\n🏆 Best Model: {best_model_name.upper()}")
        print(f"🎯 Accuracy: {best_accuracy*100:.2f}%")
        
        # Save all models
        print("\n💾 Saving models...")
        for model_name, model in self.models.items():
            model_path = self.model_dir / f'unsw_{model_name}.pkl'
            joblib.dump(model, model_path)
            print(f"  ✅ Saved {model_name} to {model_path}")
        
        # Save best model as default
        best_model_path = self.model_dir / 'unsw_best_model.pkl'
        joblib.dump(self.models[best_model_name], best_model_path)
        print(f"  ✅ Saved best model to {best_model_path}")
        
        # Save preprocessor
        self.loader.save_preprocessor()
        
        # Save model metadata
        metadata = {
            'best_model': best_model_name,
            'results': self.results,
            'feature_count': len(self.loader.feature_columns),
            'training_samples': len(X_train_balanced),
            'test_samples': len(X_test)
        }
        metadata_path = self.model_dir / 'unsw_model_metadata.pkl'
        joblib.dump(metadata, metadata_path)
        print(f"  ✅ Saved metadata to {metadata_path}")
        
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETE!")
        print("="*60)
        
        return best_model_name, best_accuracy
    
    def print_comparison_table(self):
        """Print model comparison table"""
        print("\n" + "="*80)
        print("MODEL COMPARISON TABLE")
        print("="*80)
        print(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("-"*80)
        
        for model_name, metrics in self.results.items():
            print(f"{model_name:<25} "
                  f"{metrics['accuracy']*100:>10.2f}% "
                  f"{metrics['precision']*100:>10.2f}% "
                  f"{metrics['recall']*100:>10.2f}% "
                  f"{metrics['f1_score']*100:>10.2f}%")
        print("="*80)

if __name__ == '__main__':
    trainer = UNSWModelTrainer()
    
    try:
        best_model, accuracy = trainer.train_all_models()
        trainer.print_comparison_table()
        
        print(f"\n🎉 Training successful!")
        print(f"🏆 Best model: {best_model}")
        print(f"🎯 Accuracy: {accuracy*100:.2f}%")
        print(f"\n📁 Models saved in: backend/ml/models/")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📥 Please download UNSW-NB15 dataset:")
        print("   1. Visit: https://research.unsw.edu.au/projects/unsw-nb15-dataset")
        print("   2. Download: UNSW_NB15_training-set.csv and UNSW_NB15_testing-set.csv")
        print("   3. Place files in: backend/datasets/")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
