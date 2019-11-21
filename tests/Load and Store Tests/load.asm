START   0500
        LDA     NUM1
        LDX     VALX
        LDL     NUM2
        LDCH    CHAR,X


NUM1    WORD    -50
        WORD    1
NUM2    WORD    40
CHAR    BYTE    C'A'
VALX    WORD    6