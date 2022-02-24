# Evaluating the Performance of Computational Methods for Language Comparison in South-East-Asian Languages

This tutorial supplements the study "Evaluating the Performance of
Computational Methods for Language Comparison in SEALanguages". In this
tutorial, we explain in detail how our workflow can be tested and applied.

We start by installing the dependencies from the command-line. To do so, we
first download the code and the data from the website and execute the following
command-lines. 

```{.bash}
$ cd evaluation-paper
$ pip install -r requirements.txt
```

You also need to install the data package `liusinitic`:

```
$ pip install -r liusinitic
```

The stand-alone software `tqDist` was applied to compute the *normalized
quartet distance (NQD)* from two given phylogenies. The [`tqDist`
website](https://users-cs.au.dk/cstorm/software/tqdist/) gives instructions on
the installation and usages.

The stand-alone softare `MrBayes` was used to compute the Bayesian phylogenies. The installation instruction can be found on [MrBayes website](https://nbisweden.github.io/MrBayes/download.html).

## Summary of all Scripts

The following summary shows all scripts that you can run at once to replicate the studies discussed in the paper.

```
$ python cognate-set-comparison.py
$ python cross-semantic-cognate-statistics.py
$ python lexical-distances.py
$ python analyze-distances.py --nqd
$ python plot-distances.py
$ Rscript step9-maximum-likelihood-tree.R
```

## Morpheme Annotation with the Help of the EDICTOR

Assuming that you are familiar with the basic features of the EDICTOR, you can
annotate morpheme glosses in your data for saliency by first making sure
morpheme glosses have been added to your data (see our file at
`liusinitic/raw/liusinitic.tsv` for an example). When you load your data in
the EDICTOR interface, you can then toggle the individual morpheme glosses for
each word by right-clicking the morpheme gloss with the mouse. Check again our
sample file to see how we have done this for the current dataset on Chinese
dialects.


## Comparing Cognate Sets

We first convert the partial cognates to full cognates with **"loose"** and
**"strict"** conversion methods via LingPy's `add_cognate_ids` function. And
then we test the difference between  **"loose"** and **"strict"**
cognate sets which are derived from **"loose"** and **"strict"** conversion
methods respectively. This evaluation aims to detect the extreme cases in
which the conversion of partial to full cognates causes trouble. The output is written to a TSV file and also shown on the terminal. 

To run this study, simply type:

```
$ python cognate-set-comparison.py
```
This will yield the following output on screen.

| Concept  | Precision | Recall   | F-Score | Chinese       | 
| -------- | --------- | -------- |-------- |-------------  |
|  knee    |    1.00   |  0.08    |  0.15   |膝,膝蓋,簸棱盖  |
|  child   |    1.00   |  0.15    |  0.26   |孩,小孩,小嘎    | 
|  neck    |    1.00   |  0.18    |  0.31   |脖子,脖颈子,頸項| 
|   ...    |    ...    |   ...    |  ...    |        ...    |

Our second analysis looks at cross-semantic cognates and checks how often
individual cognate sets recur across different meaning slots.
For example, the morpheme *water* is
frequently seen in compound words in Southeast Asian languages, such as *saliva
(mouth water)*, *tear (eye water)* and *environment* (water earth, lit. 水土).
Since *water* has such a good compounding ability, the concepts whichever
contain *water* should receive higher scores in our analysis of cross-semantically recurring cognates.

To run this code, simply type:

```
$ python cross-semantic-cognate-statistics.py
```

High scores indicate high variation with respect to cross-semantic partial cognate sets.

The output is given in part in the following table.

| Concept  | Scores   | Flag     | Chinese character| 
| -------- | -------- | -------- | ---------------- |
| back     | 0        |          | 背,脊背,背骶身    |
| bad      | 0        |          | 壞,恘,毛         |
| ...      | ...      | ...      |  ...             |
| nose     | 3.45455  | !derivation! | 鼻子,鼻,鼻孔  |
| rope     | 3.625    | !derivation! | 繩,繩子,繩索   |
| seed     | 3.71053  | !derivation! | 种子,种籽,种   |
| head     | 3.90909  |          |    頭,得腦        |
| belly    | 3.95     | !derivation! |  肚子,肚皮,肚  |

# Deriving Distance Matrices from Cognate Sets

The script `lexical-distances.py` reports the distance matrices which derive
from the four types of full cognate sets, namely, "loose", "strict", "greedy",
and "salient" cognate sets. Please note that this script only takes into
account concepts with F-scores lower than 0.8.

```
$ python lexical-distances.py 
```

# Rooting the Neighbor-Joining Trees

For some visualizations, we use rooted trees, for this, we use the MAD tool
(Kümmel Tria et al. 2017), which we downloaded from
https://www.mikrobio.uni-kiel.de/de/ag-dagan/ressourcen. The tool is available
as a commandline tool to root trees in Newick format for R and Python. Since it
is freely distributed, we add it to this repository (see folder `dependencies`)
and explicitly quote the original study in our paper. Rooted trees are provided
with the suffix `.rooted` in the folder `results`. 

On the commandline, you can root a tree with the Python version as follows:

```
$ python dependencies/mad.py results/common.tre
```


# Statistics and Tree Comparison

The script `analyze-distances.py` calculates four different statistics:
* the correlation between the cross semantic cognate statistics and the cognate set comparison
* the Mantel test
* the Generalized Robinson-Foulds Distance (GRF)
* the Normalized Quartet Distance (NQD)

```
$ python analyze-distances.py 
```

Additionally, adding the argument `--nqd` calculates the NQD distance.

```
$ python analyze-distances.py --nqd
```

# Visualizing the Distance Matrices

To visualize the distance matrices, simply use the following command:

```
$ python plot-distances.py
```

Results are written to the folder `plots`.
