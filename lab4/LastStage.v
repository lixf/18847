`timescale 1ns / 1ps

module LastStage #(parameter N = 16)(in, out);
    input [N-1:0] in;
    output [N-1:0] out;


    genvar i, group_idx, inst_idx;

    wire [N-1:0] connect [$clog2(N) : 0];

    generate
        for (i = N/2; i > 0; i = i/2) begin : loop1
            for (group_idx = 0; group_idx < (N/2)/i; group_idx = group_idx + 1) begin : loop2
    
                for (inst_idx = 0; inst_idx < i; inst_idx = inst_idx + 1) begin : loop3

                    bitonic_sort_2 u0(.a(connect[$clog2((N/2)/i)  ][(2*i)*group_idx + inst_idx]    ), 
				                     .b(connect[$clog2((N/2)/i)  ][(2*i)*group_idx + inst_idx + i]), 
                                   .max(connect[$clog2((N/2)/i)+1][(2*i)*group_idx + inst_idx + i]), 
                                   .min(connect[$clog2((N/2)/i)+1][(2*i)*group_idx + inst_idx]    ));
                end 
            end
        end
    endgenerate

    assign connect[0] = in;
    assign out = connect[$clog2(N)];
endmodule
