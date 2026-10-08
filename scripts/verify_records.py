"""Read-only verification of the published frozen sources, inputs and records."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import hashlib,json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    sources=read(ROOT/'provenance/frozen_sources.json')
    for key in ['B_source_files','E_source_files']:
        for item in sources[key]:
            if sha(ROOT/item['path'])!=item['sha256']:raise ValueError('Source SHA differs: '+item['path'])
    graphs={}
    for item in read(ROOT/'provenance/inputs.json'):
        for kind in ['original','normalized']:
            path=ROOT/'data/CP-SCALE-AU-L002'/kind/(item['graph']+'.npz')
            if sha(path)!=item[kind+'_sha256']:raise ValueError('Input SHA differs: '+item['graph'])
        with np.load(ROOT/'data/CP-SCALE-AU-L002/original'/(item['graph']+'.npz'),allow_pickle=False) as z:
            graphs[item['graph']]={k:z[k] for k in z.files}
    expected={(c['batch'],c['phase'],c['cell_id']):c for c in read(ROOT/'provenance/release_result_verification.json')['checks']}
    groups=defaultdict(lambda:defaultdict(list))
    rows=read(ROOT/'results/all_runs.json')
    if len(rows)!=290 or len(expected)!=290:raise ValueError('Record census differs')
    for row in rows:
        path=ROOT/row['record'];record=read(path);g=graphs[row['graph']]
        original=expected[(row['batch'],row['phase'],row['cell_id'])]
        if sha(path)!=original['original_result_sha256']:raise ValueError('Record SHA differs: '+row['cell_id'])
        ids=np.asarray(record['selected'])
        if ids.ndim!=1 or not np.issubdtype(ids.dtype,np.integer):raise ValueError('Invalid membership type')
        if len(ids)!=len(np.unique(ids)) or np.any(ids<0) or np.any(ids>=len(g['weight_ticks'])):raise ValueError('Invalid membership')
        mask=np.zeros(len(g['weight_ticks']),dtype=bool);mask[ids]=True
        if np.any(mask[g['edge_u']] & mask[g['edge_v']]):raise ValueError('Selected conflict edge')
        ticks=sum(int(g['weight_ticks'][v]) for v in ids)
        if ticks!=record['quality_ticks'] or ticks!=row['quality_ticks']:raise ValueError('Integer objective differs')
        for resource in ['satellite_id','antenna_id']:
            by_resource=defaultdict(list)
            for v in ids:by_resource[str(g[resource][v])].append(int(v))
            for members in by_resource.values():
                frontier=None
                for v in sorted(members,key=lambda v:(int(g['start_ticks'][v]),int(g['end_ticks'][v]),v)):
                    if frontier is not None and int(g['start_ticks'][v])<frontier:raise ValueError('Resource time conflict')
                    gap=int(g['satellite_gap_ticks']) if resource=='satellite_id' else int(g['ground_gap_by_node_ticks'][v])
                    end=int(g['end_ticks'][v])+gap
                    frontier=end if frontier is None else max(frontier,end)
        groups[(row['batch'],row['phase'],row['arm'])][row['graph']].append(ticks)
    summaries=read(ROOT/'results/summary.json')
    for item in summaries:
        views=groups[(item['batch'],item['phase'],item['arm'])]
        mean=sum(Fraction(sum(values),len(values)*1_000_000) for values in views.values())/len(views)
        if mean!=Fraction(item['exact_mean_fraction']):raise ValueError('Exact batch mean differs')
    print(json.dumps({'status':'PASS','frozen_source_files':97,'input_views':len(graphs),'raw_results':len(rows),'exact_batch_means':len(summaries),'checks':['integer objectives','all graph edges','satellite timelines','antenna timelines','source/input/result SHA256'],'performance_searches_started':0},indent=2))

if __name__=='__main__':main()
