
# Note that all RV32G opcodes are defined here, not just the ones that Risque can handle.
class Opcode:
    LOAD      = 0b00000
    LOAD_FP   = 0b00001
    CUSTOM_0  = 0b00010
    MISC_MEM  = 0b00011
    OP_IMM    = 0b00100
    AUIPC     = 0b00101
    OP_IMM_32 = 0b00110
    STORE     = 0b01000
    STORE_FP  = 0b01001
    CUSTOM_1  = 0b01010
    AMO       = 0b01011
    OP        = 0b01100
    LUI       = 0b01101
    OP_32     = 0b01110
    MADD      = 0b10000
    MSUB      = 0b10001
    NMSUB     = 0b10010
    NMADD     = 0b10011
    OP_FP     = 0b10100
    #RESERV_0 = 0b10101
    CUSTOM_2  = 0b10110
    BRANCH    = 0b11000
    JALR      = 0b11001
    #RESERV_1 = 0b11010
    JAL       = 0b11011
    SYSTEM    = 0b11100
    #RESERV_2 = 0b11101
    CUSTOM_3  = 0b11110

# Only RV32I funct3s are defined here.
class Funct3:
#OP JALR | BRANCH | LOAD | STORE | OP_IMM      | OP        | MISC_MEM | SYSTEM         | funct3
#  --------------------------------------------------------------------------------------------
    JALR = BEQ    = LB   = SB    = ADDI        = ADD = SUB = FENCE    = ECALL = EBREAK = 0b000
    _    = BNE    = LH   = SH    = SLLI        = SLL       = _        = _              = 0b001
    _    = _      = LW   = SW    = SLTI        = SLT       = _        = _              = 0b010
    _    = _      = _    = _     = SLTIU       = SLTU      = _        = _              = 0b011
    _    = BLT    = LBU  = _     = XORI        = XOR       = _        = _              = 0b100
    _    = BGE    = LHU  = _     = SRLI = SRAI = SRL = SRA = _        = _              = 0b101
    _    = BLTU   = _    = _     = ORI         = OR        = _        = _              = 0b110
    _    = BGEU   = _    = _     = ANDI        = AND       = _        = _              = 0b111

# Only RV32I funct7s are defined here.
class Funct7:
#OP OP_IMM      | OP                                            | funct7
#  ------------------------------------------------------------------------
    SLLI = SRLI = ADD = SLL = SLT = SLTU = XOR = SRL = OR = AND = 0b0000000
    SRAI        = SUB = SRA                                     = 0b0100000

# Only RV32I funct12s are defined here.
class Funct12:
#OP SYSTEM | funct12
#  ------------------------
    ECALL  = 0b000000000000
    EBREAK = 0b000000000001
