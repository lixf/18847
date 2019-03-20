`timescale 1ns / 1ps

module Bitonic_sort8(in, out);
    input [7:0] in;
    output [7:0] out;

    wire [7:0] AtoB;
    wire [7:0] BtoC;
    wire [7:0] CtoD;

    //Ascending and descending instances
    Bitonic_sort4 a0(.in(in[3:0]), .out(AtoB[3:0]));
    Bitonic_sort4 a1(.in(in[7:4]), .out({AtoB[4], AtoB[5], AtoB[6], AtoB[7]}));




    //Last Stage
    Bitonic_sort2 b0(.a(AtoB[0]), .b(AtoB[4]), .min(BtoC[0]), .max(BtoC[4]));
    Bitonic_sort2 b1(.a(AtoB[1]), .b(AtoB[5]), .min(BtoC[1]), .max(BtoC[5]));
    Bitonic_sort2 b2(.a(AtoB[2]), .b(AtoB[6]), .min(BtoC[2]), .max(BtoC[6]));
    Bitonic_sort2 b3(.a(AtoB[3]), .b(AtoB[7]), .min(BtoC[3]), .max(BtoC[7]));
    

    Bitonic_sort2 c0(.a(BtoC[0]), .b(BtoC[2]), .min(CtoD[0]), .max(CtoD[2]));
    Bitonic_sort2 c1(.a(BtoC[1]), .b(BtoC[3]), .min(CtoD[1]), .max(CtoD[3]));
    Bitonic_sort2 c2(.a(BtoC[4]), .b(BtoC[6]), .min(CtoD[4]), .max(CtoD[6]));
    Bitonic_sort2 c3(.a(BtoC[5]), .b(BtoC[7]), .min(CtoD[5]), .max(CtoD[7]));


    Bitonic_sort2 d0(.a(CtoD[0]), .b(CtoD[1]), .min(out[0]), .max(out[1]));
    Bitonic_sort2 d1(.a(CtoD[2]), .b(CtoD[3]), .min(out[2]), .max(out[3]));
    Bitonic_sort2 d2(.a(CtoD[4]), .b(CtoD[5]), .min(out[4]), .max(out[5]));
    Bitonic_sort2 d3(.a(CtoD[6]), .b(CtoD[7]), .min(out[6]), .max(out[7]));    



    //3 groups of 4
    //=> log2(N) of N/2


    for (int i=N/2; i>0; i /= 2)//i=2, 1, 0
    {
        //int stride = 2^i;
        //int inc = (N/2)/stride;
        for (int j=i; j>0; j++)
        {
            
        }
    }
endmodule



module LastStage()
