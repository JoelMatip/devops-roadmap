#!/bin/bash

name="DevOps Learner"
echo "Welcome, $name!"

for i in {1..3}
do
  echo "Day $i of DevOps practice"
done

if [ -f hello.sh ]; then
  echo "Found your hello.sh script!"
else
  echo "No hello.sh script found."
fi