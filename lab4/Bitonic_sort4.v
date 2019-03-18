`timescale 1ns / 1ps

module Bitonic_sort4(in, out);
    input [3:0] in;
    output [3:0] out;

    wire [3:0] AtoB;
    wire [3:0] BtoC;

    Bitonic_sort2 a0(.a(in[0]), .b(in[1]), .min(AtoB[0]), .max(AtoB[1]));
    Bitonic_sort2 a1(.a(in[2]), .b(in[3]), .min(AtoB[3]), .max(AtoB[2]));

    Bitonic_sort2 b0(.a(AtoB[0]), .b(AtoB[2]), .min(BtoC[0]), .max(BtoC[2]));
    Bitonic_sort2 b1(.a(AtoB[1]), .b(AtoB[3]), .min(BtoC[1]), .max(BtoC[3]));

    Bitonic_sort2 c0(.a(BtoC[0]), .b(BtoC[1]), .min(out[0]), .max(out[1]));
    Bitonic_sort2 c1(.a(BtoC[2]), .b(BtoC[3]), .min(out[2]), .max(out[3]));

endmodule
