// 4-bit ALU slice design
// Mike McCann 7/5/2024
// tested on an Altera/Intel Cyclone II EP2C20F484C7 FPGA

module tt_um_kb2ghz_xalu (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
	
// define two 4-bit data input ports 

// port A
`define ui_in[0]  da0
`define ui_in[1]  da1
`define ui_in[2]  da2
`define ui_in[3]  da3

// port B
`define ui_in[4]  db0
`define ui_in[5]  db1
`define ui_in[6]  db2
`define ui_in[7]  db3

// define an 4-bit data output port

`define ui_out[0] d0
`define ui_out[1] d1 
`define ui_out[2] d2 
`define ui_out[3] d3 

// define carry outputs

`define ui_out[4] co_left   // left carry output
`define ui_out[5] co_right  // right carry ouput

// comparator output

`define ui_out[6]  EQU    //  A=B

// zero detect

`define ui_out[7]  ZERO     // output = +zero
`define uio_out[0] NEG_ZERO // output = -zero

// define carry inputs

`define uio_in[1]     ci_left   // left side carry input
`define uio_in[2]     ci_right  // right side carry input

// complment output mode

`define uio_out[3]  COM 

// enable path settings

assign uio_oe[0] = 1b'1';  // output signal
assign uio_oe[1] = 1b'0';
assign uio_oe[2] = 1b'0';
assign uio_oe[3] = 1b'1';  // output signal
assign uio_oe[4] = 1b'0';  
assign uio_oe[5] = 1b'0';
assign uio_oe[6] = 1b'0';
assign uio_oe[7] = 1b'0';

// list unused inputs to prevent warnings
wire _unused =&{ena,clk, rst_in, 1'b0};

	
output `co_left;
output `co_right;
input `ci_left;
input `ci_right;
input `da0, `da1, `da2, `da3;  // input port A
input `db0, `db1, `db2, `db3;  // input port B
output `d0, `d1, `d2, `d3;     // output port
output `ZERO, `NEG_ZERO;     // zero detector
output `EQU;                // A = B
input `COM;                 // 1's complement mode
input `F0, `F1, `F2;          // function code input

wire bit0cy, bit1cy, bit2cy;  // carry signals between full adders

wire ADD, AND, OR, XOR, PASSA, PASSB, SHL, SHR;
wire d0int, d1int, d2int, d3int;

assign d0int = (ADD & (`da0 ^ `db0 ^ `ci_right)) |
		(AND & `da0 & `db0)   |
		(OR & (`da0 | `db0))  |
		(XOR & (`da0 ^ `db0)) |
		(PASSA & `da0) |
		(PASSB & `db0) |
		(SHL & `ci_right) |
		(SHR & `da1);

assign d1int = (ADD & (`da1 ^ `db1 ^ bit0cy)) |
		(AND & `da1 & `db1)   |
		(OR & (`da1 | `db1))  |
		(XOR & (`da1 ^ `db1)) |
		(PASSA & `da1) |
		(PASSB & `db1) |
		(SHL & `da0) |
		(SHR & `da2);

assign d2int = (ADD & (`da2 ^ `db2 ^ bit1cy)) |
		(AND & `da2 & `db2)   |
		(OR & (`da2 | `db2))  |
		(XOR & (`da2 ^ `db2)) |
		(PASSA & `da2) |
		(PASSB & `db2) |
		(SHL & `da1) |
		(SHR & `da3);

assign d3int = (ADD & (`da3 ^ `db3 ^ bit2cy)) |
		(AND & `da3 & `db3)   |
		(OR & (`da3 | `db3))  |
		(XOR & ('da3 ^ 'db3)) |
		(PASSA & `da3) |
		(PASSB & `db3) |
		(SHL & `da2) |
		(SHR & `ci_left);

assign bit0cy = `da0 & `db0 | `ci_right & (`da0 | `db0);
assign bit1cy = `da1 & `db1 | bit0cy & (`da1 | `db1);
assign bit2cy = `da2 & `db2 | bit1cy & (`da2 | `db2);

// inverting output mode

assign `d0 = `COM ^ d0int;
assign `d1 = `COM ^ d1int;
assign `d2 = `COM ^ d2int;
assign `d3 = `COM ^ d3int;

// function code decode

assign ADD = ~`F2 & ~`F1 & ~`F0;     // 0
assign AND = ~`F2 & ~`F1 & `F0;      // 1
assign OR = ~`F2 & `F1 & ~`F0;       // 2
assign XOR = ~'F2 & 'F1 & 'F0;       // 3
assign PASSA = `F2 & ~`F1 & ~`F0;    // 4
assign PASSB = `F2 & ~`F1 & `F0;     // 5
assign SHR = `F2 & `F1 & ~`F0;       // 6
assign SHL = `F2 & `F1 & `F0;        // 7

// carry outputs

assign `co_left = (SHL & `da3) | (ADD & (`da3 & `db3 | bit2cy & (`da3 | `db3)));
assign `co_right = SHR & `da0;

// output status

assign `ZERO = ~`d0 & ~`d1 & ~`d2 & ~`d3;
assign `NEG_ZERO = `d0 & `d1 & `d2 & `d3;

assign `EQU = ((`da0 & `db0) | (~`da0 & ~`db0)) &
	((`da1 & `db1) | (~`da1 & ~`db1)) &
	((`da2 & `db2) | (~`da2 & ~`db2)) &
	((`da3 & `db3) | (~`da3 & ~`db3));
endmodule

