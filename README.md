# ExtWikilinks
ExtWikilinks is a dataset, obtained from http://www.iesl.cs.umass.edu/data/wiki-links using enrichment of CoreNLP and Elasticsearch .

Download at: ....

# Purpose

Original **Wikilinks**  dataset contains single entity per sentence, it is not enough to build state of the art named entity linking system, since context of entity may contain a valuable information.
More over, it may take a lot of time to apply POS-tagging to 40 million of sentences, so, this information already included into this extended dataset.

# Enrichment

There are two main mechanism involved into enrichment of **Wikilinks** dataset: CoreNLP pipeline and searching for additional entities with Elasticsearch engine in dataset itself. Let's describe both.

## CoreNLP processing
Each text abstract in original dataset was analysed using CoreNLP library with following pipeline:
abstract divided into sentences and the sentence with mention passes through following process:
```
tokenize, ssplit, pos, lemma, parse
```
Since `parse` step involves building of tree, the result of this step was converted into groups (analogue with Chunking). As a result, each token in enriched dataset store 5 parameters:

* Token
* Lemma
* POS-tag
* Parse tag (tag, assigned by parser)
* Group id

Previous and next sentence are also stored in dataset, but in raw way.

## Elasticsearch processing
In order to enrich sentences with additional links, each (except for stop words) Noun Phrase (NP) extracted on CoreNLP step was searched in mentions of original dataset (with respect to context). It is likely, that single entity have similar mentions in text, but ambiguity may appear in this case. Because of this all search results are stored in extended dataset with minimal threshold. Each additional mention contains information about hits count and average search score. 

# Storage format
Dataset consist of 79 protobuf files 500 000 sentence each compressed with tar gz. You can use following command to extract content:
```
tar -xzvf archive_name.tgz
```
Each protobuf file consists of protobuf encoded "messages" separated by the length of next message:
```
[varbyte(length of msg1)] [msg1] [varbyte(length of msg2)] [msg2] ...
```
You can find description of used protobuf in `sentence.proto` file.

For reading messages from this protobuf you can use `parseDelimitedFrom` in Java or `streamFromDelimitedInput` in Scala. Ruby example is also available in `reader.rb` file.

# Basic statistics

Number of sentences: 40 million
Number of unique entities: 2 million

# Example of extended sentence

![Alt text](/result_dataset.png)

Other sentence example (in json)

 ```json
{
    "sent": "Isaac Asimov advocated something like that with his \"Three Laws.\"",
    "mentions": [
      {
        "id": 0,
        "resolver": "wikilink", <-- original mention
        "text": "Isaac Asimov",
        "position": {
          "fromPos": 0,
          "toPos": 13
        },
        "context": {
          "size": -1,
          "left": "goals and I would say therefore at that point lets put a chip in their brain to shut them off if they get murderous thoughts.",
          "right": "advocated something like that with his \"Three Laws.\"  I say hey, put a chip in their brain to shut them off if they start"
        },
        "concepts": [
          {
            "link": "http://en.wikipedia.org/wiki/Isaac_Asimov",
            "hits": 1,
            "avgScore": 1,
            "maxScore": 1,
            "minScore": 1,
            "avgNorm": 1,
            "avgSoftMax": 1
          }
        ]
      },
      {
        "id": 2,
        "resolver": "elastic", <-- mention, detected by search
        "text": "Isaac Asimov",
        "position": {
          "fromPos": 0,
          "toPos": 12
        },
        "params": {
          "sum_weight": 1.4788535592903926,
          "avg_wight": 0.7394267796451963,
          "max_wight": 0.7675390229334701,
          "word_count": 2
        },
        "context": {
          "size": 3,
          "left": "",
          "right": "advocated something like"
        },
        "concepts": [
          {
            "link": "http://en.wikipedia.org/wiki/Isaac_Asimov",
            "hits": 23,
            "avgScore": 9.063705444335938,
            "maxScore": 9.063705444335938,
            "minScore": 9.063705444335938,
            "avgNorm": 0.3333333333333333,
            "avgSoftMax": 0.3333333333333333
          }
        ]
      },
      {
        "id": 3,
        "resolver": "elastic",
        "text": "Three Laws",
        "position": {
          "fromPos": 53,
          "toPos": 63
        },
        "params": {
          "sum_weight": 1.2180295766124987,
          "avg_wight": 0.6090147883062493,
          "max_wight": 0.7447375343930597,
          "word_count": 2
        },
        "context": {
          "size": 3,
          "left": "with his ``",
          "right": ". ''"
        },
        "concepts": [
          {
            "link": "http://en.wikipedia.org/wiki/Clarke's_three_laws",
            "hits": 4,
            "avgScore": 7.716668963432312,
            "maxScore": 7.717005729675293,
            "minScore": 7.715658664703369,
            "avgNorm": 0.20000193963662358,
            "avgSoftMax": 0.20001494353287008
          },
          {
            "link": "http://en.wikipedia.org/wiki/Three_Laws_of_Robotics",
            "hits": 18,
            "avgScore": 7.71663154496087,
            "maxScore": 7.717005729675293,
            "minScore": 7.715658664703369,
            "avgNorm": 0.20000096981831178,
            "avgSoftMax": 0.20000745941944043
          }
        ]
      }
    ],
    "parser_name": "CoreNLP",
    "parse_result": [
      {
        "token": "Isaac",
        "lemma": "Isaac",
        "pos_tag": "NNP",
        "parserTag": "NP",
        "group": 0,
        "mentions": [
          0,
          2
        ]
      },
      {
        "token": "Asimov",
        "lemma": "Asimov",
        "pos_tag": "NNP",
        "parserTag": "NP",
        "group": 0,
        "mentions": [
          0,
          2
        ]
      },
      {
        "token": "advocated",
        "lemma": "advocate",
        "pos_tag": "VBD",
        "parserTag": "VBD",
        "group": 1
      },
      {
        "token": "something",
        "lemma": "something",
        "pos_tag": "NN",
        "parserTag": "NP",
        "group": 2
      },
      {
        "token": "like",
        "lemma": "like",
        "pos_tag": "IN",
        "parserTag": "IN",
        "group": 3
      },
      {
        "token": "that",
        "lemma": "that",
        "pos_tag": "DT",
        "parserTag": "NP",
        "group": 4
      },
      {
        "token": "with",
        "lemma": "with",
        "pos_tag": "IN",
        "parserTag": "IN",
        "group": 5
      },
      {
        "token": "his",
        "lemma": "he",
        "pos_tag": "PRP$",
        "parserTag": "NP",
        "group": 6
      },
      {
        "token": "``",
        "lemma": "``",
        "pos_tag": "``",
        "parserTag": "``",
        "group": 7
      },
      {
        "token": "Three",
        "lemma": "three",
        "pos_tag": "CD",
        "parserTag": "NP",
        "group": 8,
        "mentions": [
          3
        ]
      },
      {
        "token": "Laws",
        "lemma": "law",
        "pos_tag": "NNS",
        "parserTag": "NP",
        "group": 8,
        "mentions": [
          3
        ]
      },
      {
        "token": ".",
        "lemma": ".",
        "pos_tag": ".",
        "parserTag": ".",
        "group": 9
      },
      {
        "token": "''",
        "lemma": "''",
        "pos_tag": "''",
        "parserTag": "''",
        "group": 10
      }
    ],
    "prevSentence": "goals and I would say therefore at that point lets put a chip in their brain to shut them off if they get murderous thoughts. ",
    "nextSentence": "  I say hey, put a chip in their brain to shut them off if they start"
  }
 ```
# Citations


```
@techreport{singh12:wiki-links,
      author    = "Sameer Singh and Amarnag Subramanya and Fernando Pereira and Andrew McCallum",
      title     = "Wikilinks: A Large-scale Cross-Document Coreference Corpus Labeled via Links to {Wikipedia}",
      institute = "University of Massachusetts, Amherst",
      number    = "UM-CS-2012-015",
      year      = "2012"
}
```

```
@InProceedings{manning-EtAl:2014:P14-5,
	author = {Manning, Christopher D. and Surdeanu, Mihai and Bauer, John and Finkel, Jenny and Bethard, Steven J. and McClosky, David},
	title = {The {Stanford} {CoreNLP} Natural Language Processing Toolkit},
	booktitle = {Association for Computational Linguistics (ACL) System Demonstrations},
	year = {2014},
	pages = {55--60},
	url = {http://www.aclweb.org/anthology/P/P14/P14-5010}
}
```
