      PROGRAM FIBO
      INTEGER N, I, A, B, C
      WRITE(*,*) 'ENTER N'
      READ(*,*) N
      A = 0
      B = 1
      WRITE(*,*) 'FIBONACCI SEQUENCE:'
      DO 10 I = 1, N
         WRITE(*,*) A
         C = A + B
         A = B
         B = C
   10 CONTINUE
      END
