// Testbench for a 16-input bitonic sorter - You don't have to modify it

// Input lines make 1->0 transitions at different times (essentially values
// ranging from 0 to 39) coming in at the 16 input lines in an unsorted manner.
// At the output of the sorter, the lines should have 1->0 transitions in
// ascending order.

`timescale 1ns / 1ps

module FirstLayer_tb;

    parameter NUM_SPIKES = 8;
    parameter DEL_VAL = 8+1;
    parameter FFI_PASS_NUM = 3+1;
    parameter NEURON_THRESH = 13;
    parameter NUM_NEURONS = 10;

    reg [7:0] raw_in;
    reg  rst;
    reg clk;
    reg sdtp;

    wire inhibit;
    wire [7:0] spikes_del, spikes_out;
    wire [9:0] neuron_out, wta_out, inhibited_spikes;
    genvar i;    


    //module FFI #(parameter NUM_SPIKES = 18, SPIKE_CNT=3) (clk, rst, spikes_in, inhibit);
    Delay #(DEL_VAL, NUM_SPIKES) delay(.clk(clk), .rst(rst), .spikes_in(raw_in), .spikes_out(spikes_del));
    FFI #(NUM_SPIKES, FFI_PASS_NUM) ffi(.clk(clk), .rst(rst), .spikes_in(raw_in), .inhibit(inhibit));

    Inhibitor #(NUM_SPIKES) inhibitor(.inhibit(inhibit), .spikes_in(spikes_del), .spikes_out(spikes_out));
    WTA #(NUM_NEURONS) wta(.rst(rst), .spikes_in(neuron_out), .spikes_out(wta_out), .inhibited(inhibited_spikes));

    //Neuron [9:0] #(16, 17) neurons(.rst(rst), .spikes_in(raw_in), .weights_in({16{8'd3}}), .out(out));

    generate
        for (i=0; i<NUM_NEURONS; i = i+1) begin : FOR_NEURONS
            Neuron #(NUM_SPIKES, NEURON_THRESH) neuron(.rst(rst), .spikes_in(spikes_out), .weights_in({8{8'd3}}),
                                                       .inhibited(inhibited_spikes[i]), .sdtp(sdtp), .out(neuron_out[i]));
        end
    endgenerate


    initial begin
        clk = 1;
        forever begin
            #0.5 clk = ~clk;
        end
    end

    initial
    begin

        $dumpfile("firstlayer_tb-sdtp.vcd");
        $dumpvars;//(0, delay_tb);
        raw_in = ~16'b0;       
        sdtp = 1'b0; 
        rst = 1'b1;
        #2;
        rst = 1'b0;
        

        /*
        //Generated Volley
        #1;
        raw_in[7] = 0; 
        
        #1;


        #1;
        raw_in[0] = 0;
        raw_in[6] = 0;

        #1;
        

        #1;


        #1;


        #1;
        raw_in[4] = 0;

        #1;
        raw_in[1] = 0;
        raw_in[2] = 0;
        raw_in[5] = 0;

        #1;
        raw_in[3] = 0;
        */

        //Generated Volley
        #1;
        //raw_in[7] = 0; 
        
        #1;


        #1;
        //raw_in[0] = 0;
        raw_in[6] = 0;

        #1;
        

        #1;


        #1;


        #1;
        raw_in[4] = 0;

        #1;
        //raw_in[1] = 0;
        //raw_in[2] = 0;
        //raw_in[5] = 0;

        #1;
        raw_in[3] = 0;


        /*
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

        */

       
        #30;

        sdtp = 1'b1;
        #5;
        sdtp = 1'b0;
        #20;
        rst = 1'b1;
        raw_in = ~8'b0;
 
        #10
        rst = 1'b0;
        
        #200
        $finish;

    end

endmodule
