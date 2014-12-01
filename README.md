TEXATA-2014-Finals
==================

Python code used in the finals of the TEXATA 2014 competition

Text of presentation follows:

Problem:  
How to improve relevance of customer issue search results in response to customer query or issue description
Many advantages to greatly improved search results accuracy
Customer gets solution faster

Solution:  
Problem resolutions are verbs acting on nouns (roughly)
Separate nouns and verbs from text of description and replies of forum entries and tokenize
Use fuzzy-match of incoming customer search request or issue description with the tokenized forum entries
Return urls with top match results
Tools:  Python, and libraries multiprocess, NLTK, FuzzyWuzzy, “map reduce”

Innovations:  
If search results are accurate enough, customer gets solution faster
Very accurate issue resolution search results have other applications
“Unanswered” questions can be sent highly relevant solutions
Ping authors who contributed the solutions to come to assistance
