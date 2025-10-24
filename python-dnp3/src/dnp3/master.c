#include <Python.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <pthread.h>

#include "dnp3.h"

static void log_message(dnp3_log_level_t level, const char *msg) {
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

        logging_object = PyObject_CallMethod(logging_library, "getLogger", "s", "master");
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

static void on_log_message(dnp3_log_level_t level, const char *msg, void *ctx) {
    log_message(level, msg);
}

dnp3_logger_t get_logger() {
    return (dnp3_logger_t){
        // function pointer where log messages will be sent
        .on_message = &on_log_message,
        // no context to free
        .on_destroy = NULL,
        // optional context argument applied to all log callbacks
        .ctx = NULL,
    };
}
// ANCHOR_END: logging_callback

// ClientState listener callback
void client_state_on_change(dnp3_client_state_t state, void *arg) { 
    // No logging here, see https://github.com/cps-vip/cps-cosimulation-env/wiki/Kaden-McCartney's-Notebook#outstanding-issues
}

dnp3_client_state_listener_t get_client_state_listener()
{
    return (dnp3_client_state_listener_t){
        .on_change = &client_state_on_change,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

// PortState listener callback
void port_state_on_change(dnp3_port_state_t state, void *arg) { 
    // printf("PortState = %s\n", dnp3_port_state_to_string(state)); 
}

dnp3_port_state_listener_t get_port_state_listener()
{    
    return (dnp3_port_state_listener_t){
        .on_change = &port_state_on_change,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

// ANCHOR: read_handler
void begin_fragment(dnp3_read_type_t read_type, dnp3_response_header_t header, void *arg) {
    char* string;
    if (asprintf(&string, "Beginning fragment (broadcast: %u)\n", header.iin.iin1.broadcast) < 0) {
        fprintf(stderr, "Failed to allocate memory for log message\n");
        return;
    }
    log_message(DNP3_LOG_LEVEL_INFO, string);
    free(string);
}

void end_fragment(dnp3_read_type_t read_type, dnp3_response_header_t header, void *arg) { 
    log_message(DNP3_LOG_LEVEL_INFO, "End fragment\n");
}

void handle_binary_input(dnp3_header_info_t info, dnp3_binary_input_iterator_t *it, void *arg)
{
    // printf("Binaries:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_binary_input_t *value = NULL;
    while ((value = dnp3_binary_input_iterator_next(it))) {
        // printf("BI %u: Value=%u Flags=0x%02X Time=%" PRIu64 "\n", value->index, value->value, value->flags.value, value->time.value);
    }
}

void handle_double_bit_binary_input(dnp3_header_info_t info, dnp3_double_bit_binary_input_iterator_t *it, void *arg)
{
    // printf("Double Bit Binaries:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_double_bit_binary_input_t *value = NULL;
    while ((value = dnp3_double_bit_binary_input_iterator_next(it))) {
        // printf("DBBI %u: Value=%X Flags=0x%02X Time=%" PRIu64 "\n", value->index, value->value, value->flags.value, value->time.value);
    }
}

void handle_binary_output_status(dnp3_header_info_t info, dnp3_binary_output_status_iterator_t *it, void *arg)
{
    // printf("Binary Output Statuses:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_binary_output_status_t *value = NULL;
    while ((value = dnp3_binary_output_status_iterator_next(it))) {
        // printf("BOS %u: Value=%u Flags=0x%02X Time=%" PRIu64 "\n", value->index, value->value, value->flags.value, value->time.value);
    }
}

void handle_counter(dnp3_header_info_t info, dnp3_counter_iterator_t *it, void *arg)
{
    // printf("Counters:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_counter_t *value = NULL;
    while ((value = dnp3_counter_iterator_next(it))) {
        // printf("Counter %u: Value=%u Flags=0x%02X Time=%" PRIu64 "\n", value->index, value->value, value->flags.value, value->time.value);
    }
}

void handle_frozen_counter(dnp3_header_info_t info, dnp3_frozen_counter_iterator_t *it, void *arg)
{
    // printf("Frozen Counters:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_frozen_counter_t *value = NULL;
    while ((value = dnp3_frozen_counter_iterator_next(it))) {
        // printf("Frozen Counter %u: Value=%u Flags=0x%02X Time=%" PRIu64 "\n", value->index, value->value, value->flags.value, value->time.value);
    }
}

void handle_analog_input(dnp3_header_info_t info, dnp3_analog_input_iterator_t *it, void *arg)
{
    // printf("Analogs:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_analog_input_t *value = NULL;
    while ((value = dnp3_analog_input_iterator_next(it))) {
        // printf("AI %u: Value=%f Flags=0x%02X Time=%" PRIu64 "\n", value->index, value->value, value->flags.value, value->time.value);
    }
}

void handle_analog_output_status(dnp3_header_info_t info, dnp3_analog_output_status_iterator_t *it, void *arg)
{
    // printf("Analog Output Statuses:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_analog_output_status_t *value = NULL;
    // while ((value = dnp3_analog_output_status_iterator_next(it))) {
    //     printf("AOS %u: Value=%f Flags=0x%02X Time=%" PRIu64 "\n", value->index, value->value, value->flags.value, value->time.value);
    // }
}

void handle_octet_strings(dnp3_header_info_t info, dnp3_octet_string_iterator_t *it, void *arg)
{
    // printf("Octet Strings:\n");
    // printf("Qualifier: %s \n", dnp3_qualifier_code_to_string(info.qualifier));
    // printf("Variation: %s \n", dnp3_variation_to_string(info.variation));

    dnp3_octet_string_t *value = NULL;
    while ((value = dnp3_octet_string_iterator_next(it))) {
        // printf("Octet String: %u: Value=", value->index);
        uint8_t *byte = dnp3_byte_iterator_next(value->value);
        while (byte != NULL) {
            // printf("%02X", *byte);
            byte = dnp3_byte_iterator_next(value->value);
        }

        // printf("\n");
    }
}

void handle_string_attr(dnp3_header_info_t info, dnp3_string_attr_t attr, uint8_t set, uint8_t variation, const char* value, void *arg)
{
    // printf("String attribute: %s set: %d var: %d value: %s \n", dnp3_string_attr_to_string(attr), set, variation, value);
}
// ANCHOR_END: read_handler

dnp3_read_handler_t get_read_handler()
{
    return (dnp3_read_handler_t){
        .begin_fragment = &begin_fragment,
        .end_fragment = &end_fragment,
        .handle_binary_input = &handle_binary_input,
        .handle_double_bit_binary_input = &handle_double_bit_binary_input,
        .handle_binary_output_status = &handle_binary_output_status,
        .handle_counter = &handle_counter,
        .handle_frozen_counter = &handle_frozen_counter,
        .handle_analog_input = &handle_analog_input,
        .handle_analog_output_status = &handle_analog_output_status,
        .handle_octet_string = &handle_octet_strings,
        .handle_string_attr = &handle_string_attr,        
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

// read callbacks
void on_read_success(dnp3_nothing_t nothing, void *arg) { 
    // printf("read success! \n"); 
}
void on_read_failure(dnp3_read_error_t error, void* arg) {
    // printf("read error: %s \n", dnp3_read_error_to_string(error)); 
}

// Command callbacks
// ANCHOR: assoc_control_callback
void on_command_success(dnp3_nothing_t nothing, void* arg)
{
    // printf("command success!\n");
}
void on_command_error(dnp3_command_error_t result, void *arg)
{
    // printf("command failed: %s\n", dnp3_command_error_to_string(result));
}
// ANCHOR_END: assoc_control_callback

// time sync callbacks
void on_time_sync_success(dnp3_nothing_t nothing, void* arg) { 
    // printf("time sync success! \n"); 
}
void on_time_sync_error(dnp3_time_sync_error_t error, void *arg) {
    // printf("Time sync error: %s\n", dnp3_time_sync_error_to_string(error)); 
}

// warm/cold restart callbacks
void on_restart_success(uint64_t delay, void *arg) { 
    // printf("restart success: %" PRIu64 "\n", delay); 
}
void on_restart_failure(dnp3_restart_error_t error, void* arg) {
    // printf("Restart failure: %s\n", dnp3_restart_error_to_string(error)); 
}

// link status callbacks
void on_link_status_success(dnp3_nothing_t nothing, void *arg) {
    // printf("link status success!\n"); 
}
void on_link_status_failure(dnp3_link_status_error_t error, void* arg) {
    // printf("link status error: %s\n", dnp3_link_status_error_to_string(error)); 
}

// generic callbacks
void on_generic_success(dnp3_nothing_t delay, void *arg) { 
    // printf("%s success! \n", (const char*) arg); 
}
void on_generic_failure(dnp3_empty_response_error_t error, void *arg)
{
    // printf("%s failure: %s\n", (const char *)arg, dnp3_empty_response_error_to_string(error));
}

// ANCHOR: association_config
dnp3_association_config_t get_association_config()
{
    dnp3_association_config_t config = dnp3_association_config_init(
        // disable unsolicited first (Class 1/2/3)
        dnp3_event_classes_all(),
        // after the integrity poll, enable unsolicited (Class 1/2/3)
        dnp3_event_classes_all(),
        // perform startup integrity poll with Class 1/2/3/0
        dnp3_classes_all(),
        // don't automatically scan Class 1/2/3 when the corresponding IIN bit is asserted
        dnp3_event_classes_none());

    config.auto_time_sync = DNP3_AUTO_TIME_SYNC_LAN;
    config.keep_alive_timeout = 60;
    return config;
}
// ANCHOR_END: association_config

// ANCHOR: association_handler
dnp3_utc_timestamp_t get_system_time(void *arg)
{
    time_t timer = time(NULL);

    return dnp3_utc_timestamp_valid(timer * 1000);
}

dnp3_association_handler_t get_association_handler()
{
    return (dnp3_association_handler_t){
        .get_current_time = get_system_time,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}
// ANCHOR_END: association_handler

// ANCHOR: association_information
void task_start(dnp3_task_type_t task_type, dnp3_function_code_t fc, uint8_t seq, void *arg)
{

}

void task_success(dnp3_task_type_t task_type, dnp3_function_code_t fc, uint8_t seq, void *arg)
{
    
}

void task_fail(dnp3_task_type_t task_type, dnp3_task_error_t error, void *arg)
{
    
}

void unsolicited_response(bool is_duplicate, uint8_t seq, void *arg)
{
    
}

dnp3_association_information_t get_association_information()
{
    return (dnp3_association_information_t){
        .task_start = task_start,
        .task_success = task_success,
        .task_fail = task_fail,
        .unsolicited_response = unsolicited_response,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}
// ANCHOR_END: association_information




dnp3_master_channel_config_t create_master_channel_config(int master_address)
{
    dnp3_master_channel_config_t config = dnp3_master_channel_config_init(master_address);
    config.decode_level.application = DNP3_APP_DECODE_LEVEL_OBJECT_VALUES;
    return config;
}


int add_association(dnp3_master_channel_t *channel, int outstation_addr, dnp3_association_id_t *association_id) {
    dnp3_param_error_t err =
        dnp3_master_channel_add_association(
            channel,
            outstation_addr,
            get_association_config(),
            get_read_handler(),
            get_association_handler(),
            get_association_information(),
            association_id
        );

    if (err) {
        printf("unable to add association: %s \n", dnp3_param_error_to_string(err));
        return -1;
    }
    return 0;
}

int create_poll(dnp3_master_channel_t *channel, dnp3_association_id_t association_id) {
    dnp3_request_t *poll_request = dnp3_request_new_class(false, true, true, true);
    dnp3_poll_id_t poll_id;
    dnp3_param_error_t err = dnp3_master_channel_add_poll(channel, association_id, poll_request, 1000, &poll_id);
    dnp3_request_destroy(poll_request);
    if (err) {
        printf("unable to add poll: %s \n", dnp3_param_error_to_string(err));
        return -1;
    }
    return 0;
}

void destroy_channel(dnp3_master_channel_t *channel) {
    dnp3_master_channel_destroy(channel);
}

dnp3_master_channel_t* create_tcp_channel(dnp3_runtime_t *runtime, int master_addr, char* endpoint_socket_addr, dnp3_master_channel_config_t *config)
{
    dnp3_master_channel_t* channel = NULL;
    dnp3_endpoint_list_t* endpoints = dnp3_endpoint_list_create(endpoint_socket_addr);

    dnp3_param_error_t err = dnp3_master_channel_create_tcp(
        runtime,
        DNP3_LINK_ERROR_MODE_CLOSE,
        *config,
        endpoints,
        dnp3_connect_strategy_init(),
        get_client_state_listener(),
        &channel
    );
    dnp3_endpoint_list_destroy(endpoints);

    if (err) {
        printf("unable to create TCP channel: %s \n", dnp3_param_error_to_string(err));
        return NULL;
    }

    return channel;
}

// Initialises logger and runtime
static dnp3_runtime_t* init_runtime()
{
    dnp3_runtime_t *runtime = NULL;

    // Hopefully very minimal overhead to just keeping at INFO here, 
    // and letting the Python logger filter out anything it needs to
    dnp3_logging_config_t logging_config = {
        DNP3_LOG_LEVEL_INFO,  
        DNP3_LOG_OUTPUT_FORMAT_TEXT,
        DNP3_TIME_FORMAT_NONE,  // let Python logger handle
        false,  // don't print log level, let Python logger handle
        false
    };

    dnp3_configure_logging(logging_config, get_logger());

    // Create runtime
    dnp3_runtime_config_t runtime_config = dnp3_runtime_config_init();
    runtime_config.num_core_threads = 0;  // defaults to number of cores
    dnp3_param_error_t err = dnp3_runtime_create(runtime_config, &runtime);
    if (err) {
        printf("unable to create runtime: %s \n", dnp3_param_error_to_string(err));
        return NULL;
    }
    return runtime;

}

void destroy_runtime(dnp3_runtime_t *runtime) {
    dnp3_runtime_set_shutdown_timeout(runtime, 1);
    dnp3_runtime_destroy(runtime);
}

void enable_master_channel(dnp3_master_channel_t *channel) {
    dnp3_master_channel_enable(channel);
}

void disable_master_channel(dnp3_master_channel_t *channel) {
    dnp3_master_channel_disable(channel);
}


// Capsule destructor functions
static void channel_destructor(PyObject *capsule) {
    dnp3_master_channel_t *channel = PyCapsule_GetPointer(capsule, "dnp3_master_channel_t");
    if (channel) {
        dnp3_master_channel_destroy(channel);
    }
}

static void config_destructor(PyObject *capsule) {
    dnp3_master_channel_config_t *config = PyCapsule_GetPointer(capsule, "dnp3_master_channel_config_t");
    if (config) {
        free(config); // Assuming malloc was used to allocate config
    }
}

// Python wrapper functions
static PyObject* py_create_master_channel_config(PyObject *self, PyObject *args) {
    int master_address;
    if (!PyArg_ParseTuple(args, "i", &master_address)) {
        return NULL; // TypeError is raised by PyArg_ParseTuple
    }
    dnp3_master_channel_config_t config = create_master_channel_config(master_address);
    dnp3_master_channel_config_t *config_ptr = (dnp3_master_channel_config_t*)malloc(sizeof(dnp3_master_channel_config_t));
    if (!config_ptr) {
        PyErr_NoMemory();
        return NULL;
    }
    *config_ptr = config; // Copy the struct
    return PyCapsule_New((void*)config_ptr, "dnp3_master_channel_config_t", config_destructor);
}


static PyObject* py_create_tcp_channel(PyObject *self, PyObject *args) {
    PyObject *runtime_capsule;
    int master_addr;
    const char *endpoint_socket_addr_str;
    PyObject *config_capsule;

    if (!PyArg_ParseTuple(args, "OisO", &runtime_capsule, &master_addr, &endpoint_socket_addr_str, &config_capsule)) {
        return NULL;
    }

    dnp3_runtime_t *runtime = PyCapsule_GetPointer(runtime_capsule, "dnp3_runtime_t");
    if (runtime == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid runtime capsule");
        return NULL;
    }
    dnp3_master_channel_config_t *config = PyCapsule_GetPointer(config_capsule, "dnp3_master_channel_config_t");
    if (config == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid config capsule");
        return NULL;
    }
    char *endpoint_socket_addr = strdup(endpoint_socket_addr_str);
    if (!endpoint_socket_addr) {
        PyErr_NoMemory();
        return NULL;
    }

    dnp3_master_channel_t *channel = create_tcp_channel(runtime, master_addr, endpoint_socket_addr, config);
    free(endpoint_socket_addr); // Free the duplicated string
    if (channel == NULL) {
        Py_RETURN_NONE;
    }
    return PyCapsule_New((void*)channel, "dnp3_master_channel_t", channel_destructor);
}


static PyObject* py_init_runtime(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    dnp3_runtime_t *runtime = init_runtime();
    if (runtime == NULL) {
        Py_RETURN_NONE;
    }
    return PyCapsule_New((void*)runtime, "dnp3_runtime_t", NULL);
}


static PyObject* py_destroy_runtime(PyObject *self, PyObject *args) {
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


static PyObject* py_destroy_channel(PyObject *self, PyObject *args) {
    PyObject *channel_capsule;
    if (!PyArg_ParseTuple(args, "O", &channel_capsule)) {
        return NULL;
    }
    dnp3_master_channel_t *channel = PyCapsule_GetPointer(channel_capsule, "dnp3_master_channel_t");
    if (channel == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid channel capsule");
        return NULL;
    }
    destroy_channel(channel);
    Py_RETURN_NONE;
}


static PyObject* py_enable_master_channel(PyObject *self, PyObject *args) {
    PyObject *channel_capsule;
    if (!PyArg_ParseTuple(args, "O", &channel_capsule)) {
        return NULL;
    }
    dnp3_master_channel_t *channel = PyCapsule_GetPointer(channel_capsule, "dnp3_master_channel_t");
    if (channel == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid channel capsule");
        return NULL;
    }
    enable_master_channel(channel);
    Py_RETURN_NONE;
}


static PyObject* py_disable_master_channel(PyObject *self, PyObject *args) {
    PyObject *channel_capsule;
    if (!PyArg_ParseTuple(args, "O", &channel_capsule)) {
        return NULL;
    }
    dnp3_master_channel_t *channel = PyCapsule_GetPointer(channel_capsule, "dnp3_master_channel_t");
    if (channel == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid channel capsule");
        return NULL;
    }
    disable_master_channel(channel);
    Py_RETURN_NONE;
}


static PyObject* py_add_association(PyObject *self, PyObject *args) {
    PyObject *channel_capsule;
    int outstation_addr;
    if (!PyArg_ParseTuple(args, "Oi", &channel_capsule, &outstation_addr)) {
        return NULL;
    }
    dnp3_master_channel_t *channel = PyCapsule_GetPointer(channel_capsule, "dnp3_master_channel_t");
    if (channel == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid channel capsule");
        return NULL;
    }
    dnp3_association_id_t association_id;
    int result = add_association(channel, outstation_addr, &association_id);
    if (result != 0) {
        return PyLong_FromLong(-1); // Indicate error in Python as well
    }
    return PyLong_FromLong(association_id.address); // Return association ID address as Python integer
}


static PyObject* py_create_poll(PyObject *self, PyObject *args) {
    PyObject *channel_capsule;
    int association_id_address; // Expecting association_id.address as integer from Python
    if (!PyArg_ParseTuple(args, "Oi", &channel_capsule, &association_id_address)) {
        return NULL;
    }
    dnp3_master_channel_t *channel = PyCapsule_GetPointer(channel_capsule, "dnp3_master_channel_t");
    if (channel == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid channel capsule");
        return NULL;
    }
    dnp3_association_id_t association_id;
    association_id.address = (uint16_t)association_id_address; // Construct dnp3_association_id_t from address
    int result = create_poll(channel, association_id);
     if (result != 0) {
        return PyLong_FromLong(-1); // Indicate error in Python as well
    }
    return PyLong_FromLong(0);
}


// Method definitions for the module
static PyMethodDef Dnp3Methods[] = {
    {"create_master_channel_config", py_create_master_channel_config, METH_VARARGS, "Create master channel config(master_address)-> config_capsule"},
    {"create_tcp_channel", py_create_tcp_channel, METH_VARARGS, "Create TCP channel(runtime_capsule, master_addr, endpoint_socket_addr, config_capsule) -> channel_capsule"},
    {"init_runtime", py_init_runtime, METH_NOARGS, "Initialize runtime() -> runtime_capsule"},
    {"destroy_runtime", py_destroy_runtime, METH_VARARGS, "Destroy runtime(runtime_capsule)"},
    {"destroy_channel", py_destroy_channel, METH_VARARGS, "Destroy channel(channel_capsule)"},
    {"enable_master_channel", py_enable_master_channel, METH_VARARGS, "Enable master channel(channel_capsule)"},
    {"disable_master_channel", py_disable_master_channel, METH_VARARGS, "Disable master channel(channel_capsule)"},
    {"add_association", py_add_association, METH_VARARGS, "Add association(channel_capsule, outstation_addr) -> association_id_address"},
    {"create_poll", py_create_poll, METH_VARARGS, "Create poll(channel_capsule, association_id_address)"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

// Module definition structure
static struct PyModuleDef dnp3module = {
    PyModuleDef_HEAD_INIT,
    "dnp3_master",
    "DNP3 Master extension module",
    -1,
    Dnp3Methods
};

// Module initialization function
PyMODINIT_FUNC
PyInit_master(void)
{
    return PyModule_Create(&dnp3module);
}
