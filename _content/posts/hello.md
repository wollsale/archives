title: Your friendly neighborhood article generator
tags: Other Tag
poster: medias/image.jpg
slug: your-friendy-neighborhood-article-generator

# NewsGen:  Your friendly neighborhood article generator

NewsGen provides tooling to pull corpuses of articles in order to generate new
articles utlizing parts of speech tagging and markov chain natural language
generation techniques.

![image info](../medias/image.jpg)

## Generation techniques

At the core, NewsGen, uses the excellent NLTK project to parse sentences and identify parts of
speech.  Markovify is used to generate sentences, but we add a few twists.

Markov chains by default are pretty effective at creating reasonable sounding
gobbledygook, but are ineffective at creating a reasonably coherent connection
between junk sentences.  If that is a thing at all.

In order to do slightly better, we do two things:

1) Provide a mechanism to cull the corpus based on keywords to so that we have
a more coherent starting set of data.

2) Generate a lot of candidate sentences and use Levenshtein distance to
attempt to pick the most coherent candidate sentence for our generated
articles.

```
$ python3 ./newsgen.py -h
```