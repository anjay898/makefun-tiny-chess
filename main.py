import json as j,urllib.request as u,os
B=[0]*256;S=1;C=0;E=-1;EV=0;K2=[0,0]
PS=b'GGGGyyyyQQ[eLLQ`GGG[LB=GLQQ3GGGG  )) 3GG)GQV)LV[)GV[)LQV 3GL  ))3====GGG=GLQ=LLQ=GQQ=QQQ=LGG3===GGGGLQQQBGGGBGGGBGGGBGGGBGGGGGGL3==B=GGG=GLLBGLLGGLL=LLL=GLG3==B)   )   )   )   3)) =333[[GG[eQG'
DR=(16,-16,1,-1,17,-17,15,-15);KN=(33,31,18,14,-14,-18,-31,-33)
PD=((),(),KN,DR[4:],DR[:4],DR,DR)
VL=(0,100,320,330,500,900,0);CL={0:13,4:12,7:14,112:7,116:3,119:11}
TT={};D=[];N=0
def PV(x,q):return((x>0)*2-1)*(VL[abs(x)]+PS[(abs(x)-1)*32+((q>>4)^(7*(x>0)))*4+((q&7)^(7*(q>>2&1)))]-71)
def A(q,by):
 if by in(B[q-15*by],B[q-17*by]):return 1
 for d in KN:
  if B[q+d]==2*by:return 1
 for t,ds in((4,DR[:4]),(3,DR[4:])):
  for d in ds:
   x=q+d
   while not(x&136 or B[x]):x+=d
   if B[x]*by in(t,5)or(B[x]==6*by and x==q+d):return 1
 return 0
def PR(i,j):return[i|j<<7|t<<14 for t in(5,4,3,2)]
def GEN(cap):
 ms=[]
 for i,v in enumerate(B):
  if v*S<=0:continue
  a=abs(v)
  if a==1:
   if not B[j:=i+16*S]:
    if j>>4 in(0,7):ms+=PR(i,j)
    elif not cap:
     ms.append(i|j<<7)
     if i>>4==1+5*(S<0)and not B[k:=j+16*S]:ms.append(i|k<<7)
   for d in(15,17):
    if not(j:=i+d*S)&136 and(B[j]*S<0 or j==E):
     if j>>4 in(0,7):ms+=PR(i,j)
     else:ms.append(i|j<<7)
  else:
   o=112*(S<0)
   if a==6 and i==4+o:
    for sd,bt,em,pth in((2,0,(5,6),(4,5,6)),(-2,1,(1,2,3),(4,3,2))):
     if C>>(bt+o//56)&1 and not any(B[x+o]for x in em)and not any(A(x+o,-S)for x in pth):ms.append(i|(i+sd)<<7)
   for d in PD[a]:
    j=i+d
    while not j&136 and B[j]*S<=0:
     if B[j]or not cap:ms.append(i|j<<7)
     if B[j]or a%4==2:break
     j+=d
 return ms
def MK(m):
 global S,C,E,EV
 i=m&127;j=m>>7&127;p=m>>14;v=B[j]
 D.append((m,v,E,C,EV))
 if v:EV-=PV(v,j)
 if abs(B[i])==1 and j==E:B[j-16*S]=0;EV-=PV(-S,j-16*S)
 w=B[i];EV-=PV(w,i);B[i]=0
 if p:w=p*S
 B[j]=w;k6=abs(w)==6
 if k6 and abs(j-i)==2:
  rf=i+(3 if j>i else-4);rt=(i+j)//2;EV+=PV(B[rf],rt)-PV(B[rf],rf);B[rt]=B[rf];B[rf]=0
 EV+=PV(w,j)
 if k6:K2[S>0]=j
 C&=CL.get(i,15)&CL.get(j,15)
 E=j-16*S if abs(w)==1 and abs(j-i)==32 else-1;S=-S
def UM():
 global S,C,E,EV
 S=-S;mm,v,E,C,EV=D.pop()
 i=mm&127;j=mm>>7&127;p=mm>>14
 if abs(B[j])==6 and abs(j-i)==2:
  rf=i+(3 if j>i else-4);rt=(i+j)//2;B[rf]=B[rt];B[rt]=0
 B[i]=S if p else B[j]
 if abs(B[i])==6:K2[S>0]=i
 B[j]=v
 if not v and abs(B[i])==1 and j==E:B[j-16*S]=-S
def O(ms,tm):
 def k(m):v=B[m>>7&127];return(m==tm,1 if v or m>>14 else 0,VL[abs(v)])
 return sorted(ms,key=k,reverse=True)
def R(d,a,b):
 global N;N+=1
 if N>65e3:1/0
 kk=(tuple(B),S)
 ch=A(K2[S>0],-S);best=-30000;cnt=0;w=0
 if d<=0 and not ch:
  best=S*EV
  if best>=b:return best
  a=max(a,best)
 tm=0
 if d>0 and(tt:=TT.get(kk)):
  tm=tt[3]
  if tt[0]>=d and((tt[1]==1 and tt[2]>=b)or(tt[1]==2 and tt[2]<=a)):return tt[2]
 for m in O(GEN(1 if d<=0 and not ch else 0),tm):
  MK(m)
  if A(K2[S<0],S):UM();continue
  cnt+=1
  v=-R(d-1,-b,-a)
  UM()
  a=max(a,v)
  if v>best:best,w=v,m
  if a>=b:break
 if not cnt:return-29000 if ch else(0 if d>0 else best)
 if d>0:TT[kk]=(d,1 if best>=b else 2,best,w)
 return best
def T(fen):
 global B,S,C,E,EV
 B=[0]*256;EV=0
 f=fen.split();q=112
 for x in f[0]:
  if x=='/':q=(q//16-1)*16
  elif x.isdigit():q+=int(x)
  else:
   p=(2*x.isupper()-1)*' PNBRQK'.index(x.upper());B[q]=p;EV+=PV(p,q);q+=1
   if abs(p)==6:K2[p>0]=q-1
 S=1-2*(f[1]=='b');C=sum(1<<i for i,x in enumerate('KQkq')if x in f[2])
 E=-1 if f[3]=='-'else(int(f[3][1])-1)*16+ord(f[3][0])-97
def U(m):i=m&127;j=m>>7&127;return chr(97+i%16)+str(i//16+1)+chr(97+j%16)+str(j//16+1)+('nbrq'[(m>>14)-2]if m>>14 else'')
def P(y,o):
 return j.loads(u.urlopen(os.environ['MAKEFUN_ENV_URL']+'/'+y,data=j.dumps(o).encode()).read())
def F():
 global N;T(G['fen'])
 ms=[m for m in GEN(0)if not(MK(m),A(K2[S<0],S),UM())[1]]
 N=0;bm=ms[0]
 try:
  for d in range(12):
   bb=bm;sc=-30000
   ms.remove(bb);ms.insert(0,bb)
   for m in ms:
    MK(m);v=-R(d-1,-30000,30000);UM()
    if v>sc:sc,bb=v,m;bm=bb
 except:pass
 return bm
while 1:
 g=P('game',{})
 if g['status']!='your_move':break
 G=g
 P('move',{'game':g['game'],'move':U(F())})
