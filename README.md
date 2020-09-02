# Minimum Edit Distance
In this project, I wrote a small python program that constructs the minimum cost table (using dynamic programming), it is enhanced with backtracing "pointers" to output edit operations.
### Inputs

The input consists of sets of words (one set per line in ***lowercase***) for which the mininmum edit distance should be calculated. The first word in each line is the ***target*** word. All other words in the line are source words that must be transformed to the target word (using the minimum edit distance algorithm). The input file must be named ***words.txt***. Two additional files are provided (in the same format):

* _***costs.csv***_ - a comma-delimited file containing the Levenshtein substitution costs for lowercase alphabet
* _***costs2.csv***_ - a comma-delimited file containing the confusion matrix substitution costs 

### Processing

The processing requiremnents include:
* The cost of insertions and deletions is 1 in all cases. Substitution costs will be read from input files.
* For each pair of source and target words, calculate the minimum edit distance (using both Levenshtein
and confusion matrix costs), and output the cost and backtrace of operations (see below for details).
* The dynamic programming table must be complete and correct. The backtrace table must capture all
possible sources for the minimum cost at each cell.
* When constructing the backtrace, randomly select any one of the possible cells that provide the
minimum cost to the cell being processed. This should be done by importing the random module, and
ensuring that all possibilities have an equal probability of being selected.

