module Inhibitor #(parameter NUM_SPIKES = 18)(inhibit, spikes_in, spikes_out);
    input inhibit;
    input [NUM_SPIKES-1:0]spikes_in;
    output [NUM_SPIKES-1:0]spikes_out;

    assign spikes_out = inhibit ?  ~0 : spikes_in[NUM_SPIKES:0];
endmodule
