#!/usr/bin/python3.8
import os,sys,time,json,threading
#dla trybow 0,1,2
brut='bruttt.c';brutc='B';bout='bout'#nazwa pliku bruta.cpp, nazwa do kompilacji,plik wyjsciowy
wzor='wz.c';wzorc='W';wout='wout'#nazwa pliku bruta.cpp, nazwa do kompilacji,plik wyjsciowy
tester='gen.cpp';testerc='T';test='tes'#nazwa pliku generatorki testow.cpp, nazwa do kompilacji,plik wyjsciowy
wypisywanie=1# czy wynik testu ma być wypisany przy różnicy na końcu wyjścia
rating=0 #1=on 0=off   wypisywanie stasunku wa do ac. zlicza ilosc wa i ac nie przerywajac sparwdzania dal != 0 
type_rate=1 # 0=ilość wypisana wa i ac          1=procenowo ac/ilosc testow
zliczanie_czasu=3	#1=wzorcowka   2=brut   3=2+1
wzor_max_time=0 #0 wylaczone lub podaj w sekundach np 1.000
brut_max_time=0 #0 wylaczone
run_type=0 # 0=brut&wzorcowka     1=IN poróanie z OUT    2=Generowanie restów brutem    3=geneowanie wileoma generatorkami
#################################################################################
#dla trybu 1 i 2
ilosc_testow=20
grup_pocz=0
katalog='test'
prefix='MF'
nr_poczatkowy=1
#dla trybu 3 + grup_pocz
multitest_names=['t0.cpp','t1.cpp','t2.cpp','t3.cpp','t4.cpp']
multitest_suffix='.compiled'
multitest_am=[1,1,1,1,1]
multitest_group_beg=1
multitest_beg=1
multitest_group_type=3# 1 kazdy test w odzielnej grupie 2 kazdy z przypadkow testowych w odielnie jgrupie 3 wszystko w jednej grupie
multitest_tout='tout'
#TODO dla trybu 4
auth='a.cpp'
authc='A'
a_temp='A_temp'
#systemowe:
edytor='vim'
write_stop_shell_cmd=True
grupy=True
ile_w_grupie=10
sbin=True
lang='c++'
###v.07777777##################################################################
load_from_file=False;TEST=0;path=sys.path[0];ignore=False;compiling=1;wssc=1;Debug=0;__name__;dead=0
if sys.platform=='linux':
	_prefix='./';_sudo='sudo'
else:
	_prefix='';compiling=0;_sudo=''
class color:
	att='\033[40;90;1m';mess='\033[100;93m';bblack='\033[40m';bgreen='\033[42m';err='\033[1;40;91m';black='\033[30m';red='\033[91m';default='\033[0m';bold='\033[1m';green='\033[32m';lgreen='\033[92m';lblue='\033[94m';blue='\033[94m';yellow='\033[33m';purple='\033[35m';lyellow='\033[93m';llblue='\033[96m'
if sys.argv.count('nc')!=0 or sys.argv.count('win') or sys.argv.count('nocolor')!=0:	
	class color:
		att='';mess='';bblack='';err='';bgreen='';black='';red='';default='';bold='';green='';lgreen='';lblue='';blue='';yellow='';purple='';lyellow='';llblue=''

def out(s,end=color.default,w=0):
	global wssc
	if wssc or w:
		print(s,end=end,flush=1)
###
###
def pp(s):
	print(s,end='',flush=1)
def err(s,end=''):
	s=color.red+str(s)
	out(s+end)

def dim():
	return os.get_terminal_size()
def mess_f(s):
	s=str(s);out(color.mess+s)
def exit(mess=None,s='ZAMKNIĘTO PROGRAM'):
	print();s=str(s)
	if s=='':
		sys.exit()
	if sys.argv.count('win'):
		return 1
	a=dim()[0]
	l=len(s)
	a=int(a)
	a//=2
	l//=2
	out(color.err+''.join(' ' for i in range(dim()[0]))+''.join([' ' for  i in range(0,a-l)])+s+''.join( ' ' for i in range(dim()[0]-a-l) ))
	out(color.err+''.join(' ' for i in range(dim()[0])))
	if not mess==None:
		mess_f(mess)
	print()
	sys.exit()
def ERRR():
	exit(mess=u'Skontaktuj sie z adminem Sprawdzarki pod kontem naprawienia błędów!!! Wystąpił błąd krtyczny, który uniemożliwił dalsze wykonywanie zleconego zdania.',s=u"BŁĄD KRYTYCZNY!!!")
def arg():
	l=sys.argv;global path,ignore,_sudo
	if l.count('ignore')!=0:
		ignore=True
	if l.count('se')!=0 or l.count('selfedit')!=0:
		_temp=''
		try:
			if l[0][:5]=='/bin/':
				_temp=_sudo+' '
		except:
			_temp=''
		_temp2=_temp+edytor+' '+l[0]
		if not Debug:
			os.system(_temp2)
		else:
			print(_temp2)
		exit('ok')
	if l.count('help') or l.count('-h') or l.count('h'):
		out(color.yellow+u'''Sprawdzarka ''' +color.green+color.bold+ '''fenderJS'''+color.default+color.yellow+''', parametry:gen [wypisanie kodu genratorki}\ninstall [instalacja do katalogu systemowego]\nexport [wyeksportownie z katalogu systemowego do innego]\nse/selfedit [edycja ./run]\nhelp/h [pomoc]\nnc/nocolor [brak koloryzacji]\nc/compile [kompilacja tylko]\nmj [wytworzenie pliku konfiguracyjnego]*\nset [ustawienia pliku konfguracyjnego]*\ndef [użycie ustawień domyślnych]*\nnie [nie kompiluje]\nwin [aktywuj ustawinia dla windowsa]\n\t* - opcje nie pewne, możliwość wystąpienia erroru, nie używać\

Sprawdzarka obsluguje zatrzymywanie "pokojowe". Podczas sprawdzania należy nacisnąć klawisz s i zatwierdzic enterem, a sprawdzanie sie zatrzyma.
By uzyskac wiecej opcji podczas sprawdzania użyj h.
''')
		exit('ok')
	if l.count('c')!=0 or l.count('compile')!=0:
		compile(eon=0)
		compiling=0
		out(color.lgreen+'OK\n')
		exit('ok')
	if l.count('install'):
		x=l.index('install')
		x+=1;a=''
		if x!=len(l):
			a=l[x]
		os.system(_sudo+' cp '+l[0]+' /bin/'+a)
		exit('ok')
	if l.count('del'):
		print(_sudo+' rm /'+l[0])
		exit(u'YYyyyyyy... coś tu jest nie tak :\\')
	if l.count('set')!=0:
		ERRR()
		os.system('vim .settings_json.run')
		exit('ok')
	if l.count('def'):
		load_from_file=False
	if l.count('export'):
		export()
		exit('zrobione')
	if l.count("gen"):
		print(genSC)
		exit(s='')
def write_stop():
	global wssc
	wssc=True
	def wait():
		global wssc
		wssc=False
		time.sleep(2)
		wssc=True
	th=threading.Thread(target=wait)
	th.start()
def shell():
	global dead
	while True:
		s=input()
		if s=='pomoc' or s=='help':
			write_stop()
			temp=u'''\n
	pomoc/help	pomoc w shellu
	quit/s	zakończenie pracy
			'''
			out(color.yellow+temp,w=1)
		if s=='quit' or s=='s':
			dead=1
			exit('','')
		if s=='w':
			write_stop()
def linux():
	if sys.platform!='linux':
		sys.argv.append('ns')
		sys.argv.append('win')
	
def comp(name,out):
	if not compiling:
		err('Kompilacja pominięta '+name+' !\n')
		return 1
	try:
		name=str(name)
		out=str(out)
	except:
		exit(u"Błąd parametru kompilacji w COMP!!!")
	pp('Kompilacja: '+name+' do '+out)
	if lang=='c++':
		if os.system('g++ -std=c++11 '+name+' -o '+out):
			exit("Błąd kompilacji "+name+"!!!")
	elif lang=='c':
		if os.system('gcc '+name+' -o '+out):
			exit("Błąd kompilacji "+name+"!!!")
	pp('\r')
def compile(br=1,wz=1,te=1,eon=1):
	if sys.argv.count('nie') or sys.argv.count('win'):
		return 1
	par='-std=c++11 '
	if br==1:
		comp(brut,brutc)
	if te==1:
		comp(tester,testerc)
	if wz==1:
		comp(wzor,wzorc)
def read(s):
	with open(s) as p:
		return p.read()
def deff(bout=bout,wout=wout):
	a=read(bout)
	b=read(wout)
	if a!=b:
		return 1
	else:
		return 0
def t():
	return time.time()

def main():

	ac=0;wa=0;ev=0;tw1=0;tw2=0;tb1=0;tb2=0
	global nr_poczatkowy
	global ilosc_testow
	global multitest_names
	global multitest_am
	global dead
	global multitest_suffix; global multitest_group_type
	if run_type==3:
		if compiling:
			compile(br=0,te=0)
		if compiling and not Debug:
			for i in multitest_names:
				comp(i,i+multitest_suffix)
			out('\n')
		multitest_comp=list(f+multitest_suffix for f in multitest_names)
		#TODO grupy testow
		licz=0
		for count,name in enumerate(multitest_comp):
			for cc in range(multitest_am[count]):
				if dead:
					return
				tname=prefix
				if multitest_group_type==1:#odzielna grupa na każdy testi
					tname+=str(licz+multitest_beg)
					licz+=1
				elif multitest_group_type==2:#kazda generatorka=odzielna grupa
					tname=tname+str(count+multitest_beg)+'.'+str(cc+multitest_group_beg)
				elif multitest_group_type==3:
					tname+=str(multitest_beg)+'.'+str(licz+multitest_group_beg)
					licz+=1
				else:
					exit(u'Bląd w zmiennej multitest_group_type!')
				if Debug:
					err(tname)
				out('\t\t'+color.att+tname);out('\t'+color.yellow+"TEST: ")
				os.system(_prefix+name+' > '+katalog+'/'+tname+'.in')
				out(color.green+'DONE')
				out('\t'+color.yellow+'WZORC: ')
				os.system(_prefix+wzorc+' < '+katalog+'/'+tname+'.in > '+katalog+'/'+tname+'.out')
				out(color.green+'DONE')
				out('\n')
			if Debug:
				out('\n')
	elif run_type==4:
		'''auth='a.cpp'
		   authc='A'
		   a_temp='A_temp' '''
		comp(auth,authc)
		#TODO#TODO#TODO
		while True:
			if dead:
				return
			try:
				out('\t\t'+color.blue+str(n),end=color.default)
				out('\t'+color.yellow+'TEST: ',end=color.default);os.system(_prefix+testerc+' >'+test);out(color.green+'DONE',end=color.default)
				out('\t'+color.yellow+'WZOR: ',end=color.default);tw1=t();os.system(_prefix+wzorc+'< '+test+' >'+wout);tw2=t();out(color.green+'DONE',end=color.default)
				out('\t'+color.yellow+'BRUT: ',end=color.default);tb1=t();os.system(_prefix+authc+'< '+test+' >'+a_temp);tb2=t();out(color.green+'DONE',end=color.default)

				#porównywanie testów
				def deff_auth():
					pass
					# utrzeba biedzie wstawic doklana pobranie spliku z wout i wsttawienie go doautoryzatora i tak samo z btrem i po tmy sprawdzenie kompatybilnosci czy jest wsystko ok i zalczeni tego na + lub -
					
				w=deff_auth()
				ev+=1
				if w==0:
					ac+=1
				else:
					wa+=1
				if w==0:
					out(color.lgreen+'\tAC')
				else:
					out(color.red+'\tWA')
					if rating==0:
						out('\n\n')
						if wypisywanie!=0:
							out(color.bold+'\nBrut:'+read(bout)+u'\n\nWzorcówka:'+read(wout)+'\n\n')
						exit()
				if type_rate==1:
					out('\t'+color.purple+str(round(ac/ev,2)))
				elif type_rate==0:
					out('\t'+color.purple+'AC: '+str(ac)+' WA: '+str(wa))

				if (zliczanie_czasu&1)==1: # wzor 2 br
					tw2-=tw1
					out(color.llblue+'\ttW: '+str(round(tw2,3)))
					if wzor_max_time!=0:
						if tw2>wzor_max_time:
							out('\n\n\t'+color.bold+u"PRZEKROCZONO LIMIT CZASU WZORCÓWKI!\n")
							exit()
				if (zliczanie_czasu&2)==2:
					tb2-=tb1
					out(color.llblue+'\ttB: '+str(round(tb2,3)))
					if brut_max_time!=0:
						if tb2>wzor_max_time:
							out('\n\n\t'+color.bold+"PRZEKROCZONO LIMIT CZASU BRUTA!\n")
							exit()
							
				n+=1
							
				out('\n')
			except KeyboardInterrupt:
				out(color.lyellow+"\n\nZATRZYMANO!"+color.default)
		
	elif run_type==2:
		compile(br=0)
		ii=grup_pocz
		while ilosc_testow>0:
			if dead:
				return 
			grup=''
			
			if grupy:
				ii+=1
				if ile_w_grupie>0:
					if ile_w_grupie < ii:
						ii=1
						nr_poczatkowy+=1
				grup='.'
		
				grup+=str(ii)
				
			
			out('\t\t'+color.att+str(nr_poczatkowy)+grup,end=color.default)
			outt=katalog+'/'+prefix+str(nr_poczatkowy)+grup
			out('\t'+color.yellow+'TEST: ',end=color.default);os.system(_prefix+testerc+' >'+outt+'.in');out(color.green+'DONE',end=color.default)
			out('\t'+color.yellow+'WZOR: ',end=color.default);tw1=t();os.system(_prefix+wzorc+'< '+outt+'.in'+' >'+outt+'.out');tw2=t();out(color.green+'DONE',end=color.default)
			if not grupy:
				nr_poczatkowy+=1
			ilosc_testow-=1
			out('\n')
		return 2
	elif run_type==1:
		compile(br=0)

		while ilosc_testow>0:
			if dead:
				return 
			out('\t\t'+color.blue+str(nr_poczatkowy),end=color.default)
			outt=katalog+'/'+prefix+str(nr_poczatkowy)
			out('\t'+color.yellow+'WZOR: ',end=color.default);tw1=t();os.system(_prefix+wzorc+'< '+outt+'.in'+' >'+wout);tw2=t();out(color.green+'DONE',end=color.default)
			ev+=1
			w=deff(outt+'.out',wout)
			if w==0:
				ac+=1
			else:
				wa+=1
			if w==0:
				out(color.lgreen+'\tAC')
			else:
				out(color.red+'\tWA')
			if rating==0:
				out('\n\n')
				if wypisywanie!=0:
					out(color.bold+'\nBrut:'+read(bout)+u'\n\nWzorcówka:'+read(wout))
				exit()
			else:
				if type_rate==1:
					out('\t'+color.purple+str(round(ac/ev,2)))
				elif type_rate==0:
					out('\t'+color.purple+'AC: '+str(ac)+' WA: '+str(wa))
			if (zliczanie_czasu&1)==1: # wzor 2 br
				tw2-=tw1
				out(color.llblue+'\ttW: '+str(round(tw2,3)))
				if wzor_max_time!=0:
					if tw2>wzor_max_time:
						out('\n\n\t'+color.bold+u"PRZEKROCZONO LIMIT CZASU WZORCÓWKI!\n")
						exit()

			nr_poczatkowy+=1
			ilosc_testow-=1
			out('\n')
		return 1


	elif run_type==0:
		compile()
		n=1
		while True:
			if dead:
				return
			try:
				out('\t\t'+color.blue+str(n),end=color.default)
				out('\t'+color.yellow+'TEST: ',end=color.default);os.system(_prefix+testerc+' >'+test);out(color.green+'DONE',end=color.default)
				out('\t'+color.yellow+'WZOR: ',end=color.default);tw1=t();os.system(_prefix+wzorc+'< '+test+' >'+wout);tw2=t();out(color.green+'DONE',end=color.default)
				out('\t'+color.yellow+'BRUT: ',end=color.default);tb1=t();os.system(_prefix+brutc+'< '+test+' >'+bout);tb2=t();out(color.green+'DONE',end=color.default)
				#porównywanie testów
				
		#		w= not deff()
				w=deff()
				ev+=1
				if w==0:
					ac+=1
				else:
					wa+=1
				if w==0:
					out(color.lgreen+'\tAC')
				else:
					out(color.red+'\tWA')
					if rating==0:
						out('\n\n')
						if wypisywanie!=0:
							out(color.bold+'\nBrut:'+read(bout)+u'\n\nWzorcówka:'+read(wout)+'\n\n')
						exit()
				if type_rate==1:
					out('\t'+color.purple+str(round(ac/ev,2)))
				elif type_rate==0:
					out('\t'+color.purple+'AC: '+str(ac)+' WA: '+str(wa))

				if (zliczanie_czasu&1)==1: # wzor 2 br
					tw2-=tw1
					out(color.llblue+'\ttW: '+str(round(tw2,3)))
					if wzor_max_time!=0:
						if tw2>wzor_max_time:
							out('\n\n\t'+color.bold+u"PRZEKROCZONO LIMIT CZASU WZORCÓWKI!\n")
							exit()
				if (zliczanie_czasu&2)==2:
					tb2-=tb1
					out(color.llblue+'\ttB: '+str(round(tb2,3)))
					if brut_max_time!=0:
						if tb2>wzor_max_time:
							out('\n\n\t'+color.bold+"PRZEKROCZONO LIMIT CZASU BRUTA!\n")
							exit()
							
				n+=1
							
				out('\n')
			except KeyboardInterrupt:
				out(color.lyellow+"\n\nZATRZYMANO!"+color.default)
				exit()
		return 0
def export():
	out(color.red+u"Gdzie wyeksportować?: ")
	p=' '
	p+=input()
	os.system(_sudo+' cp '+sys.argv[0]+p)
	


di={
	'brut':brut,
	'brutc':brutc,
	'bout':bout,
	'wzor':wzor,
	'wzorc':wzorc,
	'wout':wout,
	'tester': tester,
	'testerc':testerc,
	'test':test,
	'wypisywanie':wypisywanie,
	'rating':rating,
	'type_rate':type_rate,
	'zliczanie_czasu':zliczanie_czasu,
	'wzor_max_time':wzor_max_time,
	'brut_max_time':brut_max_time,
	'run_type':run_type,
	'ilosc_testow':ilosc_testow,
	'katalog':katalog,
	'prefix':prefix,
	'nr_poczatkowy':nr_poczatkowy

}
di_str='''
{
	"wzor_max_time": 0,
	"run_type": 0,
	"type_rate": 0,
	"wout": "wout",
	"test": "tes",
	"rating": 0,
	"wzorc": "W",
	"ilosc_testow": 50,
	"katalog": "test",
	"testerc": "T",
	"wzor": "w.cpp",
	"zliczanie_czasu": 3,
	"prefix": "",
	"brut":	"b.cpp",
	"brut_max_time": 0,
	"wypisywanie": 0,
	"brutc": "B",
	"bout": "bout",
	"tester": "t.cpp",
	"nr_poczatkowy": 0
}

'''

genSC="""#define ll long long
#include <bits/stdc++.h>
#include <sys/time.h>
using namespace std;
ll rn(ll a=0,ll b=1){return ((ll)rand())%(b-a+1)+a;}
int main(){struct timeval tp;gettimeofday(&tp, NULL);long int ms = tp.tv_sec * 1000 + tp.tv_usec / 1000;srand(ms);



}"""
def make_json():
	try:
		with open('.settings_json.run','w') as o:
			o.write(di_str)
	except:
		with open('.settings_json.run','x') as o:
			o.write(di_str)
def read_json():
	try:
		diraw=read('.settings_json.run')
	except:
		err(u"Błąd odczytu ustawień, użyj parametru [def] by użyć opcji domyślych, lub mj by wygenerować plik z ustawieniami i następnie uruchom program z parametrem [set] by skonfigurować go poprawnie.")
		exit()
	dii={}
	try:
		dii=json.loads(diraw)
	except:
		err(u'Błąd ładowania ustawień; wprowadź poprawki lub użyj parametru [mj] by wygenerować domyślne ustawienia.')
		exit()		
	global brut;brut=dii['brut']
	global brutc;brutc=dii['brutc']
	global bout;bout=dii['bout']
	global wzor;wzor=dii['wzor']
	global wzorc;wzorc=dii['wzorc']
	global wout;wzout=dii['wout']
	global tester;tester=dii['tester']
	global testerc;testerc=dii['testerc']
	global test;test=dii['test']
	global wypisywanie;wypisywanie=dii['wypisywanie']
	global rating;rating=dii['rating']
	global type_rate;type_rate=dii['type_rate']
	global zliczanie_czasu;zliczanie_czasu=dii['zliczanie_czasu']
	global wzor_max_time;wzor_max_time=dii['wzor_max_time']
	global brut_max_time;brut_max_time=dii['brut_max_time']
	global run_type;run_type=dii['run_type']
	global ilosc_testow;ilosc_testow=dii['ilosc_testow']
	global katalog;katalog=dii['katalog']
	global prefix;prefix=dii['prefix']
	global nr_poczatkowy;nr_poczatkowy=dii['nr_poczatkowy']
def start1(name):
	t1=t()
	os.system(name)
	t2=t()
	return t2-t1
def start(name):
	name
if __name__=='__main__':
	if False and load_from_file and not sbin:
		read_json()
	if sys.argv.count('mj'):
		make_json()
		exit()
	arg()
	linux()
	th=threading.Thread(target=shell,daemon=1)
	th.start()
	main()
	try:
		th._stop()
	except:
		pass
