import glob
import json
import multiprocessing
import subprocess

datafiles = glob.glob('./*/bills/hr/*/data.json')
datafiles.extend(glob.glob('./*/bills/s/*/data.json'))

subprocess.call(['mkdir', 'metadata'])
subprocess.call(['mv', 'field_descriptions.json', 'metadata/'])
subprocess.call(['mkdir', 'texts'])
subprocess.call(['mkdir', 'texts/raw'])

url = #


def ParseFile(datafile):
    js = json.load(open(datafile, 'r'))
    if js['summary'] is not None and js['summary']['text'] is not None:
        tmp = {}
        # Build the metadata object
        tmp['filename'] = js['bill_id']
        if 'short_title' in js and js['short_title'] is not None:
            tmp['title'] = js['short_title'].encode('utf-8')
        else:
            tmp['title'] = js['official_title'].encode('utf-8')
        tmp['chamber'] = js['bill_type']
        tmp['enacted'] = str(js['history']['enacted'])
        tmp['awaiting_signature'] = str(js['history']['awaiting_signature'])
        tmp['vetoed'] = str(js['history']['vetoed'])
        tmp['status'] = js['status']
        tmp['subjects'] = js['subjects']
        if js['subjects_top_term'] is not None:
            tmp['main_subject'] = js['subjects_top_term']
        else:
            pass
        tmp['sponsor_state'] = js['sponsor']['state']
        tmp['sponsor_name'] = js['sponsor']['name']
        tmp['sponsor_title'] = js['sponsor']['title']
        tmp['thomas_id'] = js['sponsor']['thomas_id']
        tmp['num_cosponsors'] = len(js['cosponsors'])
        tmp['date'] = js['summary']['date']
        # Create HTML for the searchstring variable
        link = '%s/%s/%s' % (url, js['congress'], js['bill_id'].split('-')[0])
        html = '<a href="%s" target="_blank">Read</a> | %s' % (link, tmp['title'])
        tmp['searchstring'] = html
        # Write the summary text to its own .txt file
        f = open('texts/raw/%s.txt' % tmp['filename'], 'w')
        f.write(js['summary']['text'].encode('utf-8'))
        f.close()
        # Return the metadata
        return tmp
    else:
        return None

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    metadata = pool.map(ParseCongressFile, datafiles)
    pool.close()

    print 'Parsing complete. Creating jsoncatalog.txt file...'
    meta = open('metadata/jsoncatalog.txt', 'w')
    for jsonobj in metadata:
        if jsonobj is not None:
            meta.write('%s\n' % json.dumps(jsonobj))
    meta.close()

    print 'Cleaning up...'
    for folder in range(93, 114):
        subprocess.call(['rm', '-rf', str(folder)])
