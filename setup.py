"""
NovaSales Dashboard - One-click Setup
Run: python setup.py
"""

import subprocess
import sys
import os


def run_step(desc, script):
    print(f"\n{'=' * 50}")
    print(f"  {desc}")
    print(f"{'=' * 50}")
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"FAILED: {script}")
        sys.exit(1)
    print(f"Done: {desc}")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  NovaSales Dashboard — Project Setup")
    print("=" * 50)

    for folder in ['data/raw', 'data/processed', 'assets',
                   'streamlit_app/pages', 'streamlit_app/utils']:
        os.makedirs(folder, exist_ok=True)
        print(f"Created: {folder}")

    run_step("Step 1/3: Generating sales data...", "src/data_generator.py")
    run_step("Step 2/3: Running commission engine...", "src/commission_engine.py")
    run_step("Step 3/3: Building SQLite database...", "src/database.py")

    print("\n" + "=" * 50)
    print("  SETUP COMPLETE!")
    print("=" * 50)
    print("\nLaunch app:")
    print("  streamlit run streamlit_app/app.py")