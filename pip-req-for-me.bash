#!/usr/bin/env bash
PKG=$1
pip install $PKG
pip freeze | grep $PKG >> req.in
pip freeze > req.txt
