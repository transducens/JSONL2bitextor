# JSONL2bitextor
This repository provides a script to extract information from a JSONL file containing a list of documents with their headlines and a publication data, into a format that the tool [bitextor](https://github.com/bitextor/bitextor) can read to produce a segment-aligned parallel corpus from them.

##JSONL format
[JSONL](http://jsonlines.org/) is a text format that that contains one JSON object per line. The script in this repository expects every object in a JSONL document to contain the following fields:
* id: an ID string that identifies the JSON object
* headline: headline or title of the document
* body: content text of the document in plain text
* firstPublished: date and time in which the document was writen or published

##Bitextor format
After running the script, a directory structure will be created containing the path `data/preprocess/XX/w2p/bitextorlang/YY`, where `XX` is the name of the domain and `Y` is a language code; both are specified at the time of running the script. Inside this path, three compressed fields will be stored: `date.xz`, `plain_text.xz`, and `url.xz`. These are the files that Bitextor will use to produce the final corpus. These files will contain:
* `date.xz`: the publication date of each JSON object
* `plain_text.xz`: the concatenation of the headline and the body of the boject
* `url.xz`: a synthetic URL obtainied from the concatenation of a web domain provided by the user at the time of running the script and the id of the object

## Example task
```
python jsonl2bitextor.py --lang am --url-prefix "http://bbc.com/" -o data/preprocess/bbc/docalign/am/ data/am.jsonl.gz
```

