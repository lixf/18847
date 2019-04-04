// Testbench for a 16-input bitonic sorter - You don't have to modify it

// Input lines make 1->0 transitions at different times (essentially values
// ranging from 0 to 39) coming in at the 16 input lines in an unsorted manner.
// At the output of the sorter, the lines should have 1->0 transitions in
// ascending order.

`timescale 1ns / 1ps

module neuorn_tb;

    reg [15:0] raw_in;
    reg  rst;
    wire out;
    reg clk;

    //reg [7:0] weights [1:0];// = {8'd3, 8'd9};


    //module FFI #(parameter NUM_SPIKES = 18, SPIKE_CNT=3) (clk, rst, spikes_in, inhibit);
    Neuron #(16, 17) DUT(.rst(rst), .spikes_in(raw_in), .weights_in({16{8'd3}}), .out(out));
    //rst, spikes_in, weights_in, ou

    initial begin
        clk = 1;
        forever begin
            #0.5 clk = ~clk;
        end
    end

    initial
    begin

        $dumpfile("neuron_tb.vcd");
        $dumpvars;//(0, delay_tb);

        //weights[0] = 8'd3;
        //weights[1] = 8'd9;            

        raw_in = ~16'b0;        
        rst = 1'b1;
        #2;
        rst = 1'b0;
        


        #5
        raw_in[1] = 0;

        //#2
        raw_in[13] = 0;

        #3
        raw_in[5] = 0;

        #1
        raw_in[12] = 0;

        #4
        raw_in[4] = 0;

        #2
        raw_in[7] = 0;

        #3
        raw_in[3] = 0;

        #1
        raw_in[15] = 0;

        #5
        raw_in[10] = 0;
        
        #4
        raw_in[2] = 0;
        
        #5
        raw_in[8] = 0;
        
        #2
        raw_in[11] = 0;
        
        #3
        raw_in[14] = 0;
        
        #1
        raw_in[0] = 0;
        
        #2
        raw_in[6] = 0;
        
        #1
        raw_in[9] = 0;
       
        #5;
        rst = 1'b1;
 
        #10
        raw_in = ~16'b0;

        #200
        $finish;

    end

endmodule
