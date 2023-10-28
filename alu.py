from nmigen import *
from nmigen.sim import *

ALU_SADD = 0b0000
ALU_UADD = 0b0001
ALU_OR   = 0b0010
ALU_AND  = 0b0011
ALU_XOR  = 0b0100
ALU_SLT  = 0b0101
ALU_ULT  = 0b0110
ALU_SRS  = 0b0111
ALU_URS  = 0b1000
ALU_LS   = 0b1001
ALU_UMUL = 0b1010
ALU_SMUL = 0b1011
ALU_UDIV = 0b1100
ALU_SDIV = 0b1101

class ALU(Elaboratable):
    def __init__(self):
        self.f = Signal(4)
        self.a = Signal(32)
        self.b = Signal(32)
        self.y = Signal(32)
    
    def elaborate(self, platform):
        m = Module()

        if platform == None:
            c = Signal(1)
            m.d.sync += c.eq(0)

        with m.If(self.f == ALU_SADD): # signed add
            m.d.comb += self.y.eq(self.a.as_signed() + self.b.as_signed())
        with m.Elif(self.f == ALU_UADD): # unsigned add
            m.d.comb += self.y.eq(self.a + self.b)
        with m.Elif(self.f == ALU_OR): # or
            m.d.comb += self.y.eq(self.a | self.b)
        with m.Elif(self.f == ALU_AND): # and
            m.d.comb += self.y.eq(self.a & self.b)
        with m.Elif(self.f == ALU_XOR): # xor
            m.d.comb += self.y.eq(self.a ^ self.b)
        with m.Elif(self.f == ALU_SLT): # a < b signed
            m.d.comb += self.y.eq(self.a.as_signed() < self.b.as_signed())
        with m.Elif(self.f == ALU_ULT): # a < b unsigned
            m.d.comb += self.y.eq(self.a < self.b)
        with m.Elif(self.f == ALU_SRS): # a >> b sign extend
            m.d.comb += self.y.eq(self.a.as_signed() >> (self.b[:5]))
        with m.Elif(self.f == ALU_URS): # a >> b unsigned
            m.d.comb += self.y.eq(self.a >> (self.b[:5]))
        with m.Elif(self.f == ALU_LS): # a << b
            m.d.comb += self.y.eq(self.a << (self.b[:5]))
        with m.Elif(self.f == ALU_UMUL): # a * b unsigned
            m.d.comb += self.y.eq(self.a * self.b)
        with m.Elif(self.f == ALU_SMUL): # a * b signed
            m.d.comb += self.y.eq(self.a.as_signed() * self.b.as_signed())
        with m.Elif(self.f == ALU_UDIV): # a / b unsigned
            m.d.comb += self.y.eq(self.a // self.b)
        with m.Elif(self.f == ALU_SDIV): # a / b signed
            # This should've worked, but see: https://github.com/nmigen/nmigen/issues/478
            # m.d.comb += self.y.eq(self.a.as_signed() // self.b.as_signed())

            # Workaround time! Thanks TiltMeSenpai.
            m.d.comb += self.y.eq(Mux(
                (self.a[-1] == 1).bool() ^ (self.b[-1] == 1).bool(), # If the dividee or the divisor is negative...
                ~(abs(self.a.as_signed()).as_unsigned() // abs(self.b.as_signed()).as_unsigned()) + 1, # Divide them as positive values, then flip them.
                # Else...
                abs(self.a.as_signed()).as_unsigned() // abs(self.b.as_signed()).as_unsigned() # Divide them as positive values.
            ))

        return m

pc = 0
fc = 0

def run_test(alu, f, a, b, ey, sign):
    global pc, fc
    yield alu.f.eq(f)
    yield alu.a.eq(a)
    yield alu.b.eq(b)

    yield Tick()
    yield Settle()

    y = None
    if sign == True:
        y = alu.y.as_signed()
    else:
        y = alu.y
    
    ys = y.shape()

    y = yield y

    print("%01X %08X %08X ? %08X = %08X (%s)"%(f, a, b, ey, y, ys))

    if "%08X"%(ey) == "%08X"%(y):
        pc = pc + 1
    else:
        fc = fc + 1


if __name__ == "__main__":
    dut = ALU()
    sim = Simulator(dut)
    def proc():
        print("Signed Add")
        yield from run_test(dut, ALU_SADD, 1, -1, 0, True)
        yield from run_test(dut, ALU_SADD, 1, 1, 2, True)
        yield from run_test(dut, ALU_SADD, 1, -5, -4, True)
        yield from run_test(dut, ALU_SADD, 0x7FFFFFFF, 1, -0x80000000, True)

        print("\nUnsigned Add")
        yield from run_test(dut, ALU_UADD, 1, 1, 2, False)
        yield from run_test(dut, ALU_UADD, 2, 1, 3, False)
        yield from run_test(dut, ALU_UADD, 0xFFFFFFFF, 1, 0, False)

        print("\nOR")
        yield from run_test(dut, ALU_OR, 0b1111, 0b11110000, 0b11111111, False)
        yield from run_test(dut, ALU_OR, 0b1110, 0b0111, 0b1111, False)
        yield from run_test(dut, ALU_OR, 0, 0, 0, False)

        print("\nAND")
        yield from run_test(dut, ALU_AND, 0b11111111, 0b01110000, 0b01110000, False)
        yield from run_test(dut, ALU_AND, 0, 0b01110000, 0, False)

        print("\nXOR")
        yield from run_test(dut, ALU_XOR, 0b10101010, 0b01110111, 0b11011101, False)

        print("\nSigned Less Than")
        yield from run_test(dut, ALU_SLT, -3, 5, 1, True)
        yield from run_test(dut, ALU_SLT, 5, -3, 0, True)
        yield from run_test(dut, ALU_SLT, 1, 1, 0, True)

        print("\nUnsigned Less Than")
        yield from run_test(dut, ALU_ULT, 3, 5, 1, False)
        yield from run_test(dut, ALU_ULT, 5, 3, 0, False)
        yield from run_test(dut, ALU_ULT, 1, 1, 0, False)

        print("\nSign Extended Right Shift")
        yield from run_test(dut, ALU_SRS, -0b1000, 3, -0b1, True)
        yield from run_test(dut, ALU_SRS, 0b1000, 3, 0b1, True)

        print("\nUnsigned Right Shift")
        yield from run_test(dut, ALU_URS, 0b1000, 3, 0b1, False)
        yield from run_test(dut, ALU_URS, 0b1010, 1, 0b101, False)

        print("\nLeft Shift")
        yield from run_test(dut, ALU_LS, -0b1, 3, -0b1000, True)
        yield from run_test(dut, ALU_LS, 0b1, 3, 0b1000, False)
        yield from run_test(dut, ALU_LS, 0b101, 2, 0b10100, False)

        print("\nUnsigned Multiplication")
        yield from run_test(dut, ALU_UMUL, 2, 2, 4, False)
        yield from run_test(dut, ALU_UMUL, 3, 3, 9, False)
        yield from run_test(dut, ALU_UMUL, 1, 1, 1, False)
        yield from run_test(dut, ALU_UMUL, 5, 0, 0, False)

        print("\nSigned Multiplication")
        yield from run_test(dut, ALU_SMUL, 2, 2, 4, True)
        yield from run_test(dut, ALU_SMUL, 2, -2, -4, True)
        yield from run_test(dut, ALU_SMUL, -2, -2, 4, True)
        yield from run_test(dut, ALU_SMUL, 1, -1, -1, True)
        yield from run_test(dut, ALU_SMUL, -5, 0, 0, True)

        print("\nUnsigned Division")
        yield from run_test(dut, ALU_UDIV, 12, 6, 2, False)
        yield from run_test(dut, ALU_UDIV, 12, 5, 2, False)

        print("\nSigned Division")
        yield from run_test(dut, ALU_SDIV, 12, 6, 2, True)
        yield from run_test(dut, ALU_SDIV, 12, -6, -2, True)
        yield from run_test(dut, ALU_SDIV, 12, 5, 2, True)

        print("\n%d passed, %d failed"%(pc, fc))
    
    sim.add_clock(1e-6)
    sim.add_sync_process(proc)
    #with sim.write_vcd("alu.vcd", "alu.gtkw"):
    sim.run()
