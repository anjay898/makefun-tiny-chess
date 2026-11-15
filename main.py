import json as j,urllib.request as u;from os import environ
W=(0,100,320,330,500,900,0)
D=(16,-16,1,-1,17,15,-17,-15)
J=(33,31,18,14,-14,-18,-31,-33)
Q=(5,4,3,2)
def A(b,k,s):
 for d in (-1,1):
  j=k-16*s+d
  if not j&136 and b[j]==s:return True
 for d in J:
  j=k+d
  if not j&136 and b[j]==2*s:return True
 for n,d in enumerate(D):
  j=k+d;t=1
  while not j&136:
   v=b[j]
   if v:
    if v*s>0 and (abs(v)==5 or abs(v)==(4 if n<4 else 3) or t==1 and abs(v)==6):return True
    break
   j+=d;t+=1
 return False
def G(p,q):
 b,s,c,e,h=p;m=[]
 for i,v in enumerate(b):
  if v*s<=0:continue
  v=abs(v)
  if v==1:
   j=i+16*s
   if not j&136 and not b[j]:
    if j>>4 in (0,7):m.extend((i,j,t) for t in Q)
    elif not q:
     m.append((i,j,0))
     if i>>4==(1 if s==1 else 6) and not b[j+16*s]:m.append((i,j+16*s,0))
   for d in (15,17):
    j=i+d*s
    if not j&136 and (b[j]*s<0 or j==e):
     m.extend((i,j,t) for t in (Q if j>>4 in (0,7) else (0,)))
  else:
   for d in J if v==2 else D[:4] if v==4 else D[4:] if v==3 else D:
    j=i+d
    while not j&136:
     if b[j]*s>0:break
     if b[j] or not q:m.append((i,j,0))
     if b[j] or v in (2,6):break
     j+=d
   if v==6 and not q and i==(4 if s==1 else 116) and not A(b,i,-s):
    for t in (1,-1):
     r=i+(3 if t==1 else -4)
     if c&((1 if s==1 else 4)*(1 if t==1 else 2)) and b[r]==4*s and not b[i+t] and not b[i+2*t] and (t==1 or not b[i-3]) and not A(b,i+t,-s):m.append((i,i+2*t,0))
 return m
def M(p,m):
 b,s,c,e,h=p;b=b[:];i,j,t=m;v=b[i];x=b[j]
 b[i]=0;b[j]=s*t if t else v
 if abs(v)==1 and j==e and not x:b[j-16*s]=0
 if abs(v)==6:
  c&=12 if s==1 else 3
  if abs(j-i)==2:
   r=i+(3 if j>i else -4);b[r]=0;b[(i+j)//2]=4*s
 for k in (i,j):c&=~{0:2,7:1,112:8,119:4}.get(k,0)
 return b,-s,c,(i+j)//2 if abs(v)==1 and abs(i-j)==32 else -1,0 if abs(v)==1 or x else h+1
def E(p):
 b,s,c,e,h=p;v=0;B=[0,0]
 for i,x in enumerate(b):
  if x:
   a=abs(x);r=i>>4;r=r if x>0 else 7-r
   z=7-abs(2*(i&7)-7)-abs(2*r-7)
   v+=(1 if x>0 else -1)*(W[a]+(r*6+z*2 if a==1 else z*(0,0,5,3,1,1,-4)[a]))
   if a==3:B[x>0]+=1
 return s*(v+25*((B[1]>1)-(B[0]>1)))
def K(p):return (tuple(p[0]),)+p[1:4]
def U(m):
 i,j,t=m
 return chr(97+(i&7))+str(1+(i>>4))+chr(97+(j&7))+str(1+(j>>4))+(' nbrq'[t] if t else '')
class Stop(Exception):pass
def S(p,d,a,z,l):
 global N
 N+=1
 if N>20000:raise Stop
 b,s,c,e,h=p;k=b.index(6*s);ck=A(b,k,-s);key=K(p)
 if l and (key in H or key in V):return 0,None
 if h>=100 and not ck:return 0,None
 if d<-7:return E(p),None
 q=d<=0 and not ck;best=-30000;bm=None;n=0
 if q:
  best=E(p)
  if best>=z:return best,None
  a=max(a,best)
 moves=G(p,q)
 if not l:moves=[m for m in moves if U(m) in L]
 moves.sort(key=lambda m:100000*(not l and m==T)+10*W[abs(b[m[1]])]+W[m[2]]-W[abs(b[m[0]])]+100*(abs(b[m[0]])==1 and m[1]==e),reverse=True)
 V.add(key)
 try:
  for m in moves:
   p1=M(p,m)
   if A(p1[0],m[1] if b[m[0]]==6*s else k,-s):continue
   n+=1
   v=-S(p1,d-1,-z,-a,l+1)[0]
   if v>best:best=v;bm=m
   a=max(a,v)
   if a>=z:break
 finally:V.remove(key)
 if not n and not q:return (-29000+l if ck else 0),None
 return best,bm
def P(y,o):
 with u.urlopen(u.Request(environ['MAKEFUN_ENV_URL']+y,data=j.dumps(o).encode(),headers={'Content-Type':'application/json'}))as r:return j.load(r)
game=None;H=set()
while True:
 g=P('/game',{})
 while g['status']=='your_move':
  if game!=g['game']:game=g['game'];H=set()
  rows,side,w,ep,hf,_=g['fen'].split()
  b=[0]*128
  for r,row in enumerate(rows.split('/')[::-1]):
   f=0
   for x in row:
    if x.isdigit():f+=int(x)
    else:b[r*16+f]=' PNBRQK'.index(x.upper())*(1 if x.isupper() else -1);f+=1
  p=b,1 if side=='w' else -1,sum(1<<i for i,x in enumerate('KQkq') if x in w),-1 if ep=='-' else ord(ep[0])-97+16*(int(ep[1])-1),int(hf)
  H.add(K(p));L=g['legal_moves'];move=L[0];T=None;N=0;V=set()
  try:
   for d in range(1,40):
    z,m=S(p,d,-30000,30000,0)
    if m is not None:T=m;move=U(m)
    if abs(z)>28000:break
  except Stop:pass
  if T is not None:H.add(K(M(p,T)))
  g=P('/move',{'game':game,'move':move if move in L else L[0]})
 if g['status']=='done':break
