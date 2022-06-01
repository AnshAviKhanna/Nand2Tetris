//AIM : R2 = R0 * R1
//R0 --> RAM[0]
//R1 --> RAM[1]
//R2 --> RAM[2]

//R2=0;
//while(R1>0)
//{
//    R2=R2+R0;
//    R1--;
//}

@R2
M=0
(ADD)
    @R1
    D=M
    @EXIT   // go to EXIT when R1=0
    D;JEQ
    @R0
    D=M
    @R2
    M=M+D  // R2 = R2 + R0 
    @R1
    M=M-1  // R1 = R1 -1
    @ADD
    0;JMP  
(EXIT)
    @EXIT
    0;JMP




