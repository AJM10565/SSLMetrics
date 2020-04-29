#!/usr/bin/env bash

echo "Running all metrics scripts for repository: $1"

docker volume create metrics

# Run Issues
cd Issues
./metrics.sh $1 $2
cd ..

# Run GitModule
cd GitModule
./metrics.sh $1
cd ..

# Run Issue_Spoilage
cd Issue_Spoilage
./metrics.sh $1 $2
cd ..

# Run Defect Density (this command should also copy volume content to the current dir)
cd Defect_Density
./metrics.sh $1 $2
cd ..

# Run Graph
cd Graph
./metrics.sh $1
cd ..



