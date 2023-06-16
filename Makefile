all: heat_2d heat_2d_omp

heat_2d: heat_2d.f03
	gfortran -cpp -o heat_2d heat_2d.f03

heat_2d_omp: heat_2d.f03
	gfortran -cpp -fopenmp -o heat_2d_omp heat_2d.f03
clean:
	rm -f heat_2d heat_2d_omp
