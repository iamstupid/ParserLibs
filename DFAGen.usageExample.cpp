#include <cstdio>
#include <vector>
#include <cstring>
using namespace std;
namespace Automaton{
	const int charty[128]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,0,2,2,1,3,0,3,4,1,5,5,5,5,5,5,5,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,2,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0};
	const int transf[12][2]={{0,5},{5,5},{0,1},{1,2},{0,2},{2,2},{0,3},{1,3},{3,4},{2,4},{4,4},{0,6}};
	const int transg[12][4]={{3,1,3,5},{3,1,3,5},{1,3},{1,5},{1,5},{1,5},{1,4},{1,4},{1,5},{1,4},{1,5},{1,2}};
	int trans[7][6];
	void init(){
		int g=12;
		for(int i=0;i<g;++i){
			int x=transf[i][0],y=transf[i][1];
			int l=transg[i][0];
			for(int j=1;j<=l;++j){
				trans[x][transg[i][j]]=y;
			}
		}
	}
	const int activ[7]={0,1,1,0,1,1,1};
	const int _trivial=0;
	const int _pre=1;
	const int _num=2;
	const int _dot=3;
	const int _flo=4;
	const int _ide=5;
	const int _bra=6;
	const char* name[7]={"trivial","pre","num","dot","flo","ide","bra"};
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
		printf("%s:",name[t.type]);
		for(char*s=t.start;s!=t.end;++s)putchar(*s);
		puts("");
	}
};

using namespace Automaton;
char t[1000];
int main(){
	fgets(t,1000,stdin);
	int len = strlen(t);
	init();
	vector<token> r = tokenize(t,t+len);
	for(token c:r)
		print_token(c);
	return 0;
}
