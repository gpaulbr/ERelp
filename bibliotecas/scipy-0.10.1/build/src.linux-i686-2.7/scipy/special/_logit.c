#line 1 "scipy/special/_logit.c.src"

/*
 *****************************************************************************
 **       This file was autogenerated from a template  DO NOT EDIT!!!!      **
 **       Changes should be made to the original source (.src) file         **
 *****************************************************************************
 */

#line 1
/*-*-c-*-*/

/*
 * ufuncs to compute logit(p) = log(p/(1-p)) and
 * expit(x) = 1/(1+exp(-x))
 */

#include <Python.h>
#include <math.h>

#include "numpy/npy_math.h"
#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"

/*
 * Inner loops for logit and expit
 */

#line 23

static void
logit_loopf(char **args, npy_intp *dimensions,
              npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in = args[0], *out = args[1];
    npy_intp in_step = steps[0], out_step = steps[1];

    npy_float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(npy_float *)in;
        tmp /= 1 - tmp;
        *((npy_float *)out) = npy_logf(tmp);

        in += in_step;
        out += out_step;
    }
}

static void
expit_loopf(char **args, npy_intp *dimensions,
              npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in = args[0], *out = args[1];
    npy_intp in_step = steps[0], out_step = steps[1];

    npy_float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(npy_float *)in;
        if (tmp > 0) {
            tmp = npy_expf(tmp);
            *((npy_float *)out) = tmp / (1 + tmp);
        }
        else{
            *((npy_float *)out) = 1 / (1 + npy_expf(-tmp));
        }
        in += in_step;
        out += out_step;
    }
}


#line 23

static void
logit_loop(char **args, npy_intp *dimensions,
              npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in = args[0], *out = args[1];
    npy_intp in_step = steps[0], out_step = steps[1];

    npy_double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(npy_double *)in;
        tmp /= 1 - tmp;
        *((npy_double *)out) = npy_log(tmp);

        in += in_step;
        out += out_step;
    }
}

static void
expit_loop(char **args, npy_intp *dimensions,
              npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in = args[0], *out = args[1];
    npy_intp in_step = steps[0], out_step = steps[1];

    npy_double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(npy_double *)in;
        if (tmp > 0) {
            tmp = npy_exp(tmp);
            *((npy_double *)out) = tmp / (1 + tmp);
        }
        else{
            *((npy_double *)out) = 1 / (1 + npy_exp(-tmp));
        }
        in += in_step;
        out += out_step;
    }
}


#line 23

static void
logit_loopl(char **args, npy_intp *dimensions,
              npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in = args[0], *out = args[1];
    npy_intp in_step = steps[0], out_step = steps[1];

    npy_longdouble tmp;

    for (i = 0; i < n; i++) {
        tmp = *(npy_longdouble *)in;
        tmp /= 1 - tmp;
        *((npy_longdouble *)out) = npy_logl(tmp);

        in += in_step;
        out += out_step;
    }
}

static void
expit_loopl(char **args, npy_intp *dimensions,
              npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *in = args[0], *out = args[1];
    npy_intp in_step = steps[0], out_step = steps[1];

    npy_longdouble tmp;

    for (i = 0; i < n; i++) {
        tmp = *(npy_longdouble *)in;
        if (tmp > 0) {
            tmp = npy_expl(tmp);
            *((npy_longdouble *)out) = tmp / (1 + tmp);
        }
        else{
            *((npy_longdouble *)out) = 1 / (1 + npy_expl(-tmp));
        }
        in += in_step;
        out += out_step;
    }
}



/*
 * Definitions for the ufuncs.
 */

static PyUFuncGenericFunction expit_funcs[3] = {&expit_loopf,
                                                &expit_loop,
                                                &expit_loopl};

static PyUFuncGenericFunction logit_funcs[3] = {&logit_loopf,
                                                &logit_loop,
                                                &logit_loopl};

static char types[6] = {NPY_FLOAT, NPY_FLOAT,
                        NPY_DOUBLE, NPY_DOUBLE,
                        NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void *data[3] = {NULL, NULL, NULL};

/* Module definition */

static PyMethodDef module_methods[] = {
    { NULL, NULL, 0, NULL }
};

#if PY_VERSION_HEX >= 0x03000000

static PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_logit",
    NULL,
    -1,
    module_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit__logit()
{
    PyObject *m, *f, *d;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }

    import_array();
    import_umath();

    d = PyModule_GetDict(m);

    f = PyUFunc_FromFuncAndData(logit_funcs,data, types, 3, 1, 1,
                                PyUFunc_None, "logit",NULL , 0);
    PyDict_SetItemString(d, "logit", f);
    Py_DECREF(f);

    f = PyUFunc_FromFuncAndData(expit_funcs,data, types, 3, 1, 1,
                                PyUFunc_None, "expit",NULL , 0);
    PyDict_SetItemString(d, "expit", f);
    Py_DECREF(f);

    return m;
}

#else

PyMODINIT_FUNC
init_logit()
{
    PyObject *m, *f,  *d;

    m  = Py_InitModule("_logit", module_methods);
    if (m == NULL) {
        return;
    }

    d = PyModule_GetDict(m);

    import_array();
    import_umath();

    f = PyUFunc_FromFuncAndData(logit_funcs,data, types, 3, 1, 1,
                                PyUFunc_None, "logit",NULL , 0);
    PyDict_SetItemString(d , "logit", f);
    Py_DECREF(f);


    f = PyUFunc_FromFuncAndData(expit_funcs,data, types, 3, 1, 1,
                                PyUFunc_None, "expit",NULL , 0);
    PyDict_SetItemString(d , "expit", f);
    Py_DECREF(f);
}

#endif

