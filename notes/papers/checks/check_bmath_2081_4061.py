# Numerical checks for 12-bmath-2081-4061
from fractions import Fraction as F
import sympy as sp, math
x,y,t,v=sp.symbols('x y t v')
# Q1 A-A^T skew
A=sp.Matrix([[1,0,2],[-2,1,3],[4,5,6]]); assert (A-A.T).T==-(A-A.T)
# Q3 Leontief I-A
assert sp.eye(2)-sp.Matrix([[F(1,10),F(2,10)],[F(3,10),F(4,10)]])==sp.Matrix([[F(9,10),-F(2,10)],[-F(3,10),F(6,10)]])
# Q6 sum, Q7 depreciation, Q8 annuity, Q11 binomial
assert sum(F(1,2**k) for k in range(60))>1.999999 and 1/(1-F(1,2))==2
assert 100000*(1-F(1,10))**2==81000
i=F(8,100); assert 1400*((1+i)**1-1)/i==1400 and 1400*(1+i)==1512
n=F(4)/F(1,4); assert n==16 and 16*F(1,4)*F(3,4)==3
# Q12
assert A.det()==-37 and (A+A.T)==(A+A.T).T and (A+A.T)==sp.Matrix([[2,-2,6],[-2,2,8],[6,8,12]])
# Q13(a)
a,b,c=sp.symbols('a b c')
D=sp.Matrix([[a,b,a*x+b*y],[b,c,b*x+c*y],[a*x+b*y,b*x+c*y,0]]).det()
assert sp.expand(D-(b**2-a*c)*(a*x**2+2*b*x*y+c*y**2))==0
# Q13(b)
s=sp.solve([3*x-2*y-300,x-3*y+300],[x,y]); assert s[x]==F(1500,7) and s[y]==F(1200,7)
# Q14
f=x**3-3*x**2+5
assert [f.subs(x,k) for k in (-2,0,1,2)]==[-15,5,3,1] and sp.solve(sp.diff(f,x))==[0,2] and sp.diff(f,x,2).subs(x,1)==0
# Q16
assert sp.integrate(2*sp.sqrt(x),(x,0,4))==F(32,3)
P=sp.Function('p'); sol=sp.dsolve(sp.Eq(P(t).diff(t),F(5,100)*((240-3*P(t))-(5*P(t)-150))),P(t),ics={P(0):50})
assert sp.simplify(sol.rhs-(F(195,4)+F(5,4)*sp.exp(-F(2,5)*t)))==0
# Q17 simplex + brute force corners
pts=[(0,0),(F(60,9),0),(0,9),(4,6)]; best=max(pts,key=lambda q:50*q[0]+60*q[1]); assert best==(4,6) and 50*4+60*6==560
assert 3*4+4*6==36 and 9*4+4*6==60
# Q18(c)
w=[500,1000,1500]; d=[F(3,100),F(5,100),F(8,100)]
tot=sum(wi*di for wi,di in zip(w,d)); assert tot==185 and F(1500*8,100)/tot==F(24,37) and round(float(F(24,37)),4)==0.6486
# Q19
p0=0.6**10; p1=10*0.4*0.6**9
assert round(p0,4)==0.0060 and round(1-p0,4)==0.9940 and round(p0+p1,4)==0.0464
# Q20
r=1-(1/3)**(1/15); assert round(r*100,2)==7.06 and abs(450000*(1-r)**15-150000)<1e-6
assert 4368/(3**6-1)*2==12
assert round(2500*(1.04**2-1),6)==204 and 2500*.04*3==300
# Q21
X=[100,120,190,200,240,260]; Y=[20,15,16,12,14,13]; mx=sum(X)/6; my=sum(Y)/6
assert mx==185 and my==15
sxy=sum((p-mx)*(q-my) for p,q in zip(X,Y)); sxx=sum((p-mx)**2 for p in X); syy=sum((q-my)**2 for q in Y)
assert (sxy,sxx,syy)==(-670,20350,40)
rr=sxy/math.sqrt(sxx*syy); assert round(rr,3)==-0.743, rr
# Q21(b)
q=F(1875,1000)/F(75,10); assert q==F(1,4) and 1-q==F(3,4) and F(75,10)/F(3,4)==10
P2=45*F(3,4)**2*F(1,4)**8; P0_=F(1,4)**10
assert P2==F(405,1048576) and abs(float(P2)-0.000386)<1e-6 and abs(float(P0_)-9.54e-7)<1e-9
# Q22(a)
xs=sp.solve(sp.Eq(40-x**2,3*x**2+8*x+8),x); assert 2 in xs
CS=sp.integrate(40-x**2,(x,0,2))-36*2; PS=36*2-sp.integrate(3*x**2+8*x+8,(x,0,2))
assert CS==F(16,3) and PS==32
# Q22(b)
g=sp.Function('g'); s2=sp.dsolve(sp.Eq(g(x).diff(x),(x+g(x))/x)); assert sp.simplify(s2.rhs-x*(sp.log(x)+sp.Symbol('C1')))==0
print('ALL BMATH CHECKS PASS')
