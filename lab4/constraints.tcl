# Elaborating the model #
elaborate bitonic_sort_16 -architecture verilog -library WORK

# Create user defined variables # 
set CLK_PERIOD 10000.00 
set CLK_SKEW   [expr {$CLK_PERIOD} * 0.04]

# Create user-defined clock just for getting timing information #
# It doesn't mean there is a clock in the logic circuit #
create_clock -period $CLK_PERIOD -name my_clock
set_clock_uncertainty $CLK_SKEW my_clock

# Compile the model #
compile -map_effort medium

# Create output files for collecting metrics #
report_area                                                                                                                  > bitonic_sort_16.area
report_power                                                                                                                 > bitonic_sort_16.pow
report_timing  -from { raw_in[0] } -to { sorted_out[0] } -path full -delay max -nworst 1 -max_paths 1 -significant_digits 2 -sort_by group  > bitonic_sort_16.tim

check_timing
check_design
