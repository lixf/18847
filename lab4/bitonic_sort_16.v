`timescale 1ns / 1ps

module bitonic_sort_16(sorted_out, raw_in);
    input [15:0] raw_in;
    output [15:0] sorted_out;

    wire [15:0] AtoB;

    bitonic_sort_8 a0(.in(raw_in[7:0]), .out(AtoB[7:0]));
    bitonic_sort_8 a1(.in(raw_in[15:8]), 
                     .out({AtoB[8], AtoB[9], AtoB[10], AtoB[11], 
                           AtoB[12], AtoB[13], AtoB[14], AtoB[15]}));

    LastStage #(16) l0(.in(AtoB), .out(sorted_out));
endmodule
