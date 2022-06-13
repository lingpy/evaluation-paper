# Evaluating the Performance of Computational Methods for Language Comparison in South-East-Asian Languages

## Installation

In order to install all code required to run the Python analyses, just type:

```
$ pip install -r requirements.txt
```

In order to run the MrBayes analyses, you need to install the MrBayes software.

## Preparing the Wordlist File

Our data is curated within the Lexibank repository and can be accessed in the form of a CLDF datasets at https://github.com/lexibank/liusinitic (we use version 1.3 in our experiments, archived with Zenodo under DOI [10.5281/zenodo.6634125](https://doi.org/10.5281/zenodo.6637640)).

In order to run the code shown here, you won't need this repository, as we already converted the CLDF data into our LingPy wordlist format we need for the analysis. This file can be found at `edictor/liusinitic.tsv`. 

However, if you want to replicate this step of the workflow, you can do so by cloning the GitHub repository and checking out the relevant version:

```
$ git clone https://github.com/lexibank/liusinitic/
$ cd liusinitic
$ git checkout v1.2
```

Alternatively, you can download the archived version and place it into this repository folder.

Having done this, you can convert the data with the help of the `pyedictor` tool, which you should install first, and the Makefile.

```
$ pip install pyedictor
$ make wordlist
```

This command will add strict, loose, common, and salient cognate identifiers from the partial cognate sets. The methods used for the conversion are described in detail in our paper. 

The conversion to strict and loose cognates is implemented in LingPy (https://github.com/lingpy/lingpy, module `compare.partial`, as part of the `Partial` class). The new conversion methods for common and salient cognates are implemented in LingRex (https://github.com/lingpy/lingrex, as part of the `cognates` module).

## Running Python Analysis with the Makefile

In order to run the analysis up the creation of the Nexus files, you can just use our Makefile, or check the commands that are provided in there.

We have numerated the commands, so typing `make part-one` will trigger the first analysis, `make part-two` will trigger the second analysis, etc.

So you can just type:

```
$ make part-one
$ make part-two
$ make part-three
$ make part-four
$ make part-five
$ make part-six
```

## Summary of all Scripts

The following summary shows all scripts that you can run at once to replicate the studies discussed in the paper.

```
$ python cognate-set-comparison.py
$ python cross-semantic-cognate-statistics.py
$ python lexical-distances.py
$ python plot-distances.py
$ python analyze-distances.py
$ python export-nexus.py
```



### 1 Comparing Cognate Sets

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

### 2 Deriving Distance and Comparing Matrices from Cognate Sets

The script `lexical-distances.py` reports the distance matrices which derive
from the four types of full cognate sets, namely, "loose", "strict", "greedy",
and "salient" cognate sets. Please note that this script only takes into
account concepts with F-scores lower than 0.8.

```
$ python lexical-distances.py 
```

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

To visualize the distance matrices, simply use the following command:

```
$ python plot-distances.py
```

Results are written to the folder `plots`.

### 3 Bayesian Phylogenetic Analysis

To export the nexus files for conducting Bayesian phylogenetic analysis, type the following command in the terminal:

```
$ python export-nexus.py
```

The files can be found in the folder `bayes`. To run individual analyses from MrBayes, you best open the interactive mode in MrBayes and then run `execute filename.nexus`. Afterwards, you type `mcmc` and this should trigger the analysis, which can well take some time, depending on the speed of your machine.
 
