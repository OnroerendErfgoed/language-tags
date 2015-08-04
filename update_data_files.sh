#!/usr/bin/env bash

# Install language_subtag-registry with npm from config in package.json
npm install

# Copy necessary data files into project
cp -r node_modules/language-subtag-registry/data/json language_tags/data

# Delete installed node_modules folder
rm -r node_modules