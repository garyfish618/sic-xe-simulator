. -3 + 3 = 0
. FFFD = -3
        START   0500
        LDA     NUM1
        ADD     NUM2

. -3 - 3 = -6
. FFFA = -6
        LDA     NUM1
        SUB     NUM2

. -3 * 3 = -9
.FFF7 = -9
        LDA     NUM1
        MUL     NUM2

.-3 / 1 = -3
.NUMX is 6. &(NUM2 + 6) = NUM3 (1)
        LDA     NUM1
        LDX     NUMX
        DIV     NUM2,X

.-3 & 1 = 1
        LDA     NUM1
        AND     NUM3

.-3 | 1 = -3
.FFFD = -3
        LDA     NUM1
        OR      NUM3

. ASCII for H = 48
. 1 < 2 - Second time around: FF in A; 2 = 2; shouldnt JGT 
        LDX     ZERO
        LDA     ZERO
LOOP    LDA     STRING,X
        TIX     TIW
        JLT     LOOP

. 0 = 0 - Should Jump
        LDA     ZERO
        COMP    ZERO
        JEQ     HERE

.Should not get executed
        LDX     ZERO

HERE    LDA     ZERO
        JSUB    RDDAT
        LDA     ZERO
        END

.Execution should start at HERE
.Should wait until device is ready to read
.001D should hold AA
RDDAT    TD      DEV1
        JEQ     RDDAT
        RD      DEV1
        STCH    BUFF
        LDA     ZERO
        LDCH    BUFF

.Should wait until device is ready to write
.Device should get byte AA
WRDAT   TD      DEV1
        JEQ     WRDAT
        WD      DEV1
        RSUB




ZERO    WORD    0
NUM1    WORD    -3
NUM2    WORD    3
BUFF    RESW    1
NUM3    WORD    1
NUMX    WORD    6
TIW     WORD    2

STRING  BYTE    C'H'
        BYTE    X'FF'

DEV1    BYTE    X'F1'

