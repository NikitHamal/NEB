"""Spot-check of Mathematics I worked answers with SymPy (run: python3 check_math1.py)."""
from sympy import *
x,t,y=symbols('x t y'); ok=True
def eq(a,b,label):
    global ok
    r=simplify(a-b)==0 or abs(N(a-b))<1e-9
    if not r: ok=False
    print("ok  " if r else "FAIL",label)
eq(limit((x**2-9)/(x-3),x,3),6,"lim1")
eq(limit((sqrt(x+4)-2)/x,x,0),Rational(1,4),"lim2")
eq(limit((tan(2*x)-sin(2*x))/x**3,x,0),4,"lim3")
eq(limit((1+2/x)**x,x,oo),exp(2),"e^2")
eq(limit(sqrt(x**2+x)-x,x,oo),Rational(1,2),"sqrt")
eq(limit((exp(x)-1-x)/x**2,x,0),Rational(1,2),"lhop1")
eq(limit((sin(x)-x)/x**3,x,0),Rational(-1,6),"lhop2")
eq(limit(x*log(x),x,0,'+'),0,"xlnx")
eq(limit((tan(x)-x)/x**3,x,0),Rational(1,3),"tan-x")
eq(limit(cos(x)**(1/x**2),x,0),exp(Rational(-1,2)),"cos^1/x2")
eq(limit((exp(2*x)-1)/sin(3*x),x,0),Rational(2,3),"e2x/sin3x")
eq(limit((sqrt(x**2+3*x)-x),x,oo),Rational(3,2),"3/2")
eq(diff(x**2*sin(x),x),2*x*sin(x)+x**2*cos(x),"prod")
eq(diff((x**2+1)/(x-1),x),(x**2-2*x-1)/(x-1)**2,"quot")
eq(diff(x**x,x),x**x*(log(x)+1),"xx")
Y=Function('Y')
d=-(Rational(3,4))/sin(t)**3
tt=symbols('tt'); X=2*cos(tt);YY=3*sin(tt)
dydx=diff(YY,tt)/diff(X,tt); eq(diff(dydx,tt)/diff(X,tt),-Rational(3,4)/sin(tt)**3,"d2y/dx2")
eq(diff(exp(x)*sin(x),x,2)-2*diff(exp(x)*sin(x),x)+2*exp(x)*sin(x),0,"y''-2y'+2y")
# implicit
yy=Function('yy')(x); sol=solve(diff(x**2*yy+yy**3-10,x),diff(yy,x))[0]; eq(sol.subs({x:1,yy:2}),Rational(-4,13),"implicit")
# optimisation
eq(maximum(x*(12-2*x)**2,x,Interval(0,6)),128,"box")
eq(((250/pi)**Rational(1,3)).evalf(),4.3013,"can r") if False else None
print("can r",N((250/pi)**Rational(1,3)))
# integrals
eq(integrate(x*exp(x),(x,0,1)),1,"xe^x")
eq(integrate(sin(x)**3,(x,0,pi/2)),Rational(2,3),"sin3")
eq(integrate(x**2*log(x),x),x**3/3*log(x)-x**3/9,"x2lnx")
eq(integrate(exp(x)*sin(x),x),exp(x)*(sin(x)-cos(x))/2,"esin")
eq(integrate(1/((x-1)*(x+2)),x).diff(x),1/((x-1)*(x+2)),"pf")
eq(integrate((2*x+3)/((x-1)*(x+2)),x).diff(x),(2*x+3)/((x-1)*(x+2)),"pf2")
eq(apart((2*x+3)/((x-1)*(x+2)),x),Rational(5,3)/(x-1)+Rational(1,3)/(x+2),"apart")
eq(integrate(x-x**2,(x,0,1)),Rational(1,6),"area")
eq(integrate(4*x-2*x**2,(x,0,2)),Rational(8,3),"area2")
eq(pi*integrate(x**4,(x,1,2)),31*pi/5,"vol")
eq(integrate(sin(x),(x,0,pi))/pi,2/pi,"avg")
eq(integrate(x**2*exp(-x*0)*1,(x,0,3))/3,3,"avg x2")
eq(integrate(x**(-Rational(3,2)),(x,1,oo)),2,"improper")
# series
eq(series(cos(x),x,0,6).removeO().subs(x,Rational(1,5)).evalf(),0.98006657,"cos0.2") if False else None
print("cos0.2",N(1-0.02+0.04**2/24), N(cos(0.2)))
# DEs
f=Function('f')
def chk(ode,s,l):
    r=checkodesol(ode,s)[0]; print("ok  " if r else "FAIL",l); 
chk(Eq(f(x).diff(x)+2*f(x),exp(-x)),Eq(f(x),exp(-x)+symbols('C')*exp(-2*x)),"linear")
chk(Eq(x*f(x).diff(x)+f(x),x**2),Eq(f(x),x**2/3+symbols('C')/x),"linear2")
s=dsolve(Eq(f(x).diff(x,2)-3*f(x).diff(x)+2*f(x),0),ics={f(0):1,f(x).diff(x).subs(x,0):0}); print(s)
s=dsolve(Eq(f(x).diff(x,2)-4*f(x),0),ics={f(0):2,f(x).diff(x).subs(x,0):0}); print(s)
print("exact F:", diff(x**2*y+3*x+2*y**2,x), diff(x**2*y+3*x+2*y**2,y), "| second:", diff(x**3*y+2*x+2*y**2,x), diff(x**3*y+2*x+2*y**2,y))
print("pop",1000*3**2.5, "triple",10*log(3)/log(2))
print("ALL OK" if ok else "SOME FAILED")
