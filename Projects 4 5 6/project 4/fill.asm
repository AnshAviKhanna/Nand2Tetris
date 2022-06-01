// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Infinite loop that keeps on executing as per the keyboard input
(PRESS)
@KBD
D=M
@CHANGE_B
D;JGT       // go to CHANGE_B if Key is pressed
@CHANGE_W
D;JLE       // go to CHANGE_W if Key is not pressed

// loop to change the screen colour to black
(CHANGE_B)
    @0
    D=A
    (BLACKEN)
    @SCREEN
    A=A+D
    M=-1   // changes colour of the specified pixels to black
    D=D+1
    @8192
    D=D-A
    @PRESS
    D;JEQ  // go to press when colour of entire screen has been changed
    @8192
    D=D+A
    @BLACKEN
    0;JMP  // go to BLACKEN till the entire screen is not black

// loop to change the screen colour to white
(CHANGE_W)
    @0
    D=A
    (WHITEN)
    @SCREEN
    A=A+D
    M=0    // changes colour of the specified pixels to white
    D=D+1
    @8192
    D=D-A
    @PRESS
    D;JEQ  // go to press when colour of entire screen has been changed
    @8192
    D=D+A
    @WHITEN
    0;JMP  // go to BLACKEN till the entire screen is not white
    
