/* interface de gerador de parser */

extern grammar gram;

extern grammar *meta_grammar PROTO((void));
extern grammar *pgen PROTO((node *));