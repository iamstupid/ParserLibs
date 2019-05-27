import sys
def parseCh(c):
	if len(c)==1:
		return ord(c)
	assert(c[0]=='%')
	return int(c[1:])
identf=lambda x:x
ifname=sys.argv[1]
ofname=sys.argv[2]
fo=open(ifname,"r")
lines=[t.strip('\n').split(' ') for t in fo]
csname={}
rsname={}
charattr=[0 for i in range(128)]
for i in lines:
	if i[0]=='charset' or i[0]=='cst':
		name=i[1]
		attrp=0
		if not(i[1] in csname):
			csname[i[1]]=[]
			attrp=len(rsname)
			rsname[i[1]]=len(rsname)
		else:
			attrp=rsname[i[1]]
		zu=csname[i[1]]
		attrp=1<<attrp
		for q in i[2:]:
			if q[0]=='[' and q[-1:]==']':
				a,b=q[1:-1].split('-')
				a,b=parseCh(a),parseCh(b)
				for u in range(a,b+1):
					charattr[u]=charattr[u]|attrp
					zu.append(u)
			else:
				z=list(map(ord,q))
				for u in z:
					charattr[u]=charattr[u]|attrp
					zu.append(u)
ezmap={}
for i in charattr:
	if not(i in ezmap):
		ezmap[i]=len(ezmap)
ezarr=[ezmap[i] for i in charattr]
for i in csname:
	t=csname[i]
	csname[i]=set()
	for j in t:
		csname[i].add(ezarr[j])

# print(csname)
# print([(chr(i),ezarr[i]) for i in range(len(ezarr))])
# Charset parsing part.
nodes={}
nact=[]
ntran={}
def readr(name):
	r=0
	if not(name in nodes):
		r=len(nodes)
		nodes[name]=len(nodes)
		nact.append(0)
	else:
		r=nodes[name]
	return r

for i in lines:
	if i[0]=='node':
		r=readr(i[1])
		if i[2]=='active' or i[2]=='A':
			nact[r]=1
		else:
			nact[r]=0
	elif i[0]=='link':
		ra,rb=readr(i[1]),readr(i[2])
		if not((ra,rb) in ntran):
			ntran[(ra,rb)]=[]
		for j in i[3:]:
			for k in csname[j]:
				ntran[(ra,rb)].append(k)
str1=','.join(map(str,ezarr))
trsf=len(ntran)
def pts(a):
	a,b=a
	return "{%d,%d}"%(a,b)
trsrr=[t for t in ntran]
gpt=list(map(lambda x:ntran[x],trsrr))
trsff=",".join(map(pts,trsrr))
def ats(a):
	z=len(a)
	z=[z]+a
	return "{%s}"%",".join(map(str,z))
trsfg=max(map(len,gpt))+1
trsgg=",".join(map(ats,gpt))
trscnt=len(nodes)
wf=open(ofname,"w")
def nbc(a):
	a,b=a
	return "	const int _%s=%d;"%(a,b)
strg="\n".join(map(nbc,[(t,nodes[t]) for t in nodes]));

zz=[0 for i in range(len(nodes))]
for i in nodes:
	zz[nodes[i]]='"'+i+'"';
strh=",".join(zz)

template="""namespace Automaton{
	const int charty[128]={%s};
	const int transf[%d][2]={%s};
	const int transg[%d][%d]={%s};
	int trans[%d][%d];
	void init(){
		int g=%d;
		for(int i=0;i<g;++i){
			int x=transf[i][0],y=transf[i][1];
			int l=transg[i][0];
			for(int j=1;j<=l;++j){
				trans[x][transg[i][j]]=y;
			}
		}
	}
	const int activ[%d]={%s};
%s
	const char* name[%d]={%s};
	struct token{char*start,*end;int type;};
	vector<token>tokenize(char*s,char*e){
		*e=0;
		int state=_trivial;
		vector<token>ret;
		for(char*k,*r;s!=e;s=k){
			while(s!=e&&(state=trans[state][charty[*(s++)]])==_trivial);
			if(s==e)break;
			k=s,r=s,--s;int typ;
			do{if(activ[state])k=r,typ=state;}while(r!=e&&(state=trans[state][charty[*r]])!=_trivial&&r++);
			if(k!=r)throw("error: tokenizer exception");
			if(s!=k)ret.push_back((token){s,k,typ});
		}return ret;
	}
	void print_token(token t){
		printf("%%s:",name[t.type]);
		for(char*s=t.start;s!=t.end;++s)putchar(*s);
		puts("");
	}
};
"""%(str1,trsf,trsff,trsf,trsfg,trsgg,trscnt,len(ezmap),trsf,trscnt,",".join(map(str,nact)),strg,len(zz),strh)
wf.write(template);
