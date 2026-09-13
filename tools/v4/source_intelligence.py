#!/usr/bin/env python3
"""CWI v4 source intelligence CLI.

Uses documented JSON APIs only. Restricted/manual sources are never scraped.
Python stdlib only.
"""
from __future__ import annotations
import argparse, json, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/'data/v4/source_registry.json'
CACHE=ROOT/'cache/v4'
CACHE.mkdir(parents=True, exist_ok=True)

def load_registry():
    return json.loads(REGISTRY.read_text(encoding='utf-8'))

def source(source_id):
    for s in load_registry():
        if s['id']==source_id: return s
    raise SystemExit(f'Unknown source: {source_id}')

def get_json(url, timeout=15):
    req=urllib.request.Request(url, headers={'User-Agent':'CreativeWebIntelligence-v4/1.0 (+metadata research; license-aware)'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f'HTTP {e.code}: {url}')
    except urllib.error.URLError as e:
        raise SystemExit(f'Network error: {e.reason}')

def save(name, payload):
    obj={'retrievedAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'payload':payload}
    p=CACHE/name
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return p

def cmd_sources(_):
    for s in load_registry():
        print(f"{s['id']:<20} {s['automation']:<42} {s['name']}")

def cmd_policy(args):
    s=source(args.source)
    print(json.dumps({k:s.get(k) for k in ['id','name','access','automation','bundlePolicy','licenseModel','guardrails','evidence']},indent=2,ensure_ascii=False))

def ensure_automated(s):
    if s['automation'] in {'restricted_no_generic_scrape','do-not-scrape-or-automate-without-consent'}:
        raise SystemExit(f"{s['name']} is restricted/manual in CWI v4. Use an official approved integration or manual selection; generic scraping is intentionally disabled.")

def cmd_icon_collections(args):
    s=source('iconify'); ensure_automated(s)
    url=s['endpoints']['base']+s['endpoints']['collections']
    data=get_json(url)
    # Keep the source response because collection objects contain author/license metadata.
    p=save('iconify-collections.json',data)
    print(json.dumps(data,indent=2,ensure_ascii=False)); print(f'cached: {p}',file=sys.stderr)

def cmd_icon_search(args):
    s=source('iconify'); ensure_automated(s)
    qs={'query':args.query,'limit':args.limit}
    if args.prefix: qs['prefix']=args.prefix
    url=s['endpoints']['base']+s['endpoints']['search'].split('?')[0]+'?'+urllib.parse.urlencode(qs)
    data=get_json(url)
    out={'source':'iconify','query':args.query,'prefix':args.prefix,'icons':data.get('icons',[]),'collections':data.get('collections',{}),'total':data.get('total',0)}
    p=save('iconify-search.json',out)
    print(json.dumps(out,indent=2,ensure_ascii=False)); print(f'cached: {p}',file=sys.stderr)

def cmd_icon_collection(args):
    s=source('iconify'); ensure_automated(s)
    url=s['endpoints']['base']+'/collection?'+urllib.parse.urlencode({'prefix':args.prefix})
    data=get_json(url)
    p=save(f"iconify-collection-{args.prefix}.json",data)
    print(json.dumps(data,indent=2,ensure_ascii=False)); print(f'cached: {p}',file=sys.stderr)

def cmd_font_catalog(args):
    s=source('fontsource'); ensure_automated(s)
    url=s['endpoints']['base']+s['endpoints']['fonts']
    data=get_json(url)
    p=save('fontsource-catalog.json',data)
    summary={'source':'fontsource','count':len(data) if isinstance(data,list) else None,'variable':sum(1 for x in data if isinstance(x,dict) and x.get('variable')) if isinstance(data,list) else None,'cache':str(p)}
    print(json.dumps(summary,indent=2,ensure_ascii=False))

def cmd_font_search(args):
    s=source('fontsource'); ensure_automated(s)
    q={}
    if args.family: q['family']=args.family
    if args.subsets: q['subsets']=args.subsets
    if args.variable is not None: q['variable']='true' if args.variable else 'false'
    if args.category: q['category']=args.category
    url=s['endpoints']['base']+s['endpoints']['fonts']
    if q: url+='?'+urllib.parse.urlencode(q)
    data=get_json(url)
    p=save('fontsource-search.json',data)
    print(json.dumps(data[:args.limit] if isinstance(data,list) else data,indent=2,ensure_ascii=False)); print(f'cached: {p}',file=sys.stderr)

def cmd_font(args):
    s=source('fontsource'); ensure_automated(s)
    base=s['endpoints']['base']
    meta=get_json(base+s['endpoints']['font'].format(id=urllib.parse.quote(args.id)))
    out={'metadata':meta}
    if meta.get('variable'):
        try: out['variable']=get_json(base+s['endpoints']['variable'].format(id=urllib.parse.quote(args.id)))
        except SystemExit as e: out['variableError']=str(e)
    p=save(f"fontsource-{args.id}.json",out)
    print(json.dumps(out,indent=2,ensure_ascii=False)); print(f'cached: {p}',file=sys.stderr)

def build_parser():
    p=argparse.ArgumentParser(description='CWI v4 source intelligence')
    sub=p.add_subparsers(dest='cmd',required=True)
    q=sub.add_parser('sources'); q.set_defaults(fn=cmd_sources)
    q=sub.add_parser('policy'); q.add_argument('source'); q.set_defaults(fn=cmd_policy)
    q=sub.add_parser('icon-collections'); q.set_defaults(fn=cmd_icon_collections)
    q=sub.add_parser('icon-search'); q.add_argument('query'); q.add_argument('--prefix'); q.add_argument('--limit',type=int,default=64); q.set_defaults(fn=cmd_icon_search)
    q=sub.add_parser('icon-collection'); q.add_argument('prefix'); q.set_defaults(fn=cmd_icon_collection)
    q=sub.add_parser('font-catalog'); q.set_defaults(fn=cmd_font_catalog)
    q=sub.add_parser('font-search'); q.add_argument('--family'); q.add_argument('--subsets'); q.add_argument('--variable',action=argparse.BooleanOptionalAction,default=None); q.add_argument('--category'); q.add_argument('--limit',type=int,default=40); q.set_defaults(fn=cmd_font_search)
    q=sub.add_parser('font'); q.add_argument('id'); q.set_defaults(fn=cmd_font)
    return p

def main():
    p=build_parser(); a=p.parse_args(); a.fn(a)
if __name__=='__main__': main()
