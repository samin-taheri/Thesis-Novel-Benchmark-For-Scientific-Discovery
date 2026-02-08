#!/usr/bin/env python3
"""
Simple test script to verify the thesis benchmark setup is working correctly.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all main modules can be imported."""
    try:
        from src.config import ExperimentConfig
        from src.adapters import ADAPTERS
        from src.data.loaders import LOADERS
        from src.scenarios import SCENARIOS
        from src.eval.evaluator import Evaluator
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_adapters():
    """Test that adapters are properly configured."""
    try:
        from src.adapters import ADAPTERS
        print(f"✓ Available adapters: {list(ADAPTERS.keys())}")
        
        # Test mock adapter with proper initialization
        mock_adapter = ADAPTERS['mock'](
            model="mock-science-001",
            temperature=0.0,
            top_p=1.0,
            max_tokens=512
        )
        result = mock_adapter.generate("Test prompt", {"task_type": "equation"})
        print(f"✓ Mock adapter working: {result['content'][:50]}...")
        
        # Test that real adapters can be imported (but don't initialize without API keys)
        print("✓ Real adapters can be imported:")
        for name in ['openai', 'anthropic', 'google']:
            try:
                adapter_class = ADAPTERS[name]
                print(f"  - {name}: {adapter_class.__name__}")
            except Exception as e:
                print(f"  - {name}: Import failed - {e}")
        
        return True
    except Exception as e:
        print(f"✗ Adapter test failed: {e}")
        return False

def test_data_loaders():
    """Test that data loaders are working."""
    try:
        from src.data.loaders import LOADERS
        print(f"✓ Available loaders: {list(LOADERS.keys())}")
        
        # Test synthetic loader
        synthetic_loader = LOADERS['synthetic']()
        items = synthetic_loader.load(limit=3)
        print(f"✓ Synthetic loader working: {len(items)} items loaded")
        return True
    except Exception as e:
        print(f"✗ Data loader test failed: {e}")
        return False

def test_scenarios():
    """Test that scenarios are working."""
    try:
        from src.scenarios import SCENARIOS
        print(f"✓ Available scenarios: {list(SCENARIOS.keys())}")
        return True
    except Exception as e:
        print(f"✗ Scenario test failed: {e}")
        return False

def test_file_structure():
    """Test that required directories and files exist."""
    required_dirs = ['src', 'experiments', 'prompts', 'results', 'logs']
    required_files = ['requirements.txt', 'run_experiment.py', 'README.md']
    
    all_good = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Directory exists: {directory}")
        else:
            print(f"✗ Missing directory: {directory}")
            all_good = False
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ File exists: {file}")
        else:
            print(f"✗ Missing file: {file}")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("=== Thesis Benchmark Setup Test ===\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Adapters", test_adapters),
        ("Data Loaders", test_data_loaders),
        ("Scenarios", test_scenarios),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- Testing {test_name} ---")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append(False)
    
    print(f"\n=== Test Summary ===")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! Your setup is ready to go.")
        print("\nNext steps:")
        print("1. Run: python run_experiment.py experiments/example_autobench.yaml")
        print("2. Check results/ and logs/ directories")
        print("3. To use real models, set up API keys and change 'provider' in YAML")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
