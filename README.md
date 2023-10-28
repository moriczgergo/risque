# Risque
Risque is going to be a decent RISC-V core. It is currently under development, and not ready for meaningful use at all.

## Goals

### 1.0.0
 * Unprivileged RV32IM support.
 * Extendable memory mapping system for peripherals and memory.
 * Adequate testbench for every module in the system.

### Future goals
 * Pipelined design
 * RV32GC/RV64GC support
 * Multicore support

## Files
 * `alu.py` - ALU capable of un/signed addition, OR, AND, XOR, un/signed less than, un/signed right shift, left shift, un/signed multiplication, and un/signed floor division.
 * `isa.py` - ISA definition.
 * `memmap.py` - Memory mapping module, inspired by [Vivonomicon's "RISC-V Memories" module](https://github.com/WRansohoff/rv32i_nmigen_blog/blob/master/rvmem.py)
 * `ram.py` - Internal RAM module, basically [Vivonomicon's RAM module](https://github.com/WRansohoff/rv32i_nmigen_blog/blob/master/ram.py)
 * `rom.py` - Internal ROM module, basicall [Vivonomicon's ROM module](https://github.com/WRansohoff/rv32i_nmigen_blog/blob/master/rom.py)