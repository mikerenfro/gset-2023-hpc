! usage: heat_2d rows cols k t_boundary steps temps_file outfile
program heat_2d
  use, intrinsic :: ieee_arithmetic

  implicit none

  integer :: num_args, rows, cols, steps, num_fixed_temps, temp_line_number, step
  real :: k, t_boundary, nan, fixed_temp
  character(len=1000) :: temps_file, outfile
  real, allocatable :: temp_old(:, :), temp_new(:, :), temp_fixed(:, :)
  integer :: i, j ! for row/column/loop counters

  num_args = command_argument_count()
  nan = ieee_value(nan, ieee_quiet_nan) ! nan = 'not a number', like 0.0/0.0

  if (num_args /= 7) then
    write(*,*) 'Usage: heat_2d rows cols k t_boundary steps temps_file outfile'
    stop
  end if
  call get_args(rows, cols, k, t_boundary, steps, temps_file, outfile)
  write(*,*) 'rows = ', rows, ', cols = ', cols, ', k = ', k, &
    ', t_boundary = ', t_boundary, ', steps = ', steps, &
    ', temps_file = ', trim(temps_file), ', outfile = ', trim(outfile)
  ! make room for the required temperature grids and initalize them
  allocate(temp_old(rows+2, cols+2))
  allocate(temp_new(rows+2, cols+2))
  allocate(temp_fixed(rows+2, cols+2))
  do i=1, rows+2
    do j=1, cols+2
        temp_old(i, j) = t_boundary
        temp_new(i, j) = t_boundary
        temp_fixed(i, j) = nan
    end do    
  end do
  ! read fixed temperatures into temp_fixed and temp_old
  open(unit=10, file=temps_file, status='old')
  read(10, *) num_fixed_temps
  do temp_line_number=1, num_fixed_temps
    read(10, *) i, j, fixed_temp
    temp_old(i+1, j+1) = fixed_temp
    temp_fixed(i+1, j+1) = fixed_temp
  end do

  write(*, *) 'starting temperatures'
  call print_grid(temp_old, rows, cols)
  write(*, *) 'fixed temperatures'
  call print_grid(temp_fixed, rows, cols)

  do step=1, steps
    ! calculate each new temperature from averaging old neighboring temperatures
    do i=2, rows+1
      do j=2, cols+1
        ! if temp_fixed has a nan value at this position, calculate temp_new
        if (isnan(temp_fixed(i, j))) then
          temp_new(i, j) = &
            (k/8.0)*(&
              temp_old(i-1, j-1)+temp_old(i-1, j)+temp_old(i-1, j+1)+ &
              temp_old(i, j-1)                   +temp_old(i, j+1)+ &
              temp_old(i+1, j-1)+temp_old(i+1, j)+temp_old(i+1, j+1) &
            ) &
            + (1-k)*temp_old(i, j)
        else ! make sure we keep the original fixed temperature
          temp_new(i, j) = temp_fixed(i, j)
        end if
      end do
    end do
    write(*,*) 'step = ', step
    call print_grid(temp_new, rows, cols)
    ! copy new temperatures back to old
    do i=2, rows+1
      do j=2, cols+1
        temp_old(i, j) = temp_new(i, j)
      end do
    end do
  end do

  contains ! including this function inside the main program so that it can take any size t

  subroutine print_grid(t, rows, cols)
    implicit none
    integer, intent(in) :: rows, cols
    real, allocatable, intent(in) :: t(:, :)
    integer :: i, j

    do i=1, rows
      do j=1, cols
        write(*, '(f7.2,1x)', advance='no') t(i+1, j+1)
      end do
      write(*, *)
    end do
  end

end

subroutine get_args(rows, cols, k, t_boundary, steps, temps_file, outfile)
  implicit none
  integer, intent(out) :: rows, cols, steps
  real, intent(out) :: k, t_boundary
  character(len=1000), intent(out) :: temps_file, outfile
  character(len=1000) :: arg
  call get_command_argument(1, arg)
  call char_to_int(arg, rows)
  call get_command_argument(2, arg)
  call char_to_int(arg, cols)
  call get_command_argument(3, arg)
  call char_to_real(arg, k)
  call get_command_argument(4, arg)
  call char_to_real(arg, t_boundary)
  call get_command_argument(5, arg)
  call char_to_int(arg, steps)
  call get_command_argument(6, temps_file)
  call get_command_argument(7, outfile)
end

subroutine char_to_int(c,i)
  implicit none
  character(len=1000), intent(in) :: c
  integer, intent(out) :: i
  read(c, *) i
end

subroutine char_to_real(c,r)
  implicit none
  character(len=1000), intent(in) :: c
  real, intent(out) :: r
  read(c, *) r
end
