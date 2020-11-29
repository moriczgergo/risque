from nmigen import *
from nmigen_soc.memory import *
from nmigen_soc.wishbone import *
from math import ceil, log2

# Internal ROM module, basically Vivonomicon's ROM module.
# NOTE: The Memory itself is actually writable, but this doesn't expose any write ports to it.
class ROM(Elaboratable, Interface):
    def __init__(self, data):
        self.size = len(data) # Get data size
        self.awidth = ceil(log2(self.size + 1)) # Calculate width of address bus.
        self.data = Memory(width = 32, depth = self.size, init = data) # Create memory.
        self.r = self.data.read_port() # Get read port.
        Interface.__init__(self, data_width = 32, addr_width = self.awidth) # Initialize interface.
        self.memory_map = MemoryMap(data_width = self.data_width, addr_width = self.addr_width, alignment = 0)
    
    def elaborate(self, platform):
        m = Module()
        m.submodules.r = self.r # Register read port as submodule
        
        m.d.sync += self.ack.eq(0)
        with m.If(self.cyc):
            m.d.sync += self.ack.eq(self.stb)

        # Do reads combinatorically
        m.d.comb += [
            self.r.addr.eq(self.adr),
            self.dat_r.eq(self.r.data)
        ]

        return m