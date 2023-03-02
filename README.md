# educational_CQG

To add:
- generation file
- candidates (for reproducability?) and the teacher ratings (?)
  - at least the full dataset of results (ie mean and stdev of each prompt category for each metric)
- fill out read me with examples
- taxonomic defintions, metric definitions

## Project Abstract

## Control Elements - Taxonomic Categories
| Prompt | Taxonomy | Definition |
|:---:|:---:|:---:|
| remembering | Bloom's | The question should ask students to retrieve from memory a fact, term, concept, etc.. |
| understanding | Bloom's | The question should ask students to demonstrate their understanding of material by describing, explaining, comparing, interpreting, etc. |
| applying | Bloom's | The question should ask students to use the presented concepts to solve problems, or explain ideas in a different way. |
| analyzing | Bloom's | The question should ask students to break material into parts, and/or show how different ideas relate to one another. |
| evaluating | Bloom's | The question should ask students to give opinions on, make judgments about, or interpret meaning from material. |
| creating | Bloom's | The question should ask students to combine material together in a different way than it was presented. |
| beginner | Level | The question should be posed so that the correct answer is a simple span from the input context (often a single concept or a list). |
| intermediate | Level | The question should be posed so that the correct answer is a span from the input context that is more complex than a single concept (eg. an explanation or an example), or requires understanding on the part of the student to arrive at a simple answer. |
| advanced | Level | The question should be posed so that the correct answer requires a student's rephrasing of multiple parts of the input, or the answer must require independent thought. |

## Teacher Assessment Metrics
| Metric | Definition |
|:---:|:---:|
| on topic | A binary variable representing if the question is related to the context provided. In order for a question to be on topic, at least one key concept from the context passage must be referenced or mentioned in the candidate (note that the context doesn't necessarily have to contain the answer to the question on this concept). |
| grammatically correct | A binary variable representing if the question is grammatically correct. Any grammatical error (including capitalization or other minor errors) results in an ungrammatical question. |
| adherence | A binary variable representing if the question is an instance of the question type provided. This is done with the definitions of question types at the discretion of the annotator. |
| answerable | A binary variable representing if there is a text span from the context that answers the question, or that could lead to an answer with no other information required (e.g., a student's opinion about presented facts could be answerable). Note that any reasonable answer is acceptable, it does not have to be the best/most complete answer to the question. |
| useful | We define the 'usefulness metric' as a teacher's own answer to the question:  “Assume you wanted to teach about context X. Do you think candidate Y would be useful in a lesson, home work, quiz, etc.?” where X is replaced by the context passage, and Y is replaced by the candidate question.  The possible answers to this question are as follows: 
1. Not useful = The core content of the question is not useful to teach context X at all. For example, the candidate might be off topic, have logical issues, simply not a useful question to teach context X, or be otherwise unacceptable. 
2. Useful with major edits = The core content of the question is useful, but the phrasing or presentation of the candidate is not, and would require changes that take more than a minute. For example, the candidate might present an interesting idea that would be useful to teach context X, but the sentence structure is confusing and would need to be completely re-written. 
3. Useful with minor edits = The core content of the question is useful, but the phrasing or presentation of the candidate has some minor issues (e.g. grammatical errors, word choice problems) that could be fixed in less than a minute. 
4. Useful with no edits = The question is useful as is, and can be used directly without making any changes.  
Note that the question does not necessarily need to be answerable from the context or adhere to the question type in order to be considered useful. |