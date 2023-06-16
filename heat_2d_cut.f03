! usage: heat_2d rows cols k t_boundary steps temps_file outfile
program heat_2d
  use omp_lib

  implicit none

  integer :: rows, cols
  real :: t_boundary
  ! real, allocatable :: temp_old(:, :)
  real :: temp_old(12, 12)
  integer :: i, i_min, i_max, j ! for row/column/loop counters

  ! make room for the required temperature grids and initalize them
  rows = 10
  cols = 10
  t_boundary = 1.5
  ! allocate(temp_old(rows+2, cols+2))

  !$omp parallel default(none) &
  !$omp   private(i, i_min, i_max, j) &
  !$omp   shared(temp_old, rows, cols, t_boundary)
  i_min = omp_get_thread_num()*(rows+2)/omp_get_num_threads()
  i_max = (omp_get_thread_num()+1)*(rows+2)/omp_get_num_threads()
  do i=i_min, i_max
    do j=1, cols+2
        temp_old(i, j) = t_boundary
    end do ! j
  end do ! i
  !$omp end parallel

  write(*, *) 'second starting temperatures, should be ', t_boundary, 'throughout'
  call print_grid(temp_old, rows, cols)

  contains
  ! including these functions inside the main program so that they can
  ! take any size t

  subroutine print_grid(t, rows, cols)
    implicit none
    integer, intent(in) :: rows, cols
    real, intent(in) :: t(:, :)
    integer :: i, j

    do i=1, rows
      do j=1, cols
        write(*, '(f7.2,1x)', advance='no') t(i+1, j+1)
      end do
      write(*, *) ! write a newline before starting next row
    end do
  end

end
