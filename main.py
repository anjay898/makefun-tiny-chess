import json as j,urllib.request as u,os
WV=(0,100,320,330,500,1000,0)
PS=b'GGGGyyyyQQ[eLLQ`GGG[LB=GLQQ3GGGG  )) 3GG)GQV)LV[)GV[)LQV 3GL  ))3====GGG=GLQ=LLQ=GQQ=QQQ=LGG3===GGGGLQQQBGGGBGGGBGGGBGGGBGGGGGGL3==B=GGG=GLLBGLLGGLL=LLL=GLG3==B)   )   )   )   3)) =333[[GG[eQG'
KN=(33,31,18,14,-14,-18,-31,-33);DR=(16,-16,1,-1,17,15,-17,-15)
CLR={4:3,0:2,7:1,116:12,112:8,119:4}
PD={2:KN,3:DR[4:],4:DR[:4],5:DR,6:DR}
CST=((4,1,(5,6),(4,5,6),6),(4,2,(1,2,3),(2,3,4),2),(116,4,(117,118),(116,117,118),118),(116,8,(113,114,115),(114,115,116),114))
Stop=Exception
def PV(x,q):a=abs(x);s=2*(x>0)-1;return (WV[a]+PS[(a-1)*32+(q>>4 if s>0 else 7-(q>>4))*4+min(q&7,7-(q&7))]-71)*s
def PR(i,j):return[i|j<<7|t<<14 for t in(5,4,3,2)]
def ATK(q,by):
 for d in(15,17):
  x=q-d*by
  if not x&136 and B[x]==by:return 1
 for d in KN:
  x=q+d
  if not x&136 and B[x]==2*by:return 1
 for n,d in enumerate(DR):
  x=q
  for t in range(7):
   x+=d
   if x&136:break
   v=B[x]
   if v*by>0 and(abs(v)==(4 if n<4 else 3)or abs(v)==5 or t==0 and abs(v)==6):return 1
   if v:break
 return 0
def GEN(cap):
 ms=[]
 for i in range(128):
  if i&136:continue
  v=B[i]
  if v*S<=0:continue
  a=abs(v)
  if a==1:
   j=i+16*S
   if not B[j]:
    if j>>4 in(0,7):ms+=PR(i,j)
    elif not cap:
     ms.append(i|j<<7)
     if i>>4==1+5*(S<0)and not B[j+16*S]:ms.append(i|(j+16*S)<<7)
   for d in(15,17):
    j=i+d*S
    if j&136:continue
    if B[j]*S<0 or j==E:
     if j>>4 in(0,7):ms+=PR(i,j)
     else:ms.append(i|j<<7)
  else:
   for d in PD[a]:
    j=i
    for t in range(7):
     j+=d
     if j&136:break
     if B[j]*S>0:break
     if B[j]or not cap:ms.append(i|j<<7)
     if B[j]or a in(2,6):break
 if not cap:
  for kf,bit,emp,safe,kt in CST:
   if B[kf]==6*S and C&bit and not any(B[x]for x in emp)and not any(ATK(x,-S)for x in safe):ms.append(kf|kt<<7)
 return ms
def MK(m):
 global S,C,E,EV
 i=m&127;j=(m>>7)&127;t=m>>14;v=B[i];cap=B[j];ep=0
 if abs(v)==1 and j==E:ep=B[j-16*S]
 UND.append((cap,C,E,ep,EV));EV-=PV(v,i)
 if cap:EV-=PV(cap,j)
 if ep:EV-=PV(ep,j-16*S);B[j-16*S]=0
 B[i]=0;B[j]=t*S if t else v;EV+=PV(B[j],j)
 if abs(v)==6 and abs(j-i)==2:
  rf=i+(3 if j>i else-4);rp=B[rf];EV+=PV(rp,(i+j)//2)-PV(rp,rf);B[(i+j)//2]=rp;B[rf]=0
 for z in(i,j):C&=~CLR.get(z,0)
 E=(i+j)//2 if abs(v)==1 and abs(j-i)==32 else-1
 S=-S
def UM(m):
 global S,C,E,EV
 S=-S;i=m&127;j=(m>>7)&127;cap,C,E,ep,EV=UND.pop();v=B[j]
 B[i]=v//abs(v)if m>>14 else v
 B[j]=cap
 if abs(v)==6 and abs(j-i)==2:
  rf=i+(3 if j>i else-4);B[rf]=B[(i+j)//2];B[(i+j)//2]=0
 if ep:B[j-16*S]=ep
def ORD(ms):return sorted(ms,key=lambda m:-WV[abs(B[m>>7&127])])
def Q(d,a,b,ply):
 global N
 N+=1
 if N>NCAP:raise Stop
 chk=ATK(B.index(6*S),-S)
 q=d<=0;best=-30000
 if q and not chk:
  best=S*EV
  if best>=b:return best
  a=max(a,best)
 for m in ORD(GEN(q and not chk)):
  MK(m)
  if ATK(B.index(-6*S),S):UM(m);continue
  v=-Q(d-1,-b,-a,ply+1);UM(m)
  best=max(best,v);a=max(a,v)
  if a>=b:break
 if best==-30000:return-29000+ply if chk else 0
 return best
def U(m):i=m&127;j=(m>>7)&127;return chr(97+(i&7))+str(1+(i>>4))+chr(97+(j&7))+str(1+(j>>4))+('  nbrq'[m>>14]if m>>14 else'')
def SETUP(fen):
 global B,S,C,E,EV
 ps,side,w,ep,*_=fen.split();B=[0]*128;EV=0;q=112
 for x in ps:
  if x=='/':q-=24
  elif x.isdigit():q+=int(x)
  else:
   p=(2*x.isupper()-1)*' PNBRQK'.index(x.upper());B[q]=p;EV+=PV(p,q);q+=1
 S=1-2*(side=='b')
 C=('K'in w)+2*('Q'in w)+4*('k'in w)+8*('q'in w)
 E=-1 if ep=='-'else ord(ep[0])-97+16*int(ep[1])-16
def POST(y,o):
 with u.urlopen(u.Request(os.environ['MAKEFUN_ENV_URL']+y,j.dumps(o).encode(),{'Content-Type':'application/json'}))as r:return j.load(r)
UND=[];N=0;NCAP=8e4
while True:
 g=POST('/game',{})
 while g['status']=='your_move':
  SETUP(g['fen']);N=0;best=None
  legal=GEN(0)
  try:
   for d in range(80):
    bb=None;bv=al=-30000
    for m in ORD(legal):
     MK(m)
     if ATK(B.index(-6*S),S):UM(m);continue
     v=-Q(d-1,-30000,-al,1);UM(m)
     if v>bv:bv,bb=v,m;al=max(al,v)
    if bb:best=bb
  except Stop:pass
  best=best or legal[0]
  g=POST('/move',{'game':g['game'],'move':U(best)})
 if g['status']=='done':break