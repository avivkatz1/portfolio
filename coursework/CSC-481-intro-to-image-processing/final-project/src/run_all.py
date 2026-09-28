#!/usr/bin/env python3
"""
Master script to run all detection, analysis, and evaluation.

Usage:
    python src/run_all.py
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and display results."""
    print(f"\n{'='*70}")
    print(f"{description}")
    print('='*70)

    result = subprocess.run([sys.executable, script_name],
                          capture_output=False,
                          text=True)

    if result.returncode != 0:
        print(f"⚠️  {script_name} failed with code {result.returncode}")
        return False
    return True


if __name__ == "__main__":
    src_dir = Path(__file__).parent

    print("="*70)
    print("RUNNING COMPLETE DETECTION PIPELINE")
    print("="*70)

    # Step 1: Generate validated detection results with IoU scoring
    if not run_script(
        str(src_dir / "generate_validated_results.py"),
        "Step 1: Generating Validated Results with IoU Scoring"
    ):
        print("❌ Failed to generate results")
        sys.exit(1)

    # Step 2: Generate pipeline analysis
    if not run_script(
        str(src_dir / "generate_pipeline_analysis.py"),
        "Step 2: Generating Pipeline Analysis"
    ):
        print("❌ Failed to generate pipeline analysis")
        sys.exit(1)

    # Step 3: Generate slideshow for top 3
    if not run_script(
        str(src_dir / "generate_slideshow.py"),
        "Step 3: Generating Slideshow for Top 3"
    ):
        print("⚠️  Slideshow generation skipped")

    # Step 4: Evaluate against ground truth
    if not run_script(
        str(src_dir / "evaluate_detections.py"),
        "Step 4: Evaluating Against Ground Truth"
    ):
        print("⚠️  Evaluation skipped (may not have ground truth)")

    print("\n" + "="*70)
    print("✓ COMPLETE!")
    print("="*70)
    print("\nResults locations:")
    print("  - Detection results: images/result_images/")
    print("  - Pipeline analysis: images/pipeline_images/")
    print("  - Slideshow (top 3): images/slideshow/")
    print("  - Evaluation report: evaluation_results.json")
    print("="*70)
