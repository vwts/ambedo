/* interface de objeto classe */

/*
classes são hackeadas no último momento

deverá ser possível utilizar outros tipos de objeto como classes base,
porém atualmente não dá
*/

extern typeobject Classtype, Classmembertype, Classmethodtype;

#define is_classobject(op) ((op)->ob_type == &Classtype)
#define is_classmemberobject(op) ((op)->ob_type == &Classmembertype)
#define is_classmethodobject(op) ((op)->ob_type == &Classmethodtype)

extern object *newclassobject PROTO((node *, object *, object *));
extern object *newclassmemberobject PROTO((object *));
extern object *newclassmethodobject PROTO((object *, object *));

extern object *classmethodgetfunc PROTO((object *));
extern object *classmethodgetself PROTO((object *));