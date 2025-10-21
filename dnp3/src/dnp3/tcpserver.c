#include <Python.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdatomic.h>
#include "dnp3.h"

static void on_log_message(dnp3_log_level_t level, const char *msg, void *ctx) {
    static PyObject *logging_library = NULL;
    static PyObject *logging_object = NULL;

    PyGILState_STATE gstate;
    gstate = PyGILState_Ensure();

    if (logging_library == NULL || logging_object == NULL) {
        logging_library = PyImport_ImportModule("logging");
        if (logging_library == NULL) {
            PyErr_Print();
            return;
        }

        logging_object = PyObject_CallMethod(logging_library, "getLogger", "s", "outstation");
        if (logging_object == NULL) {
            PyErr_Print();
            Py_DECREF(logging_library);
            return;
        }
    }

    PyObject *logging_message = PyUnicode_FromString(msg);
    if (logging_message == NULL) {
        PyErr_Print();
        PyGILState_Release(gstate);
        return;
    }

    const char *method_name;
    switch (level) {
        // Python's logger doesn't have a trace level
        case DNP3_LOG_LEVEL_TRACE:
        case DNP3_LOG_LEVEL_DEBUG:
            method_name = "debug";
            break;
        case DNP3_LOG_LEVEL_INFO:
            method_name = "info";
            break;
        case DNP3_LOG_LEVEL_WARN:
            method_name = "warning";
            break;
        case DNP3_LOG_LEVEL_ERROR:
            method_name = "error";
            break;
        default:
            method_name = "info";
            break;
    }

    // Returns None, which is an immortal object since Python 3.12 (https://peps.python.org/pep-0683/)
    // So no need to Py_DECREF the return value
    PyObject_CallMethod(logging_object, method_name, "O", logging_message);
    Py_DECREF(logging_message);
    PyGILState_Release(gstate);
}

static dnp3_logger_t get_logger() {
    return (dnp3_logger_t){
        .on_message = &on_log_message,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

static dnp3_runtime_t* init_runtime() {
    dnp3_runtime_t *runtime = NULL;
    // initialize logging with the default configuration
    dnp3_configure_logging(dnp3_logging_config_init(), get_logger());

    // Create runtime
    dnp3_runtime_config_t runtime_config = dnp3_runtime_config_init();
    runtime_config.num_core_threads = 0;  // defaults to number of cores
    dnp3_param_error_t err = dnp3_runtime_create(runtime_config, &runtime);
    if (err) {
        fprintf(stderr, "Unable to create runtime: %s \n", dnp3_param_error_to_string(err));
        return NULL;
    }
    return runtime;
}

dnp3_outstation_server_t* init_server(dnp3_runtime_t *runtime, const char *socket_addr) {
    dnp3_outstation_server_t *server = NULL;
    dnp3_param_error_t err = dnp3_outstation_server_create_tcp_server(runtime, DNP3_LINK_ERROR_MODE_CLOSE, socket_addr, &server);
    if (err) {
        fprintf(stderr, "Unable to create TCP server: %s \n", dnp3_param_error_to_string(err));
        return NULL;
    }
    return server;
}

int start_server(dnp3_outstation_server_t *server) {
    dnp3_param_error_t err = dnp3_outstation_server_bind(server);
    if (err) {
        fprintf(stderr, "Unable to bind server: %s \n", dnp3_param_error_to_string(err));
        return -1;
    }
    return 0;
}

static void destroy_runtime(dnp3_runtime_t *runtime) {
    dnp3_runtime_set_shutdown_timeout(runtime, 1);
    dnp3_runtime_destroy(runtime);
}

// Capsule Destructors

static void server_capsule_destructor(PyObject *capsule) {
    dnp3_outstation_server_t *server = PyCapsule_GetPointer(capsule, "dnp3_outstation_server");
    if (server) {
        dnp3_outstation_server_destroy(server);
    }
}

// Wrapper functions
static PyObject* dnp3_wrapper_init_runtime(PyObject *self, PyObject *Py_UNUSED(args)) {
    dnp3_runtime_t *runtime = init_runtime();
    if (runtime == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to initialize runtime");
        return NULL;
    }
    return PyCapsule_New(runtime, "dnp3_runtime_t", NULL);
}

static PyObject* dnp3_wrapper_init_server(PyObject *self, PyObject *args) {
    PyObject *runtime_capsule;
    const char *socket_addr;

    if (!PyArg_ParseTuple(args, "Os", &runtime_capsule, &socket_addr)) {
        return NULL;
    }

    dnp3_runtime_t *runtime = PyCapsule_GetPointer(runtime_capsule, "dnp3_runtime_t");
    if (runtime == NULL) {
        PyErr_SetString(PyExc_ValueError, "Invalid runtime capsule");
        return NULL;
    }

    dnp3_outstation_server_t *server = init_server(runtime, socket_addr);
    if (server == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to initialize server");
        return NULL;
    }
    return PyCapsule_New(server, "dnp3_outstation_server", server_capsule_destructor);
}

static PyObject* dnp3_wrapper_start_server(PyObject *self, PyObject *args) {
    PyObject *server_capsule;

    if (!PyArg_ParseTuple(args, "O", &server_capsule)) {
        return NULL;
    }

    dnp3_outstation_server_t *server = PyCapsule_GetPointer(server_capsule, "dnp3_outstation_server");
    if (server == NULL) {
        PyErr_SetString(PyExc_ValueError, "Invalid server capsule");
        return NULL;
    }

    int result = start_server(server);
    if (result != 0) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to start server");
        return NULL;
    }
    Py_RETURN_NONE;
}


static PyObject* dnp3_wrapper_destroy_runtime(PyObject *self, PyObject *args) {
    PyObject *runtime_capsule;
    if (!PyArg_ParseTuple(args, "O", &runtime_capsule)) {
        return NULL;
    }
    dnp3_runtime_t *runtime = PyCapsule_GetPointer(runtime_capsule, "dnp3_runtime_t");
    if (runtime == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid runtime capsule");
        return NULL;
    }
    destroy_runtime(runtime);
    Py_RETURN_NONE;
}


// Method definitions
static PyMethodDef methods[] = {
    {"init_runtime", dnp3_wrapper_init_runtime, METH_NOARGS, "Initializes the DNP3 runtime."},
    {"init_server", dnp3_wrapper_init_server, METH_VARARGS, "Initializes the DNP3 server."},
    {"start_server", dnp3_wrapper_start_server, METH_VARARGS, "Starts the DNP3 server."},
    {"destroy_runtime", dnp3_wrapper_destroy_runtime, METH_VARARGS, "Destroy runtime(runtime_capsule)"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef tcpserver_module = {
    PyModuleDef_HEAD_INIT,
    "dnp3_module",
    "DNP3 TCP server module extension",
    -1,
    methods
};

// Module initialization function
PyMODINIT_FUNC PyInit_tcpserver(void)
{
    return PyModule_Create(&tcpserver_module);
}
