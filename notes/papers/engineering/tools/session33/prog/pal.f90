      PROGRAM PALIN
      INTEGER N, M, R, D
      PRINT *, 'ENTER A POSITIVE INTEGER'
      READ *, N
      M = N
      R = 0
   10 IF (M) 99, 30, 20
   20 D = MOD(M, 10)
      R = R * 10 + D
      M = M / 10
      GO TO 10
   30 IF (R - N) 40, 50, 40
   40 PRINT *, N, ' IS NOT A PALINDROME'
      GO TO 60
   50 PRINT *, N, ' IS A PALINDROME'
   60 STOP
   99 PRINT *, 'NUMBER MUST BE POSITIVE'
      END
