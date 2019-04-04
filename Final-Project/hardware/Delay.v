module Delay #(parameter N = 1, NUM_SPIKES = 16) (clk, rst, spikes_in, spikes_out);
    input clk;
    input rst;
    input [NUM_SPIKES-1:0] spikes_in;
    output [NUM_SPIKES-1:0] spikes_out;
    

    reg test;
    reg [NUM_SPIKES-1:0] del [N-1:0];
    //reg [NUM_SPIKES-1:0] spikes_out;
    integer i;

    assign spikes_out = del[N-1];

    always @(rst or posedge clk) begin
        test = 1'b1;
        if (rst) begin
            for (i=0; i<N; i= i+1) begin
                del[i] <= ~0;
            end 
        end
        else begin
            for (i=N-1; i>=0; i = i-1) begin
                if (i == 0) begin
                    del[i] <= spikes_in;
                end    
                else begin
                    del[i] <= del[i-1];
                end
            end              
        end
    end

endmodule
