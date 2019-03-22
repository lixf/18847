`timescale 1ns / 1ps

module bitonic_sort_8(in, out);
    input [7:0] in;
    output [7:0] out;

    wire [7:0] AtoB;

    bitonic_sort_4 a0(.in(in[3:0]), .out(AtoB[3:0]));
    bitonic_sort_4 a1(.in(in[7:4]), .out({AtoB[4], AtoB[5], AtoB[6], AtoB[7]}));


    LastStage #(8) l0(.in(AtoB), .out(out));
endmodule


