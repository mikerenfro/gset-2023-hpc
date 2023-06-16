program pi  
    implicit none
    integer :: i, total, totalwithin
    real :: x, y, r2

    total = 2000000000
    totalwithin = 0
    do i=1,total    
        call random_number(x)
        call random_number(y)
        r2 = x**2+y**2
        if (r2 <= 1.0) then
            totalwithin = totalwithin + 1
        end if
    end do
    write (*,*) 'totalwithin/total = ', real(totalwithin)/real(total)
end program pi
