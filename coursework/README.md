# Graduate Coursework — M.S. in Artificial Intelligence, DePaul University

My own work from graduate courses: implementations, experiments, and write-ups.

| Course | Title | Term | Highlights |
| --- | --- | --- | --- |
| [DSC 445](DSC-445-machine-learning/) | Machine Learning I | [term] | [best assignment] |
| [CSC 480](CSC-480-artificial-intelligence-1/) | Artificial Intelligence I | [term] | [best assignment] |
| [CSC 481](CSC-481-intro-to-image-processing/) | Introduction to Image Processing | Winter 2025 | [Final project: finding houses in hand-drawn pictures](CSC-481-intro-to-image-processing/final-project/) — 93% best Dice |
| [CSC 580](CSC-580-artificial-intelligence-2/) | Artificial Intelligence II | [term] | [best assignment] |
| [CSC 483](CSC-483-applied-deep-learning/) | Applied Deep Learning | [term] | [best assignment] |
| [SE 489](SE-489-mlops/) | Machine Learning Operations (MLOps) | [term] | [best assignment] |

## How each course is organized

```
<COURSE-CODE>-<short-name>/
├── README.md                 Course overview + table of assignments
├── assignments/
│   └── hw01-<topic>/
│       ├── README.md         Problem (in my words), approach, results, what I learned
│       ├── notebooks/        Jupyter notebooks (outputs cleared or kept small)
│       ├── src/              Reusable Python code
│       ├── results/          Figures/metrics referenced in the README
│       └── requirements.txt  Pinned dependencies to reproduce
└── final-project/            Same structure as an assignment
```

New course: `./scripts/new-course.sh <CODE> "<Title>" "<Term>"` from the `portfolio/` folder.

## Academic integrity

- Only **my own work** is published here. Assignment prompts, starter code, solutions keys, and
  course datasets belong to the instructor/university and are **not** included; each README restates
  the problem in my own words.
- I publish work **after** the course ends, and I follow each instructor's policy on sharing solutions.
  If a course doesn't allow public solutions, I keep that work in a private repo.
- Collaborators and outside resources are credited in each assignment's README.
