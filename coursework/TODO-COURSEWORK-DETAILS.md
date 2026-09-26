# TODO: Complete Coursework Details

This file tracks placeholders that need to be filled in the coursework section before the repositories are fully polished.

## Current Coursework Structure

The following courses have folder structure but need term/year and highlights filled in:

### 1. DSC-445 Machine Learning
**File:** `DSC-445-machine-learning/README.md`
- [ ] Fill `[term]` with actual semester/year (e.g., "Fall 2024")
- [ ] Fill `[best assignment]` with actual assignment title/description
- [ ] Verify assignment folders have complete READMEs

### 2. CSC-480 Artificial Intelligence I
**File:** `CSC-480-artificial-intelligence-1/README.md`
- [ ] Fill `[term]` with actual semester/year
- [ ] Fill `[best assignment]` with actual assignment title/description
- [ ] Verify assignment folders have complete READMEs

### 3. CSC-580 Artificial Intelligence II
**File:** `CSC-580-artificial-intelligence-2/README.md`
- [ ] Fill `[term]` with actual semester/year
- [ ] Fill `[best assignment]` with actual assignment title/description
- [ ] Verify assignment folders have complete READMEs

### 4. CSC-483 Applied Deep Learning
**File:** `CSC-483-applied-deep-learning/README.md`
- [ ] Fill `[term]` with actual semester/year
- [ ] Fill `[best assignment]` with actual assignment title/description
- [ ] Verify assignment folders have complete READMEs

### 5. SE-489 MLOps
**File:** `SE-489-mlops/README.md`
- [ ] Fill `[term]` with actual semester/year
- [ ] Fill `[best assignment]` with actual assignment title/description
- [ ] Verify assignment folders have complete READMEs

## Future Courses to Add

### Robotics (Current Work)
- [ ] Create folder: `CSC-XXX-robotics/` (or appropriate course code)
- [ ] Add DRAKE file and project
- [ ] Write course README using template in `../templates/course-template.md`
- [ ] Document Drake animations work

### Other Graduate Coursework
- [ ] Hunt down and identify other completed courses
- [ ] For each course:
  - [ ] Create course folder using `../scripts/new-course.sh`
  - [ ] Add assignments
  - [ ] Write course-level README
  - [ ] Update main `coursework/README.md` with new course

## Suggested Organization Approach

**For existing courses:**
1. Go through each course folder one by one
2. Review actual assignment submissions to identify the best work
3. Fill in the term/year from your records
4. Update the course README highlighting your best assignment
5. Ensure each assignment folder has a clear README explaining what it does

**For new courses (robotics, etc.):**
1. Use `scripts/new-course.sh CSC-XXX "Course Name"` to scaffold
2. Move your code/notebooks into appropriate assignment folders
3. Write READMEs for each assignment (see `templates/assignment-template.md`)
4. Add course to the main `coursework/README.md` table

## Notes

- Don't feel pressured to add everything at once - start with your strongest work
- Robotics/DRAKE project might be especially impressive for AI roles
- Each course can have 1-5 assignments - choose quality over quantity
- Make sure any datasets in `data/` folders are not private/sensitive

## After Completion

Once coursework details are filled in:
- [ ] Remove this TODO file
- [ ] Commit updates: `git commit -m "Add coursework details and highlights"`
- [ ] Push: `git push`
- [ ] GitHub Actions link checker should pass
