# Folio Task 1

A project designed to fulfill the criteria specified in "Folio Task 1 - A Character Map".

> 1. You must represent the relationships between characters as a graph (either directed or undirected)
> 2. There must be at least 10 Characters on your map
> 3. Your graphical representation must feature weightings and labels on the edges and vertices respectively.
> 4. You must write an explanation of what your weighting actually represents and how you ‘measured’ this (200 word minimum). Include in your explanation any special features like directed edges, multiple edges between vertices, etc. and why you have used these.

### Addressing the Criteria

1. You must represent the relationships between characters as a graph (either directed or undirected).
	* This criterion will attempt to be addressed through the use of PyCharm to create a undirected, weighted graph of both the US Senate and House of Representatives' voting habits. Senators who vote the same way on certain bills will have weights assigned to the edges connecting them equal to the number of similar votes they have cast. It is hypothesised that Republican senators will be linked strongly to other Republican senators, and the same for Democratic senators. It is also hypothesised that senators who have states in close geographic proximity, or who are interested in the same sort of issues will also be linked more strongly.
2. There must be at least 10 Characters on your map.
	* There are currently 535 members of the 115th United States Congress. 100 of whom are part of the United States Senate and the latter 435 work in the house of representatives.
3. Your graphical representation must feature weightings and labels on the edges and vertices respectively.
	* PyCharm easily supports adding weightings and labels to edges of the graph. The weightings and labels on the edges will both be equal to the number of votes that the members of congress have cast similarly.
4. You must write an explanation of what your weighting actually represents and how you ‘measured’ this (200 word minimum). Include in your explanation any special features like directed edges, multiple edges between vertices, etc. and why you have used these.
	* This is explained further down the page.

### Justification and Explanation of Task
