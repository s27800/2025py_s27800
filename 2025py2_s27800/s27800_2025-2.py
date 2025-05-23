from Bio import Entrez,SeqIO;import matplotlib.pyplot as x;import pandas as y
class R:
 def __init__(s,e,k):Entrez.email=e;Entrez.api_key=k
 def s(s,t):
  try:h=Entrez.efetch(db="taxonomy",id=t,retmode="xml");Entrez.read(h);h=Entrez.esearch(db="nucleotide",term=f"txid{t}[Organism]",usehistory="y");r=Entrez.read(h);s.w,s.q,s.n=r["WebEnv"],r["QueryKey"],int(r["Count"]);return s.n
  except:return 0
 def f(s,a,b):
  d=[]
  for i in range(0,s.n,500):
   try:
    h=Entrez.efetch(db="nucleotide",rettype="gb",retmode="text",retstart=i,retmax=500,webenv=s.w,query_key=s.q)
    for r in SeqIO.parse(h,"genbank"):
     l=len(r.seq)
     if a<=l<=b:d+=[{"accession":r.id,"length":l,"description":r.description}]
   except:pass
  return d
 def c(s,d,f):y.DataFrame(d).to_csv(f,index=0)
 def p(s,d,f):df=y.DataFrame(d).sort_values("length",ascending=0);x.plot(df["accession"],df["length"],'o');x.xticks([]);x.tight_layout();x.savefig(f,dpi=80)
e=input('email:');k=input('api:');t=input('id:');a=int(input('min:'));b=int(input('max:'));r=R(e,k)
if r.s(t):d=r.f(a,b);d and r.c(d,f"{t}.csv") or 1 and r.p(d,f"{t}.jpg")
