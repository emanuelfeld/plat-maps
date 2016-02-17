(define (filename-basename orig-name)
    (car (strbreakup orig-name "."))
)

(define (get-file-path filename)
  (unbreakupstr (reverse (cdr (reverse (strbreakup filename "/")))) "/")
)

(define (script-fu-export-selection img layer)
	(define imgPath (car (gimp-image-get-filename img)))
	(define imgDir (get-file-path imgPath))
	(define outputName (filename-basename 
		(car (gimp-drawable-get-name layer))
	))
	(define imageNewPath (string-append (unbreakupstr (list imgDir outputName) "/") ".tif"))
	(gimp-layer-add-alpha layer)
	(gimp-selection-invert img)
	(gimp-edit-clear layer)
	(file-tiff-save
		RUN-NONINTERACTIVE
		img
		layer
		imageNewPath
		imageNewPath
		1
	)
)


(script-fu-register
	"script-fu-export-selection"                ;func name
	"Export Selection"                          ;menu label
	"Export a selection as a TIFF."                             ;description
	"elefbet"                                   ;author
	"Public Domain"                             ;copyright notice
	"2015"                                      ;date created
	""                                          ;image type that the script works on
	SF-IMAGE    "Image"    0
	SF-DRAWABLE "Drawable" 0
)
(script-fu-menu-register "script-fu-export-selection" "<Image>/Script-Fu")
