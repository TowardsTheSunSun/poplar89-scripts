#Action:{"name":"Open In Terminal","appleScriptHandler":"open_in_terminal_window","requiresDirectory":1}
#Action:{"name":"Open In Sublime","appleScriptHandler":"open_in_sublime"}

on open_in_terminal_window(dir)
	set p to (dir as text)
	tell application "Terminal"
		do script "cd " & quoted form of p
		activate
	end tell
end open_in_terminal_window

on open_in_sublime(dir)
	set p to (dir as text)
	tell application "Terminal"
		do script "subl " & quoted form of p
	end tell
end open_in_sublime
