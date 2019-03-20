module LastStage #(parameter N = 16)(in, out);
    input [N-1:0] in;
    output [N-1:0] out;


    genvar i, group_idx, inst_idx;
    integer gpl, bpg, stride, beginning, idx_start, idx_end, inc, layer_idx;


    wire [N-1:0] connect [$clog2(N) : 0];

    generate
    //always @(*) begin
        assign layer_idx = 0;
        for (i = N/2; i > 0; i = i/2) begin : loop1
            assign gpl = (N/2)/i;
            assign stride = i;
            for (group_idx = 0; group_idx < (N/2)/i; group_idx = group_idx + 1) begin : loop2
                assign beginning = (2*stride)*group_idx;
                assign bpg = (N/2)/gpl;
    
                for (inst_idx = 0; inst_idx < i; inst_idx = inst_idx + 1) begin : loop3
                    assign idx_start = beginning + inst_idx;
                    assign idx_end = idx_start + stride;
                    assign inc = layer_idx+1'b1;

                    Bitonic_sort2 u0(.a(connect[layer_idx][idx_start]), .b(connect[layer_idx][idx_end]), 
                                     .max(connect[layer_idx+1][idx_end]), 
                                     .min(connect[inc][idx_start]));
                end 
            end
            assign layer_idx = layer_idx + 1;
        end
    //end
    endgenerate


    assign connect[0] = in;
    assign out = connect[$clog2(N)];
endmodule
