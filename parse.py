#!/usr/bin/env python
import sys
from writeSong import writeFile	


def main():
    Patterns = []
    with open('4mat-carvup2-no-effects-chrom.Forth') as fp:
        for line in fp:
            if line[0] == 'T':
                i = 0
                ps = ""
                vs = ""
                while line[i] != 'V':
                    ps = ps + line[i]
                    i = i+1
                # remove traling comma
                ps = ps[:-1] 
                while line[i] != '\n':
                    vs = vs + line[i]
                    i = i+1
                
                # Get rid of extraneous information
                ps = ps.replace('T','')
                ps = ps.replace('P','')
                ps = ps.replace('p','')
                ps = ps.replace('(','')
                ps = ps.replace(')','')
                
                vs = vs.replace('V','')
                vs = vs.replace('v','')
                vs = vs.replace('(','')
                vs = vs.replace(')','')
                
                # Split on commas
                ps_Arr = ps.split(",")
                vs_Arr = vs.split(",")
                
                # A list of 2D points
                points = []
                # A list of 2D translations
                vectors = []
                
                i = 0
                while (i < len(ps_Arr)):
                    point = []
                    point.append(int(ps_Arr[i])//30)
                    point.append(int(ps_Arr[i+1]))
                    points.append(point)
                    i = i+2
                print(points)
                i = 0
                while (i < len(vs_Arr)):
                    vector = []
                    vector.append(vs_Arr[i])
                    vector.append(vs_Arr[i+1])
                    vectors.append(vector)
                    i = i+2
                pattern = []
                pattern.append(points)
                pattern.append(vectors)
                #print(pattern)
                Patterns.append(pattern)
                break
    #print(Patterns)
    writeFile(points, points, "parse_demo.mod")

main()
