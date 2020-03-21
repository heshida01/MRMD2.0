import argparse
import subprocess
import os
from pprint import pprint as pp
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=int, help="start index", default=1)
    parser.add_argument("-i", type=str, help="input file",required=True)
    parser.add_argument("-e", type=int, help="end index", default=-1)
    parser.add_argument("-l",  type=int, help="step length", default=1)
    parser.add_argument("-m", type=int, help="mrmd2.0 features top n",default=-1)
    parser.add_argument("-t", type=str, help="metric basline", default="f1")
    parser.add_argument("-o", type=str, help="output the metrics file",default="")
    parser.add_argument("-c", type=str, help="output the dimensionality reduction file",default="")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    current_path = os.path.dirname(os.path.abspath(__file__))
    #print("current_path=",current_path)
    output_c = os.path.basename(args.i)+'.dimensionality_reduction'+os.path.splitext(args.i)[-1]
    output_o = os.path.basename(args.i)+'.metrics.'+"csv"

    if not os.path.exists('Results'):
        os.mkdir('Results')
    if not os.path.exists('Logs'):
        os.mkdir('Logs')

    cmd = f" sudo docker container run \
     -v {current_path}{os.sep}Results:/Results:rw \
     -v  {current_path}{os.sep}Logs:/Logs:rw  \
     -v {current_path}{os.sep}{args.i}:/{args.i}:ro \
     --rm -it mrmd:v05 python mrmd2.0.py \
     -i {args.i} -c {output_c} -o {output_o} -l {args.l} -m {args.m} -t {args.t}"
    #print(cmd)
    procExe = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #sp1.communicate()
    while procExe.poll() is None:
        line = str(procExe.stdout.readline()).strip()
        if line == '':
            break
        print(line+'\r')


