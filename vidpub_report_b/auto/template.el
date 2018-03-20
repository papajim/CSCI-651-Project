(TeX-add-style-hook
 "template"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("$documentclass$" "$if(fontsize)$$fontsize$" "$endif$$if(lang)$$babel-lang$" "$endif$$if(papersize)$$papersize$" "$endif$$for(classoption)$$classoption$$sep$" "$endfor$")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("$fontfamily$" "$for(fontfamilyoptions)$$fontfamilyoptions$$sep$" "$endfor$") ("fontenc" "$if(fontenc)$$fontenc$$else$T1$endif$") ("inputenc" "utf8") ("geometry" "$for(geometry)$$geometry$$sep$" "$endfor$") ("babel" "shorthands=off" "$for(babel-otherlangs)$$babel-otherlangs$" "$endfor$main=$babel-lang$") ("biblatex" "backend=bibtex" "style=numeric" "hyperref=true" "backref=true" "maxnames=99") ("ulem" "normalem") ("bidi" "RTLdocument")))
   (TeX-run-style-hooks
    "latex2e"
    "packages"
    "macros"
    "$documentclass$"
    "$documentclass$10"
    "$fontfamily$"
    "lmodern"
    "setspace"
    "amssymb"
    "amsmath"
    "ifxetex"
    "ifluatex"
    "fixltx2e"
    "fontenc"
    "inputenc"
    "eurosym"
    "mathspec"
    "fontspec"
    "xeCJK"
    "upquote"
    "microtype"
    "geometry"
    "hyperref"
    "babel"
    "polyglossia"
    "natbib"
    "biblatex"
    "listings"
    "fancyvrb"
    "longtable"
    "booktabs"
    "graphicx"
    "grffile"
    "ulem"
    "bidi")
   (TeX-add-symbols
    '("LR" 1)
    '("RL" 1)
    "euro"
    "tightlist"
    "maxwidth"
    "maxheight")
   (LaTeX-add-environments
    "RTL"
    "LTR")
   (LaTeX-add-bibliographies
    "$for(bibliography)$$bibliography$$sep$"
    "$endfor$")))

