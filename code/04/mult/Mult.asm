// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// add R1 to itself R0 many times

// High-level:
// for(i=0; i<R0; i++){
//    R2=R2+R1
// }

@2    // call R2
M=0   // set R2=0
@i    // counter
M=0   // set i=0

(LOOP)
    @i      // call counter
    D=M     // set D to counter -> D=i
    @0      // call R0
    D=D-M   // D=i-R0
    @END    // call END label
    D;JGE   // if i-R0 >= 0 goto END (exit LOOP)

    @1      // call R1
    D=M     // set D=R1
    @2      // call R2
    M=D+M   // R2=R2+R1
    @i      // call counter
    M=M+1   // increment counter -> i=i+1
    @LOOP   // call LOOP label
    0; JMP  // goto LOOP (repeat LOOP)

(END)
    @END
    0; JMP  // infinite loop to end hack program
