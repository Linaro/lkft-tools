#!/bin/sh

mkdir -p $HOME/bin
for f in $(find bin/ -maxdepth 1 -executable -type f); do
    ln -fs $(pwd)/${f} $HOME/bin/
done
