# Numerical checks for 12-bmath-2082-4061A
from fractions import Fraction as F
import sympy as sp, math
x,y,Q=sp.symbols('x y Q')
# Q2 determinant
assert sp.Matrix([[4,3,5],[0,0,7],[8,6,-1]]).det()==0
# Q3 Hawkins-Simon for option D
D=sp.Matrix([[F(3,10),-F(5,10)],[-F(2,10),F(7,10)]]); assert D[0,0]>0 and D.det()==F(11,100)
for M in ([[-.5,.3],[.7,-.2]],[[-.5,-.2],[.7,.3]],[[.3,.7],[-.2,-.5]]): assert M[0][0]<0 or M[1][1]<0
# Q4 f'(4)>0 and f'(2)=0
f=x**2-4*x; assert sp.diff(f,x).subs(x,4)==4 and sp.diff(f,x).subs(x,2)==0
# Q6 ratio
k=sp.symbols('k'); assert sp.solve((4*k)**2-(k+1)*12*k,k)==[0,3] and 3*4==12 and 3*12==36 and 12*12==4*36
# Q8 depreciation
assert 50000*F(9,10)**3==36450
# Q10 Bowley
q1,m,q3=1,2,3; assert (q3+q1-2*m)==0
# Q13 input-output
A=sp.Matrix([[F(1500,5000),F(2500,7500)],[F(2000,5000),F(2500,7500)]])
assert A[0,0]==F(3,10) and A[1,0]==F(2,5) and A[0,1]==F(1,3) and A[1,1]==F(1,3)
L=sp.eye(2)-A; assert L.det()==F(1,3) and L[0,0]==F(7,10) and 1500+2500+1000==5000 and 2000+2500+3000==7500
# Q15
pi=sp.expand((Q-3*Q**2)-(Q**2-2*Q)); q=sp.solve(sp.diff(pi,Q),Q)[0]
assert q==F(3,8) and pi.subs(Q,q)==F(9,16) and sp.diff(pi,Q,2)==-8
assert F(1,3)*F(3*3+6,3)==F(5,3)
# Q16
assert (4*10+6)==46
area=sp.integrate(2*sp.sqrt(x),(x,2,5)); assert abs(float(area)-11.1359)<0.01
# Q17 simplex: brute-force corners
pts=[(0,0),(2,0),(0,3),(F(20,19),F(45,19))]
assert all(3*a+5*b<=15 and 5*a+2*b<=10 for a,b in pts)
assert max(5*a+2*b for a,b in pts)==10 and 5*2+2*0==10 and 5*F(20,19)+2*F(45,19)==10
# Q18
X=[48,50,52,54,58]; Y=[36,42,43,45,60]
mx,my=sum(X)/5,sum(Y)/5; assert abs(mx-52.4)<1e-9 and abs(my-45.2)<1e-9
sxy=sum((a-mx)*(b-my) for a,b in zip(X,Y)); sxx=sum((a-mx)**2 for a in X); syy=sum((b-my)**2 for b in Y)
assert abs(sxy-131.6)<0.01 and abs(sxx-59.2)<0.01 and abs(syy-318.8)<0.01
assert abs(sxy/math.sqrt(sxx*syy)-0.958)<0.001
# Q19
pd=0.30*0.02+0.35*0.03+0.45*0.04; assert abs(pd-0.0345)<1e-9 and F(6,100)/F(345,1000)==F(4,23)
# Q21
assert 9*3**3==243 and 9*3==27 and 27*3==81 and 2**2==4
c=200000/((1-1.15**-10)/0.15); assert abs(c-39850.4)<1 and abs(c/1.15-34652.6)<1
assert abs(2**(1/5)-1-0.1487)<0.0001
# Q20 ODE
t=sp.Function('y'); sol=sp.dsolve(sp.Eq(t(x).diff(x)+2*t(x),6),t(x)); assert sp.simplify(sol.rhs.subs(sp.Symbol('C1'),0)-3)==0
assert sp.diff(1/x,x,2).subs(x,-4)<0 and sp.diff(1/x,x,2).subs(x,-8)<0
# Q22 regression
Xr=[1,2,3,5,6]; Yr=[5,7,8,10,12]
n=5; sx,sy=sum(Xr),sum(Yr); sxy_=sum(a*b for a,b in zip(Xr,Yr)); sxx_=sum(a*a for a in Xr); syy_=sum(b*b for b in Yr)
assert (sx,sy,sxy_,sxx_,syy_)==(17,42,165,75,382)
byx=F(n*sxy_-sx*sy,n*sxx_-sx**2); bxy=F(n*sxy_-sx*sy,n*syy_-sy**2); assert byx==F(111,86) and bxy==F(111,146)
w4=float(F(42,5)+byx*(4-F(17,5))); a6=float(F(17,5)+bxy*(6-F(42,5)))
assert abs(w4-9.174)<0.01 and abs(a6-1.575)<0.01 and abs(math.sqrt(float(byx*bxy))-0.99)<0.01
assert F(11,16)==1-F(1,16)-F(4,16)==F(6+4+1,16)
print('bmath 2082 4061A checks OK')
