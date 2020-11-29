from nmigen import *
from nmigen_soc.wishbone import *
from nmigen_soc.memory import *

# Memory mapping module, inspired by Vivonomicon's "RISC-V Memories" module.
class MemMap(Elaboratable):
    def __init__(self, rom, ram):
        # Multiplexers
        self.dmux = Decoder(addr_width = 32, data_width = 32, alignment = 0) # Data bus multiplexer
        self.imux = Decoder(addr_width = 32, data_width = 32, alignment = 0) # Instruction bus multiplexer

        # Save ROM and RAM to self
        self.rom = rom
        self.ram = ram

        # Create wishbone buses for ROM and RAM
        self.rom_b = self.rom.new_bus()
        self.ram_b = self.ram.new_bus()

        # Add buses to data multiplexer
        self.dmux.add(self.rom_b, addr = 0x00000000)
        self.dmux.add(self.ram_b, addr = 0x20000000)

        # Add buses to instruction multiplexer
        self.imux.add(self.rom_b, addr = 0x00000000)
        self.imux.add(self.ram_b, addr = 0x20000000)
