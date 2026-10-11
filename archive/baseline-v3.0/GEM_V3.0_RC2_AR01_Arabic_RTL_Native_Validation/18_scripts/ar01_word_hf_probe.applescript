-- AR01 read-only native Word header/footer + document-level probe (no save, no edit). argv: documentName
-- Output (tab-separated): S rows = section facts; H rows = header/footer kind, exists, char count, paragraph count, field count, alignment of paragraph 1, language ID.
on run argv
	set dn to item 1 of argv
	with timeout of 240 seconds
		tell application "Microsoft Word"
			set d to document dn
			set res to ""
			set sec to section 1 of d
			set pgs to (get range information (text object of d) information type number of pages in document)
			set res to res & "S" & tab & "pages" & tab & pgs & tab & "diff-first-page" & tab & (different first page header footer of page setup of sec as string) & tab & "fields-in-body" & tab & (count of fields of d) & linefeed
			repeat with kk0 in {"primary", "first"}
				set kk to contents of kk0
				repeat with isHd0 in {true, false}
					set isHd to contents of isHd0
					try
						if isHd then
							if kk is "primary" then set hf to get header sec index header footer primary
							if kk is "first" then set hf to get header sec index header footer first page
						else
							if kk is "primary" then set hf to get footer sec index header footer primary
							if kk is "first" then set hf to get footer sec index header footer first page
						end if
						set r to text object of hf
						set res to res & "H" & tab & kk & tab & (isHd as string) & tab & "-" & tab & (count of characters of r) & tab & (count of paragraphs of r) & tab & (count of fields of r) & tab & (alignment of paragraph 1 of r as string) & tab & (language ID of r as string) & linefeed
					on error m
						set res to res & "H" & tab & kk & tab & (isHd as string) & tab & "ERR " & m & linefeed
					end try
				end repeat
			end repeat
			return res
		end tell
	end timeout
end run
