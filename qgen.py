import random,math,json,datetime
R=random.Random(0);out=[]
TQ={'work_together': 'Time & Work', 'work_alone': 'Time & Work', 'pipes': 'Time & Work', 'pct_of': 'Percentage, Profit & Loss', 'pct_change': 'Percentage, Profit & Loss', 'succ_disc': 'Percentage, Profit & Loss', 'profit_pct': 'Percentage, Profit & Loss', 'loss_sp': 'Percentage, Profit & Loss', 'cp_from_sp': 'Percentage, Profit & Loss', 'mp_disc': 'Percentage, Profit & Loss', 'gst': 'Percentage, Profit & Loss', 'pop': 'Percentage, Profit & Loss', 'sale_two': 'Percentage, Profit & Loss', 'si_P': 'Simple & Compound Interest', 'si_rate': 'Simple & Compound Interest', 'ci2': 'Simple & Compound Interest', 'avg_n': 'Average & Ratio', 'avg_age': 'Average & Ratio', 'ratio_share': 'Average & Ratio', 'prop_xy': 'Average & Ratio', 'partner': 'Average & Ratio', 'mix': 'Average & Ratio', 'age_sum': 'Average & Ratio', 'age_future': 'Average & Ratio', 'median_mode': 'Average & Ratio', 'std': 'Time, Speed & Distance', 'avg_speed': 'Time, Speed & Distance', 'train_pole': 'Time, Speed & Distance', 'train_rel': 'Time, Speed & Distance', 'boat': 'Time, Speed & Distance', 'boat_up': 'Time, Speed & Distance', 'hcf': 'Number System', 'lcm': 'Number System', 'lcm_word': 'Number System', 'remainder': 'Number System', 'sq_root': 'Number System', 'cube_root': 'Number System', 'bodmas': 'Number System', 'bodmas2': 'Number System', 'consec': 'Number System', 'nfactors': 'Number System', 'unit_digit': 'Number System', 'frac_cmp': 'Number System', 'linear': 'Algebra & Series', 'ap_nth': 'Algebra & Series', 'ap_sum': 'Algebra & Series', 'quad': 'Algebra & Series', 'tri_area': 'Mensuration & Geometry', 'circ_area': 'Mensuration & Geometry', 'circum': 'Mensuration & Geometry', 'cyl_vol': 'Mensuration & Geometry', 'cube_vol': 'Mensuration & Geometry', 'pyth': 'Mensuration & Geometry', 'poly_angle': 'Mensuration & Geometry', 'tri_angle': 'Mensuration & Geometry', 'trapezium': 'Mensuration & Geometry', 'prob_dice': 'Mixed', 'prob_cards': 'Mixed', 'comb': 'Mixed', 'perm_word': 'Mixed'}
from fractions import Fraction
def fmt(v):
    if isinstance(v,float):
        if abs(v-round(v))<1e-9:return str(int(round(v)))
        return ('%.2f'%v).rstrip('0').rstrip('.')
    return str(v)
def distract(c,kind='num',spread=None):
    # produce 3 distinct wrong numerics near c
    ws=set();cv=float(c);tries=0
    steps=[0.1,0.2,0.25,0.5,1,2,3,5,10]
    while len(ws)<3 and tries<200:
        tries+=1
        f=R.choice([0.5,0.8,0.9,1.1,1.2,1.25,1.5,2])
        d=R.choice([-10,-5,-2,-1,1,2,5,10]) if abs(cv)<50 else None
        w=cv*f if d is None else cv+d
        if kind=='int':w=round(w)
        else:w=round(w,2)
        if w!=cv and w>0 and fmt(w)!=fmt(cv):ws.add(w)
    return [fmt(w) for w in list(ws)[:3]]
CUR=''
def add(sub,q,c,w,x,l='medium'):
    c=fmt(c) if not isinstance(c,str) else c
    w=[fmt(v) if not isinstance(v,str) else v for v in w]
    if len(set(w+[c]))==4 and len(w)==3:out.append((sub,q,c,w,x,TQ.get(CUR,'Mixed')))
def gen(fn,n):
    k=0;t=0
    while k<n and t<n*20:
        t+=1;before=len(out);fn();k+=len(out)-before
Q='Quant'
def pct_of():
    p=R.choice([5,8,12,15,18,20,24,25,30,35,40,45,60,75]);n=R.choice([80,120,150,200,240,320,450,600,720,840]);c=p*n/100
    add(Q,f"A shop has {n} items and {p}% of them are sold. How many items are sold?",c,distract(c,'int'),f"{p}% of {n} = {fmt(c)}.",'easy')
def pct_change():
    a=R.choice([40,50,80,120,200,250,400]);p=R.choice([10,15,20,25,30,40]);c=a*(100+p)//100
    add(Q,f"The price of a book rises from Rs {a} by {p}%. What is the new price (in Rs)?",c,distract(c,'int'),f"New price = {a} x (100+{p})/100 = {c}.",'easy')
def succ_disc():
    a,b=R.choice([(10,10),(20,10),(20,20),(25,20),(30,10),(10,20),(40,10),(50,20)]);c=100-(100-a)*(100-b)/100
    add(Q,f"Two successive discounts of {a}% and {b}% are equal to a single discount of:",f"{fmt(c)}%",[fmt(a+b)+"%",fmt(abs(a-b))+"%",fmt(c+2.5)+"%"],f"Net = 100 - ({100-a} x {100-b})/100 = {fmt(c)}%.")
def profit_pct():
    cp=R.choice([200,250,400,500,800,1200]);pr=R.choice([10,12.5,15,20,25,30]);sp=cp*(100+pr)/100
    add(Q,f"An article bought for Rs {cp} is sold for Rs {fmt(sp)}. The profit percent is:",f"{fmt(pr)}%",[fmt(pr+5)+"%",fmt(pr-5 if pr>7 else pr+10)+"%",fmt(pr*2)+"%"],f"Profit = {fmt(sp-cp)}; % = {fmt(sp-cp)}/{cp} x 100 = {fmt(pr)}%.")
def loss_sp():
    cp=R.choice([300,500,750,1000,1500,2000]);l=R.choice([8,10,12,15,20,25]);c=cp*(100-l)/100
    add(Q,f"A trader buys a fan for Rs {cp} and sells it at a loss of {l}%. The selling price (in Rs) is:",c,distract(c,'int'),f"SP = {cp} x {100-l}/100 = {fmt(c)}.")
def cp_from_sp():
    cp=R.choice([400,500,600,800,1000,1200,2000]);p=R.choice([10,20,25,50]);sp=cp*(100+p)//100
    add(Q,f"A man sells a bag for Rs {sp} at a profit of {p}%. The cost price (in Rs) is:",cp,distract(cp,'int'),f"CP = {sp} x 100/{100+p} = {cp}.")
def mp_disc():
    mp=R.choice([500,800,1000,1200,1500,2000]);d=R.choice([10,15,20,25]);c=mp*(100-d)//100
    add(Q,f"The marked price of a shirt is Rs {mp}. After a discount of {d}%, the price paid (in Rs) is:",c,distract(c,'int'),f"{mp} x {100-d}/100 = {c}.",'easy')
def si_P():
    P=R.choice([2000,4000,5000,8000,10000]);r=R.choice([5,6,8,10]);t=R.choice([2,3,4,5]);I=P*r*t//100
    add(Q,f"At {r}% simple interest per annum, a sum earns Rs {I} in {t} years. The sum (in Rs) is:",P,distract(P,'int'),f"P = I x 100/(r x t) = {I} x 100/({r} x {t}) = {P}.")
def si_rate():
    P=R.choice([2000,5000,8000,10000]);r=R.choice([4,5,6,8,10]);t=R.choice([2,3,4,5]);I=P*r*t//100
    add(Q,f"Rs {P} gives simple interest of Rs {I} in {t} years. The rate of interest per annum is:",f"{r}%",[f"{r+2}%",f"{r+4}%",f"{max(r-2,1)}%"],f"r = {I} x 100/({P} x {t}) = {r}%.")
def ci2():
    P=R.choice([2000,4000,5000,10000,20000]);r=R.choice([5,10,20]);A=P*(100+r)**2/10000;ci=A-P
    add(Q,f"The compound interest on Rs {P} at {r}% per annum for 2 years (compounded yearly) is (in Rs):",ci,distract(ci,'int') if True else [],f"A = {P}(1+{r}/100)^2 = {fmt(A)}; CI = {fmt(ci)}.",'medium')
def avg_n():
    n=R.choice([4,5,6,8]);avg=R.choice([12,15,20,24,30,36]);missing=R.choice([5,10,15])
    tot=n*avg;
    add(Q,f"The average of {n} numbers is {avg}. If one number, {avg+missing}, is removed, the average of the remaining numbers is:",fmt((tot-avg-missing)/(n-1)),[fmt(avg),fmt(avg+1),fmt((tot-avg-missing)/(n-1)+2)],f"Sum = {tot}; remaining sum = {tot-avg-missing}; average = {fmt((tot-avg-missing)/(n-1))}.")
def avg_age():
    n=R.choice([5,6,8,10]);a=R.choice([20,22,24,25,30]);inc=R.choice([1,2,3]);new=a+inc*(n+1)
    add(Q,f"The average age of {n} students is {a} years. When a new student joins, the average increases by {inc} year(s). The age of the new student is:",new,distract(new,'int'),f"New age = {a} + {inc} x {n+1} = {new}.",'medium')
def ratio_share():
    a,b=R.choice([(2,3),(3,5),(4,5),(1,4),(2,7),(3,4)]);k=R.choice([20,30,40,50,60]);tot=(a+b)*k
    add(Q,f"Rs {tot} is divided between P and Q in the ratio {a}:{b}. Q's share (in Rs) is:",b*k,distract(b*k,'int'),f"Q = {tot} x {b}/{a+b} = {b*k}.",'easy')
def prop_xy():
    a,b=R.choice([(2,5),(3,4),(5,6),(4,9),(7,3)]);m=R.choice([2,3,4,5])
    add(Q,f"If {a}:{b} = {a*m}:x, then x equals:",b*m,distract(b*m,'int'),f"x = {b} x {a*m}/{a} = {b*m}.",'easy')
def std():
    sp=R.choice([36,45,54,60,72,90]);t=R.choice([2,3,4,5]);
    add(Q,f"A bus travelling at {sp} km/h covers how many kilometres in {t} hours?",sp*t,distract(sp*t,'int'),f"Distance = {sp} x {t} = {sp*t} km.",'easy')
def avg_speed():
    a,b=R.choice([(40,60),(30,60),(20,30),(60,90),(50,75),(40,40)]);c=2*a*b/(a+b)
    add(Q,f"A man travels from A to B at {a} km/h and returns at {b} km/h. His average speed for the whole trip is:",f"{fmt(c)} km/h",[f"{fmt((a+b)/2)} km/h",f"{fmt(c+3)} km/h",f"{fmt(c-3)} km/h"],f"Average speed = 2ab/(a+b) = {fmt(c)} km/h.",'medium')
def train_pole():
    L=R.choice([100,150,200,250,300]);s=R.choice([36,54,72,90]);t=L/(s*5/18)
    add(Q,f"A train {L} m long runs at {s} km/h. The time taken to cross a pole is (in seconds):",t,distract(t),f"Speed = {s} x 5/18 m/s; time = {L}/({fmt(s*5/18)}) = {fmt(t)} s.",'medium')
def train_rel():
    s1,s2=R.choice([(60,40),(72,54),(50,40),(90,72),(80,40)]);d=R.choice([100,200,300])
    c=d/((s1+s2)*5/18)
    add(Q,f"Two trains of total length {d} m run in opposite directions at {s1} km/h and {s2} km/h. The time they take to cross each other is (in seconds):",c,distract(c),f"Relative speed = {s1+s2} km/h = {fmt((s1+s2)*5/18)} m/s; time = {d}/{fmt((s1+s2)*5/18)} = {fmt(c)} s.",'hard')
def boat():
    b,s=R.choice([(10,2),(12,3),(15,5),(8,2),(20,4)]);
    add(Q,f"A boat's speed in still water is {b} km/h and the stream flows at {s} km/h. Its downstream speed (km/h) is:",b+s,[b-s,b,b+2*s],f"Downstream = {b} + {s} = {b+s} km/h.",'easy')
def boat_up():
    b,s=R.choice([(10,2),(12,3),(15,5),(8,2),(20,4)])
    add(Q,f"A boat goes at {b} km/h in still water. If the stream speed is {s} km/h, its upstream speed (km/h) is:",b-s,[b+s,b,b-2*s if b-2*s>0 else b+1],f"Upstream = {b} - {s} = {b-s} km/h.",'easy')
def work_together():
    a,b=R.choice([(10,15),(12,6),(20,30),(15,30),(12,4),(6,3),(8,24),(30,60)]);c=a*b/(a+b)
    add(Q,f"A can do a piece of work in {a} days and B in {b} days. Working together, they finish it in (days):",c,distract(c),f"Together = {a}x{b}/({a}+{b}) = {fmt(c)} days.",'medium')
def work_alone():
    a,t=R.choice([(12,4),(20,5),(30,10),(15,6),(10,5)]);# together t days, A alone a -> B alone
    b=Fraction(a*t,a-t);
    if b.denominator!=1:return
    add(Q,f"A and B together finish a job in {t} days. A alone can finish it in {a} days. B alone will finish it in (days):",int(b),distract(int(b),'int'),f"1/B = 1/{t} - 1/{a} so B = {int(b)} days.",'hard')
def pipes():
    a,b=R.choice([(10,15),(12,6),(20,30),(15,10),(6,3)]);c=a*b/(a+b)
    add(Q,f"Two pipes can fill a tank in {a} hours and {b} hours respectively. Opened together, the tank will fill in (hours):",c,distract(c),f"Together = {a}x{b}/({a}+{b}) = {fmt(c)} hours.",'medium')
def hcf():
    k=R.choice([3,4,5,6,7,8,9,12]);a,b=R.sample([2,3,4,5,6,7,9,10],2);x,y=a*k,b*k;h=math.gcd(x,y)
    add(Q,f"The HCF of {x} and {y} is:",h,distract(h,'int'),f"HCF({x},{y}) = {h}.",'easy')
def lcm():
    x,y=R.sample([4,6,8,9,10,12,14,15,18,20,24],2);l=x*y//math.gcd(x,y)
    add(Q,f"The LCM of {x} and {y} is:",l,distract(l,'int'),f"LCM = {x} x {y}/HCF = {l}.",'easy')
def lcm_word():
    a,b=R.choice([(4,6),(6,8),(10,15),(12,18),(20,30)]);l=a*b//math.gcd(a,b)
    add(Q,f"Two bells ring every {a} minutes and every {b} minutes. If they ring together now, they will ring together again after (minutes):",l,distract(l,'int'),f"LCM({a},{b}) = {l}.",'medium')
def remainder():
    d=R.choice([5,7,9,11,13]);q=R.choice([12,15,23,31,40]);r=R.randrange(1,d);n=d*q+r
    add(Q,f"What is the remainder when {n} is divided by {d}?",r,[x for x in {(r+1)%d,(r+2)%d,(r+3)%d,(r-1)%d} if x!=r][:3] if len({(r+1)%d,(r+2)%d,(r+3)%d,(r-1)%d}-{r})>=3 else [],f"{n} = {d} x {q} + {r}.",'easy')
def sq_root():
    n=R.choice([441,529,576,625,676,729,784,841,900,961,1024,1089,1156,1225,1296]);r=int(math.isqrt(n))
    add(Q,f"The square root of {n} is:",r,[r+1,r-1,r+2],f"{r} x {r} = {n}.",'easy')
def cube_root():
    r=R.choice([6,7,8,9,11,12,13,14,15]);n=r**3
    add(Q,f"The cube root of {n} is:",r,[r+1,r-1,r+2],f"{r}^3 = {n}.",'easy')
def bodmas():
    a,b,c,d=R.sample(range(2,15),4);v=a+b*c-d
    add(Q,f"Find the value of {a} + {b} x {c} - {d}:",v,distract(v,'int'),f"Multiply first: {b*c}; then {a} + {b*c} - {d} = {v}.",'easy')
def bodmas2():
    a,b,c=R.sample(range(2,12),3);v=(a+b)*c
    add(Q,f"Evaluate: ({a} + {b}) x {c}",v,[a+b*c,v+c,v-c],f"({a+b}) x {c} = {v}.",'easy')
def linear():
    x=R.randrange(3,20);a=R.choice([2,3,4,5,6,7]);b=R.randrange(1,20);c=a*x+b
    add(Q,f"If {a}x + {b} = {c}, the value of x is:",x,[x+1,x-1,x+2],f"x = ({c} - {b})/{a} = {x}.",'easy')
def age_sum():
    a=R.randrange(8,16);k=R.choice([2,3]);y=R.choice([3,4,5,6]);f=k*a;
    add(Q,f"A father is {k} times as old as his son. The sum of their ages is {f+a} years. The son's age is:",a,[a+2,a-2,a+4],f"Let son = x: x + {k}x = {f+a} so x = {a}.",'medium')
def age_future():
    a=R.randrange(10,20);f=a+R.choice([20,24,26,30]);t=R.choice([4,5,6,8])
    add(Q,f"A boy is {a} years old and his father is {f} years old. After {t} years, the sum of their ages will be:",a+f+2*t,[a+f+t,a+f+3*t,a+f],f"({a}+{t}) + ({f}+{t}) = {a+f+2*t}.",'easy')
def consec():
    n=R.choice([3,5]);s=R.randrange(5,40);tot=sum(range(s,s+n))
    add(Q,f"The sum of {n} consecutive integers is {tot}. The smallest of them is:",s,[s+1,s-1,s+2],f"Middle = {tot}/{n} = {tot//n}; smallest = {s}.",'medium')
def ap_nth():
    a=R.randrange(2,10);d=R.randrange(2,7);n=R.choice([8,10,12,15]);v=a+(n-1)*d
    add(Q,f"The {n}th term of the arithmetic progression {a}, {a+d}, {a+2*d}, ... is:",v,distract(v,'int'),f"a + (n-1)d = {a} + {n-1} x {d} = {v}.",'medium')
def ap_sum():
    a=R.randrange(1,6);d=R.randrange(1,5);n=R.choice([10,12,15,20]);v=n*(2*a+(n-1)*d)//2
    add(Q,f"The sum of the first {n} terms of the AP {a}, {a+d}, {a+2*d}, ... is:",v,distract(v,'int'),f"S = n/2 [2a + (n-1)d] = {v}.",'hard')
def tri_area():
    b=R.choice([6,8,10,12,14,16,20]);h=R.choice([5,7,9,11,13]);c=b*h/2
    add(Q,f"The area of a triangle with base {b} cm and height {h} cm is (sq cm):",c,distract(c),f"Area = 1/2 x {b} x {h} = {fmt(c)}.",'easy')
def circ_area():
    r=R.choice([7,14,21,28]);c=22*r*r/7
    add(Q,f"The area of a circle of radius {r} cm (use pi = 22/7) is (sq cm):",c,distract(c,'int'),f"Area = 22/7 x {r}^2 = {fmt(c)}.",'medium')
def circum():
    r=R.choice([7,14,21,35]);c=44*r/7
    add(Q,f"The circumference of a circle of radius {r} cm (pi = 22/7) is (cm):",c,distract(c,'int'),f"2 x 22/7 x {r} = {fmt(c)}.",'easy')
def cyl_vol():
    r=R.choice([7,14]);h=R.choice([5,10,15,20]);v=22*r*r*h/7
    add(Q,f"The volume of a cylinder with radius {r} cm and height {h} cm (pi = 22/7) is (cu cm):",v,distract(v,'int'),f"V = 22/7 x {r}^2 x {h} = {fmt(v)}.",'medium')
def cube_vol():
    a=R.choice([3,4,5,6,7,8,9,10,12]);
    add(Q,f"The total surface area of a cube of side {a} cm is (sq cm):",6*a*a,[4*a*a,a**3,6*a],f"TSA = 6a^2 = {6*a*a}.",'easy')
def pyth():
    a,b,c=R.choice([(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29),(9,40,41)]);k=R.choice([1,2,3])
    add(Q,f"The two perpendicular sides of a right-angled triangle are {a*k} cm and {b*k} cm. The hypotenuse is (cm):",c*k,[c*k+1,c*k-1,(a+b)*k],f"sqrt({(a*k)**2}+{(b*k)**2}) = {c*k}.",'medium')
def poly_angle():
    n=R.choice([5,6,8,9,10,12]);c=180*(n-2)//n
    add(Q,f"Each interior angle of a regular polygon with {n} sides is (degrees):",c,distract(c,'int'),f"(n-2) x 180/n = {c}.",'medium')
def tri_angle():
    a=R.randrange(30,70);b=R.randrange(30,80);c=180-a-b
    add(Q,f"Two angles of a triangle are {a} degrees and {b} degrees. The third angle is:",f"{c} degrees",[f"{c+10} degrees",f"{c-10} degrees",f"{c+20} degrees"],f"180 - {a} - {b} = {c}.",'easy')
def prob_dice():
    k=R.choice([('an even number',3),('a number greater than 4',2),('a prime number',3),('a multiple of 3',2),('a number less than 3',2)])
    f=Fraction(k[1],6)
    add(Q,f"A fair die is thrown once. The probability of getting {k[0]} is:",f"{f.numerator}/{f.denominator}",["1/6","1/4","5/6"] if f!=Fraction(1,6) else ["1/2","1/4","5/6"],f"Favourable = {k[1]}, total = 6.",'easy')
def prob_cards():
    k=R.choice([('a king',4),('a heart',13),('a red card',26),('a face card',12),('an ace',4)]);f=Fraction(k[1],52)
    pool=["1/2","1/4","1/13","3/13","1/26","1/52","4/13"]
    w=[p for p in pool if p!=f"{f.numerator}/{f.denominator}"][:3]
    add(Q,f"One card is drawn from a well-shuffled pack of 52 cards. The probability that it is {k[0]} is:",f"{f.numerator}/{f.denominator}",w,f"{k[1]}/52 = {f.numerator}/{f.denominator}.",'medium')
def comb():
    n=R.choice([5,6,7,8,9,10]);r=R.choice([2,3]);v=math.comb(n,r)
    add(Q,f"In how many ways can {r} students be chosen from a group of {n}?",v,distract(v,'int'),f"C({n},{r}) = {v}.",'medium')
def perm_word():
    w=R.choice(["MOON","TREE","BOOK","DOOR","LEVEL"]);from collections import Counter
    v=math.factorial(len(w));
    for c in Counter(w).values():v//=math.factorial(c)
    add(Q,f"The number of different arrangements of the letters of the word {w} is:",v,distract(v,'int'),f"{len(w)}!/repeats = {v}.",'hard')
def median_mode():
    xs=sorted(R.sample(range(3,40),5));
    add(Q,f"The median of the data {', '.join(map(str,R.sample(xs,5)))} is:",xs[2],[xs[1],xs[3],xs[0]],f"Sorted: {', '.join(map(str,xs))}; middle = {xs[2]}.",'easy')
def nfactors():
    p,q=R.sample([2,3,5,7],2);a,b=R.choice([(2,1),(2,2),(3,1),(1,1),(3,2)]);n=p**a*q**b;v=(a+1)*(b+1)
    add(Q,f"The number of factors of {n} is:",v,[v+1,v-1,v+2],f"{n} = {p}^{a} x {q}^{b}; factors = ({a}+1)({b}+1) = {v}.",'hard')
def unit_digit():
    b=R.choice([2,3,7,8,9]);e=R.choice([13,22,27,35,46]);cyc={2:[2,4,8,6],3:[3,9,7,1],7:[7,9,3,1],8:[8,4,2,6],9:[9,1]};v=cyc[b][(e-1)%len(cyc[b])]
    add(Q,f"The unit digit of {b}^{e} is:",v,[x for x in [1,3,5,7,9,2,4,6,8] if x!=v][:3],f"Powers of {b} repeat; unit digit = {v}.",'hard')
def mix():
    a,b,c=R.choice([(20,40,30),(10,50,30),(30,60,50)]);
    # ratio quantities milk water: cheaper cost a, dearer b, mean c : ratio (b-c):(c-a)
    r1,r2=b-c,c-a;g=math.gcd(r1,r2)
    add(Q,f"Rice costing Rs {a}/kg is mixed with rice costing Rs {b}/kg so that the mixture is worth Rs {c}/kg. The ratio of cheaper to dearer rice is:",f"{r1//g}:{r2//g}",[f"{r2//g}:{r1//g}","1:1","2:1" if (r1//g,r2//g)!=(2,1) else "3:1"],f"Alligation: ({b}-{c}):({c}-{a}) = {r1//g}:{r2//g}.",'hard')
def partner():
    a,b,pf=R.choice([(2000,3000,5000),(4000,6000,10000),(5000,10000,9000),(3000,6000,12000)]);v=pf*a//(a+b)
    add(Q,f"A and B invest Rs {a} and Rs {b} in a business. If the total profit is Rs {pf}, A's share (in Rs) is:",v,distract(v,'int'),f"A's share = {pf} x {a}/{a+b} = {v}.",'medium')
def pop():
    p=R.choice([20000,40000,50000,80000]);r=R.choice([5,10,20]);v=p*(100+r)//100
    add(Q,f"The population of a town is {p}. If it increases by {r}% in a year, the population after one year will be:",v,distract(v,'int'),f"{p} x {100+r}/100 = {v}.",'easy')
def frac_cmp():
    a,b,c,d=R.sample([2,3,4,5,7,9],4);
    vals={f"{a}/{b}":a/b,f"{c}/{d}":c/d}
    if len(set(vals.values()))<2 or a==b or c==d:return
    big=max(vals,key=vals.get);small=min(vals,key=vals.get)
    add(Q,f"Which of the following fractions is larger: {a}/{b} or {c}/{d}?",big,[small,"Both are equal","Cannot be determined"],f"{a}/{b} = {a/b:.3f}, {c}/{d} = {c/d:.3f}.",'easy')
def quad():
    r1,r2=R.sample(range(1,10),2);s=r1+r2;p=r1*r2
    add(Q,f"The roots of x^2 - {s}x + {p} = 0 are:",f"{r1} and {r2}",[f"{r1+1} and {r2}",f"{r1} and {r2+1}",f"-{r1} and -{r2}"],f"Sum = {s}, product = {p}, so roots are {r1} and {r2}.",'medium')
def trapezium():
    a,b,h=R.choice([(6,10,4),(8,12,5),(10,14,6),(12,18,8)]);v=(a+b)*h/2
    add(Q,f"The area of a trapezium with parallel sides {a} cm and {b} cm and height {h} cm is (sq cm):",v,distract(v,'int'),f"Area = (a+b)/2 x h = {fmt(v)}.",'medium')
def gst():
    p=R.choice([1000,2000,5000]);g=R.choice([5,12,18]);v=p*(100+g)//100
    add(Q,f"A bill is Rs {p} before tax. If {g}% GST is added, the total bill (in Rs) is:",v,distract(v,'int'),f"{p} x {100+g}/100 = {v}.",'easy')
def sale_two():
    p=R.choice([10,20,25]);v=p*p/100
    add(Q,f"A trader sells two articles at the same price, one at a profit of {p}% and the other at a loss of {p}%. His overall result is a:",f"loss of {fmt(v)}%",[f"profit of {fmt(v)}%","no profit, no loss",f"loss of {fmt(p)}%"],f"Loss % = (x^2)/100 = {fmt(v)}%.",'hard')

FNS=[pct_of,pct_change,succ_disc,profit_pct,loss_sp,cp_from_sp,mp_disc,si_P,si_rate,ci2,avg_n,avg_age,ratio_share,prop_xy,std,avg_speed,train_pole,train_rel,boat,boat_up,work_together,work_alone,pipes,hcf,lcm,lcm_word,remainder,sq_root,cube_root,bodmas,bodmas2,linear,age_sum,age_future,consec,ap_nth,ap_sum,tri_area,circ_area,circum,cyl_vol,cube_vol,pyth,poly_angle,tri_angle,prob_dice,prob_cards,comb,perm_word,median_mode,nfactors,unit_digit,mix,partner,pop,frac_cmp,quad,trapezium,gst,sale_two]
def run(seed,n):
    global R,out,CUR
    R=random.Random(seed);out=[];i=0
    order=FNS[:];R.shuffle(order)
    tries=0
    while len(out)<n and tries<n*40:
        fn=order[tries%len(order)];tries+=1;CUR=fn.__name__
        try:fn()
        except Exception:pass
    return out[:n]
