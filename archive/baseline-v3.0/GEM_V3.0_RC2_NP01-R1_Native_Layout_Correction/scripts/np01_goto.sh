#!/bin/zsh
osascript -e "tell application \"Microsoft PowerPoint\" to go to slide (view of active window) number $1" 2>&1
osascript -e 'tell application "Microsoft PowerPoint" to return "slide " & (slide index of slide of view of active window as string) & " saved=" & (saved of presentation 1 as string)' 2>&1
