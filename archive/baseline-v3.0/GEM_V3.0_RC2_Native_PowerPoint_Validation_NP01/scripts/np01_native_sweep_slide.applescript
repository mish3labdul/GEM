-- NP01 read-only native sweep of ONE slide in an already-open presentation. No save, no edit.
-- argv: presentationName, slideIndex.  Output: tab-separated rows (S=shape, P=paragraph, N=notes).
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
	if (length of s) > 90 then set s to (text 1 thru 90 of s)
	return s
end clean

on emitShape(shp, tg, si, idx)
	tell application "Microsoft PowerPoint"
		set stype to (shape type of shp) as string
		set nm to name of shp
		set vis to (visible of shp) as string
		set rw to "S" & tab & si & tab & idx & tab & nm & tab & stype & tab & vis & tab & tg
		set acc to ""
		try
			if has text frame of shp then
				set tf to text frame of shp
				set tr to text range of tf
				set f to font of tr
				set txt to my clean(content of tr)
				set fam to (font name of f) as string
				set asc to (ASCII name of f) as string
				set ea to (east asian name of f) as string
				set cs to (font name other of f) as string
				set bld to (bold of f) as string
				set sz to (font size of f) as string
				set bh to (bounds height of tr) as string
				set sh to (height of shp) as string
				set wr to (word wrap of tf) as string
				set au to (auto size of tf) as string
				set rw to rw & tab & fam & tab & asc & tab & ea & tab & cs & tab & bld & tab & sz & tab & bh & tab & sh & tab & wr & tab & au & tab & txt
				set acc to acc & rw & linefeed
				-- Range-level bold=true can be PowerPoint's MIXED state (run boundary inside a word); resolve per character.
				if bld is "true" or fam is "" or fam is "missing value" then
					set nch to count of characters of tr
					set boldN to 0
					set firstB to 0
					set fset to ""
					repeat with c from 1 to nch
						set cr to character c of tr
						set cf to font of cr
						if (bold of cf) is true then
							set boldN to boldN + 1
							if firstB is 0 then set firstB to c
						end if
						set cn to (font name of cf) as string
						if fset does not contain ("|" & cn & "|") then set fset to fset & "|" & cn & "|"
					end repeat
					set acc to acc & "B" & tab & si & tab & idx & tab & boldN & tab & nch & tab & firstB & tab & fset & linefeed
				end if
				set npg to count of paragraphs of tr
				if npg > 1 then
					repeat with p from 1 to npg
						set pr to paragraph p of tr
						set pf to font of pr
						set acc to acc & "P" & tab & si & tab & idx & tab & p & tab & (font name of pf) & tab & (bold of pf) & tab & (font size of pf) & tab & (my clean(content of pr)) & linefeed
					end repeat
				end if
				return acc
			end if
		end try
		return rw & linefeed
	end tell
end emitShape

on run argv
	set pn to item 1 of argv
	set si to (item 2 of argv) as integer
	with timeout of 60 seconds
		tell application "Microsoft PowerPoint"
			set sl to slide si of presentation pn
			set res to ""
			set n to count of shapes of sl
			repeat with i from 1 to n
				set shp to shape i of sl
				set res to res & my emitShape(shp, "", si, i)
				if (shape type of shp as string) is "shape type group" then
					try
						set gi to group items of shp
						set gn to count of gi
						repeat with g from 1 to gn
							set res to res & my emitShape(item g of gi, "grp" & i, si, i & "." & g)
						end repeat
					end try
				end if
			end repeat
			try
				set npg to notes page of sl
				repeat with k from 1 to (count of shapes of npg)
					set ns to shape k of npg
					if has text frame of ns then
						set res to res & "N" & tab & si & tab & k & tab & (name of ns) & tab & (shape type of ns as string) & tab & (my clean(content of text range of text frame of ns)) & linefeed
					end if
				end repeat
			end try
			return res
		end tell
	end timeout
end run
