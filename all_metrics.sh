#!/usr/bin/env bash

# Run Commits
./Commits/metrics.sh

# Run Issues
./Issues/metrics.sh

# Run Lines of Code
./Lines_Of_Code/metrics.sh

# Run Issue_Spoilage
./Issue_Spoilage/metrics.sh

# Run Defect Density (this command should also copy volume content to the current dir)
./Defect_Density/metrics.sh