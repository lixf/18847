`timescale 1ns / 1ps

module bitonic_sort_2(a, b, max, min);
    input a;
    input b;
    output max;
    output min;

    assign max = a | b;
    assign min = a & b;

endmodule
