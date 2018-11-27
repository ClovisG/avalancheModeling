
DATADIR=~/Documents/projects/avalanches/data/epa
PARSEDDIR=~/Documents/projects/avalanches/data/epaParsed

mkdir -p $PARSEDDIR

for f in `ls $DATADIR`; do
	for pdfFile in `ls $DATADIR/$f/*.pdf`; do
		echo "Parsing $pdfFile..."
		fileName=$(basename $pdfFile)
		/home/clovis/software/poppler-master/utils/pdftotext  -fixed 3 "$pdfFile" "$PARSEDDIR/$fileName.txt"
	done;
done;

