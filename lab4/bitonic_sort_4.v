`timescale 1ns / 1ps

module bitonic_sort_4(in, out);
    input [3:0] in;
    output [3:0] out;

    wire [3:0] AtoB;

    bitonic_sort_2 a0(.a(in[0]), .b(in[1]), .min(AtoB[0]), .max(AtoB[1]));
    bitonic_sort_2 a1(.a(in[2]), .b(in[3]), .min(AtoB[3]), .max(AtoB[2]));

    LastStage #(4) l0(.in(AtoB), .out(out));
endmodule
