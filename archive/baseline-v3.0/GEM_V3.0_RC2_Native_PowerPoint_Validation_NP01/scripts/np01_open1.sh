#!/bin/zsh
T=~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_NP01_NATIVE_TEST
perl -e 'alarm 60; exec @ARGV' osascript -e 'on run argv
 with timeout of 50 seconds
  tell application "Microsoft PowerPoint" to open (POSIX file (item 1 of argv))
 end timeout
end run' "$T/NP01_Part_${1}_test_copy.pptx"
sleep 2
osascript -e 'tell application "Microsoft PowerPoint" to return (name of presentation 1) & " slides=" & (count of slides of presentation 1) & " saved=" & (saved of presentation 1 as string)'
