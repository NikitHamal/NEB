      PROGRAM SORT100
      INTEGER N
      PARAMETER (N = 100)
      REAL A(N), T
      INTEGER I, J
      PRINT *, 'ENTER 100 NUMBERS'
      READ *, (A(I), I = 1, N)
      DO 20 I = 1, N - 1
         DO 10 J = 1, N - I
            IF (A(J) .GT. A(J+1)) THEN
               T = A(J)
               A(J) = A(J+1)
               A(J+1) = T
            END IF
   10    CONTINUE
   20 CONTINUE
      PRINT *, 'SORTED (ASCENDING) NUMBERS:'
      PRINT *, (A(I), I = 1, N)
      END
