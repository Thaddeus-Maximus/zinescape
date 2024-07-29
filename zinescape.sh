#!/bin/sh

# usage: exporter.sh <directory> <number of pages in booklet>

WIDTH=5.5
HEIGHT=8.5
SPACING=1.0
MARGIN=0.5

for i in "$@"; do
  case $i in
    n=*)
      NPAGES="${i#*=}"
      shift # past argument=value
      ;;
    w=*)
      WIDTH="${i#*=}"
      shift # past argument=value
      ;;
    h=*)
      HEIGHT="${i#*=}"
      shift # past argument=value
      ;;
    s=*)
      SPACING="${i#*=}"
      shift # past argument=value
      ;;
    m=*)
      MARGIN="${i#*=}"
      shift # past argument=value
      ;;

    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
    *)
		if [ -z "${CMD}" ]; then
			CMD="${i}"
		else
			FNAME="${i}"
		fi
      ;;
  esac
done

EXT="${FNAME##*.}"
FBASE="${FNAME%.*}"

case $CMD in
	compile)

		pdfbook2 --paper=letter -n -o 0 -i 0 -t 0 -b 0 --signature=$NPAGES "${FNAME}"
		gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile="${FBASE}-book_compressed.pdf" "${FBASE}-book.pdf"
		gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile="${FBASE}-compressed.pdf" "${FBASE}.pdf"
		exit 0
	;;
	template)
		truncate -s 0 "${FNAME}"
		echo "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
			<svg
			   width=\"${WIDTH}in\"
			   height=\"${HEIGHT}in\"
			   viewBox=\"0 0 ${WIDTH} ${HEIGHT}\"
			   version=\"1.1\"
			   id=\"svg5\"
			   inkscape:version=\"1.2.2 (b0a8486541, 2022-12-01)\"
			   sodipodi:docname=\"out_split.svg\"
			   inkscape:export-filename=\"/mnt/data/Branding/med.png\"
			   inkscape:export-xdpi=\"95.999992\"
			   inkscape:export-ydpi=\"95.999992\"
			   xml:space=\"preserve\"
			   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"
			   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"
			   xmlns=\"http://www.w3.org/2000/svg\"
			   xmlns:svg=\"http://www.w3.org/2000/svg\"><defs
			     id=\"defs21\" /><sodipodi:namedview
			     id=\"namedview7\"
			     pagecolor=\"#ffffff\"
			     bordercolor=\"#666666\"
			     borderopacity=\"1.0\"
			     inkscape:pageshadow=\"2\"
			     inkscape:pageopacity=\"0.0\"
			     inkscape:pagecheckerboard=\"0\"
			     inkscape:document-units=\"in\"
			     showgrid=\"false\"
			     inkscape:snap-global=\"false\"
			     fit-margin-top=\"0\"
			     fit-margin-left=\"0\"
			     fit-margin-right=\"0\"
			     fit-margin-bottom=\"0\"
			     units=\"in\"
			     inkscape:zoom=\"1\"
			     inkscape:cx=\"270\"
			     inkscape:cy=\"535.5\"
			     inkscape:window-width=\"1036\"
			     inkscape:window-height=\"1040\"
			     inkscape:window-x=\"10\"
			     inkscape:window-y=\"30\"
			     inkscape:window-maximized=\"1\"
			     inkscape:current-layer=\"svg5\"
			     width=\"${WIDTH}in\"
			     inkscape:showpageshadow=\"2\"
			     inkscape:deskcolor=\"#d1d1d1\"
			     showguides=\"false\"
			     inkscape:lockguides=\"false\"><inkscape:grid
			   type=\"xygrid\"
			   id=\"grid1046\"
			   originx=\"0\"
			   originy=\"0\"
			   spacingy=\"1\"
			   spacingx=\"1\"
			   units=\"in\"
			   visible=\"false\" />" >> "${FNAME}"


				for i in $(seq 1 $NPAGES); do
					j=$i

					if [ $i -eq $NPAGES ]; then
						j=0
					fi

			    	echo '<inkscape:page' >> "${FNAME}"
			        echo "x=\"$(echo "($j-1)*$WIDTH + (($j/2) + ($j%2)/2) * $SPACING" | bc)\"" >> "${FNAME}"
			        echo 'y="0"' >> "${FNAME}"
			        echo "width=\"${WIDTH}\"" >> "${FNAME}"
			        echo "height=\"${HEIGHT}\"" >> "${FNAME}"
			        echo "id=\"page${i}\"" >> "${FNAME}"
			        echo "margin=\"${MARGIN}\"" >> "${FNAME}"
			        echo 'bleed="0"/>' >> "${FNAME}"
				done

				echo "</svg>" >> "${FNAME}"
				exit 0
			   ;;

	*)
		echo "Usage: zinescape <command> <file> <arguments>"
		echo "       zinescape compile input.pdf n=12"
		echo "       zinescape template output.pdf n=12"
		exit 1
		;;
esac
