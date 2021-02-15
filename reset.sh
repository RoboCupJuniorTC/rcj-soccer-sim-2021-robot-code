#!/bin/bash
git reset --hard
find ./ -iname logo.png | xargs rmdir --ignore-fail-on-non-empty
find ./ -iname robot1.py | xargs rmdir --ignore-fail-on-non-empty
find ./ -iname robot2.py | xargs rmdir --ignore-fail-on-non-empty
find ./ -iname robot3.py | xargs rmdir --ignore-fail-on-non-empty
find ./ -iname robot1 | xargs rmdir --ignore-fail-on-non-empty
find ./ -iname robot2 | xargs rmdir --ignore-fail-on-non-empty
find ./ -iname robot3 | xargs rmdir --ignore-fail-on-non-empty
find ./ -iname team_libraries | xargs rmdir
