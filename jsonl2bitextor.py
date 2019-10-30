import sys
import json_lines
import base64
import argparse
import lzma
import dateutil.parser
import gzip

oparser = argparse.ArgumentParser(
    description="Tool that transforms a JSON file containing news pieces with some metadata to the pre-processing format used in Bitextor")
oparser.add_argument('newsfile', metavar='FILE', nargs='?',
                     help='JSON file to be read (if undefined, the script reads from the standard input)',
                     default=None)
oparser.add_argument("--lang", help="Two-characters-code for language of the documents in the file to be processed", dest="lang", required=True)
oparser.add_argument("--url-prefix", help="Prefix of the URL that will be used to create the pseudo URL to store in the file url.gz that will consist of the concatenation of this prefix and the id in the JSON file for every news piece", dest="urlprefix", required=True)
oparser.add_argument("-o", "--output-path", help="Output path where the preprocessing files for Bitextor (url.xz, plain_text.xz, date.xz, etc.) will be stored", dest="opath", required=True)

options = oparser.parse_args()

json_file=gzip.open(options.newsfile, "rb")
with lzma.open(options.opath+"url.xz", 'w') as urlfile, lzma.open(options.opath+"plain_text.xz", 'w') as bodyfile, lzma.open(options.opath+"date.xz", 'w') as datefile:
    for newspiece in json_lines.reader(json_file):
        body=base64.b64encode(str.encode(newspiece["headline"]+"\n"+newspiece["body"]))
        date=dateutil.parser.parse(newspiece["firstPublished"])
        url=options.urlprefix+newspiece["id"]
            
        urlfile.write(str.encode(url+"\n"))
        datefile.write(str.encode("%04d%02d%02d\n" % (date.year,date.month,date.day)))
        bodyfile.write(str.encode(body.decode("utf-8")+"\n"))