#!/usr/bin/env bash

echo "Running all metrics scripts for repository: $1"

docker volume create metrics

# Run Commits
cd Commits
./metrics.sh $1 $2
cd ..

# Run Issues
cd Issues
./metrics.sh $1 $2
cd ..

# Run Lines of Code
cd Lines_Of_Code_Num_Of_Chars
./metrics.sh $1 $2
cd ..

# Run Issue_Spoilage
cd Issue_Spoilage
./metrics.sh $1 $2
cd ..

# Run Defect Density (this command should also copy volume content to the current dir)
cd Defect_Density
./metrics.sh $1 $2
cd ..


