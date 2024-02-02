/* implementação de objeto type */

#include <stdio.h>

#include "PROTO.h"
#include "object.h"
#include "stringobject.h"
#include "objimpl.h"

/* implementação de objeto type */

static void
typescript(v, fp, flags)
    typeobject *v;
    FILE *fp;
    int flags;
{
    fprintf(fp, "<type '%s'>", v->tp_name);
}

static object *
typerepr(v)
    typeobject *v;
{
    char buf[100];

    sprintf(buf, "<type '%.80s'>", v->tp_name);

    return newstringobject(buf);
}

typedef struct {
    OB_HEAD
    long ob_ival;
} intobject;

typeobject Typetype = {
    OB_HEAD_INIT(&Typetype)
    0,                  /* número de itens para varobject */
    "type",             /* nome desse tipo */
    sizeof(typeobject), /* tamanho padrão de objeto */
    0,                  /* tamanho de item para varobject */
    0,                  /* tp_dealloc */
    typeprint,          /* tp_print */
    0,                  /* tp_getattr */
    0,                  /* tp_setattr */
    0,                  /* tp_compare */
    typerepr            /* tp_repr */
};