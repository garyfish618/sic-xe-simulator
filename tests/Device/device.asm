    START   0500
    TD      DEV1
    RD      DEV1
    WD      DEV1

    TD      DEV2
    RD      DEV2
    WD      DEV2

    LDX     INC
    TD      DEV2,X
    RD      DEV2,X
    WD      DEV2,X





INC     WORD    2
DEV1    BYTE    X'AA'
DEV2    WORD    1