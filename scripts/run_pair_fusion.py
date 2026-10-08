"""Explicit frozen pair-fusion profile; original source and CLI stay unchanged."""
from pathlib import Path
import argparse,json,os,subprocess,sys,time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'native/BARR_v0.4B/python'))
from barr_io import load_npz,write_native,sha256

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--graph',default='g0340')
    p.add_argument('--seed',type=int,default=31)
    p.add_argument('--seconds',type=float,default=360.)
    p.add_argument('--variant',choices=['B','E-full','E-pulse'],default='B')
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--dry-run',action='store_true')
    a=p.parse_args()
    if a.seconds<360 or not 0<=a.seed<=100000000:raise ValueError('Use at least 360 seconds and a valid seed')
    inputs=json.loads((ROOT/'provenance/inputs.json').read_text(encoding='utf-8'))
    meta=next((r for r in inputs if r['graph']==a.graph),None)
    if meta is None:raise ValueError('Unknown frozen input view')
    graph=ROOT/'data/CP-SCALE-AU-L002/normalized'/(a.graph+'.npz')
    if sha256(graph)!=meta['normalized_sha256']:raise ValueError('Input hash differs from the frozen profile')
    profile=json.loads((ROOT/'profiles/pair-fusion.json').read_text(encoding='utf-8'))
    binary=ROOT/'build'/('B' if a.variant=='B' else 'E')/'barr_solver'
    out=a.out.resolve()
    if out.exists():raise FileExistsError('Output directory must be new')
    command=[str(binary),'--input',str(out/'input.barr'),'--output',str(out/'native_result.json'),
             '--seconds',str(a.seconds),'--seed',str(a.seed),'--threads','1','--population','4','--mode','pair',
             '--events',str(out/'events.jsonl'),'--checkpoint',str(out/'checkpoint.json')]
    for key,value in {**profile['inherited_options'],**profile['options']}.items():command += ['--'+key,str(value)]
    if a.variant!='B':command += ['--pair-component','full' if a.variant=='E-full' else 'pulse-only']
    if a.dry_run:
        print(json.dumps({'command':command,'quality_search_started':False},indent=2));return
    if not binary.is_file():raise FileNotFoundError('Run scripts/build_native.py for the requested variant first')
    out.mkdir(parents=True)
    begin=time.perf_counter()
    instance=load_npz(graph)
    write_native(out/'input.barr',instance,instance.ticks(1.0/meta['ticks_per_second']))
    if sha256(out/'input.barr')!=meta['native_input_sha256']:raise ValueError('Native input differs from frozen historical input')
    preparation=time.perf_counter()-begin
    env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'}
    with (out/'stdout.log').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:
        subprocess.run(command,stdout=stdout,stderr=stderr,env=env,check=True)
    result=json.loads((out/'native_result.json').read_text(encoding='utf-8'))
    result['release_graph']=a.graph;result['release_variant']=a.variant
    result['release_preparation_seconds']=preparation
    result['release_quality_contact_seconds']=instance.objective(result['selected'])
    result['release_binary_sha256']=sha256(binary)
    (out/'release_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'out':str(out),'contact_seconds':result['release_quality_contact_seconds']}))

if __name__=='__main__':main()
