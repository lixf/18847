#include <stdio.h>
#include <math.h>




void getIndexes(int N)
{
    int layer_idx = 0;
    for (int i=N/2; i>0; i /= 2)//Layers
    {
        int gpl = (N/2)/i;
        int stride = i;

        for (int j=0; j<gpl; j++)//Groups per layer
        {
            int beginning = j * (2*stride);
            int bpg = (N/2)/gpl;
            //printf("--i: %d, j: %d\n", i, j);
            for (int k=0; k<i; k++)
            {
                int idx_start = beginning + k;
                int idx_end = idx_start + stride;
                printf("i: %d, j: %d, k: %d, layer_idx: %d, idx_start: %d, idx_end: %d\n", i, j, k, layer_idx, idx_start, idx_end);
            }
            printf("\n");
        }
        printf("\n");
        layer_idx++;
    }



}

int main()
{
    getIndexes(16);
    return 0;
}
