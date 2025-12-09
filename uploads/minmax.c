#include<stdio.h>

void minmax(int seq[],int size,int *min,int*max);

int main(int argc,char *argv[])
{

	int seq[]={5,15,10,30,25};
	int size=sizeof(seq)/sizeof(seq[0]);

	int min=seq[0];                  //initializing min and max to starting ele of array
	int max=seq[0];

	minmax(seq,size,&min,&max);     //passing address of min and max so that the manipulations done in the function can be reflected back

	printf("\n the min ele is %d",min);
	printf("\n the max ele is %d",max);

	return 0;
}

void minmax(int seq[],int size,int *min,int *max)
{
	for(int i=1;i<size;i++)
	{
		if(seq[i]<*min)
		{
			*min=seq[i];      //using dereference operator to reach the location and get the value to compare with min
		}
		
		if(seq[i]>*max)
		{
			*max=seq[i];
		}
	}
}
			





