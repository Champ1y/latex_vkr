$pdf_mode = 5;
$xelatex = 'xelatex -shell-escape -interaction=nonstopmode -halt-on-error %O %S';
$pdflatex = $xelatex;
$bibtex_use = 2;
$success_cmd = 'python3 tools/fix_pdf_semicolon.py rpz.pdf';
