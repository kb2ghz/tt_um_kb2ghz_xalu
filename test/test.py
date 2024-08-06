# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
  
@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # ADD function test A
    # Set the input values you want to test
    dut.ui_in.value = int("00000000",2)
    dut.uio_in.value = int("00000000",2)

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 10)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == int("11000000",2)
    assert dut.uio_out.value == int("00000000",2)
    
    # AND function test A
    dut.ui_in.value = int("00000000",2)
    dut.uio_in.value = int("00010000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("11000000",2)
    assert dut.uio_out.value == int("00000000",2)

    # AND function test B
    dut.ui_in.value = int("11111111",2)
    dut.uio_in.value = int("00010000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("01001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # AND function test C
    dut.ui_in.value = int("01010101",2)
    dut.uio_in.value = int("00010000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("01000101",2)
    assert dut.uio_out.value == int("00000000",2)

    # AND function test D
    dut.ui_in.value = int("10101010",2)
    dut.uio_in.value = int("00010000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("01001010",2)
    assert dut.uio_out.value == int("00000000",2)

    # OR function test A
    dut.ui_in.value = int("00001111",2)
    dut.uio_in.value = int("00100000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # OR function test B
    dut.ui_in.value = int("11110000",2)
    dut.uio_in.value = int("00100000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # OR function test C
    dut.ui_in.value = int("10100101",2)
    dut.uio_in.value = int("00100000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # OR function test D
    dut.ui_in.value = int("00000000",2)
    dut.uio_in.value = int("00100000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("11000000",2)
    assert dut.uio_out.value == int("00000000",2)

    # XOR function test A
    dut.ui_in.value = int("00000000",2)
    dut.uio_in.value = int("00110000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("11000000",2)
    assert dut.uio_out.value == int("00000000",2)

    # XOR function test B
    dut.ui_in.value = int("00001111",2)
    dut.uio_in.value = int("00110000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # XOR function test C
    dut.ui_in.value = int("11110000",2)
    dut.uio_in.value = int("00110000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # XOR function test D
    dut.ui_in.value = int("11111111",2)
    dut.uio_in.value = int("00110000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("11000000",2)
    assert dut.uio_out.value == int("00000000",2)
     
    # PASSA function test A
    dut.ui_in.value = int("00001111",2)
    dut.uio_in.value = int("01000000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # PASSA function test B
    dut.ui_in.value = int("00001111",2)
    dut.uio_in.value = int("01000000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)
  
    # PASSB function test A
    dut.ui_in.value = int("00001111",2)
    dut.uio_in.value = int("01010000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("10000000",2)
    assert dut.uio_out.value == int("00000000",2)

    # PASSB function test B
    dut.ui_in.value = int("11110000",2)
    dut.uio_in.value = int("01010000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001111",2)
    assert dut.uio_out.value == int("00000001",2)

    # SHR function test A
    dut.ui_in.value = int("00001010",2)
    dut.uio_in.value = int("01100010",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001101",2)
    assert dut.uio_out.value == int("00000000",2)

    # SHR function test B
    dut.ui_in.value = int("00001010",2)
    dut.uio_in.value = int("01100000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00000101",2)
    assert dut.uio_out.value == int("00000000",2)

    # SHR function test C
    dut.ui_in.value = int("00000101",2)
    dut.uio_in.value = int("01100000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00100010",2)
    assert dut.uio_out.value == int("00000000",2)

    # SHR function test D
    dut.ui_in.value = int("00000101",2)
    dut.uio_in.value = int("01100010",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00101010",2)
    assert dut.uio_out.value == int("00000000",2)

    # SHL function test A
    dut.ui_in.value = int("00001111",2)
    dut.uio_in.value = int("01110000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00011110",2)
    assert dut.uio_out.value == int("00000000",2)

    # SHL function test B
    dut.ui_in.value = int("00001111",2)
    dut.uio_in.value = int("01110100",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00011111",2)
    assert dut.uio_out.value == int("00000001",2)

    # SHL function test C
    dut.ui_in.value = int("00000101",2)
    dut.uio_in.value = int("01110000",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001010",2)
    assert dut.uio_out.value == int("00000000",2)
  
    # SHL function test D
    dut.ui_in.value = int("00000101",2)
    dut.uio_in.value = int("01110100",2)
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == int("00001011",2)
    assert dut.uio_out.value == int("00000000",2)

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
