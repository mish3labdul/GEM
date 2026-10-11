-- AR01 read-only native probe (no save, no edit). argv: presentationName, slideIndex, shapeName
-- Output (tab-separated, NO text content): header line with shape geometry + paragraph format; then one line per character: index, left, top, width.
on run argv
	set pn to item 1 of argv
	set si to (item 2 of argv) as integer
	set sn to item 3 of argv
	with timeout of 120 seconds
		tell application "Microsoft PowerPoint"
			set shp to shape sn of slide si of presentation pn
			set tf to text frame of shp
			set tr to text range of tf
			set pf to paragraph format of tr
			set hdr to "H" & tab & (left position of shp) & tab & (top of shp) & tab & (width of shp) & tab & (height of shp) & tab & (alignment of pf as string) & tab & (text direction of pf as string) & tab & (font name of font of tr) & tab & (font size of font of tr) & tab & (bold of font of tr as string)
			set res to hdr & linefeed
			set n to count of characters of tr
			repeat with i from 1 to n
				set c to character i of tr
				set res to res & "C" & tab & i & tab & (left bounds of c) & tab & (top bounds of c) & tab & (bounds width of c) & linefeed
			end repeat
			return res
		end tell
	end timeout
end run
