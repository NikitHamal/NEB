program transpose_matrix
    implicit none
    integer :: m, n, i, j
    real, allocatable :: a(:,:), t(:,:)

    print *, 'Enter number of rows and columns:'
    read *, m, n
    allocate(a(m,n), t(n,m))
    print *, 'Enter the matrix row by row:'
    do i = 1, m
        read *, (a(i,j), j = 1, n)
    end do
    do i = 1, m
        do j = 1, n
            t(j,i) = a(i,j)
        end do
    end do
    print *, 'Transpose of the matrix:'
    do i = 1, n
        print '(10F8.2)', (t(i,j), j = 1, m)
    end do
end program transpose_matrix
