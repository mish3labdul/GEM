-- AR01 read-only native Word probe (no save, no edit). argv: documentName
-- Output (tab-separated, NO text content). P rows: paragraph index, alignment, language ID, font name, complex-script font, size, bold, bold-bi, character spacing, char count.
-- X rows: paragraph index, character index, horizontal position relative to page (pt), horizontal position relative to text boundary (pt) for every character (single-character ranges made with create range).
-- NOTE (AR01): the page-relative reading returns sporadic outliers (e.g. the first character of a paragraph); the text-boundary reading is smooth and is the one the analysis uses.
on run argv
	set dn to item 1 of argv
	with timeout of 240 seconds
		tell application "Microsoft Word"
			set d to document dn
			set np to count of paragraphs of d
			set res to "D" & tab & np & tab & (count of sections of d) & linefeed
			repeat with i from 1 to np
				set p to paragraph i of d
				set r to text object of p
				set f to font object of r
				set n to count of characters of r
				set res to res & "P" & tab & i & tab & (alignment of p as string) & tab & (language ID of r as string) & tab & (name of f) & tab & (complex script name of f) & tab & (font size of f) & tab & (bold of f as string) & tab & (bold bi of f as string) & tab & (spacing of f) & tab & n & linefeed
				set s0 to (get start of content of r)
				repeat with j from 1 to n
					set cr to create range d start (s0 + j - 1) end (s0 + j)
					set res to res & "X" & tab & i & tab & j & tab & (get range information cr information type horizontal position relative to page) & tab & (get range information cr information type horizontal position relative to text boundary) & linefeed
				end repeat
			end repeat
			return res
		end tell
	end timeout
end run
