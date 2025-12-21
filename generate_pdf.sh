#!/bin/bash

# Script to generate PDF from REPORT.md
# Usage: ./generate_pdf.sh

cd "$(dirname "$0")"

echo "Generating PDF from REPORT.md..."

# Try with xelatex first (better Unicode support)
pandoc REPORT.md \
    -o "CDD_Project2_Report_Ahmed_Wahba.pdf" \
    --pdf-engine=xelatex \
    -V geometry:margin=2.5cm \
    -V fontsize=11pt \
    -V documentclass=article \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    -V mainfont="DejaVu Sans" \
    -V monofont="DejaVu Sans Mono" \
    --toc \
    --toc-depth=3 \
    --highlight-style=tango \
    2>/dev/null

if [ $? -eq 0 ]; then
    echo "PDF generated successfully: CDD_Project2_Report_Ahmed_Wahba.pdf"
    exit 0
fi

echo "xelatex failed, trying pdflatex..."

# Fallback: Create a version without Unicode diagrams
sed 's/[┌┐└┘│─├┤┬┴┼▼►◄▲]/+/g; s/[│]/|/g' REPORT.md > REPORT_ascii.md

pandoc REPORT_ascii.md \
    -o "CDD_Project2_Report_Ahmed_Wahba.pdf" \
    --pdf-engine=pdflatex \
    -V geometry:margin=2.5cm \
    -V fontsize=11pt \
    -V documentclass=article \
    -V colorlinks=true \
    --toc \
    --toc-depth=3 \
    --highlight-style=tango

if [ $? -eq 0 ]; then
    echo "PDF generated successfully: CDD_Project2_Report_Ahmed_Wahba.pdf"
    rm -f REPORT_ascii.md
    exit 0
fi

# Final fallback: very simple conversion
echo "Trying simple HTML to PDF conversion..."

pandoc REPORT.md -o REPORT.html
if command -v wkhtmltopdf &> /dev/null; then
    wkhtmltopdf REPORT.html "CDD_Project2_Report_Ahmed_Wahba.pdf"
    rm -f REPORT.html
    echo "PDF generated via wkhtmltopdf"
else
    echo "Generated HTML instead: REPORT.html"
    echo "You can convert to PDF using a browser or online tool"
fi
