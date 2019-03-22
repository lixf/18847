`timescale 1ns / 1ps

module LastStage #(parameter N = 16)(in, out);
    input [N-1:0] in;
    output [N-1:0] out;


    genvar i, group_idx, inst_idx;
    //integer gpl, bpg, stride, beginning, idx_start, idx_end, inc, layer_idx;


    wire [N-1:0] connect [$clog2(N) : 0];

    generate
    //initial begin
        //assign layer_idx = 0;
        for (i = N/2; i > 0; i = i/2) begin : loop1
            //assign gpl = (N/2)/i;
            //assign stride = i;
            for (group_idx = 0; group_idx < (N/2)/i; group_idx = group_idx + 1) begin : loop2
                //assign beginning = (2*i)*group_idx;
                //assign bpg = (N/2)/((N/2)/i);
    
                for (inst_idx = 0; inst_idx < i; inst_idx = inst_idx + 1) begin : loop3
                    //assign idx_start = (2*i)*group_idx + inst_idx;
                    //assign idx_end = (2*i)*group_idx + inst_idx + i;
                    //assign inc = $clog2((N/2)/i)+1'b1;

                    bitonic_sort_2 u0(.a(connect[$clog2((N/2)/i)  ][(2*i)*group_idx + inst_idx]    ), 
				                     .b(connect[$clog2((N/2)/i)  ][(2*i)*group_idx + inst_idx + i]), 
                                   .max(connect[$clog2((N/2)/i)+1][(2*i)*group_idx + inst_idx + i]), 
                                   .min(connect[$clog2((N/2)/i)+1][(2*i)*group_idx + inst_idx]    ));
                end 
            end
            //assign layer_idx = layer_idx + 1;
        end
    //end
    endgenerate

    assign connect[0] = in;
    assign out = connect[$clog2(N)];
endmodule

module bitonic_sort_2(a, b, max, min);
    input a;
    input b;
    output max;
    output min;

    assign max = a | b;
    assign min = a & b;

endmodule

module bitonic_sort_4(in, out);
    input [3:0] in;
    output [3:0] out;

    wire [3:0] AtoB;
    //wire [3:0] BtoC;

    bitonic_sort_2 a0(.a(in[0]), .b(in[1]), .min(AtoB[0]), .max(AtoB[1]));
    bitonic_sort_2 a1(.a(in[2]), .b(in[3]), .min(AtoB[3]), .max(AtoB[2]));

    LastStage #(4) l0(.in(AtoB), .out(out));


endmodule

module bitonic_sort_8(in, out);
    input [7:0] in;
    output [7:0] out;

    wire [7:0] AtoB;


    //Ascending and descending instances
    bitonic_sort_4 a0(.in(in[3:0]), .out(AtoB[3:0]));
    bitonic_sort_4 a1(.in(in[7:4]), .out({AtoB[4], AtoB[5], AtoB[6], AtoB[7]}));


    LastStage #(8) l0(.in(AtoB), .out(out));


endmodule

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