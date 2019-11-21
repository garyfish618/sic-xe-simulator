        START   0500
        LDA     NUM2

        ADD     NUM6

        SUB     NUM1
        SUB     NUM2
        SUB     NUM3
        SUB     NUM4
        SUB     NUM5
        SUB     NUM6

        MUL     NUM1
        MUL     NUM2
        MUL     NUM3
        MUL     NUM4
        MUL     NUM5
        MUL     NUM6

        DIV     NUM1
        DIV     NUM2
        DIV     NUM3
        DIV     NUM4
        DIV     NUM5
        DIV     NUM6


NUM1    WORD    -10
NUM2    WORD    0
NUM3    BYTE    X'0F'
NUM4    BYTE    X'10'
NUM5    BYTE    X'00'
NUM6    BYTE    X'FF'