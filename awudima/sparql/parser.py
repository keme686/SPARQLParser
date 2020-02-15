# -*- coding: utf-8 -*-

__version__ = '0.1'
__author__ = 'Kemele M. Endris'

from ply import lex, yacc
from awudima.sparql import RDFTerm, Expression, PathTerm, \
    PropertyPath, TriplePattern, Filter, Bind, BGP, \
    UnionGP, OptionalGP, GGP, MinusGP, GraphGP, \
    ServiceGP, SelectQuery, ConstructQuery, AskQuery, DescribeQuery, ValuesClause

tokens = [
    'IRIREF',
    # 'DATA_TYPE',
    # 'RDF_TYPE',
    'BLANK_NODE_LABEL',

    'ID',
    'VAR',
    'LANGTAG',
    'INTEGER',
    'DECIMAL',
    'DOUBLE',
    'INTEGER_POSITIVE',
    'DECIMAL_POSITIVE',
    'DOUBLE_POSITIVE',
    'INTEGER_NEGATIVE',
    'DECIMAL_NEGATIVE',
    'DOUBLE_NEGATIVE',
    # 'EXPONENT',
    # 'ECHAR',
    'STRING_LITERAL1',
    'STRING_LITERAL2',
    'STRING_LITERAL_LONG1',
    'STRING_LITERAL_LONG2',
    'NIL',
    'ANON',

    'LTRUE',
    'LFALSE',
    'ALL',
    'QMARK',
    'CARRET',
    'PIPE',

    'LKEY',
    'RKEY',
    'LPAR',
    'RPAR',
    'LBRC',
    'RBRC',
    'COLON',
    'SEMI_COLON',
    'POINT',
    'COMA',
    'EQUALSSYM',
    'NEQUALSSYM',
    'LESS',
    'LESSEQ',
    'GREATER',
    'GREATEREQ',
    'NEG',
    'ANDSYMB',
    'ORSYMB',
    'ART_PLUS',
    'ART_MINUS',
    'ART_DIV'
]

reserved = {
    "PREFIX": "PREFIX",
    "BASE": "BASE",
    'SELECT': 'SELECT',
    'ASK': 'ASK',
    'DESCRIBE': 'DESCRIBE',
    'DISTINCT': 'DISTINCT',
    "AS": "AS",
    "IN": 'IN',
    "NOT": 'NOT',
    'CONSTRUCT': 'CONSTRUCT',
    'FROM': 'FROM',
    'NAMED': 'NAMED',
    'WHERE': 'WHERE',
    'UNION': 'UNION',
    'OPTIONAL': 'OPTIONAL',
    'MINUS': 'MINUS',
    'GRAPH': 'GRAPH',
    'SERVICE': 'SERVICE',
    'SILENT': 'SILENT',
    'FILTER': 'FILTER',
    'BIND': 'BIND',
    'VALUES': 'VALUES',
    'UNDEF': 'UNDEF',

    'AND': 'AND',
    'OR': 'OR',

    'GROUP': 'GROUP',
    'ORDER': 'ORDER',
    'BY': 'BY',
    'HAVING': 'HAVING',
    'ASC': 'ASC',
    'DESC': 'DESC',
    'LIMIT': 'LIMIT',
    'OFFSET': 'OFFSET',

    'STR': 'STR',
    'LANG': 'LANG',
    'LANGMATCHES': 'LANGMATCHES',
    'BOUND': 'BOUND',
    'IRI': 'IRI',
    'URI': 'URI',
    'BNODE': 'BNODE',
    'RAND': 'RAND',
    'ABS': 'ABS',
    'CEIL': 'CEIL',
    'FLOOR': 'FLOOR',
    'ROUND': 'ROUND',
    'CONCAT': 'CONCAT',
    'STRLEN': 'STRLEN',
    'UCASE': 'UCASE',
    'LCASE': 'LCASE',
    'ENCODE_FOR_URI': 'ENCODE_FOR_URI',
    'CONTAINS': 'CONTAINS',
    'STRSTARTS': 'STRSTARTS',
    'STRENDS': 'STRENDS',
    'STRBEFORE': 'STRBEFORE',
    'STRAFTER': 'STRAFTER',
    'YEAR': 'YEAR',
    'MONTH': 'MONTH',
    'DAY': 'DAY',
    'HOURS': 'HOURS',
    'MINUTES': 'MINUTES',
    'SECONDS': 'SECONDS',
    'TIMEZONE': 'TIMEZONE',
    'TZ': 'TZ',
    'NOW': 'NOW',
    'UUID': 'UUID',
    'STRUUID': 'STRUUID',
    'MD5': 'MD5',
    'SHA1': 'SHA1',
    'SHA256': 'SHA256',
    'SHA384': 'SHA384',
    'SHA512': 'SHA512',
    'COALESCE': 'COALESCE',
    'IF': 'IF',
    'STRLANG': 'STRLANG',
    'STRDT': 'STRDT',
    'isIRI': 'isIRI',
    'isURI': 'isURI',
    'isBLANK': 'isBLANK',
    'isLITERAL': 'isLITERAL',
    'isNUMERIC': 'isNUMERIC',

    'DATATYPE': 'DATATYPE',
    'SAMETERM': 'SAMETERM',

    'SUBSTR': 'SUBSTR',
    'REGEX': 'REGEX',
    'REPLACE': 'REPLACE',
    'EXISTS': 'EXISTS',
    'SUM': 'SUM',
    'MIN': 'MIN',
    'MAX': 'MAX',
    'AVG': 'AVG',
    'SAMPLE': 'SAMPLE',
    'GROUP_CONCAT': 'GROUP_CONCAT',
    'SEPARATOR': 'SEPARATOR',
    'COUNT': 'COUNT'
}

# declare tokens
tokens = tokens + list(reserved.values())

# t_IRIREF = r"<\S+>" #  r"<([^<>\"\{\}\|\^`\\]-[\\#x00-\\#x20])*>"
t_VAR = r"([\?]|[\$])([A-Z]|[a-z]|[_])\w*"
t_ALL = r"[*]"
t_QMARK = r"[\?]\s"
t_CARRET = r"[\^]"
t_PIPE = r"[\|]"

# t_RDF_TYPE = r"[\s]+[a][\s]+"

# t_DATA_TYPE = r"\^\^"
t_LANGTAG = r"@[a-zA-Z]+(\-[a-zA-Z0-9]+)*"
t_INTEGER = r"[0-9]+"
t_DECIMAL = r"[0-9]*\.[0-9]+"
EXPONENT = r"[eE][+-]?[0-9]+"
t_DOUBLE = r"[0-9]+\.[0-9]*" + EXPONENT + "|\.([0-9])+" + EXPONENT + "|([0-9])+" + EXPONENT
t_INTEGER_POSITIVE = r"\+" + t_INTEGER
t_DECIMAL_POSITIVE = r"\+" + t_DECIMAL
t_DOUBLE_POSITIVE = r"\+" + t_DOUBLE
t_INTEGER_NEGATIVE = r"\-" + t_INTEGER
t_DECIMAL_NEGATIVE = r"\-" + t_DECIMAL
t_DOUBLE_NEGATIVE = r"\-" + t_DOUBLE

# t_NIL = r"\((\#x20|\#x9|\#xD|\#xA)*\)"
# t_PATH_MOD =r"" # r"\?|\*|\+"

"""
The set of RDF terms defined in RDF Concepts and Abstract Syntax includes RDF URI references while SPARQL terms include IRIs. 
RDF URI references containing "<", ">", '"' (double quote), space, "{", "}", "|", "\", "^", and "`" are not IRIs. 
The behavior of a SPARQL query against RDF statements composed of such RDF URI references is not defined.
"""
t_IRIREF = r"<([^<>\"{}|\^`\\\]\[\x00-\x20])*>"
# t_PNAME_NS = r"([a-zA-Z_](([a-zA-Z_]|\-|[0-9])*([a-zA-Z_]|\-|[0-9])))?:"


PN_CHARS_BASE = r"[A-Z]|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]" \
                r"|[\u0370-\u037D]|[\u037F-\u1FFF]" \
                r"|[\u200C-\u200D]|[\u2070-\u218F]" \
                r"|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]" \
                r"|[\uFDF0-\uFFFD]"  # |[\u10000-\uEFFFF]
PN_CHARS_U = r"" + PN_CHARS_BASE + r"|_"
PN_CHARS = r"(" + PN_CHARS_U + "|-|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040])"
PN_PREFIX = r"(" + PN_CHARS_BASE + ")((" + PN_CHARS + "|.)*(" + PN_CHARS + "))?"

PNAME_NS = r"(" + PN_PREFIX + ")?:"

HEX = r"[0-9]|[A-F]|[a-f]"
PN_LOCAL_ESC = r"\\(\_|\~|\.|\-|\!|\$|\&|'|\(|\)|\*|\+|\,|\;|\=|/|\?|\#|\@|\%)"
PERCENT = r"\%" + HEX + " " + HEX
PLX = r"(" + PERCENT + "|" + PN_LOCAL_ESC + ")"

PN_LOCAL = r"(" + PN_CHARS_U + "|:|[0-9]|" + PLX + ")((" + PN_CHARS + "|.|:|" + PLX + ")*(" + PN_CHARS + "|:|" + PLX + "))?"

# PNAME_NS = r"(" + PN_PREFIX + ")?:(" + PN_LOCAL + ')*'
PNAME_LN = PNAME_NS + PN_LOCAL

ECHAR = r"\\[tbnrf\"\']"  # escaped characters
t_STRING_LITERAL1 = r"'(([^\x27\x5C\x0A\x0D])|(" + ECHAR + "))*'"
t_STRING_LITERAL2 = r"\"(([^\x22\x5C\x0A\x0D])|(" + ECHAR + "))*\""
t_STRING_LITERAL_LONG1 = r"\'\'\'((\'|\'\')?([^\']|" + ECHAR + "))*\'\'\'"
t_STRING_LITERAL_LONG2 = r'\"\"\"((\"|\"\")?([^"]|' + ECHAR + '))*\"\"\"'

t_NIL = r"\((\x20|\x09|\x0D|\x0A)*\)"
t_BLANK_NODE_LABEL = r"\_\:([A-Z]|[a-z]|\_|[0-9])(([A-Z]|[a-z]|\_|\-|[0-9]|\.)*([A-Z]|[a-z]|\_|\-|[0-9]))?"
t_ANON = r"\[(\x20|\x09|\x0D|\x0A)*\]"

t_LTRUE = r"true"
t_LFALSE = r"false"
t_LPAR = r"\("
t_RPAR = r"\)"
t_LKEY = r"\{"
t_RKEY = r"\}"
t_LBRC = r"\["
t_RBRC = r"\]"

t_COLON = r"[\:]"
t_SEMI_COLON = r"\;"
# t_RDFTYPE = r"a"
# t_RKEY = r"(\.)?\}"
t_POINT = r"\."
t_COMA = r"\,"

t_EQUALSSYM = r"\="
t_NEQUALSSYM = r"[\!][\=]"
t_LESS = r"<"
t_LESSEQ = r"<="
t_GREATER = r">"
t_GREATEREQ = r">="

t_NEG = r"\!"

t_ANDSYMB = r"\&\&"
t_ORSYMB = r"\|\|"

t_ART_PLUS = r"\+"
t_ART_MINUS = r"\-"

t_ART_DIV = r"/"

t_ignore = ' \t\n'
t_ignore_COMMENT = r'\#.*'


def t_ID(t):
    r'[a-zA-Z_]([a-zA-Z_0-9\-\.]*[a-zA-Z_0-9\-])?'
    # '[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value.upper(), 'ID')  # Check for reserved words
    return t


# def t_COMMENT(t):
#     r'\#.*'
#     pass
#     # No return value. Token discarded

def t_error(t):
    print(t, repr(xstring))

    if t is None:
        raise TypeError("Unknown text '%s' in line %d " % (t.value, t.lexer.lineno,))
    else:
        raise TypeError("Unknown text ", t, repr(xstring))


def p_error(t):
    print(t, repr(xstring))
    if t is not None:
        raise TypeError("Unknown text '%s' in line %d " % (t.value, t.lexer.lineno,))
    else:
        raise TypeError("Unknown text ", t, repr(xstring))


####################################################
# Query Parser:
"""
    Query	  ::=  Prefix_List  SelectQuery ValuesClause
"""


#####################################################
def p_parse_sparql_0(p):
    """
    parse_sparql : prefixes select_query values_clause
    """
    dist, prj, dsc, ggp, sm = p[2]
    prfxs = p[1]
    prefix = {v[0]: v[1] for v in prfxs}

    p[0] = SelectQuery(prefix, projections=prj, ggp=ggp, solution_modifiers=sm,
                       dataset_clauses=dsc, values_clause=p[3], distinct=dist)


############################################
# Query Parser:
"""
    Query	  ::=  Prefix_List  ConstructQuery ValuesClause
"""


########################################
def p_parse_sparql_1(p):
    """
    parse_sparql : prefixes construct_query values_clause
    """
    # construct_template,     dataset_clauses,     where_clause,     solution_modifier
    ctemp, dst, wc, sm = p[2]
    prfxs = p[1]
    prefix = {v[0]: v[1] for v in prfxs}
    p[0] = ConstructQuery(prefix, wc, ctemp, dst, sm, p[3])


############################################
# Query Parser:
"""
    Query	  ::=  Prefix_List  AskQuery ValuesClause
"""


########################################
def p_parse_sparql_2(p):
    """
    parse_sparql : prefixes ask_query values_clause
    """
    dst, wc, sm = p[2]
    prfxs = p[1]
    prefix = {v[0]: v[1] for v in prfxs}
    p[0] = AskQuery(prefix, wc, dst, sm, p[3])


############################################
# Query Parser:
"""
    Query	  ::=  Prefix_List  DescribeQuery ValuesClause
"""


########################################
def p_parse_sparql_3(p):
    """
    parse_sparql : prefixes describe_query values_clause
    """
    iris, dst, wc, sm = p[2]
    prfxs = p[1]
    prefix = {v[0]: v[1] for v in prfxs}
    p[0] = DescribeQuery(prefix, iris, wc, dst, sm, p[3])


############################################################
# Prefix list
"""
    Prefix_List   ::=   ( BaseDecl | PrefixDecl )*
    BaseDecl	  ::=  	'BASE' IRIREF
    PrefixDecl	  ::=  	'PREFIX' PNAME_NS IRIREF
"""


###########################################################
def p_prefixes_0(p):
    """
    prefixes : empty
    """
    p[0] = []


def p_prefixes_1(p):
    """
    prefixes : base_decl prefixes
    """
    p[0] = [p[1]] + p[2]


def p_prefixes_2(p):
    """
    prefixes : prefix_decl prefixes
    """

    p[0] = [p[1]] + p[2]


#
# def p_prefixes(p):
#     """
#     prefixes : prefix_exp prefix_list
#     """
#     prfxs = p[1] + p[2]
#     prefix = {v[0]: v[1] for v in prfxs}
#     p[0] = prefix
#
#
# def p_prefix_exp_0(p):
#     """
#     prefix_exp : base_decl
#                     | prefix_decl
#     """
#     p[0] = [p[1]]
#
#
# def p_prefix_exp_1(p):
#     """
#     prefix_exp : empty
#     """
#     p[0] = []
#
#
# def p_prefix_list_0(p):
#     """
#     prefix_list : prefix_exp prefix_exp
#     """
#     p[0] = p[1]+ p[2]
#
#
# def p_prefix_list_2(p):
#     """
#     prefix_list : empty
#     """
#     p[0] = {}
#

def p_base_decl(p):
    """
    base_decl :  BASE IRIREF
    """
    p[0] = ('[' + p[1] + ']', p[2])


def p_prefix_decl_0(p):
    """
    prefix_decl : PREFIX ID COLON IRIREF
    """
    p[0] = (p[2], p[4])


def p_prefix_decl_1(p):
    """
    prefix_decl :  PREFIX COLON IRIREF
    """
    p[0] = ("<noname>", p[3])


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


####################################################################################################################
# Select Query
"""
    SelectQuery	  ::=  	SelectClause DatasetClause* WhereClause SolutionModifier
    SelectClause  ::=  	'SELECT' ( 'DISTINCT' | 'REDUCED' )? ( ( Var | ( '(' Expression 'AS' Var ')' ) )+ | '*' )
"""


####################################################################################################################
def p_select_query(p):
    """
    select_query : select_clause dataset_clauses where_clause solution_modifier
    """
    p[0] = p[1][0], p[1][1], p[2], p[3], p[4]


def p_select_clause_0(p):
    """
    select_clause : SELECT distinct var_list
    """
    p[0] = p[2], p[3]


def p_select_clause_1(p):
    """
    select_clause : SELECT distinct ALL
    """
    p[0] = p[2], ['*']


# distinct
def p_distinct_0(p):
    """
    distinct : DISTINCT
    """
    p[0] = True


def p_distinct_1(p):
    """
    distinct : empty
    """
    p[0] = False


# Var list
def p_var_list_0(p):
    """
    var_list : VAR var_lists
    """
    p[0] = [RDFTerm(p[1], is_const=False)] + p[2]


def p_var_list_1(p):
    """
    var_list : LPAR expression AS VAR RPAR var_lists
    """
    p[0] = [Expression(p[2], 'AS', RDFTerm(p[4], is_const=False))] + p[6]


def p_var_list_2(p):
    """
    var_list :  expression AS VAR var_lists
    """
    p[0] = [Expression(p[1], 'AS', RDFTerm(p[3], is_const=False))] + p[4]


def p_var_list_3(p):
    """
    var_list :  expression var_lists
    """
    import random
    varname = '?' + str(p[1]).split('(')[0] + '_' + str(random.randint(0, 100))
    p[0] = [Expression(p[1], 'AS', RDFTerm(varname.lower(), is_const=False))] + p[2]


def p_var_lists_0(p):
    """
    var_lists :  var_list
    """
    p[0] = p[1]


def p_var_lists_1(p):
    """
    var_lists :  empty
    """
    p[0] = []


################################################
# Construct Query
"""
    ConstructQuery ::= 'CONSTRUCT' ( ConstructTemplate DatasetClause* WhereClause SolutionModifier 
                                    | DatasetClause* 'WHERE' '{' TriplesTemplate? '}' SolutionModifier 
                                  )
    ConstructTemplate	  ::=  	'{' ConstructTriples? '}'
    TriplesTemplate	      ::=  	TriplesSameSubject ( '.' TriplesTemplate? )?
  	ConstructTriples	  ::=  	TriplesSameSubject ( '.' ConstructTriples? )?
  	TriplesSameSubject	  ::=  	VarOrTerm PropertyListNotEmpty | TriplesNode PropertyList
  	PropertyList	      ::=  	PropertyListNotEmpty?
  	PropertyListNotEmpty  ::=  	Verb ObjectList ( ';' ( Verb ObjectList )? )*
	Verb	              ::=  	VarOrIri | 'a'
  	ObjectList	          ::=  	Object ( ',' Object )*
  	Object	              ::=  	GraphNode
  	GraphNode	          ::=  	VarOrTerm | TriplesNode
    TriplesNode	          ::=  	Collection | BlankNodePropertyList
  	BlankNodePropertyList ::=  	'[' PropertyListNotEmpty ']'  	
"""


##############################################
def p_construct_query_0(p):
    """
    construct_query : CONSTRUCT construct_template dataset_clauses where_clause solution_modifier
    """
    p[0] = p[2], p[3], p[4], p[5]


def p_construct_query_1(p):
    """
    construct_query : CONSTRUCT dataset_clauses WHERE LKEY triples_templates RKEY solution_modifier
    """
    p[0] = None, p[2], GGP([BGP(p[5])]), p[7]


def p_construct_template_0(p):
    """
    construct_template : LKEY construct_triples RKEY
    """
    p[0] = BGP(p[2])


def p_construct_template_1(p):
    """
    construct_template : LKEY RKEY
    """
    p[0] = None


#
# def p_construct_template_2(p):
#     """
#     construct_template : empty
#     """
#     p[0] = None


def p_construct_triples_0(p):
    """
    construct_triples : triples_same_subject construct_triples_expr
    """
    p[0] = p[1] + p[2]


def p_construct_triples_1(p):
    """
    construct_triples : empty
    """
    p[0] = []


def p_construct_triples_expr_0(p):
    """
    construct_triples_expr : POINT construct_triples
    """
    if len(p[2]) > 0:
        p[0] = p[2]
    else:
        p[0] = []


def p_construct_triples_expr_1(p):
    """
    construct_triples_expr : POINT
    """
    p[0] = []


def p_construct_triples_expr_2(p):
    """
    construct_triples_expr : empty
    """
    p[0] = []


### Triples template
def p_triples_templates(p):
    """
      triples_templates : triples_same_subject triples_template_expr
    """
    p[0] = p[1] + p[2]


def p_triples_template_expr_0(p):
    """
    triples_template_expr : POINT triples_templates
    """
    p[0] = p[2]


def p_triples_template_expr_1(p):
    """
    triples_template_expr : POINT
    """
    p[0] = []


def p_triples_template_expr_2(p):
    """
    triples_template_expr : empty
    """
    p[0] = []


def p_triples_same_subject_0(p):
    """
    triples_same_subject : var_or_term property_list_not_empty
    """
    triples = []
    for po in p[2]:
        if isinstance(po[1], RDFTerm):
            triples.append(TriplePattern(p[1], po[0], po[1]))
        else:
            for o in po[1]:
                triples.append(TriplePattern(p[1], po[0], o))
    p[0] = triples


def p_triples_same_subject_1(p):
    """
    triples_same_subject : triples_node property_list
    """
    triples = []
    for po in p[2]:
        if isinstance(po[1], RDFTerm):
            triples.append(TriplePattern(p[1], po[0], po[1]))
        else:
            for o in po[1]:
                triples.append(TriplePattern(p[1], po[0], o))

    p[0] = triples


def p_property_list_0(p):
    """
    property_list : property_list_not_empty
    """
    p[0] = p[1]


def p_property_list_1(p):
    """
    property_list : empty
    """
    p[0] = []


def p_object_list(p):
    """
    object_list :  object object_list_exp
    """
    p[0] = p[1] + p[2]


def p_object_list_exp_0(p):
    """
     object_list_exp :  COMA object object_list_exp
    """
    p[0] = p[2] + p[3]


def p_object_list_exp_1(p):
    """
     object_list_exp :  empty
    """
    p[0] = []


def p_object(p):
    """
     object : graph_node
    """
    p[0] = p[1]


####################################################################################################################
# Ask Query
"""
    AskQuery	  ::=  	'ASK' DatasetClause* WhereClause SolutionModifier
"""


####################################################################################################################
def p_ask_query(p):
    """
    ask_query : ASK dataset_clauses where_clause solution_modifier
    """
    p[0] = p[2], p[3], p[4]


####################################################################################################################
# Describe Query
"""
    DescribeQuery	  ::=  	'DESCRIBE' ( VarOrIri+ | '*' ) DatasetClause* WhereClause? SolutionModifier
"""


####################################################################################################################
def p_describe_query_0(p):
    """
    describe_query : DESCRIBE VAR var_or_iris dataset_clauses where_clause solution_modifier
    """
    iris = [RDFTerm(p[1], is_const=False)] + p[3]
    p[0] = iris, p[4], p[5], p[6]


def p_describe_query_1(p):
    """
    describe_query : DESCRIBE VAR var_or_iris dataset_clauses solution_modifier
    """
    iris = [RDFTerm(p[1], is_const=False)] + p[3]
    p[0] = iris, p[4], None, p[5]


def p_describe_query_2(p):
    """
    describe_query : DESCRIBE iri var_or_iris dataset_clauses where_clause solution_modifier
    """
    iris = [p[2]] + p[3]
    p[0] = iris, p[4], p[5], p[6]


def p_describe_query_3(p):
    """
    describe_query : DESCRIBE iri var_or_iris dataset_clauses solution_modifier
    """
    iris = [p[2]] + p[3]
    p[0] = iris, p[4], None, p[5]


def p_describe_query_4(p):
    """
    describe_query : DESCRIBE ALL dataset_clauses where_clause solution_modifier
    """
    p[0] = [], p[3], p[4], p[5]


def p_describe_query_5(p):
    """
    describe_query : DESCRIBE ALL dataset_clauses solution_modifier
    """
    p[0] = [], p[3], None, p[4]


def p_var_or_iris_0(p):
    """
    var_or_iris : VAR var_or_iris
    """
    p[0] = [RDFTerm(p[1], is_const=False)] + p[2]


def p_var_or_iris_1(p):
    """
    var_or_iris : iri var_or_iris
    """
    p[0] = [p[1]] + p[2]


def p_var_or_iris_2(p):
    """
    var_or_iris : empty
    """
    p[0] = []


#####################################################################################
# Dataset Clauses
"""
    DatasetClause	    ::=  	'FROM' ( DefaultGraphClause | NamedGraphClause )
  	DefaultGraphClause	::=  	SourceSelector
  	NamedGraphClause	::=  	'NAMED' SourceSelector
  	SourceSelector	    ::=  	iri
"""


####################################################################################

def p_dataset_clauses_0(p):
    """
    dataset_clauses : FROM default_graph_clause dataset_clauses
    """
    p[0] = [str(p[2])] + p[3]


def p_dataset_clauses_1(p):
    """
    dataset_clauses : FROM named_graph_clause dataset_clauses
    """
    p[0] = [str(p[2])] + p[3]


def p_dataset_clauses_2(p):
    """
    dataset_clauses : empty
    """
    p[0] = []


def p_default_graph_clause(p):
    """
    default_graph_clause : source_selector
    """
    p[0] = str(p[1])


def p_named_graph_clause(p):
    """
    named_graph_clause : NAMED source_selector
    """
    p[0] = str(p[1]) + " " + str(p[2])


def p_source_selector(p):
    """
    source_selector : iri
    """
    p[0] = str(p[1])


########################################
# WHERE Clause
"""
    WhereClause	  ::=  	'WHERE'? GroupGraphPattern
"""


###################################
def p_where_clause_0(p):
    """
     where_clause : WHERE group_graph_pattern
    """
    p[0] = p[2]


def p_where_clause_1(p):
    """
     where_clause : group_graph_pattern
    """
    p[0] = p[1]


#####################################################
# SubSelect
"""
    SubSelect	  ::=  	SelectClause WhereClause SolutionModifier ValuesClause
"""


##############################################################
def p_sub_select(p):
    """
    sub_select : select_clause where_clause solution_modifier values_clause
    """
    # p[0] = str(p[1]) + ' \n\t' + str(p[2]) + ' \n\t' + str(p[3]) + ' \n\t' + str(p[4])
    dist, prj = p[1]
    p[0] = [SelectQuery({}, projections=prj, ggp=p[2], solution_modifiers=p[3],
                        dataset_clauses=[], values_clause=p[4], distinct=dist)]


#######################################
# GraphPatterns
"""
   	GroupGraphPattern	  ::=  	'{' ( SubSelect | GroupGraphPatternSub )  '}'
   	SubSelect	  ::=  	SelectClause WhereClause SolutionModifier ValuesClause
  	GroupGraphPatternSub	  ::=  	TriplesBlock? ( GraphPatternNotTriples '.'? TriplesBlock? )*

  	TriplesBlock	  ::=  	TriplesSameSubjectPath ( '.' TriplesBlock? )?

  	GraphPatternNotTriples	  ::=  	GroupOrUnionGraphPattern 
  	                                | OptionalGraphPattern 
  	                                | MinusGraphPattern 
  	                                | GraphGraphPattern 
  	                                | ServiceGraphPattern 
  	                                | Filter 
  	                                | Bind 
  	                                | InlineData
  	OptionalGraphPattern	  ::=  	'OPTIONAL' GroupGraphPattern
  	GraphGraphPattern	  ::=  	'GRAPH' VarOrIri GroupGraphPattern
  	ServiceGraphPattern	  ::=  	'SERVICE' 'SILENT'? VarOrIri GroupGraphPattern
  	Bind	  ::=  	'BIND' '(' Expression 'AS' Var ')'
  	InlineData	  ::=  	'VALUES' DataBlock
  	DataBlock	  ::=  	InlineDataOneVar 
  	                    | InlineDataFull
  	InlineDataOneVar	  ::=  	Var '{' DataBlockValue* '}'
  	InlineDataFull	  ::=  	( NIL | '(' Var* ')' ) '{' ( '(' DataBlockValue* ')' | NIL )* '}'
  	DataBlockValue	  ::=  	iri | RDFLiteral | NumericLiteral | BooleanLiteral | 'UNDEF'
  	MinusGraphPattern	  ::=  	'MINUS' GroupGraphPattern
  	GroupOrUnionGraphPattern	  ::=  	GroupGraphPattern ( 'UNION' GroupGraphPattern )*
  	Filter	  ::=  	'FILTER' Constraint
  	Constraint	  ::=  	BrackettedExpression 
  	                    | BuiltInCall 
  	                    | FunctionCall
  	FunctionCall	  ::=  	iri ArgList
  	ArgList	  ::=  	NIL | '(' 'DISTINCT'? Expression ( ',' Expression )* ')'
  	ExpressionList	  ::=  	NIL | '(' Expression ( ',' Expression )* ')' 
"""


################################################
def p_group_graph_pattern_0(p):
    """
    group_graph_pattern : LKEY group_graph_pattern_sub RKEY
    """
    p[0] = GGP(p[2])


def p_group_graph_pattern_1(p):
    """
    group_graph_pattern : LKEY sub_select RKEY
    """
    p[0] = GGP(p[2])


# GroupGraphPatternSub	  ::=  	TriplesBlock? ( GraphPatternNotTriples '.'? TriplesBlock? )*
def p_group_graph_pattern_sub_0(p):
    """
    group_graph_pattern_sub :  triples_block pattern_blocks
    """
    if len(p[2]) > 0:
        filters = []
        # if len(p[1]) > 0:
        for f in p[2]:
            if isinstance(f, Filter):
                filters.append(f)
        [p[2].remove(f) for f in filters]
        if len(p[1]) > 0 or len(filters) > 0:
            p[0] = [BGP(p[1], filters)] + p[2]
        else:
            p[0] = p[2]
    else:
        if len(p[1]) > 0:
            p[0] = [BGP(p[1])]
        else:
            p[0] = []


def p_group_graph_pattern_sub_1(p):
    """
    group_graph_pattern_sub :  pattern_blocks
    """
    if len(p[1]) > 0:
        filters = []
        bgps = []
        for f in p[1]:
            if isinstance(f, Filter):
                filters.append(f)
            if isinstance(f, BGP):
                bgps.append(f)
        [p[1].remove(f) for f in filters]
        [p[1].remove(f) for f in bgps]
        if len(bgps) > 0 or len(filters) > 0:
            p[0] = [BGP(bgps, filters)] + p[1]
        else:
            p[0] = p[1]
    else:
        p[0] = p[1]


def p_pattern_blocks_0(p):
    """
    pattern_blocks : graph_pattern_not_triples POINT triples_block pattern_blocks
    """
    if isinstance(p[1], Filter):
        if len(p[3]) > 0:
            p[0] = [BGP(p[3], [p[1]])] + p[4]
        else:
            p[0] = [p[1]] + p[4]
    else:
        if len(p[3]) > 0:
            p[0] = [p[1]] + [BGP(p[3])] + p[4]
        else:
            p[0] = [p[1]] + p[4]


def p_pattern_blocks_1(p):
    """
    pattern_blocks : graph_pattern_not_triples triples_block pattern_blocks
    """
    if isinstance(p[1], Filter):
        if len(p[2]) > 0:
            p[0] = [BGP(p[2], [p[1]])] + p[3]
        else:
            p[0] = [p[1]] + p[3]
    else:
        if len(p[2]) > 0:
            p[0] = [p[1]] + [BGP(p[2])] + p[3]
        else:
            p[0] = [p[1]] + p[3]


def p_pattern_blocks_2(p):
    """
    pattern_blocks : graph_pattern_not_triples POINT pattern_blocks
    """
    p[0] = [p[1]] + p[3]


def p_pattern_blocks_3(p):
    """
    pattern_blocks : graph_pattern_not_triples pattern_blocks
    """
    p[0] = [p[1]] + p[2]


def p_pattern_blocks_4(p):
    """
    pattern_blocks : empty
    """
    p[0] = []


###############################################################
# GraphPatternsNotTriples
"""
    GraphPatternNotTriples	  ::=  	GroupOrUnionGraphPattern 
  	                                | OptionalGraphPattern 
  	                                | MinusGraphPattern 
  	                                | GraphGraphPattern 
  	                                | ServiceGraphPattern 
  	                                | Filter 
  	                                | Bind 
  	                                | InlineData
"""


######################################################################
def p_graph_pattern_not_triples(p):
    """
    graph_pattern_not_triples :  group_or_union_graph_pattern
                                | optional_graph_pattern
                                | minus_graph_pattern
                                | graph_graph_pattern
                                | service_graph_pattern
                                | filter
                                | bind
                                | inline_data
    """
    p[0] = p[1]


##############################################################
# UNIONs
"""
    GroupOrUnionGraphPattern  ::=  	GroupGraphPattern ( 'UNION' GroupGraphPattern )*
"""


######################
def p_group_or_union_graph_pattern(p):
    """
     group_or_union_graph_pattern : group_graph_pattern union_patterns
    """

    if len(p[2]) > 0:
        # print(p[1],'\n\n', p[2])
        p[0] = UnionGP([p[1]] + p[2])
    else:
        p[0] = p[1]


def p_union_patterns_0(p):
    """
    union_patterns : UNION group_graph_pattern union_patterns
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = [p[2]] + p[3]


def p_union_patterns_1(p):
    """
    union_patterns : empty
    """
    p[0] = []


############################
# OPTIONAL
"""
    OptionalGraphPattern	  ::=  	'OPTIONAL' GroupGraphPattern
"""


############################
def p_optional_graph_pattern(p):
    """
    optional_graph_pattern : OPTIONAL group_graph_pattern
    """
    p[0] = OptionalGP(p[2])


##############################################
# MINUS
"""
    MinusGraphPattern	  ::=  	'MINUS' GroupGraphPattern
"""


#######################################
def p_minus_graph_pattern(p):
    """
    minus_graph_pattern : MINUS group_graph_pattern
    """
    p[0] = MinusGP(p[2])


####################################################
# GRAPH
"""
    GraphGraphPattern	  ::=  	'GRAPH' VarOrIri GroupGraphPattern
"""


#######################################
def p_graph_graph_pattern_0(p):
    """
    graph_graph_pattern : GRAPH VAR group_graph_pattern
    """
    p[0] = GraphGP(RDFTerm(p[2], is_const=False), p[3])


def p_graph_graph_pattern_1(p):
    """
    graph_graph_pattern : GRAPH iri group_graph_pattern
    """
    p[0] = GraphGP(p[2], p[3])


###################################
# SERVICE
"""
    ServiceGraphPattern	  ::=  	'SERVICE' 'SILENT'? VarOrIri GroupGraphPattern
"""


###############################
def p_service_graph_pattern_0(p):
    """
    service_graph_pattern : SERVICE silent VAR group_graph_pattern
    """
    p[0] = ServiceGP(RDFTerm(p[3], is_const=False), p[4], p[2])


def p_service_graph_pattern_1(p):
    """
    service_graph_pattern : SERVICE silent iri group_graph_pattern
    """
    p[0] = ServiceGP(p[3], p[4], p[2])


def p_silent_0(p):
    """
    silent : SILENT
    """
    p[0] = True


def p_silent_1(p):
    """
    silent : empty
    """
    p[0] = False


########################################
# FILTER
"""
    Filter	  ::=  	'FILTER' Constraint
"""


#########################################
def p_filter(p):
    """
    filter : FILTER constraint
    """
    p[0] = Filter(p[2])


#####################################
# BIND
"""
    Bind	  ::=  	'BIND' '(' Expression 'AS' Var ')'
"""


#########################################
def p_bind(p):
    """
    bind : BIND LPAR expression AS VAR RPAR
    """
    p[0] = Bind(RDFTerm(str(p[3]), is_const=False), p[5])


###################################
# VALUES inline data
"""
    InlineData	  ::=  	'VALUES' DataBlock
"""


#########################################
# replaced by values_clause
def p_inline_data(p):
    """
    inline_data : VALUES data_block
    """
    p[0] = ValuesClause(p[2]['vars'], p[2]['values'])


###############################
# Constraints
"""
    Constraint	  ::=  	BrackettedExpression 
                        | BuiltInCall 
                        | FunctionCall
  	FunctionCall  ::=  	iri ArgList
"""


#######################
def p_constraint(p):
    """
    constraint : bracketted_expression
                    | function_call
                    | built_in_call
    """
    p[0] = p[1]


def p_function_call(p):
    """
    function_call : iri arg_list
    """
    # p[0] = str(p[1]) + ' ' + str(p[2])
    p[0] = Expression(p[2], str(p[1]))


#######################
# ArgList
"""
    ArgList	  ::=  	NIL | '(' 'DISTINCT'? Expression ( ',' Expression )* ')' 
"""


################################
def p_arg_list_0(p):
    """
    arg_list :  NIL
    """
    p[0] = RDFTerm('()', is_const=True, is_nil=True)


def p_arg_list_1(p):
    """
    arg_list :  LPAR distinct expression more_args RPAR
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + " " + str(p[3]) + ' ' + str(p[4]) + ' ' + str(p[5])
    if len(p[4]) > 0:
        p[0] = Expression([p[3]] + p[4], p[2])
        # p[0] = p[2], [p[3]] + p[4]
    else:
        if isinstance(p[3], RDFTerm):
            if len(p[4]) > 0:
                argslist = [p[3]] + p[4]
                p[0] = argslist
            else:
                p[0] = p[3]
        else:
            p[0] = p[3]


def p_more_args_0(p):
    """
    more_args : COMA expression more_args
    """
    # p[0] = str(p[1]) + ' ' + str(p[2])
    p[0] = [p[2]] + p[3]


def p_more_args_1(p):
    """
    more_args : empty
    """
    p[0] = []


################################
# VALUES calues
"""
    ValuesClause  ::=  	( 'VALUES' DataBlock )?
    DataBlock	  ::=  	InlineDataOneVar | InlineDataFull
  	InlineDataOneVar	  ::=  	Var '{' DataBlockValue* '}'
  	InlineDataFull	  ::=  	( NIL | '(' Var* ')' ) '{' ( '(' DataBlockValue* ')' | NIL )* '}'
  	DataBlockValue	  ::=  	iri | RDFLiteral | NumericLiteral | BooleanLiteral | 'UNDEF'
"""


###############################
def p_values_clause_0(p):
    """
    values_clause :  VALUES data_block
    """
    # p[0] = p[2]
    p[0] = ValuesClause(p[2]['vars'], p[2]['values'])


def p_values_clause_1(p):
    """
    values_clause :  empty
    """
    # p[0] = {'vars': [],
    #         'values': []}
    p[0] = ValuesClause([], [])


def p_data_block_0(p):
    """
    data_block :  inline_data_one_var
    """
    p[0] = p[1]


def p_data_block_1(p):
    """
    data_block :  inline_data_full
    """
    p[0] = p[1]


def p_inline_data_one_var(p):
    """
    inline_data_one_var :  VAR LKEY data_block_values RKEY
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4])
    p[0] = {'vars': [RDFTerm(p[1], is_const=False)],
            'values': [[d] for d in p[3]]}


def p_data_block_values_0(p):
    """
    data_block_values :  data_block_value data_block_values
    """
    p[0] = [p[1]] + p[2]


def p_data_block_values_1(p):
    """
    data_block_values :  empty
    """
    p[0] = []


def p_data_block_value(p):
    """
    data_block_value : iri
                        | rdf_literal
                        | numeric_literal
                        | boolean_literal
                        | UNDEF
    """
    p[0] = p[1]


def p_inline_data_full_0(p):
    """
    inline_data_full :  NIL LKEY bracketed_data_block_values RKEY
    """
    p[0] = {'vars': [],
            'values': p[3]}


def p_inline_data_full_1(p):
    """
    inline_data_full :  NIL LKEY nils RKEY
    """
    p[0] = {'vars': [],
            'values': p[3]}


def p_inline_data_full_2(p):
    """
    inline_data_full :  LPAR vars RPAR LKEY nils RKEY
    """
    p[0] = {'vars': p[2],
            'values': p[5]}


def p_inline_data_full_3(p):
    """
    inline_data_full :  LPAR vars RPAR LKEY bracketed_data_block_values RKEY
    """
    p[0] = {'vars': p[2],
            'values': p[5]}


def p_vars_0(p):
    """
    vars : VAR vars
    """
    p[0] = [RDFTerm(p[1], is_const=False)] + p[2]


def p_vars_1(p):
    """
    vars : empty
    """
    p[0] = []


def p_nils_0(p):
    """
    nils : NIL nils
    """
    p[0] = [RDFTerm(p[1], is_const=True, is_nil=True)] + p[2]


def p_nils_1(p):
    """
    nils : empty
    """
    p[0] = []


def p_bracketed_data_block_values_0(p):
    """
    bracketed_data_block_values : LPAR data_block_values RPAR bracketed_data_block_values
    """
    p[0] = [p[2]] + p[4]


def p_bracketed_data_block_values_1(p):
    """
    bracketed_data_block_values : empty
    """
    p[0] = []


######################################################
# TriplesBlock
"""
    TriplesBlock	  ::=  	TriplesSameSubjectPath ( '.' TriplesBlock? )?    
"""


######################################################

def p_triples_block_0(p):
    """
    triples_block : triples_same_subject_path POINT triples_block
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = p[1] + p[3]


def p_triples_block_1(p):
    """
    triples_block : triples_same_subject_path POINT
    """
    p[0] = p[1]


def p_triples_block_2(p):
    """
    triples_block : triples_same_subject_path
    """
    p[0] = p[1]


######################################################
# TriplesBlock
"""    
    TriplesSameSubjectPath	  ::=  	VarOrTerm PropertyListPathNotEmpty | TriplesNodePath PropertyListPath
    PropertyListPath	  ::=  	PropertyListPathNotEmpty?    
"""


######################################################
def p_triples_same_subject_path_0(p):
    """
    triples_same_subject_path : var_or_term property_list_path_not_empty
    """
    p[0] = [TriplePattern(p[1], pr, o) for pr, o in p[2]]


def p_triples_same_subject_path_1(p):
    """
    triples_same_subject_path :  triples_node_path property_list_path
    """
    p[0] = [TriplePattern(s, pr, o) for s, pr, o in p[1]] + p[2]


def p_property_list_path_0(p):
    """
    property_list_path :  property_list_path_not_empty
    """
    p[0] = p[1]


def p_property_list_path_1(p):
    """
    property_list_path :  empty
    """
    p[0] = []


######################################################
# TriplesBlock - PropertyListPathNotEmpty
"""        
    PropertyListPathNotEmpty	  ::=  	( VerbPath | VerbSimple ) ObjectListPath ( ';' ( ( VerbPath | VerbSimple ) ObjectList )? )*  
"""


######################################################
def p_property_list_path_not_empty_0(p):
    """
    property_list_path_not_empty :  verb_path object_list_path object_list_path_expr
    """
    # print(p[3])
    l1 = [(p[1], obj1) for obj1 in p[2]]
    p[0] = l1 + p[3]


def p_property_list_path_not_empty_1(p):
    """
    property_list_path_not_empty :  verb_simple object_list_path object_list_path_expr
    """
    l1 = [(p[1], obj1) for obj1 in p[2]]
    p[0] = l1 + p[3]


def p_object_list_path_expr_0(p):
    """
    object_list_path_expr :  SEMI_COLON verb_path object_list object_list_path_expr
    """
    l1 = [(p[2], obj1) for obj1 in p[3]]
    p[0] = l1 + p[4]


def p_object_list_path_expr_1(p):
    """
    object_list_path_expr :  SEMI_COLON verb_simple object_list object_list_path_expr
    """
    l1 = [(p[2], obj1) for obj1 in p[3]]
    p[0] = l1 + p[4]


def p_object_list_path_expr_2(p):
    """
    object_list_path_expr :  SEMI_COLON object_list_path_expr
    """
    p[0] = p[2]


def p_object_list_path_expr_3(p):
    """
    object_list_path_expr :  empty
    """
    p[0] = []


######################################################
# TriplesBlock
""" 
  	VerbPath	  ::=  	Path
  	VerbSimple	  ::=  	Var
  	ObjectListPath	  ::=  	ObjectPath ( ',' ObjectPath )*  	
"""


######################################################

def p_verb_path(p):
    """
    verb_path : path
    """
    p[0] = p[1]


def p_verb_simple(p):
    """
    verb_simple : VAR
    """
    p[0] = RDFTerm(str(p[1]), is_const=False)


def p_object_list_path(p):
    """
    object_list_path : object_path object_path_expr
    """
    p[0] = p[1] + p[2]


def p_object_path_expr_0(p):
    """
    object_path_expr : COMA object_path object_path_expr
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = p[2] + p[3]


def p_object_path_expr_1(p):
    """
    object_path_expr : empty
    """
    p[0] = []


######################################################
# ObjectPath
"""
  	ObjectPath	  ::=  	GraphNodePath
  	GraphNodePath	  ::=  	VarOrTerm | TriplesNodePath
  	TriplesNodePath	  ::=  	CollectionPath | BlankNodePropertyListPath  	
  	BlankNodePropertyListPath	  ::=  	'[' PropertyListPathNotEmpty ']'   	
"""


######################################################
def p_object_path(p):
    """
     object_path : graph_node_path
    """
    p[0] = p[1]


def p_graph_node_path_0(p):
    """
    graph_node_path : var_or_term
    """
    p[0] = [p[1]]


def p_graph_node_path_1(p):
    """
    graph_node_path : triples_node_path
    """
    p[0] = p[1]


def p_triples_node_path(p):
    """
    triples_node_path : collection_path
                        | blank_node_property_list_path
    """
    p[0] = p[1]


def p_blank_node_property_list_path(p):
    """
    blank_node_property_list_path : LBRC  property_list_path_not_empty RBRC
    """
    # p[0] = '\t' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = [(RDFTerm('[]', is_const=True, is_bnode=True), pr, o) for pr, o in p[2]]


########################################################
# CollectionPath
"""
    CollectionPath	  ::=  	'(' GraphNodePath+ ')'
    GraphNodePath	  ::=  	VarOrTerm | TriplesNodePath    
"""


#######################################################
def p_collection_path(p):
    """
    collection_path : LPAR  graph_node_path graph_node_paths RPAR
    """
    p[0] = p[2] + p[3]


def p_graph_node_paths_0(p):
    """
    graph_node_paths : graph_node_path graph_node_paths
    """
    # p[0] = str(p[1]) + ' ' + str(p[2])
    p[0] = p[1] + p[2]


def p_graph_node_paths_1(p):
    """
    graph_node_paths : empty
    """
    p[0] = []


######################################################
# TriplesBlock
"""
  	Path	  ::=  	PathAlternative
  	PathAlternative	  ::=  	PathSequence ( '|' PathSequence )*
  	PathSequence	  ::=  	PathEltOrInverse ( '/' PathEltOrInverse )*
"""


######################################################
def p_path(p):
    """
    path : path_alternative
    """
    p[0] = p[1]


def p_path_alternative(p):
    """
    path_alternative :  path_sequence path_sequence_expr
    """
    if len(p[2]) > 0:
        oper, right = p[2]
        p[0] = PropertyPath(p[1], oper, right)
    else:
        p[0] = p[1]


def p_path_sequence_expr_0(p):
    """
    path_sequence_expr :  PIPE path_sequence path_sequence_expr
    """
    if len(p[3]) > 0:
        oper, right = p[3]
        p[0] = p[1], PropertyPath(p[2], oper, right)
    else:
        p[0] = p[1], p[2]


def p_path_sequence_expr_1(p):
    """
    path_sequence_expr :  empty
    """
    p[0] = ()


def p_path_sequence(p):
    """
    path_sequence :  path_elt_or_inverse path_elt_or_inverse_expr
    """
    if len(p[2]) > 0:
        oper, right = p[2]
        p[0] = PropertyPath(p[1], oper, right)
    else:
        p[0] = p[1]


def p_path_elt_or_inverse_expr_0(p):
    """
    path_elt_or_inverse_expr : ART_DIV path_elt_or_inverse path_elt_or_inverse_expr
    """
    if len(p[3]) > 0:
        oper, right = p[3]
        p[0] = p[1], PropertyPath(p[2], oper, right)
    else:
        p[0] = p[1], p[2]


def p_path_elt_or_inverse_expr_1(p):
    """
    path_elt_or_inverse_expr : empty
    """
    p[0] = ()


######################################################
# TriplesBlock
"""
    PathEltOrInverse	  ::=  	PathElt | '^' PathElt
  	PathElt	  ::=  	PathPrimary PathMod?  	
  	PathMod	  ::=  	'?' | '*' | '+'
"""


######################################################

def p_path_elt_or_inverse(p):
    """
    path_elt_or_inverse : path_elt
                            | path_elt_expr
    """
    if isinstance(p[1], tuple):
        term, mode = p[1]
        p[0] = PathTerm(term, False, mode)
    else:
        p[0] = p[1]


def p_path_elt_expr(p):
    """
    path_elt_expr : CARRET path_elt
    """
    term, mode = p[2]
    p[0] = PathTerm(term, True, mode)


def p_path_elt(p):
    """
    path_elt : path_primary path_mod
    """
    if p[2] is None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2]


def p_path_mod_0(p):
    """
    path_mod : 	QMARK
                | ALL
                | ART_PLUS
    """
    p[0] = str(p[1])


def p_path_mod_1(p):
    """
    path_mod : 	empty
    """
    p[0] = None


######################################################
# TriplesBlock - PathPrimary
"""  
  	PathPrimary	  ::=  	iri | 'a' | '!' PathNegatedPropertySet | '(' Path ')'
  	PathNegatedPropertySet	  ::=  	PathOneInPropertySet | '(' ( PathOneInPropertySet ( '|' PathOneInPropertySet )* )? ')'
  	PathOneInPropertySet	  ::=  	iri | 'a' | '^' ( iri | 'a' ) 
"""


######################################################
def p_path_primary_0(p):
    """
    path_primary :  iri
    """
    p[0] = p[1]


def p_path_primary_1(p):
    """
    path_primary : ID
    """
    #  | not_path_negated_property_set # not implemented atm
    if str(p[1]) == 'a':
        value = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
        p[0] = RDFTerm(value, is_const=True, is_iri=True)
    else:
        print('raising syntax error:')
        p_error(str(p[1]))
        raise SyntaxError


def p_path_primary_2(p):
    """
    path_primary :  bracketed_path
    """
    #  | not_path_negated_property_set  # not implemented atm
    p[0] = p[1]


def p_bracketed_path(p):
    """
    bracketed_path :  LPAR path RPAR
    """
    p[0] = p[2]


#########################################################
# Collections
"""
    Collection	  ::=  	'(' GraphNode+ ')'
    GraphNode	  ::=  	VarOrTerm | TriplesNode
    TriplesNode	  ::=  	Collection | BlankNodePropertyList
    BlankNodePropertyList	  ::=  	'[' PropertyListNotEmpty ']'
    PropertyListNotEmpty	  ::=  	Verb ObjectList ( ';' ( Verb ObjectList )? )*
"""


#########################################################
def p_collection(p):
    """
    collection :  LPAR graph_node graph_nodes RPAR
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4])
    p[0] = p[2] + p[3]


def p_graph_nodes_0(p):
    """
    graph_nodes :  graph_node graph_nodes
    """
    p[0] = p[1] + p[2]


def p_graph_nodes_1(p):
    """
    graph_nodes :  empty
    """
    p[0] = []


def p_graph_node_0(p):
    """
    graph_node : var_or_term
    """
    p[0] = [p[1]]


def p_graph_node_1(p):
    """
    graph_node : triples_node
    """
    p[0] = p[1]


def p_triples_node(p):
    """
    triples_node : 	collection
                    | blank_node_property_list
    """
    p[0] = p[1]


def p_blank_node_property_list(p):
    """
    blank_node_property_list :  LBRC property_list_not_empty RBRC
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = p[2]


def p_property_list_not_empty_0(p):
    """
    property_list_not_empty :  verb object_list verb_object_list_expr
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = [(p[1], o) for o in p[2]] + p[3]


def p_verb_object_list_expr_0(p):
    """
    verb_object_list_expr :  SEMI_COLON verb_object_list verb_object_list_expr
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = p[2] + p[3]


def p_verb_object_list_expr_1(p):
    """
    verb_object_list_expr :  SEMI_COLON verb_object_list_expr
    """
    p[0] = p[2]


def p_verb_object_list_expr_2(p):
    """
    verb_object_list_expr :  empty
    """
    p[0] = []


def p_verb_object_list(p):
    """
    verb_object_list :  verb object_list
    """
    # p[0] = str(p[1]) + ' ' + str(p[2])
    p[0] = [(p[1], o) for o in p[2]]


def p_verb_0(p):
    """
    verb :  ID
    """
    if str(p[1]) == 'a':
        value = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
        p[0] = RDFTerm(value, is_const=True, is_iri=True)
    else:
        print('raising syntax error:')
        p_error(str(p[1]))
        raise SyntaxError


def p_verb_1(p):
    """
    verb :  VAR
    """
    p[0] = RDFTerm(p[1], is_const=False)


def p_verb_2(p):
    """
    verb :  iri
    """
    p[0] = p[1]


################################################
# Solution modifier
"""
    SolutionModifier	  ::=  	GroupClause? HavingClause? OrderClause? LimitOffsetClauses?
  	GroupClause	          ::=  	'GROUP' 'BY' GroupCondition+
  	GroupCondition	      ::=  	BuiltInCall | FunctionCall | '(' Expression ( 'AS' Var )? ')' | Var
  	HavingClause	      ::=  	'HAVING' HavingCondition+
  	HavingCondition	      ::=  	Constraint
  	OrderClause	          ::=  	'ORDER' 'BY' OrderCondition+
  	OrderCondition	      ::=  	( ( 'ASC' | 'DESC' ) BrackettedExpression ) | ( Constraint | Var )
  	LimitOffsetClauses	  ::=  	LimitClause OffsetClause? | OffsetClause LimitClause?
  	LimitClause	          ::=  	'LIMIT' INTEGER
 	OffsetClause	      ::=  	'OFFSET' INTEGER
"""


#####################################
def p_solution_modifier_0(p):
    """
     solution_modifier : group_clause having_clause order_clause limit_offset_clauses
    """
    limit, offset = p[4]
    p[0] = {'GROUP BY': p[1], 'HAVING': p[2], 'ORDER BY': p[3], 'LIMIT': limit, 'OFFSET': offset}


# additions by me
def p_solution_modifier_1(p):
    """
     solution_modifier : having_clause group_clause order_clause limit_offset_clauses
    """
    limit, offset = p[4]
    p[0] = {'HAVING': p[1], 'GROUP BY': p[2], 'ORDER BY': p[3], 'LIMIT': limit, 'OFFSET': offset}


# additions by me
def p_solution_modifier_2(p):
    """
     solution_modifier : order_clause group_clause having_clause  limit_offset_clauses
    """
    limit, offset = p[4]
    p[0] = {'ORDER BY': p[1], 'GROUP BY': p[2], 'HAVING': p[3], 'LIMIT': limit, 'OFFSET': offset}


# additions by me
def p_solution_modifier_3(p):
    """
     solution_modifier : group_clause order_clause having_clause limit_offset_clauses
    """
    limit, offset = p[4]
    p[0] = {'GROUP BY': p[1], 'ORDER BY': p[2], 'HAVING': p[3], 'LIMIT': limit, 'OFFSET': offset}


# additions by me
def p_solution_modifier_4(p):
    """
     solution_modifier : order_clause having_clause group_clause limit_offset_clauses
    """
    limit, offset = p[4]
    p[0] = {'ORDER BY': p[1], 'HAVING': p[2], 'GROUP BY': p[3], 'LIMIT': limit, 'OFFSET': offset}


# additions by me
def p_solution_modifier_5(p):
    """
     solution_modifier : having_clause order_clause group_clause limit_offset_clauses
    """
    limit, offset = p[4]
    p[0] = {'HAVING': p[1], 'ORDER BY': p[2], 'GROUP BY': p[3], 'LIMIT': limit, 'OFFSET': offset}


def p_group_clause_0(p):
    """
     group_clause : GROUP BY group_condition
    """
    p[0] = p[3]


def p_group_clause_1(p):
    """
     group_clause : empty
    """
    p[0] = []


def p_group_condition_0(p):
    """
     group_condition : group_expr group_condition
    """
    p[0] = [p[1]] + p[2]


def p_group_condition_1(p):
    """
     group_condition : group_expr
    """
    p[0] = [p[1]]


def p_group_expr_0(p):
    """
    group_expr : built_in_call
    """
    p[0] = p[1]


def p_group_expr_1(p):
    """
    group_expr : function_call
    """
    p[0] = p[1]


def p_group_expr_2(p):
    """
    group_expr : LPAR expression AS VAR RPAR
    """
    p[0] = Expression(p[1], "AS", RDFTerm(p[3], is_const=False))


def p_group_expr_3(p):
    """
    group_expr : LPAR expression RPAR
    """
    p[0] = p[2]


def p_group_expr_4(p):
    """
    group_expr : VAR
    """
    p[0] = RDFTerm(str(p[1]), is_const=False)


# having clause
def p_having_clause_0(p):
    """
     having_clause : HAVING having_condition
    """
    p[0] = p[2]


def p_having_clause_1(p):
    """
     having_clause : empty
    """
    p[0] = []


def p_having_condition_0(p):
    """
     having_condition : constraint having_condition
    """
    p[0] = [p[1]] + p[2]


def p_having_condition_1(p):
    """
     having_condition : constraint
    """
    p[0] = [p[1]]


# ORDER BY clause
def p_order_clause_0(p):
    """
    order_clause : ORDER BY order_condition
    """
    p[0] = p[3]


def p_order_clause_1(p):
    """
     order_clause : empty
    """
    p[0] = []


def p_order_condition_0(p):
    """
    order_condition :  ASC bracketted_expression  order_condition
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = [Expression(p[2], p[1])] + p[3]


def p_order_condition_1(p):
    """
    order_condition :  DESC bracketted_expression  order_condition
    """
    p[0] = [Expression(p[2], p[1])] + p[3]


def p_order_condition_2(p):
    """
    order_condition :  bracketted_expression  order_condition
    """
    p[0] = [Expression(p[1], 'ASC')] + p[2]


def p_order_condition_3(p):
    """
    order_condition : constraint  order_condition
    """
    p[0] = [Expression(p[1], 'ASC')] + p[2]


def p_order_condition_4(p):
    """
    order_condition : VAR  order_condition
    """
    p[0] = [Expression(RDFTerm(p[1], is_const=False), 'ASC')] + p[2]


def p_order_condition_5(p):
    """
    order_condition :  ASC bracketted_expression
    """
    p[0] = [Expression(p[2], p[1])]


def p_order_condition_6(p):
    """
    order_condition :  DESC bracketted_expression
    """
    p[0] = [Expression(p[2], p[1])]


# additions by me
def p_order_condition_7(p):
    """
    order_condition :  bracketted_expression
    """
    p[0] = [p[1]]


def p_order_condition_8(p):
    """
    order_condition : constraint
    """
    p[0] = [p[1]]


def p_order_condition_9(p):
    """
    order_condition : VAR
    """
    p[0] = [RDFTerm(p[1], is_const=False)]


# LIMIT OFFSET clauses
###
def p_limit_offset_clauses_0(p):
    """
    limit_offset_clauses : 	limit_clause offset_clause
    """
    p[0] = p[1], p[2]


def p_limit_offset_clauses_1(p):
    """
    limit_offset_clauses : 	limit_clause
    """
    p[0] = p[1], -1


def p_limit_offset_clauses_2(p):
    """
    limit_offset_clauses : 	offset_clause limit_clause
    """
    p[0] = p[2], p[1]


def p_limit_offset_clauses_3(p):
    """
    limit_offset_clauses : 	offset_clause
    """
    p[0] = -1, p[1]


def p_limit_offset_clauses_4(p):
    """
    limit_offset_clauses : 	empty
    """
    p[0] = -1, -1


def p_limit_clause(p):
    """
    limit_clause : LIMIT INTEGER
    """
    p[0] = p[2]


def p_offset_clause(p):
    """
    offset_clause : OFFSET INTEGER
    """
    p[0] = p[2]


# ignore empty
def p_empty(p):
    """
    empty :
    """
    pass


###########################################################################################################
# Expressions
"""
    Expression	                ::=  	ConditionalOrExpression
  	ConditionalOrExpression	    ::=  	ConditionalAndExpression ( '||' ConditionalAndExpression )*
  	ConditionalAndExpression	::=  	ValueLogical ( '&&' ValueLogical )*
  	ValueLogical	            ::=  	RelationalExpression
"""


############################################################################################################
def p_expression(p):
    """
    expression : conditional_or_expression
    """
    p[0] = p[1]


def p_conditional_or_expression(p):
    """
    conditional_or_expression : conditional_and_expression or_expr
    """
    if p[2] is not None:
        p[0] = Expression(p[1], "||", p[2])
    else:
        p[0] = p[1]


def p_or_expr_0(p):
    """
    or_expr : OR conditional_and_expression
    """
    # p[0] = str(p[1]) + ' ' + str(p[2])
    p[0] = p[2]


def p_or_expr_1(p):
    """
    or_expr : ORSYMB conditional_and_expression
    """
    # p[0] = str(p[1]) + ' ' + str(p[2])
    p[0] = p[2]


def p_or_expr_2(p):
    """
    or_expr : empty
    """
    p[0] = None


def p_conditional_and_expression(p):
    """
    conditional_and_expression :  value_logical and_expr
    """
    if p[2] is not None:
        p[0] = Expression(p[1], "&&", p[2])
    else:
        p[0] = p[1]


def p_and_expr_0(p):
    """
    and_expr :  AND value_logical
    """
    p[0] = p[2]


def p_and_expr_1(p):
    """
    and_expr :  ANDSYMB value_logical
    """
    p[0] = p[2]


def p_and_expr_2(p):
    """
    and_expr : empty
    """
    p[0] = None


def p_value_logical(p):
    """
    value_logical :  relational_expression
    """
    p[0] = p[1]


#########################################
# Relational expressions
"""
    RelationalExpression	  ::=  	NumericExpression ( '=' NumericExpression 
                                                        | '!=' NumericExpression 
                                                        | '<' NumericExpression 
                                                        | '>' NumericExpression 
                                                        | '<=' NumericExpression 
                                                        | '>=' NumericExpression 
                                                        | 'IN' ExpressionList 
                                                        | 'NOT' 'IN' ExpressionList )?
    NumericExpression	  ::=  	AdditiveExpression
    ExpressionList	  ::=  	NIL | '(' Expression ( ',' Expression )* ')' 
"""


#######################################
def p_relational_expression_0(p):
    """
    relational_expression : numeric_expression EQUALSSYM numeric_expression
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
    p[0] = Expression(p[1], "=", p[3])


def p_relational_expression_1(p):
    """
    relational_expression : numeric_expression NEQUALSSYM numeric_expression
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
    p[0] = Expression(p[1], "!=", p[3])


def p_relational_expression_2(p):
    """
    relational_expression : numeric_expression LESS numeric_expression
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
    p[0] = Expression(p[1], "<", p[3])


def p_relational_expression_3(p):
    """
    relational_expression : numeric_expression GREATER numeric_expression
    """
    p[0] = Expression(p[1], ">", p[3])


def p_relational_expression_4(p):
    """
    relational_expression : numeric_expression LESSEQ numeric_expression
    """
    p[0] = Expression(p[1], "<=", p[3])


def p_relational_expression_5(p):
    """
    relational_expression : numeric_expression GREATEREQ numeric_expression
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
    p[0] = Expression(p[1], ">=", p[3])


def p_relational_expression_6(p):
    """
    relational_expression : numeric_expression IN expression_list
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
    p[0] = Expression(p[1], "IN", p[3])


def p_relational_expression_7(p):
    """
    relational_expression : numeric_expression NOT IN expression_list
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3]) + " " + str(p[4])
    p[0] = Expression(p[1], "NOT IN", p[4])


def p_relational_expression_8(p):
    """
    relational_expression : numeric_expression
    """
    p[0] = p[1]


def p_numeric_expression(p):
    """
     numeric_expression : additive_expression
    """
    p[0] = p[1]


def p_expression_list_0(p):
    """
    expression_list :  NIL
    """
    p[0] = [RDFTerm('', is_const=True, is_nil=True)]


def p_expression_list_1(p):
    """
    expression_list :  LPAR expression other_expr_list RPAR
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4])
    p[0] = [p[2]] + p[3]


def p_expression_list_2(p):
    """
    expression_list :  LPAR expression RPAR
    """
    # p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])
    p[0] = [p[2]]


def p_other_expr_list_0(p):
    """
    other_expr_list : COMA expression other_expr_list
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
    p[0] = [p[2]] + p[3]


def p_other_expr_list_1(p):
    """
    other_expr_list : empty
    """
    p[0] = []


###############################################################
# Additive expression
"""
    AdditiveExpression	  ::=  	MultiplicativeExpression ( '+' MultiplicativeExpression 
                                                            | '-' MultiplicativeExpression 
                                                            | ( NumericLiteralPositive 
                                                                | NumericLiteralNegative 
                                                               ) 
                                                              ( ( '*' UnaryExpression ) 
                                                                    | ( '/' UnaryExpression ) 
                                                                )* 
                                                        )*
"""


#######################################################
def p_additive_expression(p):
    """
    additive_expression :  multiplicative_expression add_minus_div_mult_expr
    """
    # p[0] = str(p[1]) + " " + str(p[2])
    if len(p[2]) > 0:
        op, right = p[2]
        p[0] = Expression(p[1], op, right)
    else:
        p[0] = p[1]


def p_add_minus_div_mult_expr_0(p):
    """
     add_minus_div_mult_expr : add_or_minus_multiplicative_expr
    """
    p[0] = p[1]


def p_add_minus_div_mult_expr_1(p):
    """
     add_minus_div_mult_expr : mult_or_div_multiplicative_expr
    """
    p[0] = p[1]


def p_add_minus_div_mult_expr_2(p):
    """
     add_minus_div_mult_expr : empty
    """
    p[0] = []


#
# def p_additive_expression_1(p):
#     """
#     additive_expression :  multiplicative_expression mult_or_div_multiplicative_expr
#     """
#     # p[0] = str(p[1]) + " " + str(p[2])
#     if len(p[2]) > 0:
#         op, right = p[2]
#         p[0] = Expression(p[1], op, right)
#     else:
#         p[0] = str(p[1])


def p_add_or_minus_multiplicative_expr_0(p):
    """
     add_or_minus_multiplicative_expr : ART_PLUS multiplicative_expression add_minus_div_mult_expr
    """
    if len(p[3]) > 0:
        op, right = p[3]
        p[0] = p[1], Expression(p[2], op, right)
    else:
        p[0] = p[1], p[2]


def p_add_or_minus_multiplicative_expr_1(p):
    """
     add_or_minus_multiplicative_expr : ART_MINUS multiplicative_expression add_minus_div_mult_expr
    """
    if len(p[3]) > 0:
        op, right = p[3]
        p[0] = p[1], Expression(p[2], op, right)
    else:
        p[0] = p[1], p[2]


def p_mult_or_div_multiplicative_expr_0(p):
    """
     mult_or_div_multiplicative_expr :  numeric_literal_positive  art_mult_or_art_div_unary_expr add_minus_div_mult_expr
    """
    if len(p[2]) > 0:
        op, right = p[2]
        if len(p[3]) > 0:
            op2, right2 = p[3]
            p[0] = str(p[1])[:1], Expression(Expression(RDFTerm(str(p[1])[1:], is_const=True), op, right), op2, right2)
        else:
            p[0] = str(p[1])[:1], Expression(RDFTerm(str(p[1])[1:], is_const=True), op, right)
    elif len(p[3]) > 0:
        op2, right2 = p[3]
        p[0] = str(p[1])[:1], Expression(RDFTerm(str(p[1])[1:], is_const=True), op2, right2)
    else:
        p[0] = str(p[1])[:1], RDFTerm(str(p[1])[1:], is_const=True)


def p_mult_or_div_multiplicative_expr_1(p):
    """
     mult_or_div_multiplicative_expr :  numeric_literal_negative art_mult_or_art_div_unary_expr add_minus_div_mult_expr
    """
    if len(p[2]) > 0:
        op, right = p[2]
        if len(p[3]) > 0:
            op2, right2 = p[3]
            p[0] = str(p[1])[:1], Expression(Expression(RDFTerm(str(p[1])[1:], is_const=True), op, right), op2, right2)
        else:
            p[0] = str(p[1])[:1], Expression(RDFTerm(str(p[1])[1:], is_const=True), op, right)
    elif len(p[3]) > 0:
        op2, right2 = p[3]
        p[0] = str(p[1])[:1], Expression(RDFTerm(str(p[1])[1:], is_const=True), op2, right2)
    else:
        p[0] = str(p[1])[:1], RDFTerm(str(p[1])[1:], is_const=True)


def p_art_mult_or_art_div_unary_expr_0(p):
    """
     art_mult_or_art_div_unary_expr : ALL unary_expression art_mult_or_art_div_unary_expr
    """
    if len(p[3]) > 0:
        op, right = p[3]
        p[0] = p[1], Expression(p[2], op, right)
    else:
        p[0] = p[1], p[2]


def p_art_mult_or_art_div_unary_expr_1(p):
    """
     art_mult_or_art_div_unary_expr : ART_DIV unary_expression art_mult_or_art_div_unary_expr
    """
    if len(p[3]) > 0:
        op, right = p[3]
        p[0] = p[1], Expression(p[2], op, right)
    else:
        p[0] = p[1], p[2]


def p_art_mult_or_art_div_unary_expr_2(p):
    """
     art_mult_or_art_div_unary_expr : empty
    """
    p[0] = ''


##############################################
# multiplicative_expression
"""
    MultiplicativeExpression	  ::=  	UnaryExpression ( '*' UnaryExpression | '/' UnaryExpression )*    
"""


#################################################
def p_multiplicative_expression(p):
    """
    multiplicative_expression :  unary_expression art_mult_or_div_unary_expr
    """
    if len(p[2]) > 0:
        op, right = p[2]
        p[0] = Expression(p[1], op, right)
    else:
        p[0] = p[1]


def p_art_mult_or_div_unary_expr_0(p):
    """
     art_mult_or_div_unary_expr : ALL unary_expression art_mult_or_div_unary_expr
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
    if len(p[3]) > 0:
        op, right = p[3]
        p[0] = p[1], Expression(p[2], op, right)
    else:
        p[0] = p[1], p[2]


def p_art_mult_or_div_unary_expr_1(p):
    """
     art_mult_or_div_unary_expr : ART_DIV unary_expression art_mult_or_div_unary_expr
    """
    if len(p[3]) > 0:
        op, right = p[3]
        p[0] = p[1], Expression(p[2], op, right)
    else:
        p[0] = p[1], p[2]


def p_art_mult_or_div_unary_expr_2(p):
    """
     art_mult_or_div_unary_expr : empty
    """
    p[0] = []


######################################
# Unary Expressions
"""
    UnaryExpression	  ::=  	  '!' PrimaryExpression
                               | '+' PrimaryExpression
                               | '-' PrimaryExpression
                               | PrimaryExpression
    PrimaryExpression	  ::=  	BrackettedExpression 
                                | BuiltInCall 
                                | iriOrFunction 
                                | RDFLiteral 
                                | NumericLiteral 
                                | BooleanLiteral 
                                | Var
    BrackettedExpression	  ::=  	'(' Expression ')'
    iriOrFunction	  ::=  	iri ArgList?
"""


########################
def p_unary_expression_0(p):
    """
    unary_expression :  NEG primary_expression
    """
    p[0] = Expression(p[2], str(p[1]))


def p_unary_expression_1(p):
    """
    unary_expression :  ART_PLUS primary_expression
    """
    p[0] = Expression(p[2], str(p[1]))


def p_unary_expression_2(p):
    """
    unary_expression :  ART_MINUS primary_expression
    """
    p[0] = Expression(p[2], str(p[1]))


def p_unary_expression_3(p):
    """
    unary_expression : primary_expression
    """
    p[0] = p[1]


def p_primary_expression_0(p):
    """
     primary_expression :  	bracketted_expression
                            | iri_or_function
                            | built_in_call
                            | rdf_literal
                            | numeric_literal
                            | boolean_literal
    """
    p[0] = p[1]


def p_primary_expression_1(p):
    """
     primary_expression :  	VAR
    """
    p[0] = RDFTerm(p[1], is_const=False)


def p_bracketted_expression(p):
    """
    bracketted_expression :  LPAR expression RPAR
    """
    p[0] = p[2]


###################
# IRIORFunction
"""
    iriOrFunction	  ::=  	iri ArgList?
"""


###################
def p_iri_or_function_0(p):
    """
    iri_or_function :  	iri arg_list
    """
    p[0] = Expression(p[2], str(p[1]))


def p_iri_or_function_1(p):
    """
    iri_or_function :  	iri
    """
    p[0] = p[1]


##################################################################################
# Built-in Function Calls
"""
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
                        | 'CONCAT' ExpressionList
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
"""


##########################################################################
def p_built_in_call_0(p):
    """
     built_in_call : STR LPAR expression RPAR
                    | LANG LPAR expression RPAR
                    | DATATYPE LPAR expression RPAR
                    | IRI LPAR expression RPAR
                    | URI LPAR expression RPAR
                    | ABS LPAR expression RPAR
                    | CEIL LPAR expression RPAR
                    | FLOOR LPAR expression RPAR
                    | ROUND LPAR expression RPAR
                    | STRLEN LPAR expression RPAR
                    | UCASE LPAR expression RPAR
                    | LCASE LPAR expression RPAR
                    | ENCODE_FOR_URI LPAR expression RPAR
                    | YEAR LPAR expression RPAR
                    | MONTH LPAR expression RPAR
                    | DAY LPAR expression RPAR
                    | HOURS LPAR expression RPAR
                    | MINUTES LPAR expression RPAR
                    | SECONDS LPAR expression RPAR
                    | TIMEZONE LPAR expression RPAR
                    | TZ LPAR expression RPAR
                    | MD5 LPAR expression RPAR
                    | SHA1 LPAR expression RPAR
                    | SHA256 LPAR expression RPAR
                    | SHA384 LPAR expression RPAR
                    | SHA512 LPAR expression RPAR
                    | isIRI LPAR expression RPAR
                    | isURI LPAR expression RPAR
                    | isBLANK LPAR expression RPAR
                    | isLITERAL LPAR expression RPAR
                    | isNUMERIC LPAR expression RPAR
                    | BNODE LPAR expression RPAR
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3]) + " " + str(p[4])
    p[0] = Expression(p[3], str(p[1]))


def p_built_in_call_1(p):
    """
     built_in_call : LANGMATCHES LPAR expression COMA expression RPAR
                    | CONTAINS LPAR expression COMA expression RPAR
                    | STRSTARTS LPAR expression COMA expression RPAR
                    | STRENDS LPAR expression COMA expression RPAR
                    | STRBEFORE LPAR expression COMA expression RPAR
                    | STRAFTER LPAR expression COMA expression RPAR
                    | STRLANG LPAR expression COMA expression RPAR
                    | STRDT LPAR expression COMA expression RPAR
                    | SAMETERM LPAR expression COMA expression RPAR
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3]) + " " + str(p[4]) + " " + str(p[5]) + " " + str(p[6])
    p[0] = Expression(p[3], str(p[1]), p[5])


def p_built_in_call_2(p):
    """
     built_in_call : RAND NIL
                    | NOW NIL
                    | UUID NIL
                    | STRUUID NIL
                    | BNODE NIL
    """
    p[0] = Expression(RDFTerm('()', is_const=True, is_nil=True), str(p[1]))


def p_built_in_call_3(p):
    """
     built_in_call : aggregate
                    | regex_expression
                    | exists_func
                    | not_exists_func
                    | substring_expression
                    | str_replace_expression
                    | if_else_func
    """
    p[0] = p[1]


def p_built_in_call_4(p):
    """
     built_in_call : BOUND LPAR VAR RPAR
    """
    p[0] = Expression(RDFTerm(str(p[3]), is_const=False), str(p[1]))


def p_built_in_call_5(p):
    """
     built_in_call : CONCAT expression_list
    """
    p[0] = Expression(p[2], p[1])


def p_built_in_call_6(p):
    """
     built_in_call : COALESCE expression_list
    """
    p[0] = Expression(p[2], p[1])


#######################################
# Aggregate
"""
    Aggregate	  ::=  	  'COUNT' '(' 'DISTINCT'? ( '*' | Expression ) ')'
                        | 'SUM' '(' 'DISTINCT'? Expression ')'
                        | 'MIN' '(' 'DISTINCT'? Expression ')'
                        | 'MAX' '(' 'DISTINCT'? Expression ')'
                        | 'AVG' '(' 'DISTINCT'? Expression ')'
                        | 'SAMPLE' '(' 'DISTINCT'? Expression ')'
                        | 'GROUP_CONCAT' '(' 'DISTINCT'? Expression ( ';' 'SEPARATOR' '=' String )? ')' 
"""


######################################
def p_aggregate_0(p):
    """
    aggregate : SUM LPAR distinct expression RPAR
                | MIN LPAR distinct expression RPAR
                | MAX LPAR distinct expression RPAR
                | AVG LPAR distinct expression RPAR
                | SAMPLE LPAR distinct expression RPAR
                | COUNT LPAR distinct expression RPAR
                | COUNT LPAR distinct ALL RPAR
    """
    if p[3]:
        p[0] = Expression(p[3], p[1], p[4])
    else:
        p[0] = Expression(p[4], p[1])


def p_aggregate_1(p):
    """
    aggregate :  GROUP_CONCAT LPAR distinct expression concat_equals_str RPAR
    """
    if p[3]:
        p[0] = Expression(p[3], p[1], p[4], str(p[5]))
    else:
        p[0] = Expression(p[3], p[1], p[4], str(p[5]))


def p_aggregate_2(p):
    """
    aggregate :  GROUP_CONCAT LPAR distinct expression RPAR
    """
    if p[3]:
        p[0] = Expression(p[3], p[1], p[4])
    else:
        p[0] = Expression(p[4], p[1])


def p_concat_equals_str(p):
    """
     concat_equals_str :  SEMI_COLON SEPARATOR EQUALSSYM string
    """
    # p[0] = str(p[1]) + " " + str(p[2]) + " " + str(p[3]) + " " + str(p[4])
    p[0] = str(p[4])


####################################
# REGEX Expression
"""
    RegexExpression	  ::=  	'REGEX' '(' Expression ',' Expression ( ',' Expression )? ')'
"""


###################################
def p_regex_expression_0(p):
    """
    regex_expression : REGEX LPAR expression COMA expression COMA expression RPAR
    """
    p[0] = Expression(p[3], str(p[1]), p[5], p[7])


def p_regex_expression_1(p):
    """
    regex_expression : REGEX LPAR expression COMA expression RPAR
    """
    p[0] = Expression(p[3], str(p[1]), p[5])


####################################
#### IF else funct #################
"""
    'IF' '(' Expression ',' Expression ',' Expression ')'
"""


###################################

def p_if_else_func(p):
    """
    if_else_func : IF LPAR expression COMA expression COMA expression RPAR
    """
    p[0] = Expression(p[3], str(p[1]), p[5], p[7])


#######################################################
# exists_func
"""
    	ExistsFunc	  ::=  	'EXISTS' GroupGraphPattern
"""


########################################################
def p_exists_func(p):
    """
    exists_func :  EXISTS group_graph_pattern
    """
    # p[0] = str(p[1]) + " " + str(p[2])
    p[0] = Expression(p[2], str(p[1]))


#################################
# substring_expression
"""
    SubstringExpression	  ::=  	'SUBSTR' '(' Expression ',' Expression ( ',' Expression )? ')'
"""


#################################
def p_substring_expression_0(p):
    """
    substring_expression : SUBSTR LPAR expression COMA expression COMA expression RPAR
    """
    p[0] = Expression(p[3], str(p[1]), p[5], p[7])


def p_substring_expression_1(p):
    """
    substring_expression : SUBSTR LPAR expression COMA expression RPAR
    """
    p[0] = Expression(p[3], str(p[1]), p[5])


##################################
# not_exists_func
"""
    NotExistsFunc	  ::=  	'NOT' 'EXISTS' GroupGraphPattern
"""


##############################
def p_not_exists_func(p):
    """
    not_exists_func :  NOT EXISTS group_graph_pattern
    """
    p[0] = Expression(p[3], str(p[1]) + ' ' + str(p[2]))


################################
# str_replace_expression
"""
    StrReplaceExpression	  ::=  	'REPLACE' '(' Expression ',' Expression ',' Expression ( ',' Expression )? ')'
"""


############################
def p_str_replace_expression_0(p):
    """
    str_replace_expression :  REPLACE LPAR expression COMA expression COMA expression COMA expression RPAR
    """
    p[0] = Expression(p[3], str(p[1]), p[5], p[7], p[9])


def p_str_replace_expression_1(p):
    """
    str_replace_expression :  REPLACE LPAR expression COMA expression COMA expression RPAR
    """
    p[0] = Expression(p[3], str(p[1]), p[5], p[7])


########################################################################################################
# VAR OR Term
"""
    VarOrTerm	  ::=  	Var | GraphTerm  	
    GraphTerm	  ::=  	iri | RDFLiteral | NumericLiteral | BooleanLiteral | BlankNode | NIL
"""


####################################################################################################
def p_var_or_term_0(p):
    """
    var_or_term : VAR
    """
    p[0] = RDFTerm(str(p[1]), is_const=False)


def p_var_or_term_1(p):
    """
    var_or_term : graph_term
    """
    p[0] = p[1]


def p_graph_term_0(p):
    """
    graph_term : iri
    """
    p[0] = p[1]


def p_graph_term_1(p):
    """
    graph_term : rdf_literal
    """
    p[0] = p[1]


def p_graph_term_2(p):
    """
    graph_term : numeric_literal
    """
    p[0] = p[1]


def p_graph_term_3(p):
    """
    graph_term : boolean_literal
    """
    p[0] = p[1]


def p_graph_term_4(p):
    """
    graph_term : blank_node
    """
    p[0] = p[1]


def p_graph_term(p):
    """
    graph_term : NIL
    """
    p[0] = RDFTerm(str(p[1]), is_const=True, is_nil=True)


###############################
# RDF Literal
"""
    RDFLiteral	              ::=  	String ( LANGTAG | ( '^^' iri ) )?
  	String	                  ::=  	STRING_LITERAL1 | STRING_LITERAL2 | STRING_LITERAL_LONG1 | STRING_LITERAL_LONG2  	
  	iri	                      ::=  	IRIREF | PrefixedName
"""


#############################
def p_rdf_literal(p):
    """
    rdf_literal : string language_or_type
    """
    langtype = str(p[2]).strip()
    if len(langtype) > 0:
        if '@' == langtype[0]:
            p[0] = RDFTerm(str(p[1]), is_const=True, lang_tag=langtype[1:])
        elif '^' == langtype[0]:
            p[0] = RDFTerm(str(p[1]), is_const=True, xsd_datatype=langtype[2:])
    else:
        p[0] = RDFTerm(str(p[1]), is_const=True)


def p_language_or_type_0(p):
    """
    language_or_type : language
    """
    p[0] = str(p[1])


def p_language_or_type_1(p):
    """
    language_or_type : typed_literal
    """
    p[0] = str(p[1])


def p_language(p):
    """
    language : LANGTAG
    """
    p[0] = str(p[1])


def p_typed_literal(p):
    """
    typed_literal : CARRET CARRET iri
    """
    p[0] = str(p[1] + p[2]) + str(p[3])


def p_language_or_type_2(p):
    """
    language_or_type : empty
    """
    p[0] = ''


def p_string(p):
    """
    string :  STRING_LITERAL1
                | STRING_LITERAL2
                | STRING_LITERAL_LONG1
                | STRING_LITERAL_LONG2
    """
    p[0] = str(p[1])


#####################################################
# BlankNode
"""
    BlankNode	  ::=  	BLANK_NODE_LABEL | ANON
"""


######################################################
def p_blank_node(p):
    """
    blank_node : BLANK_NODE_LABEL
                    | ANON
    """
    p[0] = RDFTerm(str(p[1]), is_const=True, is_bnode=True)


###########################################
# Numeric Literal
"""    
  	NumericLiteral	          ::=  	NumericLiteralUnsigned | NumericLiteralPositive | NumericLiteralNegative
  	NumericLiteralUnsigned	  ::=  	INTEGER | DECIMAL | DOUBLE
  	NumericLiteralPositive	  ::=  	INTEGER_POSITIVE | DECIMAL_POSITIVE | DOUBLE_POSITIVE
  	NumericLiteralNegative	  ::=  	INTEGER_NEGATIVE | DECIMAL_NEGATIVE | DOUBLE_NEGATIVE
  	BooleanLiteral	          ::=  	'true' | 'false'  	
"""


##########################################
def p_numeric_literal_0(p):
    """
    numeric_literal :  numeric_literal_unsigned
    """
    p[0] = RDFTerm(str(p[1]), is_const=True)


def p_numeric_literal_1(p):
    """
    numeric_literal :  numeric_literal_positive
    """
    p[0] = RDFTerm(str(p[1]), is_const=True)


def p_numeric_literal_2(p):
    """
    numeric_literal : numeric_literal_negative
    """
    p[0] = RDFTerm(str(p[1]), is_const=True)


def p_numeric_literal_unsigned_0(p):
    """
    numeric_literal_unsigned :  INTEGER
    """
    p[0] = str(p[1])


def p_numeric_literal_unsigned_1(p):
    """
    numeric_literal_unsigned :  DECIMAL
    """
    p[0] = str(p[1])


def p_numeric_literal_unsigned_2(p):
    """
    numeric_literal_unsigned :  DOUBLE
    """
    p[0] = str(p[1])


def p_numeric_literal_positive_0(p):
    """
    numeric_literal_positive :  INTEGER_POSITIVE
    """
    p[0] = str(p[1])


def p_numeric_literal_positive_1(p):
    """
    numeric_literal_positive :  DECIMAL_POSITIVE
    """
    p[0] = str(p[1])


def p_numeric_literal_positive_2(p):
    """
    numeric_literal_positive :  DOUBLE_POSITIVE
    """
    p[0] = str(p[1])


def p_numeric_literal_negative_0(p):
    """
    numeric_literal_negative : INTEGER_NEGATIVE
    """
    p[0] = str(p[1])


def p_numeric_literal_negative_1(p):
    """
    numeric_literal_negative : DECIMAL_NEGATIVE
    """
    p[0] = str(p[1])


def p_numeric_literal_negative_2(p):
    """
    numeric_literal_negative : DOUBLE_NEGATIVE
    """
    p[0] = str(p[1])


def p_boolean_literal_0(p):
    """
    boolean_literal : LTRUE
    """
    # p[0] = str(p[1])
    p[0] = RDFTerm(str(p[1]), is_const=True)


def p_boolean_literal_1(p):
    """
    boolean_literal : LFALSE
    """
    # p[0] = str(p[1])
    p[0] = RDFTerm(str(p[1]), is_const=True)


#################################################
# IRI
"""
    iri	            ::=  	IRIREF | PrefixedName
    PrefixedName	::=  	PNAME_LN | PNAME_NS
"""


################################################
def p_iri_0(p):
    """
    iri : IRIREF
    """
    p[0] = RDFTerm(str(p[1]), is_const=True, is_iri=True)


#
#
# def p_iri_1(p):
#     """
#     iri : prefixed_name
#     """
#     p[0] = str(p[1])


def p_iri_1(p):
    """
    iri : ID COLON ID
    """
    p[0] = RDFTerm(str(p[1]) + str(p[2]) + str(p[3]), is_const=True, is_iri=True, prefix=str(p[1]))


def p_iri_2(p):
    """
    iri : COLON ID
    """
    # p[0] = '<noname> ' + str(p[1]) + ' ' + str(p[2])
    p[0] = RDFTerm(str(p[1]) + str(p[2]), is_const=True, is_iri=True, prefix='')


def p_iri_3(p):
    """
    iri : COLON
    """
    # p[0] = '<noname> ' + str(p[1]) + '<noname> '
    p[0] = RDFTerm(str(p[1]), is_const=True, is_iri=True, prefix='')


# ##########################################
# # VarORIri
# """
#     VarOrIri	  ::=  	Var | iri
# """
# ########################################
# def p_var_or_iri(p):
#     """
#     var_or_iri : VAR
#     """
#     if not isinstance(str(p[1]), RDFTerm):
#         p[0] = RDFTerm(str(p[1]), is_const=False)
#     else:
#         p[0] = str(p[1])

# Helpers
xstring = ""

_lexer = lex.lex()
_sparql_parser = yacc.yacc(debug=1)


def sparql(string):
    global xstring
    xstring = string
    return _sparql_parser.parse(string, lexer=_lexer)


if __name__ == '__main__':
    prefixes = """    
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
    query = sparql(prefixes)

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

    print(query)
    # print(type(query))
    # print(query.projections)
    # print(query.distinct)
    # print(query.dataset_clauses)
    # for ggp in query.ggp.ggps:
    #     print(type(ggp))
    #     print(ggp)
