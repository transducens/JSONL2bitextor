# JSONL2bitextor
This repository provides a script to extract information from a JSONL file containing a list of documents with their headlines and a publication data, into a format that the tool [bitextor](https://github.com/bitextor/bitextor) can read to produce a segment-aligned parallel corpus from them.

## Dependences
Before running the script provided in this repository, it is necessary to install some Python dependences. To do so, run the command:
```shell
pip3 install tldextract json_lines
```

## JSONL format
[JSONL](http://jsonlines.org/) is a text format that that contains one JSON object per line. The script in this repository expects every object in a JSONL document to contain the following fields:
* id: an ID string that identifies the JSON object
* headline: headline or title of the document
* body: content text of the document in plain text
* firstPublished: date and time in which the document was writen or published

## Bitextor format
After running the script, a directory structure will be created containing the path `data/preprocess/XX/w2p/bitextorlang/YY`, where `XX` is the name of the domain and `Y` is a language code; both are specified at the time of running the script. Inside this path, three compressed fields will be stored: `date.xz`, `plain_text.xz`, and `url.xz`. These are the files that Bitextor will use to produce the final corpus. These files will contain:
* `date.xz`: the publication date of each JSON object
* `plain_text.xz`: the concatenation of the headline and the body of the boject
* `url.xz`: a synthetic URL obtainied from the concatenation of a web domain provided by the user at the time of running the script and the id of the object

## Example task
Supose that we have two files, `am.jsonl.gz` and `en.jsonl.gz`, in which we have a collection of documents in Amharic and English, respectively, and we want to extract a parallel corpus from them using Bitextor. To do so, we will first need to extract and prepare the data in our JSONL files to be used by Bitextor:
```shell
mkdir preprocessing_data
python jsonl2bitextor.py --lang am --url-prefix "http://bbc.com/" -o json2parallel_experiment/ am.jsonl.gz
python jsonl2bitextor.py --lang en --url-prefix "http://bbc.com/" -o json2parallel_experiment/ en.jsonl.gz
```
As a result, we will have a directory structure `bitextor_preprocessing_data/preprocess/bbc/w2p/bitextorlang/am` and `json2parallel_experiment/preprocessing_data/preprocess/bbc/w2p/bitextorlang/en`, and each language folder (`am` and `en`) will contain files: `date.xz`, `plain_text.xz`, and `url.xz`.

Install Bitextor from branch `JSONnews`:
```shell
git clone https://github.com/bitextor/bitextor.git --recursive
cd bitextor
git checkout JSONnews
```
Follow the instructions in the file `README.md` for installation.

Two more things will be needed to run Bitextor: a machine translation system between the languages to be aligned, Amharic to English, in this case, and a configuration file such as the following:

```yaml
bitextor: /home/user/bitextor_JSON2bitextor
permanentDir: /home/user/json2parallel_experiment/permanent
dataDir: /home/user/json2parallel_experiment/preprocessing_data
transientDir: /home/user/json2parallel_experiment/transient
documentAligner: externalMT
alignerCmd: "bash /home/user/am-en-smt/translate.sh"
bleualign: true
lang1: am
lang2: en
date_window: 7
wordTokenizers: {
  'am': 'bash /work/espla/BBC_corpus/bitextor/amharic_word_split.sh',
  'en': '/work/espla/BBC_corpus/bitextor/preprocess/moses/tokenizer/tokenizer.perl -q -b -a -l en'
}

sentenceSplitters: {
  'am': 'bash /home/user/resources/amharic_sent_split.sh',
  'en': '/home/user/resources/moses/ems/support/split-sentences.perl -q -b -l en'
}
```
In this example config file, Bitextor has been installed at `/home/user/bitextor_JSON2bitextor`, and the working directory (where all the data will be stored) is at `/home/user/json2parallel_experiment/`. A machine translation system has been trained and the script `bash /home/user/am-en-smt/translate.sh` reads text in Amharic from the standard input, internally runs the MT system (including tokenization and detokenization) and writes the English translation to the standard output. Bleualign is activated for sentence alignment, and commands for word tokenization and sentence splitting are provided for both languages.

Bitextor can be run with the following command:
```shell
/home/user/bitextor_JSON2bitextor/bitextor.sh -s config.yaml -j 4
```
where `config.yaml` is the example config file and `-j` allows to define the maximum number of threads that can be used at the same time for parallelization. After running Bitextor, the resulting corpus will be stored in `/home/user/json2parallel_experiment/permanent/am-en-sent.xz`. The format of the corpus will be a TSV with 5 fields: URL1, URL2, sentence1, sentence2, bleualign_score. This corpus can be later filtered using either [Bicleaner](https://github.com/bitextor/bicleaner) or [LASER](https://github.com/facebookresearch/LASER).

## Acknowledgements
Developed by Universitat d'Alacant as part of its contribution to the [GoURMET](https://gourmet-project.eu/) project, which  received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 825299.

