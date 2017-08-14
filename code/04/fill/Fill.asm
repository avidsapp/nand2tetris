// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// SCREEN is predefined to RAM address 16384 (0x4000)
// KBD is predefined to RAM address 24576 (0x6000)

(START)
    @SCREEN   // call SCREEN address
    D=A       // set D to SCREEN address
    @pixel    // declare pixel variable to hold address of current pixel
    M=D       // initialize pixel to top left pixel of the screen

(LOOP)
    @KBD      // call KBD (keyboard input) address
    D=M       // set D to current KBD input

    @WHITE    // call WHITE label
    D;JEQ     // if D=0 (no keyboard input present) goto WHITE

    @BLACK    // call BLACK label
    D;JNE     // else if D!=0 (keyboard input present) goto BLACK

(WHITE)
    @pixel    // call pixel
    A=M       // set A to current pixel address
    M=0       // set pixel to white

    @INC      // call INC label
    0;JMP     // goto INC

(BLACK)
    @pixel    // call pixel
    A=M       // set A to current pixel address
    M=-1      // set pixel to black

    @INC      // call INC label
    0;JMP     // goto INC

(INC)
    @pixel    // call pixel
    D=M+1     // increment pixel
    M=D       // set pixel to incremented pixel
    @KBD      // call KBD
    D=A-D     // subtract incremented pixel from KBD

    // if SCREEN is black, M=-1, else M=0
    // if KBD input present, D!=0, else D=0
    // if SCREEN is white and no KPD input present, D=A-D -> 0=0-0

    @START    // call START label
    D;JEQ     // if D=0 goto START

    @LOOP     // call LOOP label
    D;JNE     // else if D!=0 goto LOOP and restart with a
