# wordleTTY

A text-based client for the popular Wordle game, to play in your terminal. Real programmers don't need browsers!  
Compatible with ANSI and VT220-style terminals. Has built-in monochrome fallback mode. 

play remotely:  
`telnet wordle.xereeto.co.uk 7777 `  
`telnet wordle.xereeto.co.uk 7777 -l random`, for a random puzzle  
`telnet wordle.xereeto.co.uk 7777 -l play-lineonly`, to play in single line mode (for dumb terminals)  
`telnet wordle.xereeto.co.uk 7777 -l play-lineonly-random`, for a random puzzle in single line mode   
or  
`ssh play@wordle.xereeto.co.uk -p 9999`  
`ssh play-random@wordle.xereeto.co.uk -p 9999`, for a random puzzle  
`ssh play-lineonly@wordle.xereeto.co.uk -p 9999`, to play in single line mode (for dumb terminals)  
`ssh play-lineonly-random@wordle.xereeto.co.uk -p 9999`, for a random puzzle in single line mode  

don't try to log in as root over telnet

dial-up version coming soom (yes, really)
![image](https://user-images.githubusercontent.com/4806744/152666421-ca5dd7a1-6da2-475d-9aa1-377486a37ed6.png)
