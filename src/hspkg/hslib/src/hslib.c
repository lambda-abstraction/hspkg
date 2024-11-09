#include "cbits.h"
#include <stdlib.h>

static PyMethodDef hslib_methods[] = {
    {"hs_fib", hs_fib, METH_O, NULL},
    {NULL, NULL, 0, NULL}, // Sentinel
};

static struct PyModuleDef hslib_definition = {
    PyModuleDef_HEAD_INIT,
    "hslib",
    NULL,
    -1,
    hslib_methods,
};

static void haskell_rts() {
    int32_t argc = 2;
    char *argv[] = {"+RTS", "-A32m", 0};
    char **pargv = argv;
    hs_init(&argc, &pargv);
    atexit(hs_exit);
}

PyMODINIT_FUNC PyInit_hslib() {
    haskell_rts();
    PyObject *hslib = PyModule_Create(&hslib_definition);
    return hslib;
}