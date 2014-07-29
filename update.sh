
#ON Ubuntu:
cp parsers/parseflat.py Presidio/files/metadata
#generate field_descriptions.json?
cp parsers/parseInput.py Presidio/files/texts

ulimit -s unlimited

python Presidio/files/metadata/parseFlat.py
python Presidio/files/texts/parseInput.py

rm Presidio/files/texts/parseInput.py
rm Presidio/files/metadata/parseFlat.py

#need to increase memory limits
make all bookwormName=MHL_Bookworm

