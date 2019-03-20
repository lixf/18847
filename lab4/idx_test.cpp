#include <stdio.h>
#include <math.h>




void getIndexes(int N)
{
    for (int i=N/2; i>0; i /= 2)//Layers
    {
        int gpl = (N/2)/i;
        for (int j=0; j<gpl; j++)//Groups per layer
        {
            int bpg = (N/2)/gpl;
            //printf("--i: %d, j: %d\n", i, j);
            for (int k=0; k<bpg; k++)
            {
                printf("i: %d, j: %d, k: %d\n", i, j, k);
            }
            printf("\n");
        }
        printf("\n");
    }



}

int main()
{
    getIndexes(16);
    return 0;
}
