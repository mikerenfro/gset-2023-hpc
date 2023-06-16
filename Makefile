heat_2d: heat_2d.f03
	gfortran -o heat_2d heat_2d.f03
heat_2d_omp: heat_2d.f03
	gfortran -fopenmp -o heat_2d_omp heat_2d.f03
clean:
	rm heat_2d
