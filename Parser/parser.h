/* interface de parser */

#define MAXSTACK 100

typedef struct _stackentry {
    int         s_state; /* estado do dfa atual */
    dfa         *s_dfa; /* dfa atual */
    node        *s_parent; /* aonde adicionar o próximo node */
} stackentry;

typedef struct _stack {
    stackentry  *s_top; /* entrada top */
    stackentry  s_base[MAXSTACK]; /* array das entradas de stack */
} stack;

typedef struct {
    struct _stack   p_stack; /* stack dos estados do parser */
    struct _grammar *p_grammar; /* gramática a ser utilizada */
    struct _node    *p_tree; /* top da árvore de parse */
} parser_state;

parser_state *newparser PROTO((struct _grammar *g, int start));
void delparser PROTO((parser_state *ps));
int addtoken PROTO((parser_state *ps, int type, char *str));