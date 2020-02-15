# -*- coding: utf-8 -*-
from __future__ import division, print_function

__version__ = '0.1'
__author__ = 'Kemele M. Endris'


import abc


#########################################################
###############    SPARQL Query Abstract  #################
#########################################################
class Query:
    def __init__(self, prefixes, solution_modifiers, values_clause):
        if solution_modifiers is None and not isinstance(solution_modifiers, dict):
            solution_modifiers = {}

        self.solution_modifiers = solution_modifiers
        self.prefixes = prefixes
        self.values_clause = values_clause

        self.group_by = []
        self.order_by = []
        self.having = []
        self.limit = -1
        self.offset = -1

        self.values_vars = []
        self.values_data = []

        if 'GROUP BY' in self.solution_modifiers:
            self.group_by = self.solution_modifiers['GROUP BY']
        if 'ORDER BY' in self.solution_modifiers:
            self.order_by = self.solution_modifiers['ORDER BY']
        if 'HAVING' in self.solution_modifiers:
            self.having = self.solution_modifiers['HAVING']
        if 'LIMIT' in self.solution_modifiers:
            try:
                self.limit = int(self.solution_modifiers['LIMIT'])
            except:
                self.limit = -1
        if 'OFFSET' in self.solution_modifiers:
            try:
                self.offset = int(self.solution_modifiers['OFFSET'])
            except:
                self.offset = -1

    @abc.abstractmethod
    def to_str(self):
        pass

    def modifiers_str(self):

        sm = ''
        if len(self.group_by) > 0:
            sm += "GROUP BY " + " ".join([str(g) for g in self.group_by]) + '\n'
        if len(self.order_by) > 0:
            sm += "ORDER BY " + " ".join([str(o) for o in self.order_by]) + '\n'
        if len(self.having) > 0:
            sm += "HAVING " + " ".join([str(h) for h in self.having]) + '\n'
        if self.limit > 0:
            sm += "LIMIT " + str(self.limit) + '\n'
        if self.offset > 0:
            sm += "OFFSET " + str(self.offset) + '\n'

        return sm

    def values_str(self):
        if len(self.values_clause.variables) == 0 and len(self.values_clause.values) == 0:
            return ''

        vc = "VALUES "
        if len(self.values_clause.variables) > 0:
            vc += '(' + ' '.join([str(v) for v in self.values_clause.variables]) + ') '
        else:
            vc += '()'
        if len(self.values_clause.values) > 0:
            vc += "{(" + ") (".join([" ".join([str(v) for v in d]) for d in self.values_clause.values]) + ")}"
        else:
            vc += '{}'

        return vc

    def prefixes_str(self):
        prf = ''
        for p in self.prefixes:
            if p == '[BASE]':
                prf += 'BASE : ' + self.prefixes[p] + '\n'
            elif p == '<noname>':
                prf += "PREFIX : " + self.prefixes[p] + '\n'
            else:
                prf += 'PREFIX ' + p + ": " + self.prefixes[p]  + '\n'
        return prf

    def __str__(self):
        return self.prefixes_str() + '\n' \
               + self.to_str() + '\n' \
               + self.modifiers_str() \
               + (('\n' + self.values_str()) if len(self.values_str()) > 0 else '')

    def __repr__(self):
        return self.prefixes_str() + '\n' \
               + self.to_str() + '\n' \
               + self.modifiers_str() + '\n' \
               + (('\n' + self.values_str()) if len(self.values_str()) > 0 else '')

#########################################################
###############    Select Query         #################
#########################################################
class SelectQuery(Query):
    def __init__(self, prefixes, projections, ggp, distinct=False, solution_modifiers=list(),
                 dataset_clauses=list(), values_clause=None):
        Query.__init__(self, prefixes, solution_modifiers, values_clause)

        self.ggp = ggp
        # if len(projections) == 0:
        #     projections = self.ggp.get_variables()
        self.projections = projections
        self.distinct = distinct
        self.dataset_clauses = dataset_clauses

        # self.expand_syntax_forms()

    def to_str(self):
        rep = "SELECT " + ('DISTINCT ' if self.distinct else "")
        for p in self.projections:
            rep += str(p) + " "
        if self.dataset_clauses is not None and len(self.dataset_clauses) > 0:
            rep += "'\n".join([str(d) for d in self.dataset_clauses])

        rep += "WHERE { \n" + str(self.ggp) + "\n}"

        return rep

    def expand_syntax_forms(self, prefixes=None):
        if prefixes is None:
            prefixes = self.prefixes
            self.ggp.expand_syntax_forms(prefixes)
            #self.dataset_clauses.expand_syntax_forms(self.prefixes)
            self.values_clause.expand_syntax_forms(self.prefixes)
            # self.solution_modifiers.expand_syntax_forms(self.prefixes)
            # self.projections expand them here
            if len(self.group_by) > 0:
                [g.expand_syntax_forms(prefixes) for g in self.group_by]
            if len(self.order_by) > 0:
                [g.expand_syntax_forms(prefixes) for g in self.order_by]
            if len(self.having) > 0:
                [g.expand_syntax_forms(prefixes) for g in self.having]
        else:
            self.ggp.expand_syntax_forms(prefixes)
            self.values_clause.expand_syntax_forms(prefixes)
            if len(self.group_by) > 0:
                [g.expand_syntax_forms(prefixes) for g in self.group_by]
            if len(self.order_by) > 0:
                [g.expand_syntax_forms(prefixes) for g in self.order_by]
            if len(self.having) > 0:
                [g.expand_syntax_forms(prefixes) for g in self.having]

#########################################################
###############    CONSTRUCT Query     #################
#########################################################
class ConstructQuery(Query):
    def __init__(self, prefixes, ggp, template=None, dataset_clauses=list(), solution_modifiers=list(), values_clause=None):
        Query.__init__(self, prefixes, solution_modifiers, values_clause)
        self.template = template
        self.dataset_clauses = dataset_clauses
        self.ggp = ggp

    def to_str(self):
        rep = "CONSTRUCT "
        if self.template is not None and isinstance(self.template, BGP):
            rep += ' { \n'
            rep += ". \n".join([str(t) for t in self.template.triples])
            rep += "\n}\n"
        if self.dataset_clauses is not None and len(self.dataset_clauses) > 0:
            rep += "'\n".join([str(d) for d in self.dataset_clauses])

        rep += "WHERE {\n" + str(self.ggp) + "\n}"

        return rep


#########################################################
###############    ASK Query     #################
#########################################################
class AskQuery(Query):
    def __init__(self, prefixes, ggp, dataset_clauses=list(), solution_modifiers=list(), values_clause=None):
        Query.__init__(self, prefixes, solution_modifiers, values_clause)
        self.dataset_clauses = dataset_clauses
        self.ggp = ggp

    def to_str(self):
        rep = "ASK "
        if self.dataset_clauses is not None and len(self.dataset_clauses) > 0:
            rep += "'\n".join([str(d) for d in self.dataset_clauses])

        rep += "WHERE { \n" + str(self.ggp) + "\n}"

        return rep


#########################################################
###############    DESCRIBE Query     #################
#########################################################
class DescribeQuery(Query):
    def __init__(self, prefixes, iris, ggp, dataset_clauses=list(), solution_modifiers=list(), values_clause=None):
        Query.__init__(self, prefixes, solution_modifiers, values_clause)
        self.iris = iris
        self.dataset_clauses = dataset_clauses
        self.ggp = ggp

    def to_str(self):
        rep = "DESCRIBE "
        rep += '* ' if len(self.iris) == 0 else " ".join([str(r) for r in self.iris]) + ' \n'

        if self.dataset_clauses is not None and len(self.dataset_clauses) > 0:
            rep += "'\n".join([str(d) for d in self.dataset_clauses])

        rep += "WHERE { \n" + str(self.ggp) + " \n}"

        return rep


#########################################################
###############    GroupGraphPattern     #################
#########################################################
class GGP:
    def __init__(self, ggps):
        self.ggps = ggps

    def to_str(self):
        # not isinstance(g, SelectQuery) and   #
        toprint = [str(g) if not isinstance(g, GGP) else '{' + str(g) + '}' for g in self.ggps]
        return "\n".join(toprint)

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        for ggp in self.ggps:
            vars.extend(ggp.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        for g in self.ggps:
            g.expand_syntax_forms(prefixes)

#########################################################
###############    Values Clause/InlineData     #################
#########################################################
class ValuesClause:
    def __init__(self, variables, values):
        self.variables = variables
        self.values = values

    def to_str(self):
        if len(self.variables) == 0 and len(self.values) == 0:
            return ''

        vc = "VALUES "
        if len(self.variables) > 0:
            vc += '(' + ' '.join([str(v) for v in self.variables]) + ') '
        else:
            vc += '()'
        if len(self.values) > 0:
            vc += "{(" + ") (".join([" ".join([str(v) for v in d]) for d in self.values]) + ")}"
        else:
            vc += '{}'

        return vc

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def get_variables(self):
        return self.variables

    def expand_syntax_forms(self, prefixes):
        for g in self.values:
            g.expand_syntax_forms(prefixes)


#########################################################
###############       GRAPH            #################
#########################################################
class GraphGP:
    def __init__(self, var_or_iri, ggp):
        self.var_or_iri = var_or_iri
        self.ggps = ggp.ggps

    def to_str(self):
        toprint = [str(g) for g in self.ggps]
        return "GRAPH  " + str(self.var_or_iri) + "{" + " ".join(toprint) + " }"

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        for ggp in self.ggps:
            vars.extend(ggp.get_variables())
        if not self.var_or_iri.is_const:
            vars.append(self.var_or_iri.value)
        return vars

    def expand_syntax_forms(self, prefixes):
        for g in self.ggps:
            g.expand_syntax_forms(prefixes)
        self.var_or_iri.expand_syntax_forms(prefixes)

#########################################################
###############       SERVICE         #################
#########################################################
class ServiceGP:
    def __init__(self, var_or_iri, ggp, silent=False):
        self.var_or_iri = var_or_iri
        self.ggps = ggp.ggps
        self.silent = silent

    def to_str(self):
        toprint = [str(g) for g in self.ggps]
        return "SERVICE " + ( "SILENT " if self.silent else "") + str(self.var_or_iri) \
                        + "{" + " ".join(toprint) + " }"

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        for ggp in self.ggps:
            vars.extend(ggp.get_variables())
        if not self.var_or_iri.is_const:
            vars.append(self.var_or_iri.value)
        return vars

    def expand_syntax_forms(self, prefixes):
        for g in self.ggps:
            g.expand_syntax_forms(prefixes)
        self.var_or_iri.expand_syntax_forms(prefixes)

#########################################################
###############       OPTIONAL              #################
#########################################################
class OptionalGP:
    def __init__(self, ggp):
        self.ggps = ggp.ggps

    def to_str(self):
        toprint = [str(g) for g in self.ggps]
        return "OPTIONAL {" + " ".join(toprint) + " }"

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        for ggp in self.ggps:
            vars.extend(ggp.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        for g in self.ggps:
            g.expand_syntax_forms(prefixes)


#########################################################
###############       UNION              #################
#########################################################
class UnionGP:
    def __init__(self, ggps):
        self.ggps = ggps

    def to_str(self):
        toprint = ['{' + str(ggp) + ' } ' for ggp in self.ggps]
        return "\n" + " \n UNION \n".join(toprint) + "\n"

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        for ggp in self.ggps:
            vars.extend(ggp.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        for g in self.ggps:
            g.expand_syntax_forms(prefixes)


#########################################################
###############       MINUS              #################
#########################################################
class MinusGP:
    def __init__(self, ggp):
        self.ggps = ggp.ggps

    def to_str(self):
        toprint = [str(g) for g in self.ggps]
        return "MINUS {" + " ".join(toprint) + " }"

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        for ggp in self.ggps:
            vars.extend(ggp.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        for g in self.ggps:
            g.expand_syntax_forms(prefixes)


#########################################################
###############       BGP              #################
#########################################################
class BGP:
    def __init__(self, triples=list(), filters=list()):
        self.triples = triples
        if filters is None:
            filters = []
        self.filters = filters

    def to_str(self):
        # + (' . -' if len(self.triples) > 0 else ' ')
        return " . \n".join([str(t) for t in self.triples]) \
               + '\n' + "\n".join([str(f) for f in self.filters]) + ' '

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        for t in self.triples:
            vars.extend(t.get_variables())
        for f in self.filters:
            vars.extend(f.get_variables())

        vars = list(set(vars))
        return vars

    def expand_syntax_forms(self, prefixes):
        for g in self.triples:
            g.expand_syntax_forms(prefixes)
        for f in self.filters:
            f.expand_syntax_forms(prefixes)

#########################################################
###############       Filter           #################
#########################################################
class Bind:
    """
    Bind	  ::=  	'BIND' '(' Expression 'AS' Var ')'
    """
    def __init__(self, expression, var):
        self.expression = expression
        self.as_var = var

    def to_str(self):
        return 'BIND (' + str(self.expression) + " AS " + self.as_var + ')'

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def get_variables(self):
        return self.expression.get_variables() + [self.as_var]

    def expand_syntax_forms(self, prefixes):
        self.expression.expand_syntax_forms(prefixes)


#########################################################
###############       Filter           #################
#########################################################
class Filter:
    """
    Filter	  ::=  	'FILTER' Constraint
    Constraint	  ::=  	BrackettedExpression | BuiltInCall | FunctionCall
    FunctionCall	  ::=  	iri ArgList
    """
    def __init__(self, expression):
        self.expression = expression

    def to_str(self):
        return "FILTER " + str(self.expression)

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def get_variables(self):
        return self.expression.get_variables()

    def expand_syntax_forms(self, prefixes):
        self.expression.expand_syntax_forms(prefixes)


#########################################################
###############       Triples           #################
#########################################################
class TriplePattern:
    """
    TriplesSameSubject	  ::=  	VarOrTerm PropertyListNotEmpty | TriplesNode PropertyList
    PropertyList	     ::=  	PropertyListNotEmpty?
    PropertyListNotEmpty ::=  	Verb ObjectList ( ';' ( Verb ObjectList )? )*
    """

    def __init__(self, subject, property, object_o):
        self.subject = subject
        self.property = property
        self.object = object_o
        # print(type(self.property), self.property) RDFTerm, PathTerm, of PropertyPath

    def to_str(self):
        # if isinstance(self.property, PropertyPath) and self.property.oper == '/':
        #     return str(self.subject) + ' ' + self.property.left_path + ' ?_v . ?_v ' + str(self.property.right_path + ' ' + str(self.object)
        return str(self.subject) \
               + ' ' + ('a' if str(self.property) == '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' else str(self.property) ) \
               + ' ' + str(self.object)

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        if isinstance(self.subject, RDFTerm) and not self.subject.is_nil:
            vars.extend(self.subject.get_variables())

        vars.extend(self.property.get_variables() + self.object.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        self.subject.expand_syntax_forms(prefixes)
        self.property.expand_syntax_forms(prefixes)
        self.object.expand_syntax_forms(prefixes)


#########################################################
###############  PropertyPathExpression  ################
#########################################################
class PropertyPath:
    """
        PathAlternative	  ::=  	PathSequence ( '|' PathSequence )*
        PathSequence	  ::=  	PathEltOrInverse ( '/' PathEltOrInverse )*
    """
    def __init__(self, left_path, oper=None, right_path=None):
        self.left_path = left_path
        self.oper = oper  # |, /
        self.right_path = right_path

    def to_str(self):

        return str(self.left_path) \
               + (str(self.oper) + str(self.right_path) if self.oper is not None else '')

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        vars.extend(self.left_path.get_variables())
        if self.right_path is not None:
            vars.extend(self.right_path.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        self.left_path.expand_syntax_forms(prefixes)
        if self.oper is not None:
            self.right_path.expand_syntax_forms(prefixes)


#########################################################
###############       PathTerm           ################
#########################################################
class PathTerm:
    def __init__(self, path_term, inverse=False, path_mode=None):
        self.inverse = inverse  # ^ = True, else False
        self.path_term = path_term  # RDFTerm, PathTerm, PropertyPath
        self.path_mode = path_mode  # *, ?, +

    def to_str(self):
        return ('^' if self.inverse is not None and self.inverse else '') \
               + str(self.path_term) \
               + (str(self.path_mode) if self.path_mode is not None else '')

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        vars.extend(self.path_term.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        self.path_term.expand_syntax_forms(prefixes)


#########################################################
###############       RDFTerm       #################
#########################################################
class RDFTerm:
    """
    Models the following rules:
    VarOrTerm	  ::=  	Var | GraphTerm
    GraphTerm	::=  	iri | RDFLiteral | NumericLiteral | BooleanLiteral | BlankNode | NIL
    """
    def __init__(self, value, is_const,
                 is_iri=False, is_bnode=False, is_nil=False,
                 prefix=None, lang_tag=None, xsd_datatype=None):
        self.value = value.strip()
        if '<' == self.value[0] and '>' == self.value[-1]:
            self.value = self.value[1:-1]

        self.is_constant = is_const
        self.is_iri = is_iri
        self.is_nil = is_nil
        self.prefix = prefix
        self.is_bnode = is_bnode
        self.lang_tag = lang_tag
        self.xsd_datatype = xsd_datatype
        self.is_typed_literal = self.xsd_datatype is not None
        if prefix is not None:
            self.is_iri = True
            self.is_typed_literal = False
            self.is_bnode = False
        self._is_expanded = False

    def to_str(self):
        res = self.value
        if self.is_iri and (self._is_expanded or self.prefix is None or self.prefix not in self.value):
            res = '<' + self.value + ">"
        if self.is_nil:
            res = ""
        elif self.is_typed_literal:
            if self.xsd_datatype is not None:
                res += "^^" + self.xsd_datatype
            if self.lang_tag is not None:
                res += "@" + self.lang_tag

        return res

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def __eq__(self, other):

        return self.value == other.value \
               and self.is_constant == other.is_constant \
               and self.lang_tag == self.lang_tag \
               and self.xsd_datatype == self.xsd_datatype

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.value, self.is_constant))

    def get_variables(self):
        if self.is_constant:
            return []
        else:
            return [self.value]

    def expand_syntax_forms(self, prefixes):

        if self._is_expanded:
            return

        if self.is_constant and not self.is_bnode:
            if self.value == 'a':
                self.value = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'

            if ':' in self.value:
                prefix, val = self.value.split(':')

                if len(prefix) == 0:
                    prefix = '<noname>'
                if prefix in prefixes:
                    self.prefix = {prefix: prefixes[prefix] }
                    self.value = prefixes[prefix][1:-1] + val

        self._is_expanded = True

#########################################################
###############       Expression      #################
#########################################################
class Expression:
    """
    Expression	  ::=  	ConditionalOrExpression
  	ConditionalOrExpression	  ::=  	ConditionalAndExpression ( '||' ConditionalAndExpression )*
  	ConditionalAndExpression	  ::=  	ValueLogical ( '&&' ValueLogical )*
  	ValueLogical	  ::=  	RelationalExpression
  	RelationalExpression	  ::=  	NumericExpression ( '=' NumericExpression | '!=' NumericExpression | '<' NumericExpression | '>' NumericExpression | '<=' NumericExpression | '>=' NumericExpression | 'IN' ExpressionList | 'NOT' 'IN' ExpressionList )?
  	NumericExpression	  ::=  	AdditiveExpression
  	AdditiveExpression	  ::=  	MultiplicativeExpression ( '+' MultiplicativeExpression | '-' MultiplicativeExpression | ( NumericLiteralPositive | NumericLiteralNegative ) ( ( '*' UnaryExpression ) | ( '/' UnaryExpression ) )* )*
  	MultiplicativeExpression	  ::=  	UnaryExpression ( '*' UnaryExpression | '/' UnaryExpression )*
  	UnaryExpression	  ::=  	  '!' PrimaryExpression
                                | '+' PrimaryExpression
                                | '-' PrimaryExpression
                                | PrimaryExpression
  	PrimaryExpression	  ::=  	BrackettedExpression | BuiltInCall | iriOrFunction | RDFLiteral | NumericLiteral | BooleanLiteral | Var
  	BrackettedExpression	  ::=  	'(' Expression ')'
  	BuiltInCall	  ::=  	  Aggregate
                        | 'STR' '(' Expression ')'
                        | 'LANG' '(' Expression ')'
                        | 'LANGMATCHES' '(' Expression ',' Expression ')'
                        | 'DATATYPE' '(' Expression ')'
                        | 'BOUND' '(' Var ')'
                        | 'IRI' '(' Expression ')'
                        | 'URI' '(' Expression ')'
                        | 'BNODE' ( '(' Expression ')' | NIL )
                        | 'RAND' NIL
                        | 'ABS' '(' Expression ')'
                        | 'CEIL' '(' Expression ')'
                        | 'FLOOR' '(' Expression ')'
                        | 'ROUND' '(' Expression ')'
                        | 'CONCAT' ExpressionList
                        | SubstringExpression
                        | 'STRLEN' '(' Expression ')'
                        | StrReplaceExpression
                        | 'UCASE' '(' Expression ')'
                        | 'LCASE' '(' Expression ')'
                        | 'ENCODE_FOR_URI' '(' Expression ')'
                        | 'CONTAINS' '(' Expression ',' Expression ')'
                        | 'STRSTARTS' '(' Expression ',' Expression ')'
                        | 'STRENDS' '(' Expression ',' Expression ')'
                        | 'STRBEFORE' '(' Expression ',' Expression ')'
                        | 'STRAFTER' '(' Expression ',' Expression ')'
                        | 'YEAR' '(' Expression ')'
                        | 'MONTH' '(' Expression ')'
                        | 'DAY' '(' Expression ')'
                        | 'HOURS' '(' Expression ')'
                        | 'MINUTES' '(' Expression ')'
                        | 'SECONDS' '(' Expression ')'
                        | 'TIMEZONE' '(' Expression ')'
                        | 'TZ' '(' Expression ')'
                        | 'NOW' NIL
                        | 'UUID' NIL
                        | 'STRUUID' NIL
                        | 'MD5' '(' Expression ')'
                        | 'SHA1' '(' Expression ')'
                        | 'SHA256' '(' Expression ')'
                        | 'SHA384' '(' Expression ')'
                        | 'SHA512' '(' Expression ')'
                        | 'COALESCE' ExpressionList
                        | 'IF' '(' Expression ',' Expression ',' Expression ')'
                        | 'STRLANG' '(' Expression ',' Expression ')'
                        | 'STRDT' '(' Expression ',' Expression ')'
                        | 'sameTerm' '(' Expression ',' Expression ')'
                        | 'isIRI' '(' Expression ')'
                        | 'isURI' '(' Expression ')'
                        | 'isBLANK' '(' Expression ')'
                        | 'isLITERAL' '(' Expression ')'
                        | 'isNUMERIC' '(' Expression ')'
                        | RegexExpression
                        | ExistsFunc
                        | NotExistsFunc
  	RegexExpression	  ::=  	'REGEX' '(' Expression ',' Expression ( ',' Expression )? ')'
  	SubstringExpression	  ::=  	'SUBSTR' '(' Expression ',' Expression ( ',' Expression )? ')'
  	StrReplaceExpression	  ::=  	'REPLACE' '(' Expression ',' Expression ',' Expression ( ',' Expression )? ')'
  	ExistsFunc	  ::=  	'EXISTS' GroupGraphPattern
  	NotExistsFunc	  ::=  	'NOT' 'EXISTS' GroupGraphPattern
 	Aggregate	  ::=  	  'COUNT' '(' 'DISTINCT'? ( '*' | Expression ) ')'
                            | 'SUM' '(' 'DISTINCT'? Expression ')'
                            | 'MIN' '(' 'DISTINCT'? Expression ')'
                            | 'MAX' '(' 'DISTINCT'? Expression ')'
                            | 'AVG' '(' 'DISTINCT'? Expression ')'
                            | 'SAMPLE' '(' 'DISTINCT'? Expression ')'
                            | 'GROUP_CONCAT' '(' 'DISTINCT'? Expression ( ';' 'SEPARATOR' '=' String )? ')'
 	iriOrFunction	  ::=  	iri ArgList?
    """
    def __init__(self, left_expr, oper, right_expr=None, ternary_expr=None, quaternary_expr=None):
        self.left_expr = left_expr  # RDFTerm, Expression
        self.oper = oper.strip()
        self.right_expr = right_expr
        self.ternary_expr = ternary_expr
        self.quaternary_expr = quaternary_expr

    def to_str(self):
        # print(self.oper, self.left_expr, self.right_expr)
        if self.oper.upper() in unary_operators or self.oper in unary_operators:
            return self.oper + "(" + str(self.left_expr) + ")"
        elif self.oper.upper() in unary_expression_list:
            return '(' + str(self.left_expr) + ' ' \
                   + self.oper + " (" + ", ".join([str(v) for v in self.right_expr]) + "))"
        elif self.oper.upper() in binary_operators:
            return self.oper + "(" + str(self.left_expr) + "," + str(self.right_expr) + ")"
        elif self.oper.upper() in aggregate_functions:
            if self.right_expr is None:
                return self.oper + "(" + str(self.left_expr) + ")"
            else:
                return self.oper + "(" + (str(self.left_expr) if not isinstance(self.left_expr, bool) else 'DISTINCT')\
                       + " " + str(self.right_expr) + ")"
        elif self.oper.upper() in ternary_operators:
            return self.oper + "(" + str(self.left_expr) + "," + str(self.right_expr) \
                   + ("," + str(self.ternary_expr) if self.ternary_expr is not None else "") + ")"
        elif self.oper.upper() in quaternary_operators:
            return self.oper + "(" + str(self.left_expr) + "," + str(self.right_expr) \
                   + "," + str(self.ternary_expr) + "," + str(self.quaternary_expr)+ ")"
        else:
            if self.ternary_expr is not None:
                if self.quaternary_expr is not None:
                    return self.oper + "(" + str(self.left_expr) + "," + str(self.right_expr) \
                           + "," + str(self.ternary_expr) + "," + str(self.quaternary_expr) + ")"
                else:
                    return self.oper + "(" + str(self.left_expr) + "," + str(self.right_expr) \
                           + "," + str(self.ternary_expr) + ")"
            elif self.right_expr is not None:
                if isinstance(self.right_expr, list):
                    return "(" + str(self.left_expr) + " " + self.oper + " (" + ",".join(self.right_expr) + "))"
                else:
                    return "(" + str(self.left_expr) + " " + self.oper + " " + str(self.right_expr) + ")"
            else:
                return "(" + self.oper + " " + str(self.left_expr) + ")"

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def get_variables(self):
        vars = []
        # print(self.left_expr, type(self.left_expr), '-', self.oper, '-', self.right_expr)
        if isinstance(self.left_expr, RDFTerm) and not self.left_expr.is_constant:
            vars.append(self.left_expr.value)
        elif self.left_expr is not None and not isinstance(self.left_expr, str) and not isinstance(self.left_expr, list):
            vars.extend(self.left_expr.get_variables())
        elif isinstance(self.left_expr, list):
            for exp in self.left_expr:
                if isinstance(exp, RDFTerm) and not exp.is_constant:
                    vars.append(exp.value)
                else:
                    vars.extend(exp.get_variables())

        if isinstance(self.right_expr, RDFTerm) and not self.right_expr.is_constant:
            vars.append(self.right_expr.value)
        elif isinstance(self.right_expr, list):
            for exp in self.right_expr:
                if isinstance(exp, RDFTerm) and not exp.is_constant:
                    vars.append(exp.value)
                else:
                    vars.extend(exp.get_variables())
        elif self.right_expr is not None:
            vars.extend(self.right_expr.get_variables())

        return vars

    def expand_syntax_forms(self, prefixes):
        self.left_expr.expand_syntax_forms(prefixes)
        if self.right_expr is not None:
            if self.oper.upper() in unary_expression_list:
                for e in self.right_expr:
                    e.expand_syntax_forms(prefixes)
            else:
                self.right_expr.expand_syntax_forms(prefixes)

unary_operators = {
    'STR': '',
    'LANG': '',
    'DATATYPE': '',
    'BOUND': '',
    'IRI': '',
    'URI': '',
    'BNODE': '',
    'RAND': '',
    'ABS': '',
    'CEIL': '',
    'FLOOR': '',
    'ROUND': '',
    'STRLEN': '',
    'UCASE': '',
    'LCASE': '',
    'ENCODE_FOR_URI': '',
    'YEAR': '',
    'MONTH': '',
    'DAY': '',
    'HOURS': '',
    'MINUTES': '',
    'SECONDS': '',
    'TIMEZONE': '',
    'TZ': '',
    'NOW': '',
    'UUID': '',
    'STRUUID': '',
    'MD5': '',
    'SHA1': '',
    'SHA256': '',
    'SHA384': '',
    'SHA512': '',
    'ISIRI': '',
    'ISURI': '',
    'ISBLANK': '',
    'ISLITERAL': '',
    'ISNUMERIC': '',
    'ASC': '',
    'DESC': '',

    'xsd:double': '',
    'xsd:integer': '',
    'xsd:decimal': '',
    'xsd:float': '',
    'xsd:string': '',
    'xsd:boolean': '',
    'xsd:dateTime': '',
    'xsd:nonPositiveInteger': '',
    'xsd:negativeInteger': '',
    'xsd:long': '',
    'xsd:int': '',
    'xsd:short': '',
    'xsd:byte': '',
    'xsd:nonNegativeInteger': '',
    'xsd:unsignedInt': '',
    'xsd:unsignedShort': '',
    'xsd:unsignedByte': '',
    'xsd:positiveInteger': '',
    '<http://www.w3.org/2001/XMLSchema#integer>': '',
    '<http://www.w3.org/2001/XMLSchema#decimal>': '',
    '<http://www.w3.org/2001/XMLSchema#double>': '',
    '<http://www.w3.org/2001/XMLSchema#float>': '',
    '<http://www.w3.org/2001/XMLSchema#string>': '',
    '<http://www.w3.org/2001/XMLSchema#boolean>': '',
    '<http://www.w3.org/2001/XMLSchema#dateTime>': '',
    '<http://www.w3.org/2001/XMLSchema#nonPositiveInteger>': '',
    '<http://www.w3.org/2001/XMLSchema#negativeInteger>': '',
    '<http://www.w3.org/2001/XMLSchema#long>': '',
    '<http://www.w3.org/2001/XMLSchema#int>': '',
    '<http://www.w3.org/2001/XMLSchema#short>': '',
    '<http://www.w3.org/2001/XMLSchema#byte>': '',
    '<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>': '',
    '<http://www.w3.org/2001/XMLSchema#unsignedInt>': '',
    '<http://www.w3.org/2001/XMLSchema#unsignedShort>': '',
    '<http://www.w3.org/2001/XMLSchema#unsignedByte>': '',
    '<http://www.w3.org/2001/XMLSchema#positiveInteger>': ''
}
unary_expression_list = {
    'IN': '',
    'NOT IN': '',
    'CONCAT': '',
    'COALESCE': ''
}
binary_operators = {
    'LANGMATCHES': '',
    'CONTAINS': '',
    'STRSTARTS': '',
    'STRENDS': '',
    'STRBEFORE': '',
    'STRAFTER': '',
    'STRLANG': '',
    'STRDT': '',
    'sameTerm': ''

}

ternary_operators = {
    "IF": '',
    'REGEX': '',
    "SUBSTR": ''
}

quaternary_operators = {
    "REPLACE": ""
}

aggregate_functions = {
    "COUNT": '',
    "SUM": '',
    "MIN": '',
    "MAX": '',
    "AVG": '',
    "SAMPLE": '',
    "GROUP_CONCAT": ''
}