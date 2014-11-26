#!/bin/sh

pyinstaller risc.py
mkdir -p ../../release/nix
mv dist/risc/ ../../release/nix
cp risc.example.ini ../../release/nix/risc
cp ../../README ../../release/nix
cp run-screen.sh ../../release/nix/risc
cp -R ../extplugins ../../release/nix
rm -r dist
rm -r build
rm risc.spec
echo Done
