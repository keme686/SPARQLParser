# SPARQLParser

Python based parser for SPARQL 1.1 queries, follows SPARQL grammer defined here: (https://www.w3.org/TR/sparql11-query/#grammar)



Requirements
===
`ply`


Example
===

### Parsing
```python
from awudima.sparql import parser

textquery = "SELECT DISTINCT * WHERE {?s ?p ?o} ORDER BY ?s LIMIT 10 "
query = parser.sparql(textquery)
print(query)

```
### Traversing 

```python
from awudima.sparql import parser
from awudima.sparql import BGP, GGP, UnionGP, OptionalGP, Bind, Filter, GraphGP, ServiceGP, MinusGP, SelectQuery
textquery = """    
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?path ?link ?label 
    FROM <http://purl.obolibrary.org/obo/merged/CL> 
    WHERE {
            ?s ?p ?o.
            OPTIONAL {?s1 ?p2 ?o2}
              { ?s rdfs:subClassOf ?o .

                    OPTIONAL {
                        ?o rdfs:label ?label .
                        FILTER(LANG(?label) = "" || LANG(?label) = 'en')
                    }
                } UNION {
                    ?s owl:equivalentClass ?s1 .
                    ?s1 owl:intersectionOf ?s2 .
                    ?s2 rdf:first ?o  .

                    OPTIONAL {
                        ?o rdfs:label ?label .
                        FILTER(LANG(?label) = "" || LANG(?label) = 'en')
                    }
                }
                FILTER ( ?s != ?o )

    }
    """
query = parser.sparql(textquery)
def traverse(ggps):
    for ggp in ggps:
        if isinstance(ggp, BGP):
            print('BGP:', ggp)
        if isinstance(ggp, OptionalGP):
            i = 1
            print('OPTIONAL :')
            for u in ggp.ggps:
                if isinstance(u, GGP):
                    traverse(u.ggps)
                else:
                    print(i,': ', u)
                i += 1
        if isinstance(ggp, UnionGP):
            i = 1
            for u in ggp.ggps:
                if i == 1:
                    print(str(i) +'st UNION :')
                    if isinstance(u, GGP):
                        traverse(u.ggps)
                    else:
                        print(i,': ', u)
                else:
                    print(i , ' UNION :')
                    if isinstance(u, GGP):
                        traverse(u.ggps)
                    else:
                        print(i, ': ', u)

                i += 1

traverse(query.ggp.ggps)
print("----------------------")
print(query)

```
##### Issues

- when using keywords as variable or prefix, the parser throws exception.
- multiple filter expressions with literal constants

 


