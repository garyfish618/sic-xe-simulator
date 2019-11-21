        START   0500
        LDX     ZERO
        LDCH    CHAR,X
        STCH    C1,X


ALPHA   RESW    1
ZERO    WORD    0
CHAR    BYTE    C'TEST STRING'
C1      RESB    11