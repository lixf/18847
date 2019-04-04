module Neuron #(parameter NUM_SPIKES=16, THRESH=5) (rst, spikes_in, weights_in, inhibited, sdtp, out);
    parameter MAX_WEIGHT = 10;
    
    input rst;
    input [NUM_SPIKES-1:0]spikes_in;
    input [(8*NUM_SPIKES)-1:0] weights_in;
    input inhibited;
    input sdtp;
    output out;

    //wire [7:0] weights [NUM_SPIKES-1:0];
    reg[7:0] weights [NUM_SPIKES-1:0];
    wire [(8*NUM_SPIKES)-1:0] weights_view;

    reg [NUM_SPIKES - 1:0] spikes_test;
    genvar j;
    integer i, k;
    reg [7:0]value;
    reg out;

    generate
    for (j=0; j<NUM_SPIKES; j = j+1) begin
        //assign weights[j] = weights_in[(8*(j+1))-1:(8*j)];
        assign weights_view[(8*(j+1))-1:(8*j)] = weights[j];
    end
    endgenerate

    initial begin
        for (k=0; k<NUM_SPIKES; k = k+1) begin
            weights[k]= $urandom%10;
        end
    end

/*
    always @(posedge set_weights) begin
        for (k=0; k<NUM_SPIKES; k = k+1) begin
            weights[k] = weights_in[(8*(k+1))-1:(8*k)];
        end
    end
*/

    always @(rst or spikes_in) begin

        if (rst) begin
            value = 0;
            spikes_test = ~0;
            out = 1'b1;
        end

        else begin
            for (i=0; i<NUM_SPIKES; i = i + 1) begin
                if (spikes_in[i] == 1'b0 && spikes_test[i] == 1'b1 && out != 1'b0) begin
                    value = value + weights[i];
                    spikes_test[i] = 1'b0;
                    if (value >= THRESH) begin
                        out = 1'b0;
                    end
                end
            end
        end


    end 


    always @(posedge sdtp) begin
        for (i=0; i<NUM_SPIKES; i = i + 1) begin
            case ({~out, inhibited, ~spikes_in[i]})
                3'b000: begin//No ouput spike, not pre-inhibited, no input spike
                    //weight stays the same    
                end
                3'b001: begin//No ouput spike, not pre-inhibited, input spike
                    if (weights[i] < MAX_WEIGHT) begin
                        weights[i] = weights[i] + 1'b1;
                    end
                end
                3'b010: begin////No ouput spike, pre-inhibited, no input spike  **Not a possible state**

                end
                3'b011: begin//No ouput spike, pre-inhibited, input spike  **Not a possible state**
                
                end
                3'b100: begin//Output spike(TRUE outspike), no pre-inhibited outspike, no input spike
                    weights[i] = 0;
                end
                3'b101: begin//Output spike(TRUE outspike), no pre-inhibited outspike, input spike
                    if (spikes_test[i] == 1'b0) begin//Spike happend before or at time of output spike
                        weights[i] = MAX_WEIGHT;
                    end
                    else begin
                        weights[i] = 0;
                    end
                end
                3'b110: begin//Output spike(inhibited output), pre-inhibited outspike, no input spike
                    //weight stays the same
                end
                3'b111: begin//Output spike(inhibited ouput), pre-inhibited outspike, input spike, 
                    weights[i] = 0;
                end
                default: begin
                   //weight stays the same 
                end
            endcase
        end
    end



endmodule
