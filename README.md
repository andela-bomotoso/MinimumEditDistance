# Minimum Edit Distance
In this project, I wrote a small python program that constructs the minimum cost table (using dynamic programming), it is enhanced with backtracing "pointers" to output edit operations.
### Inputs

The input consists of sets of words (one set per line in ***lowercase***) for which the mininmum edit distance should be calculated. The first word in each line is the ***target*** word. All other words in the line are source words that must be transformed to the target word (using the minimum edit distance algorithm). The input file must be named ***words.txt***. Two additional files are provided (in the same format):

* _***costs.csv***_ - a comma-delimited file containing the Levenshtein substitution costs for lowercase alphabet
