#Action:{"name":"Open In Sublime","appleScriptHandler":"open_in_sublime"}

on open_in_sublime(dir)
	set p to (dir as text)
	do shell script "open /Applications/Sublime\\ Text.app " & quoted form of p
end open_in_sublime
