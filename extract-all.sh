#!/bin/bash
for f in *.zip; do unzip -d "${f%*.zip}" "$f"; done
mkdir zipfiles
mv *.zip zipfiles/
rm -rf Copy\ of\ BishopsKnightsB\ -\ Marcus\ Jaiclin/BishopsKnightsB/bishops_knights_b1/.git
git add .

