# Evaluating the Performance of Computational Methods for Language Comparison in SEALanguages.

This tutorial supplements the study “Evaluating the Performance of Computational Methods for Language Comparison in SEALanguages”. In this tutorial, we explain in detail how our workflow can be tested and applied.

We start by installing the dependencies from the command-line. To do so, we first download the code and the data from the website and execute the following command-lines. 

```{.bash}
$ cd evaluation-paper
$ pip install -r requirements.txt
$ pip install scikit-bio
```

The stand-alone software `tqDist` was applied to compute the *normalized quartet distance (NQD)* from two given phylogenies. The [`tqDist` website](https://users-cs.au.dk/cstorm/software/tqdist/) gives instructions on the installation and usages.

## The entire process in a shell script

```{.bash}
$ % Annotate morphemes on the EDICTOR interface.
$ cldfbench download liusinitic/lexibank_liusinitic.py
$ python cognate-set-comparison.py
$ python cross-semantic-cognate-statistics.py
% Inspect the morpheme annotation on the EDICTOR interface (optional). 
% If users did change the annotation, please download the `TSV` file again.
$ python lexical-distances.py
$ python analyze-distances.py --nqd
```

The following sections introduce each step in detail.

## Morpheme annotation
The [tutorial](https://pad.gwdg.de/ouxXcKnXTnaY7aAspf8E4w?view) which accompanies Wu et al. (2020) covers the essential functions of the EDICTOR interface. In this tutorial, we show how one can use the EDICTOR interface to edit the morpheme annotation. Follow our previous pipeline to prepare the data in a `Wordlist` format.

**Show the morpheme annotation column**

Click *Select Columns > MORPHEMES* to open the morpheme annotation column. The default setting of the morphemes is the non-bold text. The tag is the same as the gloss, and the amount of the morpheme tags is equal to the morphemes in the *TOKENS* column.

![](https://pad.gwdg.de/uploads/upload_512eb3d88d1346dddc8db9a19d9f56b2.png)

**Edit the morpheme annotation**

Left click the mouse at the target entry to enable the edit mode. 

![](https://pad.gwdg.de/uploads/upload_ce943f096a8abc668b7658dcc8848281.png)

As shown in the figure below, we use concise tags to annotate the morphemes.

![](https://pad.gwdg.de/uploads/upload_fcd38c54486891da0eaff1bed5fb35da.png)

**Highlight the salient morphemes**

Right click the mouse at the target entry to turn the salient morpheme into bold font.

![](https://pad.gwdg.de/uploads/upload_bdbaed5cbaf3ce7bfdc6fa69db255d61.png)

The figure below shows how it looks like once all the entries are annotated, and the salient morphemes are highlighted. It does not have to be one morpheme per lexical entry. As shown in the figure, there are lexical entries with both or all morphemes are highlighted.

![](https://pad.gwdg.de/uploads/upload_114e7ff9dc1ec8b68b28641f163e0a4a.png)

**Save and download**

Once all the tasks are completed, press the *Save* icon and then press the *Download* icon.

![](https://pad.gwdg.de/uploads/upload_e5771ea2b475fae38a3514e43e03f588.png)

## Evaluation stage.

We first convert the partial cognates to full cognates with **"loose"** and **"strict"** conversion methods via LingPy's `add_cognate_ids` function. And then we test the harmony (agreement) between  **"loose"** and **"strict"** cognate sets which are derived from **"loose"** and **"strict"** conversion methods correspondingly. This evaluation aims to detect the extreme cases in which the conversion of partial to full cognates causes trouble. The outputs includes a screen output and a `TSV` file.

```python
python cognate-set-comparison.py
```

**The screen output is shown as below**

| Concept  | Precision | Recall   | F-Score | Chinese       | 
| -------- | --------- | -------- |-------- |-------------  |
|  knee    |    1.00   |  0.08    |  0.15   |膝,膝蓋,簸棱盖  |
|  child   |    1.00   |  0.15    |  0.26   |孩,小孩,小嘎    | 
|  neck    |    1.00   |  0.18    |  0.31   |脖子,脖颈子,頸項| 
|   ...    |    ...    |   ...    |  ...    |        ...    |

The script `cross-semantic-cognate-statistics.py` evaluates the concepts' score via the cross-semantic cognate statistics. For example, the morpheme *water* is frequently seen in compound words in Southeast Asian languages, such as *saliva (mouth water)*, *tear (eye water)* and *environment (water earth, lit. 水土). Since the *water* has such a good compounding ability, the concepts whichever contain *water* should receive higher scores of cross-semantic cognate statistics.

```python
python cross-semantic-cognate-statistics.py
```

Bearing the above working principle in mind, we design the script to list out the concepts from low scores to heigh scores. The screen output is shown as: 

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

# Derive distance matrices from the full cognate sets

The script `lexical-distances.py` reports the distance matrices which derive from the four types of full cognate sets, namely, "loose", "strict", "greedy", and "salient" cognate sets. Please note that this script only takes into account concepts with F-scores lower than 0.8.

```python
python lexical-distances.py 
```

# Basic statistics

The script `analyze-distances.py` calculates four different statistics:
- The correlation between the cross sematnic cognate statistics and the cognate set comparison.
- The Mantel test
- The Neighbor-joining trees
- The Generalized Robinson-Foulds Distance (GRF)
- The Normalized Quartet Distance (NQD)

```python
python analyze-distances.py 
```

Additionally, adding the argument `--nqd` calculates the NQD distance.

```python
python analyze-distances.py --nqd
```