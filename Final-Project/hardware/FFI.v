module FFI #(parameter NUM_SPIKES = 18, SPIKE_CNT=3) (clk, rst, spikes_in, inhibit);
    input clk;
    input rst;
    input [NUM_SPIKES - 1:0] spikes_in;
    output  inhibit;


    genvar ii;
    event ev;
    integer cnt, i;
    //reg inhibit;
    reg [NUM_SPIKES - 1:0] spikes_test;

    always @(rst or spikes_in) begin
    
        if (rst) begin
            cnt = 0;
            spikes_test = ~0;
        end
    
        else begin
            for (i=0; i<NUM_SPIKES; i = i + 1) begin
                if (spikes_in[i] == 1'b0 && spikes_test[i] == 1'b1) begin
                    cnt = cnt + 1;
                    spikes_test[i] = 1'b0;
                end
            end
        end
    
        //for (ii=0; ii<NUM_SPIKES; ii=ii+1) begin
        //    always @(negedge spikes_in[ii]) ->> ev;
        //end
    end

//    generate begin
//        for (ii=0; ii<NUM_SPIKES; ii=ii+1) begin
//            always @(negedge spikes_in[ii]) ->> ev;
//        end
  //  endgenerate

//    always @(ev) begin
//        cnt = cnt + 1;
//    end

    assign inhibit = (cnt >= SPIKE_CNT) ? 1'b1 : 1'b0;

endmodule
