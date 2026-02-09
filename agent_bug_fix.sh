#!/bin/bash

# must be run from the directory in which gemini-agent is the relative root
sed -i '' '/self\.precedence = {/,/}/ s/"\+": 2/"\+": 3/' ./calculator/pkg/calculator.py

# validate bug introduced
uv run calculator/main.py "3 + 7 * 2"

# fix bug with agent — capture output
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20" > agent_output.txt

# print output
cat agent_output.txt
