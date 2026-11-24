import json,os,sys,time,urllib.request as U
E=os.environ["MAKEFUN_ENV_URL"]
def P(p,b):
    return json.load(U.urlopen(U.Request(E+p,json.dumps(b).encode(),{"content-type":"application/json"})))
V=dict(zip("PNBRQK",(100,320,330,500,900,20000)))
D={'P':(-10,-20,-11,-9),'N':(-21,-19,-12,-8,8,12,19,21),'B':(-11,-9,9,11),'R':(-10,-1,1,10)}
D['Q']=D['K']=D['B']+D['R']
T={}
for p in V:
    t=[0]*120
    for i in range(21,99):
        c=i%10-1;k=9-i//10
        if 0<=c<8 and 0<=k<8:
            d=min(c,7-c);e=min(k,7-k)
            t[i]=V[p]+{'P':7*k+8*d*(k<5),'N':12*(d+e),'B':6*(d+e),'R':3*d+20*(k==6),'Q':3*(d+e),'K':-15*k+10*(c in(1,2,6))*(k==0)}[p]
    T[p]=t
class X(Exception):pass
def G(b):
    for i,p in enumerate(b):
        if p.isupper():
            for d in D[p]:
                j=i
                while 1:
                    j+=d;q=b[j]
                    if q==' 'or q.isupper():break
                    if p=='P':
                        if d in(-10,-20):
                            if q!='.'or(d==-20 and(i<81 or b[i-10]!='.')):break
                        elif q=='.':break
                    v=T[p][j]-T[p][i]
                    if q.islower():v+=T[q.upper()][119-j]
                    if p=='P'and j<30:v+=T['Q'][j]-T['P'][j]
                    yield v,i,j
                    if p in'PNK'or q!='.':break
def M(b,i,j):
    p=b[i]
    if p=='P'and j<30:p='Q'
    b=b[:i]+'.'+b[i+1:]
    return(b[:j]+p+b[j+1:]).swapcase()[::-1]
def S(b,s,d,a,e):
    global N;N+=1
    if N>L or N&511==0 and time.monotonic()-t0>6:raise X
    if s<-9000:return s-max(d,0)
    if b in Q:return 0
    r=s if d<1 else-30000
    if r>=e:return r
    a=max(a,r)
    for v,i,j in sorted(G(b),reverse=1):
        if d<1 and b[j]=='.'and v<300:continue
        t=-S(M(b,i,j),-(s+v),d-1,-e,-a)
        if t>r:
            r=t
            if r>a:
                a=r
                if r>=e:break
    return r
def sq(i):return"abcdefgh"[i%10-1]+str(10-i//10)
def ix(u,w):
    i=(10-int(u[1]))*10+"abcdefgh".index(u[0])+1
    return i if w else 119-i
Q=set();gn=0
def best(fen,legal,g):
    global N,t0,L,Q,gn
    N=0;L=150000;t0=time.monotonic()
    if g!=gn:Q=set();gn=g
    f=fen.split();w=f[1]=='w'
    b=' '*20
    for r in f[0].split('/'):
        b+=' '+''.join('.'*int(c) if c.isdigit() else c for c in r)+' '
    b+=' '*20
    if not w:b=b.swapcase()[::-1]
    ms=[]
    for v,i,j in G(b):
        u=sq(i if w else 119-i)+sq(j if w else 119-j)
        if b[i]=='P'and j<30:u+='q'
        if u in legal:ms.append((v,u,M(b,i,j)))
    for u in("e1g1","e1c1","e8g8","e8c8"):
        if u in legal and b[ix(u[:2],w)]=='K':
            i=ix(u[:2],w);j=ix(u[2:],w);r0=ix(("h"if u[2]=="g"else"a")+u[1],w);r1=ix(("f"if u[2]=="g"else"d")+u[1],w)
            c=list(b);c[i]=c[r0]='.';c[j]='K';c[r1]='R'
            ms.append((T['K'][j]-T['K'][i]+T['R'][r1]-T['R'][r0],u,''.join(c).swapcase()[::-1]))
    out=ms[0][1] if ms else legal[0]
    Q.add(b)
    try:
        for d in range(1,40):
            a=-30000;sc=[]
            for v,u,c in ms:
                t=-S(c,-v,d-1,-30000,-a)
                sc.append((t,v,u,c));a=max(a,t)
            sc.sort(key=lambda x:-x[0])
            ms=[x[1:] for x in sc];out=ms[0][1]
            if sc[0][0]>9000:break
    except X:pass
    return out
while 1:
    g=P("/game",{})
    if g["status"]=="done":break
    while g["status"]=="your_move":
        g=P("/move",{"game":g["game"],"move":best(g["fen"],g["legal_moves"],g["game"])})
