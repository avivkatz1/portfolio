# Project Structure

## Directory Layout

```
image_processing_git_portfolio/
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── src/                        # Source code
│   ├── final_detection.py      # Main roof detection algorithm
│   ├── functions.py            # Core image processing functions
│   ├── run_all.py             # Main entry point
│   └── generate_slideshow.py  # Slideshow generation script
├── images/
│   ├── examples/              # Sample input images
│   ├── results/               # Detection results with scores
│   ├── slideshow/             # Step-by-step process visualizations
│   │   ├── top1_image09/      # Best result (93% DICE score)
│   │   ├── top2_image11/      # Second best (90% DICE)
│   │   ├── top3_image18/      # Third best (85% DICE)
│   │   ├── failure_image05/   # Example failure case
│   │   └── ...                # More examples
│   └── pipeline_success.jpg   # Pipeline visualization
└── docs/                      # Additional documentation
```

## Key Files

- **final_detection.py**: Main detection pipeline using edge detection, connected components, and shape analysis
- **functions.py**: Utility functions for image processing (Sobel, thresholding, morphology)
- **run_all.py**: Run the complete detection pipeline on all images
- **generate_slideshow.py**: Create step-by-step visualizations

## Image Scores

Results are labeled with DICE coefficient scores:
- Success: 60-93% accuracy
- Failures: 0-37% accuracy (missed or low accuracy detections)

## Slideshow Folders

Each slideshow folder contains 8 frames showing the processing pipeline:
1. Original image
2. Red channel extraction
3. Sobel edge detection
4. Connected components
5. Shape filtering
6. Detection overlay
7. Final result
8. Summary
