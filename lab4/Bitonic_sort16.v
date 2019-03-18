`timescale 1ns / 1ps

module Bitonic_sort16(in, out);
    input [15:0] in;
    output [15:0] out;

    wire [15:0] AtoB;
    wire [15:0] BtoC;
    wire [15:0] CtoD;
    wire [15:0] DtoE;

    Bitonic_sort8 a0(.in(in[7:0]), .out(AtoB[7:0]));
    Bitonic_sort8 a1(.in(in[15:8]), 
                     .out({AtoB[8], AtoB[9], AtoB[10], AtoB[11], 
                           AtoB[12], AtoB[13], AtoB[14], AtoB[15]}));



    Bitonic_sort2 b0(.a(AtoB[0]), .b(AtoB[8]), .min(BtoC[0]), .max(BtoC[8]));
    Bitonic_sort2 b1(.a(AtoB[1]), .b(AtoB[9]), .min(BtoC[1]), .max(BtoC[9]));
    Bitonic_sort2 b2(.a(AtoB[2]), .b(AtoB[10]), .min(BtoC[2]), .max(BtoC[10]));
    Bitonic_sort2 b3(.a(AtoB[3]), .b(AtoB[11]), .min(BtoC[3]), .max(BtoC[11]));
    Bitonic_sort2 b4(.a(AtoB[4]), .b(AtoB[12]), .min(BtoC[4]), .max(BtoC[12]));
    Bitonic_sort2 b5(.a(AtoB[5]), .b(AtoB[13]), .min(BtoC[5]), .max(BtoC[13]));
    Bitonic_sort2 b6(.a(AtoB[6]), .b(AtoB[14]), .min(BtoC[6]), .max(BtoC[14]));
    Bitonic_sort2 b7(.a(AtoB[7]), .b(AtoB[15]), .min(BtoC[7]), .max(BtoC[15]));
   


    Bitonic_sort2 c0(.a(BtoC[0]), .b(BtoC[4]), .min(CtoD[0]), .max(CtoD[4]));
    Bitonic_sort2 c1(.a(BtoC[1]), .b(BtoC[5]), .min(CtoD[1]), .max(CtoD[5]));
    Bitonic_sort2 c2(.a(BtoC[2]), .b(BtoC[6]), .min(CtoD[2]), .max(CtoD[6]));
    Bitonic_sort2 c3(.a(BtoC[3]), .b(BtoC[7]), .min(CtoD[3]), .max(CtoD[7]));

    Bitonic_sort2 c4(.a(BtoC[8]), .b(BtoC[12]), .min(CtoD[8]), .max(CtoD[12]));
    Bitonic_sort2 c5(.a(BtoC[9]), .b(BtoC[13]), .min(CtoD[9]), .max(CtoD[13]));
    Bitonic_sort2 c6(.a(BtoC[10]), .b(BtoC[14]), .min(CtoD[10]), .max(CtoD[14]));
    Bitonic_sort2 c7(.a(BtoC[11]), .b(BtoC[15]), .min(CtoD[11]), .max(CtoD[15]));



    Bitonic_sort2 d0(.a(CtoD[0]), .b(CtoD[2]), .min(DtoE[0]), .max(DtoE[2]));
    Bitonic_sort2 d1(.a(CtoD[1]), .b(CtoD[3]), .min(DtoE[1]), .max(DtoE[3]));

    Bitonic_sort2 d2(.a(CtoD[4]), .b(CtoD[6]), .min(DtoE[4]), .max(DtoE[6]));
    Bitonic_sort2 d3(.a(CtoD[5]), .b(CtoD[7]), .min(DtoE[5]), .max(DtoE[7]));    

    Bitonic_sort2 d4(.a(CtoD[8]), .b(CtoD[10]), .min(DtoE[8]), .max(DtoE[10]));
    Bitonic_sort2 d5(.a(CtoD[9]), .b(CtoD[11]), .min(DtoE[9]), .max(DtoE[11]));

    Bitonic_sort2 d6(.a(CtoD[12]), .b(CtoD[14]), .min(DtoE[12]), .max(DtoE[14]));
    Bitonic_sort2 d7(.a(CtoD[13]), .b(CtoD[15]), .min(DtoE[13]), .max(DtoE[15]));





    Bitonic_sort2 e0(.a(DtoE[0]), .b(DtoE[1]), .min(out[0]), .max(out[1]));
    Bitonic_sort2 e1(.a(DtoE[2]), .b(DtoE[3]), .min(out[2]), .max(out[3]));
    Bitonic_sort2 e2(.a(DtoE[4]), .b(DtoE[5]), .min(out[4]), .max(out[5]));
    Bitonic_sort2 e3(.a(DtoE[6]), .b(DtoE[7]), .min(out[6]), .max(out[7]));    
    Bitonic_sort2 e4(.a(DtoE[8]), .b(DtoE[9]), .min(out[8]), .max(out[9]));
    Bitonic_sort2 e5(.a(DtoE[10]), .b(DtoE[11]), .min(out[10]), .max(out[11]));
    Bitonic_sort2 e6(.a(DtoE[12]), .b(DtoE[13]), .min(out[12]), .max(out[13]));
    Bitonic_sort2 e7(.a(DtoE[14]), .b(DtoE[15]), .min(out[14]), .max(out[15]));

endmodule
