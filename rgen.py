import random,json,string,math
R=random.Random(0);out=[]
def add(t,q,c,w,x):
    c=str(c);w=[str(v) for v in w]
    if len(set(w+[c]))==4 and len(w)==3:out.append(('Reasoning',q,c,w,x,t))
def gen(fn,n):
    k=0;i=0
    while k<n and i<n*30:
        i+=1;b=len(out);fn();k+=len(out)-b
A=string.ascii_uppercase
def near(v,r=(1,2,3,4,5)):
    s=[];
    for d in R.sample(list(r),len(r)):
        for sg in(1,-1):
            if v+sg*d>0 and v+sg*d not in s:s.append(v+sg*d)
    return s[:3]
S='Series & Coding'
def ser_ap():
    a=R.randint(2,30);d=R.randint(2,9);xs=[a+i*d for i in range(6)];v=xs[5]
    add(S,f"Find the next number in the series: {', '.join(map(str,xs[:5]))}, ?",v,near(v),f"Common difference is {d}, so next = {xs[4]} + {d} = {v}.")
def ser_gp():
    a=R.choice([1,2,3,4,5]);r=R.choice([2,3]);xs=[a*r**i for i in range(6)];v=xs[5]
    add(S,f"Find the missing number: {', '.join(map(str,xs[:5]))}, ?",v,[v+r,v-r*2,v+a*r],f"Each term is multiplied by {r}: {xs[4]} x {r} = {v}.")
def ser_sq():
    s=R.randint(2,9);xs=[(s+i)**2 for i in range(6)];v=xs[5]
    add(S,f"What comes next in the series: {', '.join(map(str,xs[:5]))}, ?",v,[v+2,v-(2*(s+5)),v+(2*(s+5))],f"These are squares of {s}, {s+1}, ... so next is {s+5}^2 = {v}.")
def ser_cube():
    s=R.randint(1,6);xs=[(s+i)**3 for i in range(5)];v=(s+5)**3
    add(S,f"Find the next term: {', '.join(map(str,xs))}, ?",v,[v+9,v-27,v+27],f"Cubes of consecutive numbers; next is {s+5}^3 = {v}.")
def ser_incr():
    a=R.randint(1,10);d=R.randint(1,4);e=R.randint(1,3);xs=[a];dd=d
    for i in range(5):xs.append(xs[-1]+dd);dd+=e
    v=xs[5]
    add(S,f"Complete the series: {', '.join(map(str,xs[:5]))}, ?",v,near(v,(1,2,3,4,6)),f"Differences are {', '.join(str(xs[i+1]-xs[i]) for i in range(4))} (rising by {e}); next difference {xs[5]-xs[4]}, so {v}.")
def ser_alt():
    a=R.randint(2,20);b=R.randint(30,60);d1=R.randint(2,5);d2=R.randint(2,5)
    xs=[a,b,a+d1,b-d2,a+2*d1,b-2*d2];v=a+3*d1
    add(S,f"Find the next number: {', '.join(map(str,xs))}, ?",v,[v+1,v-1,b-3*d2],f"Two interleaved series: +{d1} at odd places ({a}, {a+d1}, {a+2*d1}, ...) and -{d2} at even places. Next is {v}.")
def ser_prime():
    P=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47];i=R.randint(0,7);xs=P[i:i+5];v=P[i+5]
    add(S,f"Which number comes next: {', '.join(map(str,xs))}, ?",v,[v+1,v+2,v-1 if v-1 not in P else v+4],f"Consecutive prime numbers; the next prime after {xs[-1]} is {v}.")
def ser_letter():
    s=R.randint(0,6);d=R.randint(1,3);L=[A[s+i*d] for i in range(5)];v=A[s+5*d]
    wr=[A[s+5*d+1],A[s+5*d-1],A[s+5*d+2]]
    add(S,f"Find the next letter in the series: {', '.join(L)}, ?",v,wr,f"Each letter moves {d} step(s) forward in the alphabet, so after {L[-1]} comes {v}.")
def ser_odd():
    a=R.randint(2,9);d=R.randint(2,5);xs=[a+i*d for i in range(6)];k=R.randint(1,4);bad=xs[k]+R.choice([1,2,-1]);ys=list(xs);ys[k]=bad
    if bad==xs[k]:return
    add(S,f"One number in this series is wrong. Find it: {', '.join(map(str,ys))}",bad,[x for x in xs if x!=xs[k]][:3] if False else [ys[j] for j in range(6) if j!=k][:3],f"The series adds {d} each time, so the term at that place should be {xs[k]}, not {bad}.")
def code_shift():
    w=R.choice(["MOON","BANK","RAIL","EXAM","PAPER","STUDY","TRAIN","LEARN","NOTES","RESULT","SALARY","OFFICE"]);k=R.randint(1,5)
    enc=''.join(A[(A.index(c)+k)%26] for c in w);
    wr=[''.join(A[(A.index(c)+kk)%26] for c in w) for kk in (k+1,k-1,k+2)]
    add(S,f"In a certain code, each letter is moved {k} place(s) forward. How is {w} written in that code?",enc,wr,f"Move every letter {k} step(s) ahead: {' '.join(w)} gives {' '.join(enc)}.")
def code_decode():
    w=R.choice(["MOON","BANK","RAIL","EXAM","PAPER","STUDY","TRAIN","LEARN","NOTES","SALARY"]);k=R.randint(1,4)
    enc=''.join(A[(A.index(c)-k)%26] for c in w)
    wr=[''.join(A[(A.index(c)-kk)%26] for c in w) for kk in (k+1,k-1 if k>1 else k+2,k+2)]
    add(S,f"In a code language, every letter is shifted {k} place(s) backward. What is the code for {w}?",enc,wr,f"Move each letter {k} step(s) back: {w} becomes {enc}.")
def code_rev():
    w=R.choice(["DELHI","SAMBA","JAMMU","BANKS","TRAIN","PAPER","STUDY","EXAMS","NOTES","SHEET"])
    add(S,f"If the letters of the word {w} are written in reverse order, the third letter from the left is:",w[::-1][2],[c for c in dict.fromkeys(w[::-1]) if c!=w[::-1][2]][:3],f"Reverse of {w} is {w[::-1]}; its third letter is {w[::-1][2]}.")
def code_sum():
    w=R.choice(["CAB","BAD","FACE","HEAD","BEAD","DEAF","CAGE","BAG","FED","DAD"]);v=sum(A.index(c)+1 for c in w)
    add(S,f"If A = 1, B = 2, C = 3 and so on, the sum of the letter values of {w} is:",v,near(v,(1,2,3,4,5)),f"{' + '.join(str(A.index(c)+1) for c in w)} = {v}.")
def code_pos():
    n=R.randint(3,8);w=''.join(R.sample(A,n));k=R.randint(2,n-1)
    add(S,f"In the arrangement {' '.join(w)}, which letter is the {k}th from the left?",w[k-1],[c for c in w if c!=w[k-1]][:3],f"Count {k} places from the left: {w[k-1]}.")
def code_num():
    m={'A':R.randint(1,9)};
    d=R.sample(range(1,10),4);ls=R.sample("PQRS",4);mp=dict(zip(ls,d));w=''.join(R.sample(ls,3))
    c=''.join(str(mp[x]) for x in w);key=', '.join(f"{k} = {mp[k]}" for k in ls)
    ws=[''.join(str(mp[x]) for x in R.sample(ls,3)) for _ in range(12)]
    ws=[x for x in dict.fromkeys(ws) if x!=c][:3]
    add(S,f"In a code, {key}. What is the code for {w}?",c,ws,f"Replace each letter with its number: {' '.join(str(mp[x]) for x in w)}.")
B='Blood Relations'
names=["Ravi","Amit","Sunil","Mohan","Rakesh","Vikram","Pooja","Neha","Anita","Kiran","Seema","Rita"]
def br_mother_bro():
    add(B,"Pointing to a man, a woman said, 'He is the son of my mother's only son.' How is the man related to the woman?","Nephew",["Brother","Uncle","Cousin"],"Mother's only son is the woman's brother; his son is her nephew.")
def br_father_sister():
    add(B,"Pointing to a lady, a man said, 'She is the daughter of my father's only sister.' The lady is the man's:","Cousin",["Sister","Aunt","Niece"],"Father's sister is his paternal aunt; her daughter is his cousin.")
def br_chain():
    rel=[("father","Grandfather","my father's father"),("mother","Grandmother","my mother's mother"),("brother","Brother","my father's son"),]
    add(B,"A is the father of B. B is the sister of C. C is the son of D. How is D related to A?","Wife",["Sister","Mother","Daughter"],"B and C are A's children, so D, the mother of C, is A's wife.")
def br_gen():
    t=R.choice([("My father's father","Grandfather"),("My mother's father","Maternal grandfather"),("My brother's son","Nephew"),("My sister's daughter","Niece"),("My father's brother","Paternal uncle"),("My mother's brother","Maternal uncle"),("My wife's brother","Brother-in-law"),("My son's wife","Daughter-in-law"),("My daughter's husband","Son-in-law"),("My father's sister","Paternal aunt"),("My mother's sister","Maternal aunt"),("My husband's mother","Mother-in-law")])
    pool=["Grandfather","Maternal grandfather","Nephew","Niece","Paternal uncle","Maternal uncle","Brother-in-law","Daughter-in-law","Son-in-law","Paternal aunt","Maternal aunt","Mother-in-law","Cousin","Sister-in-law"]
    w=[p for p in pool if p!=t[1] and not (t[1]=='Maternal grandfather' and p=='Grandfather')];R.shuffle(w)
    add(B,f"Who is '{t[0]}' to the speaker?",t[1],w[:3],f"{t[0]} is the speaker's {t[1].lower()}.")
def br_count():
    n=R.randint(2,4);m=R.randint(1,3)
    add(B,f"A family has a father, a mother, {n} sons and {m} daughter(s). How many people are in the family?",2+n+m,near(2+n+m,(1,2,3)),f"2 parents + {n} sons + {m} daughter(s) = {2+n+m}.")
def br_nm():
    a,b=R.sample(names[:6],2);c,d=R.sample(names[6:],2)
    add(B,f"{a} is the brother of {c}. {c} is the daughter of {b}. How is {a} related to {b}?","Son",["Brother","Nephew","Father"],f"{a} is the brother of {b}'s daughter {c}, so {a} is {b}'s son.")
def br_in():
    a,c=R.sample(names[6:],2);b=R.choice(names[:6])
    add(B,f"{a} says, '{b} is my mother's brother's son.' How is {b} related to {a}?","Cousin",["Brother","Uncle","Nephew"],"Mother's brother is the maternal uncle; his son is a cousin.")
def br_dau():
    add(B,"If P is the sister of Q and Q is the father of R, how is P related to R?","Paternal aunt",["Mother","Grandmother","Cousin"],"P is the sister of R's father, so she is R's paternal aunt (bua).")
def br_gc():
    add(B,"A's mother is B. B's brother is C. C's daughter is D. How is D related to A?","Cousin",["Sister","Aunt","Niece"],"C is A's maternal uncle, so his daughter D is A's cousin.")
D='Direction Sense'
dirs=["North","East","South","West"];dvec={"North":(0,1),"East":(1,0),"South":(0,-1),"West":(-1,0)}
def dir_final():
    d=R.randrange(4);t=R.choice([("right",1),("left",-1)]);nd=dirs[(d+t[1])%4]
    add(D,f"A man faces {dirs[d]} and turns {t[0]} (90 degrees). He now faces:",nd,[x for x in dirs if x!=nd],f"Turning {t[0]} from {dirs[d]} makes him face {nd}.")
def dir_dist():
    a=R.choice([3,6,5,8,12,9,15,20]);b={3:4,6:8,5:12,8:6,12:5,9:12,15:8,20:15}[a];h=math.isqrt(a*a+b*b)
    if h*h!=a*a+b*b:return
    d1,d2=R.sample(["North","South"],1)[0],R.choice(["East","West"])
    add(D,f"A man walks {a} km {d1.lower()} and then {b} km {d2.lower()}. How far is he from the starting point (in km)?",h,near(h,(1,2,3)),f"Straight-line distance = sqrt({a}^2 + {b}^2) = {h} km.")
def dir_back():
    a=R.randint(3,9);b=R.randint(2,8)
    add(D,f"Rohit walks {a} km towards the east and then {b} km towards the west. How far is he from the starting point (in km)?",abs(a-b),[a+b,a,b] if abs(a-b) not in(a,b) else [a+b,a+1,b+2],f"East and west cancel out: |{a} - {b}| = {abs(a-b)} km.")

def dir_shadow():
    add(D,"One morning, after sunrise, Vikram stood facing a pole and his shadow fell to his right. Which direction was he facing?","North",["South","East","West"],"In the morning the sun is in the east, so the shadow falls west. The shadow is on his right, so his right is west, and he faces north.")
def dir_turn2():
    d=R.randrange(4);a=R.choice([1,-1]);b=R.choice([1,-1]);nd=dirs[(d+a+b)%4]
    ta="right" if a==1 else "left";tb="right" if b==1 else "left"
    add(D,f"A girl faces {dirs[d]}. She turns {ta}, then turns {tb}. Which direction does she face now?",nd,[x for x in dirs if x!=nd],f"{dirs[d]} -> {dirs[(d+a)%4]} -> {nd}.")
def dir_opp():
    d=R.randrange(4);nd=dirs[(d+2)%4]
    add(D,f"A man facing {dirs[d]} turns 180 degrees. He now faces:",nd,[x for x in dirs if x!=nd],f"A half turn reverses the direction, so {dirs[d]} becomes {nd}.")
RK='Ranking & Arrangement'
def rk_total():
    a=R.randint(3,20);b=R.randint(3,20);add(RK,f"In a row, Ajay is {a}th from the left and {b}th from the right. How many people are in the row?",a+b-1,near(a+b-1,(1,2)),f"Total = {a} + {b} - 1 = {a+b-1}.")
def rk_left():
    n=R.randint(20,45);a=R.randint(5,n-5);add(RK,f"In a row of {n} students, Sonu is {a}th from the left. What is his position from the right?",f"{n-a+1}th",[f"{n-a}th",f"{n-a+2}th",f"{n-a-1}th"],f"Position from right = {n} - {a} + 1 = {n-a+1}.")
def rk_between():
    n=R.randint(25,45);a=R.randint(4,10);b=R.randint(4,10);bt=n-a-b
    if bt<=0:return
    add(RK,f"In a class of {n}, Mohit is {a}th from the top and Sam is {b}th from the bottom. How many students are between them?",bt,near(bt,(1,2)),f"Between = {n} - ({a} + {b}) = {bt}.")
def rk_swap():
    a=R.randint(8,15);b=R.randint(5,10);s=R.randint(3,5)
    add(RK,f"A student ranks {a}th from the top in a class of {a+b}. What is his rank from the bottom?",f"{b+1}th",[f"{b}th",f"{b+2}th",f"{a}th"],f"Rank from bottom = {a+b} - {a} + 1 = {b+1}.")
def rk_tallest():
    n=R.sample(["Ram","Shyam","Mohan","Sohan","Gopal"],5)
    # a>b>c>d>e height order given in shuffled statements
    add(RK,f"{n[0]} is taller than {n[1]}. {n[1]} is taller than {n[2]}. {n[2]} is taller than {n[3]}. {n[3]} is taller than {n[4]}. Who is the shortest?",n[4],[n[0],n[1],n[2]],f"The order is {' > '.join(n)}, so {n[4]} is the shortest.")
def rk_mid():
    n=R.sample(["Ram","Shyam","Mohan","Sohan","Gopal"],5)
    add(RK,f"{n[0]} is taller than {n[1]}. {n[1]} is taller than {n[2]}. {n[2]} is taller than {n[3]}. {n[3]} is taller than {n[4]}. Who is in the middle when they are arranged by height?",n[2],[n[0],n[1],n[3]],f"Order {' > '.join(n)}: the third is {n[2]}.")
def rk_days():
    ds=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];i=R.randrange(7);k=R.randint(2,6);v=ds[(i+k)%7]
    add(RK,f"If today is {ds[i]}, what day of the week will it be after {k} days?",v,[x for x in ds if x!=v][:3],f"{ds[i]} plus {k} day(s) is {v}.")
def rk_days2():
    ds=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];i=R.randrange(7);k=R.choice([10,17,24,30,45,52]);v=ds[(i+k)%7]
    add(RK,f"If today is {ds[i]}, what day will it be after {k} days?",v,[x for x in ds if x!=v][:3],f"{k} days = {k//7} weeks and {k%7} day(s); {ds[i]} + {k%7} = {v}.")
def rk_clock():
    h=R.choice([3,6,9,12,1,2,4,5,7,8,10,11]);ang=abs(30*h)%360;ang=min(ang,360-ang)
    add(RK,f"What is the angle between the hour hand and the minute hand of a clock at {h}:00?",f"{ang} degrees",[f"{ang+30} degrees",f"{abs(ang-30)} degrees",f"{ang+60} degrees"],f"Each hour mark is 30 degrees, so at {h}:00 the angle is {ang} degrees.")
def rk_cal():
    y=R.choice([2024,2028,2032,1996,2000]);add(RK,f"How many days are there in February of the year {y}?","29",["28","30","31"],f"{y} is a leap year, so February has 29 days.")
def rk_cal2():
    y=R.choice([2025,2026,2027,2023,2022,1999]);add(RK,f"How many days are there in February of the year {y}?","28",["29","30","27"],f"{y} is not a leap year, so February has 28 days.")

Y='Syllogism & Logic'
def sy_all():
    a,b,c=R.choice([("cats","animals","dogs"),("pens","tools","books"),("roses","flowers","stones"),("teachers","graduates","farmers"),("apples","fruits","metals")])
    add(Y,f"Statements: All {a} are {b}. Some {b} are {c}. Conclusion: Some {c} are {a}. Is the conclusion valid?","Does not follow",["Definitely follows","Follows only in some cases","Cannot say anything about the statements"],"Both groups lie inside the larger group but need not overlap with each other, so the conclusion does not follow.")
def sy_all2():
    a,b,c=R.choice([("pens","pencils","erasers"),("boys","players","artists"),("trains","vehicles","machines"),("doctors","graduates","citizens")])
    add(Y,f"Statements: All {a} are {b}. All {b} are {c}. Conclusion: All {a} are {c}. The conclusion:","Definitely follows",["Does not follow","Is false","Is ambiguous"],f"A chain of 'all': {a} are inside {b}, which are inside {c}, so all {a} are {c}.")
def sy_some():
    a,b=R.choice([("books","pens"),("birds","kites"),("fruits","apples"),("cars","vehicles")])
    add(Y,f"Statement: Some {a} are {b}. Conclusion: Some {b} are {a}. The conclusion:","Definitely follows",["Does not follow","Is false","Cannot be determined from the statement"],"'Some A are B' always implies 'Some B are A'.")
def sy_no():
    a,b=R.choice([("pens","stones"),("birds","tables"),("fruits","metals"),("chairs","rivers")])
    add(Y,f"Statement: No {a} is a {b}. Conclusion: No {b} is a {a}. The conclusion:","Definitely follows",["Does not follow","Is false","Is partly true"],"'No A is B' is symmetric, so 'No B is A' follows.")
def sy_not():
    a,b=R.choice([("men","teachers"),("women","artists"),("dogs","animals")])
    add(Y,f"Statement: All {a} are {b}. Conclusion: All {b} are {a}. The conclusion:","Does not follow",["Definitely follows","Is true for all cases","Is the same as the statement"],f"'All {a} are {b}' does not mean every {b[:-1]} is among the {a}.")

def sy_odd_one():
    G=[("Dog","Cat","Lion","Eagle","Eagle is a bird; the rest are mammals."),("Rose","Lotus","Jasmine","Mango","Mango is a fruit; the rest are flowers."),("Delhi","Mumbai","Kolkata","Ganga","Ganga is a river; the rest are cities."),("Square","Triangle","Circle","Cube","Cube is three-dimensional; the rest are flat shapes."),("Red","Blue","Green","Table","Table is not a colour."),("Pen","Pencil","Chalk","Chair","Chair is not a writing tool."),("Tiger","Leopard","Wolf","Cow","Cow is a domestic animal; the rest are wild."),("Sitar","Guitar","Violin","Drum","Drum is a percussion instrument; the rest are string instruments."),("Bus","Train","Ship","Road","Road is a path, not a vehicle."),("January","March","May","June","June has 30 days; the rest have 31.")]
    g=R.choice(G);o=list(g[:4]);R.shuffle(o)
    add(Y,f"Find the odd one out: {', '.join(o)}",g[3],[x for x in o if x!=g[3]],g[4])
def sy_count_tri():
    n=R.randint(2,5);v=n*(n+1)//2
    add(Y,f"A triangle is divided by {n-1} lines drawn from the top vertex to the base, cutting the base into {n} parts. How many triangles are there in total?",v,near(v,(1,2,3)),f"Triangles = {n}(n+1)/2 with n = {n}, i.e. {v}.")
def sy_sq():
    n=R.randint(2,5);v=sum(i*i for i in range(1,n+1))
    add(Y,f"How many squares of all sizes are there in a {n} x {n} grid of squares?",v,near(v,(1,2,3,4)),f"Sum of squares 1^2 + ... + {n}^2 = {v}.")
def sy_hand():
    n=R.randint(4,10);v=n*(n-1)//2
    add(Y,f"{n} friends meet and each shakes hands with every other friend once. How many handshakes are there?",v,near(v,(1,2,3,4)),f"{n} x {n-1}/2 = {v}.")
AN='Analogy & Classification'
def an_num():
    a=R.randint(2,9);k=R.choice(['sq','cu','dbl'])
    if k=='sq':f=lambda x:x*x;n="square"
    elif k=='cu':f=lambda x:x**3;n="cube"
    else:f=lambda x:x*2;n="double"
    b=R.choice([x for x in range(2,10) if x!=a]);v=f(b)
    add(AN,f"{a} : {f(a)} :: {b} : ?",v,near(v,(1,2,3,4)) if k!='cu' else [v+b,v-b,v+9],f"The second number is the {n} of the first, so {b} gives {v}.")
def an_pair():
    P=[("Doctor","Hospital","Teacher","School"),("Pilot","Aeroplane","Driver","Bus"),("Author","Book","Painter","Picture"),("Chef","Kitchen","Student","Classroom"),("Bird","Nest","Lion","Den"),("Cow","Calf","Dog","Puppy"),("Eye","See","Ear","Hear"),("Knife","Cut","Pen","Write"),("Hot","Cold","Day","Night"),("Fish","Water","Bird","Air"),("Judge","Court","Farmer","Field"),("Hand","Glove","Foot","Sock")]
    p=R.choice(P);pool=["Library","Pencil","Shop","Road","Tree","Ocean","Garden","Office"]
    w=[x for x in pool if x!=p[3]];R.shuffle(w)
    add(AN,f"{p[0]} : {p[1]} :: {p[2]} : ?",p[3],w[:3],f"{p[0]} goes with {p[1]} in the same way that {p[2]} goes with {p[3]}.")
def an_letters():
    s=R.randint(0,6);d=R.randint(1,3);a=A[s]+A[s+d];s2=R.randint(10,18);b=A[s2]+A[s2+d]
    wr=[A[s2+d]+A[s2],A[s2+1]+A[s2+d+1],A[s2]+A[s2+d+1]]
    add(AN,f"{a} : {A[s+1]}{A[s+d+1]} :: {A[s2]}{A[s2+d]} : ?",A[s2+1]+A[s2+d+1],[A[s2+d]+A[s2],A[s2+2]+A[s2+d+2],A[s2]+A[s2+d+1]],f"Each letter moves one step ahead, so {A[s2]}{A[s2+d]} becomes {A[s2+1]}{A[s2+d+1]}.")
def an_odd_num():
    k=R.choice([('even',[2,4,6,8,10,12],[3,5,7,9,11,13,15,21,25,27],"odd")])
    ev=R.sample(k[1],3);od=R.choice(k[2]);o=ev+[od];R.shuffle(o)
    add(AN,f"Find the odd number out: {', '.join(map(str,o))}",od,[x for x in o if x!=od],f"{od} is odd; the others are even.")
def an_odd_sq():
    n=R.sample([4,9,16,25,36,49,64,81],3);b=R.choice([x for x in range(10,90) if math.isqrt(x)**2!=x]);o=n+[b];R.shuffle(o)
    add(AN,f"Which number does not belong to the group: {', '.join(map(str,o))}",b,[x for x in o if x!=b],f"{b} is not a perfect square; the others are.")
def an_odd_prime():
    p=R.sample([3,5,7,11,13,17,19,23],3);c=R.choice([9,15,21,25,27,33,35,39,45]);o=p+[c];R.shuffle(o)
    add(AN,f"Find the odd one out: {', '.join(map(str,o))}",c,[x for x in o if x!=c],f"{c} is composite; the others are prime.")
def an_mult():
    m=R.choice([3,4,5,6,7,8,9]);ms=R.sample([m*i for i in range(2,13)],3);x=R.choice([y for y in range(10,90) if y%m!=0]);o=ms+[x];R.shuffle(o)
    add(AN,f"Find the odd one out: {', '.join(map(str,o))}",x,[y for y in o if y!=x],f"Three numbers are multiples of {m}; {x} is not.")
def an_vowel():
    s=R.choice(["BANK","TRAIN","EXAM","PAPER","STUDY","LEARN"]);c=sum(ch in "AEIOU" for ch in s)
    add(AN,f"How many vowels are there in the word {s}?",c,near(c,(1,2,3)) if c<3 else [c-1,c+1,c-2],f"Vowels in {s}: {', '.join(ch for ch in s if ch in 'AEIOU')} ({c}).")

FNS=[ser_ap,ser_gp,ser_sq,ser_cube,ser_incr,ser_alt,ser_prime,ser_letter,ser_odd,code_shift,code_decode,code_rev,code_sum,code_pos,code_num,br_mother_bro,br_father_sister,br_chain,br_gen,br_count,br_nm,br_in,br_dau,br_gc,dir_final,dir_dist,dir_back,dir_shadow,dir_turn2,dir_opp,rk_total,rk_left,rk_between,rk_swap,rk_tallest,rk_mid,rk_days,rk_days2,rk_clock,rk_cal,rk_cal2,sy_all,sy_all2,sy_some,sy_no,sy_not,sy_odd_one,sy_count_tri,sy_sq,sy_hand,an_num,an_pair,an_letters,an_odd_num,an_odd_sq,an_odd_prime,an_mult,an_vowel]
def run(seed,n):
    global R,out
    R=random.Random(seed);out=[]
    order=FNS[:];R.shuffle(order)
    tries=0
    while len(out)<n and tries<n*40:
        fn=order[tries%len(order)];tries+=1
        try:fn()
        except Exception:pass
    return out[:n]
