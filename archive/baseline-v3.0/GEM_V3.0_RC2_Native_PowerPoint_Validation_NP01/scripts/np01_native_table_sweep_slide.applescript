-- NP01 read-only native sweep of table cells on ONE slide. No save, no edit.
-- argv: presentationName, slideIndex. Output rows: T (table summary), C (cell), K (cell char-level bold drill).
on clean(t)
	try
		set s to t as string
	on error
		return ""
	end try
	set AppleScript's text item delimiters to {linefeed, return, tab}
	set parts to text items of s
	set AppleScript's text item delimiters to " ⏎ "
	set s to parts as string
	set AppleScript's text item delimiters to ""
	if (length of s) > 60 then set s to (text 1 thru 60 of s)
	return s
end clean

on run argv
	set pn to item 1 of argv
	set si to (item 2 of argv) as integer
	with timeout of 120 seconds
		tell application "Microsoft PowerPoint"
			set sl to slide si of presentation pn
			set acc to ""
			repeat with i from 1 to (count of shapes of sl)
				set shp to shape i of sl
				if has table of shp then
					set tblObj to table object of shp
					set nr to count of rows of tblObj
					set nc to count of cells of row 1 of tblObj
					set acc to acc & "T" & tab & si & tab & i & tab & (name of shp) & tab & nr & tab & nc & linefeed
					repeat with r from 1 to nr
						repeat with cidx from 1 to nc
							try
								set tr to text range of text frame of shape of (cell cidx of row r of tblObj)
								set txt to my clean(content of tr)
								if txt is not "" then
									set f to font of tr
									set fam to (font name of f) as string
									set bld to (bold of f) as string
									set sz to (font size of f) as string
									set acc to acc & "C" & tab & si & tab & i & tab & r & tab & cidx & tab & fam & tab & bld & tab & sz & tab & txt & linefeed
									if bld is "true" or fam is "" or fam is "missing value" then
										set nch to count of characters of tr
										set boldN to 0
										set fset to ""
										repeat with k from 1 to nch
											set cr to character k of tr
											set cf to font of cr
											if (bold of cf) is true then set boldN to boldN + 1
											set cn to (font name of cf) as string
											if fset does not contain ("|" & cn & "|") then set fset to fset & "|" & cn & "|"
										end repeat
										set acc to acc & "K" & tab & si & tab & i & tab & r & tab & cidx & tab & boldN & tab & nch & tab & fset & linefeed
									end if
								end if
							on error e
								set acc to acc & "E" & tab & si & tab & i & tab & r & tab & cidx & tab & e & linefeed
							end try
						end repeat
					end repeat
				end if
			end repeat
			return acc
		end tell
	end timeout
end run
