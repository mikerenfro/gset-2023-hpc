	program pi

	integer i, total, totalwithin
	real x, y, r2

	total = 2000000000
	totalwithin = 0
	do 10 i=1,total
		call random_number(x)
		call random_number(y)
		r2 = x**2+y**2
		if (r2 <= 1.0) then
			totalwithin = totalwithin+1
		end if
 10     end do
	write(*,*) 'totalwithin/total = ', real(totalwithin)/real(total)

	stop
	end
