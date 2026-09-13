#!/usr/bin/env python3
"""Analyze all Sanzo Wada combinations from a Dain-style or mattdesl-style JSON file.

Usage:
  python tools/v3_2/analyze_wada_palettes.py colors.json --out data/v3_2/wada_palette_analysis.generated.json

The tool does not download third-party data. This preserves explicit provenance: provide the exact dataset snapshot you want to analyze.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path


def clamp(x,a=0,b=1): return max(a,min(b,x))

def parse_hex(h):
    h=h.strip().lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def srgb_chan(c):
    c=c/255
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4

def luminance(rgb):
    r,g,b=[srgb_chan(x) for x in rgb]
    return .2126*r+.7152*g+.0722*b

def contrast(a,b):
    l1,l2=sorted([luminance(a),luminance(b)], reverse=True)
    return (l1+.05)/(l2+.05)

def rgb_to_oklab(rgb):
    r,g,b=[srgb_chan(x) for x in rgb]
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b
    m=0.2119034982*r+0.6806995451*g+0.1073969566*b
    s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l_,m_,s_=l**(1/3),m**(1/3),s**(1/3)
    L=0.2104542553*l_+0.7936177850*m_-0.0040720468*s_
    a=1.9779984951*l_-2.4285922050*m_+0.4505937099*s_
    b=0.0259040371*l_+0.7827717662*m_-0.8086757660*s_
    return L,a,b

def rgb_to_oklch(rgb):
    L,a,b=rgb_to_oklab(rgb); C=(a*a+b*b)**.5; H=(math.degrees(math.atan2(b,a))+360)%360 if C>1e-9 else None
    return {"l":round(L,5),"c":round(C,5),"h":None if H is None else round(H,2)}

def normalize(data):
    colors=data.get('colors', data) if isinstance(data,dict) else data
    out=[]
    for idx,c in enumerate(colors):
        hexv=c.get('hex')
        rgb=c.get('rgb')
        if not rgb and hexv: rgb=list(parse_hex(hexv))
        if not hexv and rgb: hexv='#%02x%02x%02x'%tuple(rgb)
        combos=c.get('combinations',[])
        out.append({"index":c.get('index',idx),"name":c.get('name',f'color-{idx}'),"hex":hexv,"rgb":rgb,"cmyk":c.get('cmyk'),"lab":c.get('lab'),"swatch":c.get('swatch'),"combinations":combos})
    return out

def reconstruct(colors):
    m={}
    for c in colors:
        for cid in c['combinations']:
            m.setdefault(int(cid),[]).append(c)
    return dict(sorted(m.items()))

def analyze(cid, cs):
    enriched=[]
    for c in cs:
        rgb=tuple(c['rgb']); ok=rgb_to_oklch(rgb)
        enriched.append({**c,"oklch":ok,"luminance":round(luminance(rgb),6)})
    pairs=[]
    for i in range(len(enriched)):
        for k in range(i+1,len(enriched)):
            r=contrast(tuple(enriched[i]['rgb']),tuple(enriched[k]['rgb']))
            pairs.append({"a":enriched[i]['name'],"b":enriched[k]['name'],"ratio":round(r,2),"aa":r>=4.5,"aaa":r>=7,"largeText":r>=3})
    strongest=max(pairs,key=lambda x:x['ratio']) if pairs else None
    Ls=[x['oklch']['l'] for x in enriched]; Cs=[x['oklch']['c'] for x in enriched]
    byL=sorted(enriched,key=lambda x:x['oklch']['l'])
    byC=sorted(enriched,key=lambda x:x['oklch']['c'], reverse=True)
    risks=[]
    if strongest and strongest['ratio']<3: risks.append('decorative-only-no-3to1-pair')
    elif strongest and strongest['ratio']<4.5: risks.append('no-body-text-aa-pair')
    if max(Ls)-min(Ls)<.18: risks.append('narrow-lightness-range')
    if sum(1 for x in Cs if x>.16)>=3: risks.append('multiple-high-chroma-colors-compete')
    return {
      "combinationId":cid,
      "colors":[{"name":x['name'],"hex":x['hex'],"rgb":x['rgb'],"cmyk":x['cmyk'],"lab":x['lab'],"oklch":x['oklch'],"luminance":x['luminance']} for x in enriched],
      "metrics":{"colorCount":len(enriched),"lightnessMin":round(min(Ls),4),"lightnessMax":round(max(Ls),4),"lightnessRange":round(max(Ls)-min(Ls),4),"chromaAverage":round(sum(Cs)/len(Cs),4),"chromaMax":round(max(Cs),4)},
      "contrast":{"pairs":pairs,"strongest":strongest,"aaPairCount":sum(p['aa'] for p in pairs),"aaaPairCount":sum(p['aaa'] for p in pairs)},
      "roleCandidates":{"darkAnchor":byL[0]['name'],"lightAnchor":byL[-1]['name'],"accentCandidates":[x['name'] for x in byC[:2]]},
      "riskFlags":risks,
      "source":{"status":"DERIVED_FROM_PROVIDED_DATASET"}
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source'); ap.add_argument('--out',required=True); args=ap.parse_args()
    data=json.loads(Path(args.source).read_text(encoding='utf-8'))
    colors=normalize(data); combos=reconstruct(colors)
    result={"source":str(args.source),"colorCount":len(colors),"combinationCount":len(combos),"expectedHistoricalCount":348,"completeHistoricalSet":len(combos)==348,"combinations":[analyze(cid,cs) for cid,cs in combos.items()]}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True); Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"Analyzed {len(colors)} colors / {len(combos)} combinations -> {args.out}")
    if len(combos)!=348: print('WARNING: input does not reconstruct all 348 historical combinations; verify dataset snapshot/provenance.')
if __name__=='__main__': main()
