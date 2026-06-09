#!/bin/bash

# Create necessary package __init__.py files
mkdir -p analysis proto
touch analysis/__init__.py
touch proto/__init__.py

# Generate python stubs from the proto file
# The generated files will be placed in the proto/ directory
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/analyzer.proto

echo "Protobuf files generated successfully in proto/"
