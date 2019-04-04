module WTA #(parameter NUM_SPIKES = 10) (rst, spikes_in, spikes_out, inhibited);
    input rst;
    input [NUM_SPIKES-1:0] spikes_in;
    output [NUM_SPIKES-1:0] spikes_out;
    output [NUM_SPIKES-1:0] inhibited;   

    reg [NUM_SPIKES-1:0] spikes_test;
    reg [NUM_SPIKES-1:0] inhibited; 

    reg [7:0] cnt;
    integer i;


    assign spikes_out = spikes_test;

    always @(rst or spikes_in) begin
        if (rst) begin
            cnt = 0;
            spikes_test = ~0;
            inhibited = 0;
        end
        else begin
            for (i=0; i<NUM_SPIKES; i=i+1) begin
                if (spikes_in[i] == 1'b0 && spikes_test[i] == 1'b1) begin//prioritizes lsb spikes over msb
                    if (cnt == 1'b0) begin
                        spikes_test[i] = 1'b0;
                    end
                    else begin
                        inhibited[i] = 1'b1;
                    end
                    cnt = cnt + 1;
                end 
            end
        end
    end
        

endmodule
