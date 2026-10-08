"""Build the byte-identical source with GCC or Clang; optionally run its tests."""
from pathlib import Path
import argparse,json,shutil,subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--variant',choices=['B','E'],default='B')
    p.add_argument('--tests',action='store_true')
    a=p.parse_args()
    source=ROOT/('native/BARR_v0.4B' if a.variant=='B' else 'related/BARR_v0.4E')
    out=ROOT/'build'/a.variant;out.mkdir(parents=True,exist_ok=True)
    if shutil.which('cmake'):
        subprocess.run(['cmake','-S',str(source),'-B',str(out),'-DCMAKE_BUILD_TYPE=Release','-DCMAKE_CXX_FLAGS_RELEASE=-O3'],check=True)
        subprocess.run(['cmake','--build',str(out),'--parallel','2'],check=True)
        if a.tests: subprocess.run(['ctest','--test-dir',str(out),'--output-on-failure'],check=True)
    else:
        compiler=shutil.which('g++') or shutil.which('clang++')
        if not compiler:raise RuntimeError('GCC/Clang is required; run on Linux or WSL')
        targets=[('barr_solver','src/main.cpp',[])]
        if a.tests:targets += [('barr_'+name+'_tests','tests/test_'+name+'.cpp',[]) for name in ['core','coupling','selective','pair']]
        if a.tests and a.variant=='E':targets += [('barr_pulse_ablation_tests','tests/test_pulse_ablation.cpp',['-DBARR_TEST_FIXED_CLOCK=1'])]
        for name,file,flags in targets:
            subprocess.run([compiler,'-std=c++17','-O3','-pthread',*flags,'-I',str(source/'include'),str(source/file),'-o',str(out/name)],check=True)
        if a.tests:
            for name,file,flags in targets[1:]:subprocess.run([str(out/name)],check=True)
    print(json.dumps({'source':str(source),'build':str(out),'tests_requested':a.tests}))

if __name__=='__main__':main()
