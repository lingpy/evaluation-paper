# Evaluating the Performance of Computational Methods for Language ccComparison in SEALanguages.
This tutorial supplements the study “Evaluating the Performance of Computational Methods for Language ccComparison in SEALanguages”. In this tutorial, we explain in detail, how our workflow can be tested and applied.

We start by installing the dependencies from the commandline. In order to do so, we first download the code that we will use with help of `git`.

```{.bash}
$ git clone https://github.com/lingpy/evaluation-paper.git
$ cd evaluation-paper
```

## Morpheme annotation
The [tutorial](https://pad.gwdg.de/ouxXcKnXTnaY7aAspf8E4w?view) which accompanies Wu et al. (2020) covers the basic functions of the Edictor web applications. In this tutorial, we show how one can use Edictor web application to edit the morpheme annotation. The example dataset `liusinitic.tsv` can be found in the [github repository](https://github.com/lingpy/evaluation-paper).

**Show the morpheme annotation column**

Click *Select Columns > MORPHEMES* to open the morpheme annotation column. The default setting of the morphemes is the non-bold text. The tag is the same as the gloss, and the amount of the morpheme tags is equal to the morphemes in *TOKENS* column.

![](https://pad.gwdg.de/uploads/upload_512eb3d88d1346dddc8db9a19d9f56b2.png)

**Edit the morpheme annotation**

Left click the mouse at the target entry to enable the edit mode. 

![](https://pad.gwdg.de/uploads/upload_ce943f096a8abc668b7658dcc8848281.png)

As shown in the figure below, we use concise tags to annotate the morphemes.

![](https://pad.gwdg.de/uploads/upload_fcd38c54486891da0eaff1bed5fb35da.png)

**Highlight the salient morphemes**

Right click the mouse at the target entry to turn the salient morpheme into bold font.

![](https://pad.gwdg.de/uploads/upload_bdbaed5cbaf3ce7bfdc6fa69db255d61.png)

Figure below shows how it looks like once all the entires are annotated and the salient morphemes are highlighed. It does not have to be one morpheme per lexical entry. As shown in the figure, there are lexical entries with both or all morphemes are highlighted. 

![](https://pad.gwdg.de/uploads/upload_114e7ff9dc1ec8b68b28641f163e0a4a.png)

**Save and download**

Once all the tasks are completed, press the *Save* icon and then press the *Download* icon.

![](https://pad.gwdg.de/uploads/upload_e5771ea2b475fae38a3514e43e03f588.png)

## From partial cognate sets to full cognate sets


In addition to the distance matrices, the script produces a new Wordlist file `liusinitic.word_cognate.tsv` which stores all the word cognate sets.

## Evaluation stage.

To test the harmony (agreement) between different word cognate conversion methods.  

```python
python3 concept_bcube.py
```

**The output is as below**

| Concept  | Precision | Recall   | F-score | Chinese       | 
| -------- | --------- | -------- |-------- |-------------  |
|  knee    |    1.00   |  0.08    |  0.15   |膝,膝蓋,簸棱盖  |
|  child   |    1.00   |  0.15    |  0.26   |孩,小孩,小嘎    | 
|  neck    |    1.00   |  0.18    |  0.31   |脖子,脖颈子,頸項| 
|   ...    |    ...    |   ...    |  ...    |        ...    |

The script `colexifications.py` evaluates the colexification scores of concepts. For example, the morpheme *water* is frequently seen in compound words in Southeast Asian languages, such as *saliva (mouth water)*, *tear (eye water)* and *environment (water earth, lit. 水土). Since the *water* has such a good compounding ability, the concepts whichever contain *water* should receive a higher colexification scores.  

```python
python3 colexifications.py
```

Bearing the above working principle in mind, we design the script to list out the concepts with low colexification scores to heigh colexification scores.  

It is a standard output which directly print on the screen:

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

The script `lexicostatistical.py` reports the distance matrices which derive from the three types of word cognate sets, namely, loose, strict and greedy cognate sets. Please note that this script only takes into account the top 100 concepts with lowest F-scores.

```python
python3 lexicostatistical.py 
```

Execute the `lexicostatistical.py` with `add_salient` argument will generate four different distance matrices, including, loose, strict, greedy and salient cognate sets. 

```python
python3 lexicostatistical.py add_salient
```
# Basic statistics

The script `concept_statistics.py` calculate three different statistics:
- The correlation between colexification rankings and the F-scores.
- The Mantel tests
- The Neighbor-join trees

```python
python3 concept_statistics.py 
```