#include <Python.h>
#include <stdatomic.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#include "dnp3.h"

// Forward declarations
PyObject *DNP3Error;
#define CAPSULE_NAME_OUTSTATION_CONFIG "dnp3_outstation_config"
#define CAPSULE_NAME_ADDRESS_FILTER "dnp3_address_filter"
#define CAPSULE_NAME_OUTSTATION "dnp3_outstation"
#define CAPSULE_NAME_OUTSTATION_SERVER "dnp3_outstation_server"


// TODO: integrate with HELICS time
dnp3_timestamp_t now() {
    return dnp3_timestamp_synchronized_timestamp((uint64_t)time(NULL));
}


// OutstationApplication interface
uint16_t get_processing_delay_ms(void *context) { return 0; }

dnp3_write_time_result_t write_absolute_time(uint64_t time, void *context) { return DNP3_WRITE_TIME_RESULT_NOT_SUPPORTED; }

dnp3_application_iin_t get_application_iin(void *context) { return dnp3_application_iin_init(); }

dnp3_restart_delay_t cold_restart(void *context) { return dnp3_restart_delay_seconds(60); }

dnp3_restart_delay_t warm_restart(void *context) { return dnp3_restart_delay_not_supported(); }

dnp3_freeze_result_t freeze_counters_all(dnp3_freeze_type_t freeze_type, dnp3_database_handle_t *database, void *context) { return DNP3_FREEZE_RESULT_NOT_SUPPORTED; }

dnp3_freeze_result_t freeze_counters_range(uint16_t start, uint16_t stop, dnp3_freeze_type_t freeze_type, dnp3_database_handle_t *database, void *context) {
    return DNP3_FREEZE_RESULT_NOT_SUPPORTED;
}

bool write_string_attr(uint8_t set, uint8_t var, dnp3_string_attr_t attr, const char* value, void *context) {
    // Allow writing any string attributes that have been defined as writable
    return true;
}

dnp3_outstation_application_t get_outstation_application() {
    return (dnp3_outstation_application_t){
        .get_processing_delay_ms = &get_processing_delay_ms,
        .write_absolute_time = &write_absolute_time,
        .get_application_iin = &get_application_iin,
        .cold_restart = &cold_restart,
        .warm_restart = &warm_restart,
        .freeze_counters_all = &freeze_counters_all,
        .freeze_counters_range = &freeze_counters_range,
        .write_string_attr = &write_string_attr,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

// OutstationInformation interface
void process_request_from_idle(dnp3_request_header_t header, void *context) {}

void broadcast_received(dnp3_function_code_t function_code, dnp3_broadcast_action_t action, void *context) {}

void enter_solicited_confirm_wait(uint8_t ecsn, void *context) {}

void solicited_confirm_timeout(uint8_t ecsn, void *context) {}

void solicited_confirm_received(uint8_t ecsn, void *context) {}

void solicited_confirm_wait_new_request(void *context) {}

void wrong_solicited_confirm_seq(uint8_t ecsn, uint8_t seq, void *context) {}

void unexpected_confirm(bool unsolicited, uint8_t seq, void *context) {}

void enter_unsolicited_confirm_wait(uint8_t ecsn, void *context) {}

void unsolicited_confirm_timeout(uint8_t ecsn, bool retry, void *context) {}

void unsolicited_confirmed(uint8_t ecsn, void *context) {}

void clear_restart_iin(void *context) {}

dnp3_outstation_information_t get_outstation_information() {
    return (dnp3_outstation_information_t){.process_request_from_idle = &process_request_from_idle,
                                           .broadcast_received = &broadcast_received,
                                           .enter_solicited_confirm_wait = &enter_solicited_confirm_wait,
                                           .solicited_confirm_timeout = &solicited_confirm_timeout,
                                           .solicited_confirm_received = &solicited_confirm_received,
                                           .solicited_confirm_wait_new_request = &solicited_confirm_wait_new_request,
                                           .wrong_solicited_confirm_seq = &wrong_solicited_confirm_seq,
                                           .unexpected_confirm = &unexpected_confirm,
                                           .enter_unsolicited_confirm_wait = &enter_unsolicited_confirm_wait,
                                           .unsolicited_confirm_timeout = &unsolicited_confirm_timeout,
                                           .unsolicited_confirmed = &unsolicited_confirmed,
                                           .clear_restart_iin = &clear_restart_iin,
                                           .on_destroy = NULL,
                                           .ctx = NULL};
}

typedef struct binary_output_update_t {
    uint16_t index;
    bool status;
} binary_output_update_t;

void update_binary_output(dnp3_database_t* db, void* context) {
    binary_output_update_t* ctx = (binary_output_update_t*)context;

    dnp3_binary_output_status_t status = dnp3_binary_output_status_init(ctx->index, ctx->status, dnp3_flags_init(DNP3_FLAG_ONLINE), now());

    dnp3_database_update_binary_output_status(db, status, dnp3_update_options_detect_event());
}

typedef struct analog_output_update_t {
    uint16_t index;
    double value;
} analog_output_update_t;

void update_analog_output_status(dnp3_database_t* db, void* context) {
    analog_output_update_t* ctx = (analog_output_update_t*)context;

    dnp3_analog_output_status_t status = dnp3_analog_output_status_init(ctx->index, ctx->value, dnp3_flags_init(DNP3_FLAG_ONLINE), now());

    dnp3_database_update_analog_output_status(db, status, dnp3_update_options_detect_event());
}


// ControlHandler interface
// ANCHOR: control_handler

void update_binary_output_status_from_control(dnp3_database_t *database, void *ctx) {
    dnp3_binary_output_status_t value = *(dnp3_binary_output_status_t *)ctx;
    dnp3_database_update_binary_output_status(database, value, dnp3_update_options_detect_event());
}

void update_analog_output_status_from_control(dnp3_database_t *database, void *ctx) {
    dnp3_analog_output_status_t value = *(dnp3_analog_output_status_t *)ctx;
    dnp3_database_update_analog_output_status(database, value, dnp3_update_options_detect_event());
}

void begin_fragment(void *context) {}

void end_fragment(dnp3_database_handle_t *database, void *context) {}

dnp3_command_status_t select_g12v1(dnp3_group12_var1_t control, uint16_t index, dnp3_database_handle_t *database, void *context) {
    if (index < 10 && (control.code.op_type == DNP3_OP_TYPE_LATCH_ON || control.code.op_type == DNP3_OP_TYPE_LATCH_OFF)) {
        return DNP3_COMMAND_STATUS_SUCCESS;
    } else {
        return DNP3_COMMAND_STATUS_NOT_SUPPORTED;
    }
}

dnp3_command_status_t operate_g12v1(dnp3_group12_var1_t control, uint16_t index, dnp3_operate_type_t op_type, dnp3_database_handle_t *database, void *context) {
    if (index < 10 && (control.code.op_type == DNP3_OP_TYPE_LATCH_ON || control.code.op_type == DNP3_OP_TYPE_LATCH_OFF)) {
        bool status = (control.code.op_type == DNP3_OP_TYPE_LATCH_ON);
        dnp3_binary_output_status_t bo = dnp3_binary_output_status_init(index, status, dnp3_flags_init(DNP3_FLAG_ONLINE), now());
        dnp3_database_transaction_t transaction = {
            .execute = &update_binary_output_status_from_control,
            .on_destroy = NULL,
            .ctx = &bo,
        };
        dnp3_database_handle_transaction(database, transaction);
        return DNP3_COMMAND_STATUS_SUCCESS;
    } else {
        return DNP3_COMMAND_STATUS_NOT_SUPPORTED;
    }
}

dnp3_command_status_t select_analog_output(uint16_t index) {
    return (index < 10) ? DNP3_COMMAND_STATUS_SUCCESS : DNP3_COMMAND_STATUS_NOT_SUPPORTED;
}

dnp3_command_status_t operate_analog_output(double value, uint16_t index, dnp3_database_handle_t *database) {
    if (index < 10) {
        dnp3_analog_output_status_t ao = dnp3_analog_output_status_init(index, value, dnp3_flags_init(DNP3_FLAG_ONLINE), now());
        dnp3_database_transaction_t transaction = {
            .execute = &update_analog_output_status_from_control,
            .on_destroy = NULL,
            .ctx = &ao,
        };
        dnp3_database_handle_transaction(database, transaction);
        return DNP3_COMMAND_STATUS_SUCCESS;
    } else {
        return DNP3_COMMAND_STATUS_NOT_SUPPORTED;
    }
}

dnp3_command_status_t select_g41v1(int32_t value, uint16_t index, dnp3_database_handle_t *database, void *context) {
    return select_analog_output(index);
}

dnp3_command_status_t operate_g41v1(int32_t value, uint16_t index, dnp3_operate_type_t op_type, dnp3_database_handle_t *database, void *context) {
    return operate_analog_output((double)value, index, database);
}

dnp3_command_status_t select_g41v2(int16_t value, uint16_t index, dnp3_database_handle_t *database, void *context) {
    return select_analog_output(index);
}

dnp3_command_status_t operate_g41v2(int16_t value, uint16_t index, dnp3_operate_type_t op_type, dnp3_database_handle_t *database, void *context) {
    return operate_analog_output((double)value, index, database);
}

dnp3_command_status_t select_g41v3(float value, uint16_t index, dnp3_database_handle_t *database, void *context) {
    return select_analog_output(index);
}

dnp3_command_status_t operate_g41v3(float value, uint16_t index, dnp3_operate_type_t op_type, dnp3_database_handle_t *database, void *context) {
    return operate_analog_output((double)value, index, database);
}

dnp3_command_status_t select_g41v4(double value, uint16_t index, dnp3_database_handle_t *database, void *context) {
    return select_analog_output(index);
}

dnp3_command_status_t operate_g41v4(double value, uint16_t index, dnp3_operate_type_t op_type, dnp3_database_handle_t *database, void *context) {
    return operate_analog_output(value, index, database);
}
// ANCHOR_END: control_handler

dnp3_control_handler_t get_control_handler() {
    return (dnp3_control_handler_t){
        .begin_fragment = &begin_fragment,
        .end_fragment = &end_fragment,
        .select_g12v1 = &select_g12v1,
        .operate_g12v1 = &operate_g12v1,
        .select_g41v1 = &select_g41v1,
        .operate_g41v1 = &operate_g41v1,
        .select_g41v2 = &select_g41v2,
        .operate_g41v2 = &operate_g41v2,
        .select_g41v3 = &select_g41v3,
        .operate_g41v3 = &operate_g41v3,
        .select_g41v4 = &select_g41v4,
        .operate_g41v4 = &operate_g41v4,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

// ANCHOR: database_init_transaction
void outstation_transaction_startup(dnp3_database_t *db, void *context) {
    // initialize 10 values for each type
    for (uint16_t i = 0; i < 10; ++i) {
        // you can explicitly specify the configuration for each point ...
        dnp3_database_add_binary_input(db, i, DNP3_EVENT_CLASS_CLASS1,
            dnp3_binary_input_config_create(DNP3_STATIC_BINARY_INPUT_VARIATION_GROUP1_VAR1, DNP3_EVENT_BINARY_INPUT_VARIATION_GROUP2_VAR2)
        );
        // ... or just use the defaults
        dnp3_database_add_double_bit_binary_input(db, i, DNP3_EVENT_CLASS_CLASS1, dnp3_double_bit_binary_input_config_init());
        dnp3_database_add_binary_output_status(db, i, DNP3_EVENT_CLASS_CLASS1, dnp3_binary_output_status_config_init());
        dnp3_database_add_counter(db, i, DNP3_EVENT_CLASS_CLASS1, dnp3_counter_config_init());
        dnp3_database_add_frozen_counter(db, i, DNP3_EVENT_CLASS_CLASS1, dnp3_frozen_counter_config_init());
        dnp3_database_add_analog_input(db, i, DNP3_EVENT_CLASS_CLASS1, dnp3_analog_input_config_init());
        dnp3_database_add_analog_output_status(db, i, DNP3_EVENT_CLASS_CLASS1, dnp3_analog_output_status_config_init());
        dnp3_database_add_octet_string(db, i, DNP3_EVENT_CLASS_CLASS1);
    }

    // define device attributes made available to the master
    dnp3_database_define_string_attr(db, 0, false, DNP3_ATTRIBUTE_VARIATIONS_DEVICE_MANUFACTURERS_NAME, "Step Function I/O");
    dnp3_database_define_string_attr(db, 0, true, DNP3_ATTRIBUTE_VARIATIONS_USER_ASSIGNED_LOCATION, "Bend, OR");   
}
// ANCHOR_END: database_init_transaction

typedef struct database_points_t {
    bool binaryValue;
    dnp3_double_bit_t doubleBitBinaryValue;
    bool binaryOutputStatusValue;
    uint32_t counterValue;
    uint32_t frozenCounterValue;
    double analogValue;
    double analogOutputStatusValue;
} database_points_t;

void binary_transaction(dnp3_database_t *db, void *context) {
    ((database_points_t *)context)->binaryValue = !((database_points_t *)context)->binaryValue;

    dnp3_binary_input_t value =
        dnp3_binary_input_init(7, ((database_points_t *)context)->binaryValue, dnp3_flags_init(DNP3_FLAG_ONLINE), now());
    dnp3_database_update_binary_input(db, value, dnp3_update_options_detect_event());
}

void double_bit_binary_transaction(dnp3_database_t *db, void *context) {
    ((database_points_t *)context)->doubleBitBinaryValue =
        ((database_points_t *)context)->doubleBitBinaryValue == DNP3_DOUBLE_BIT_DETERMINED_OFF ? DNP3_DOUBLE_BIT_DETERMINED_ON : DNP3_DOUBLE_BIT_DETERMINED_OFF;

    dnp3_double_bit_binary_input_t value = dnp3_double_bit_binary_input_init(7, ((database_points_t *)context)->doubleBitBinaryValue,
                                                                             dnp3_flags_init(DNP3_FLAG_ONLINE), now());
    dnp3_database_update_double_bit_binary_input(db, value, dnp3_update_options_detect_event());
}

void binary_output_status_transaction(dnp3_database_t *db, void *context) {
    ((database_points_t *)context)->binaryOutputStatusValue = !((database_points_t *)context)->binaryOutputStatusValue;

    dnp3_binary_output_status_t value = dnp3_binary_output_status_init(7, ((database_points_t *)context)->binaryOutputStatusValue,
                                                                       dnp3_flags_init(DNP3_FLAG_ONLINE), now());
    dnp3_database_update_binary_output_status(db, value, dnp3_update_options_detect_event());
}

void counter_transaction(dnp3_database_t *db, void *context) {
    dnp3_counter_t value =
        dnp3_counter_init(7, ++((database_points_t *)context)->counterValue, dnp3_flags_init(DNP3_FLAG_ONLINE), now());
    dnp3_database_update_counter(db, value, dnp3_update_options_detect_event());
}

void frozen_counter_transaction(dnp3_database_t *db, void *context) {
    dnp3_frozen_counter_t value =
        dnp3_frozen_counter_init(7, ++((database_points_t *)context)->frozenCounterValue, dnp3_flags_init(DNP3_FLAG_ONLINE), now());
    dnp3_database_update_frozen_counter(db, value, dnp3_update_options_detect_event());
}

void analog_transaction(dnp3_database_t *db, void *context) {
    dnp3_analog_input_t value =
        dnp3_analog_input_init(7, ++((database_points_t *)context)->analogValue, dnp3_flags_init(DNP3_FLAG_ONLINE), now());
    dnp3_database_update_analog_input(db, value, dnp3_update_options_detect_event());
}

void analog_output_status_transaction(dnp3_database_t *db, void *context) {
    dnp3_analog_output_status_t value = dnp3_analog_output_status_init(7, ++((database_points_t *)context)->analogOutputStatusValue,
                                                                       dnp3_flags_init(DNP3_FLAG_ONLINE), now());
    dnp3_database_update_analog_output_status(db, value, dnp3_update_options_detect_event());
}

void octet_string_transaction(dnp3_database_t *db, void *context) {
    dnp3_octet_string_value_t *octet_string = dnp3_octet_string_value_create();
    dnp3_octet_string_value_add(octet_string, 0x48); // H
    dnp3_octet_string_value_add(octet_string, 0x65); // e
    dnp3_octet_string_value_add(octet_string, 0x6C); // l
    dnp3_octet_string_value_add(octet_string, 0x6C); // l
    dnp3_octet_string_value_add(octet_string, 0x6F); // o
    dnp3_octet_string_value_add(octet_string, 0x00); // \0

    dnp3_database_update_octet_string(db, 7, octet_string, dnp3_update_options_detect_event());

    dnp3_octet_string_value_destroy(octet_string);
}

void on_connection_state_change(dnp3_connection_state_t state, void *ctx) { 
    /*char* string;*/
    /*if (asprintf(&string, "Connection state change: %s\n", dnp3_connection_state_to_string(state)) < 0) {*/
    /*    on_log_message(DNP3_LOG_LEVEL_ERROR, "Unable to allocate memory for log message", NULL);*/
    /*    return;*/
    /*}*/
    /**/
    /*on_log_message(DNP3_LOG_LEVEL_INFO, string, NULL);*/
    /*free(string);*/
}

void on_port_state_change(dnp3_port_state_t state, void *ctx) {
    printf("Port state change: %s\n", dnp3_port_state_to_string(state)); 
}

dnp3_connection_state_listener_t get_connection_state_listener() {
    return (dnp3_connection_state_listener_t){
        .on_change = &on_connection_state_change,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

dnp3_port_state_listener_t get_port_state_listener() {
    return (dnp3_port_state_listener_t){
        .on_change = &on_port_state_change,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

// loop that accepts user input and updates values
int run_outstation(dnp3_outstation_t *outstation) {
    database_points_t database_points = {
        .binaryValue = false,
        .doubleBitBinaryValue = DNP3_DOUBLE_BIT_DETERMINED_OFF,
        .binaryOutputStatusValue = false,
        .counterValue = 0,
        .frozenCounterValue = 0,
        .analogValue = 0.0,
        .analogOutputStatusValue = 0.0,
    };

    char cbuf[10];
    while (true) {
        fgets(cbuf, 10, stdin);

        if (strcmp(cbuf, "x\n") == 0) {
            return 0;
        }
        else if (strcmp(cbuf, "enable\n") == 0) {
            dnp3_outstation_enable(outstation);
        }
        else if (strcmp(cbuf, "disable\n") == 0) {
            dnp3_outstation_disable(outstation);
        }
        else if (strcmp(cbuf, "bi\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &binary_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else if (strcmp(cbuf, "dbbi\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &double_bit_binary_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else if (strcmp(cbuf, "bos\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &binary_output_status_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else if (strcmp(cbuf, "co\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &counter_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else if (strcmp(cbuf, "fco\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &frozen_counter_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else if (strcmp(cbuf, "ai\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &analog_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else if (strcmp(cbuf, "aos\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &analog_output_status_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else if (strcmp(cbuf, "os\n") == 0) {
            dnp3_database_transaction_t transaction = {
                .execute = &octet_string_transaction,
                .on_destroy = NULL,
                .ctx = &database_points,
            };
            dnp3_outstation_transaction(outstation, transaction);
        }
        else {
            printf("Unknown command\n");
        }
    }
}

// ANCHOR: event_buffer_config
dnp3_event_buffer_config_t get_event_buffer_config() {
    return dnp3_event_buffer_config_init(10, // binary
                                         10, // double-bit binary
                                         10, // binary output status
                                         5,  // counter
                                         5,  // frozen counter
                                         5,  // analog
                                         5,  // analog output status
                                         3   // octet string
    );
}


static void address_filter_capsule_destructor(PyObject *capsule) {
    dnp3_address_filter_t *ptr = PyCapsule_GetPointer(capsule, CAPSULE_NAME_ADDRESS_FILTER);
    if (ptr) {
        dnp3_address_filter_destroy(ptr);
    }
}

static void outstation_capsule_destructor(PyObject *capsule) {
    dnp3_outstation_t *ptr = PyCapsule_GetPointer(capsule, CAPSULE_NAME_OUTSTATION);
    if (ptr) {
        dnp3_outstation_destroy(ptr);
    }
}

static void config_capsule_destructor(PyObject *capsule) {
    dnp3_outstation_config_t *config = PyCapsule_GetPointer(capsule, CAPSULE_NAME_OUTSTATION_CONFIG);
    if (config) {
        free(config);
    }
}

dnp3_outstation_config_t create_outstation_config(uint16_t outstation_addr, uint16_t master_addr) {
    // create an outstation configuration with default values
    dnp3_outstation_config_t config = dnp3_outstation_config_init(
        outstation_addr,
        master_addr,
        get_event_buffer_config()
    );
    // override the default application decoding level
    config.decode_level.application = DNP3_APP_DECODE_LEVEL_OBJECT_VALUES;
    return config;
}

static PyObject* dnp3_create_outstation_config(PyObject *self, PyObject *args) {
    unsigned int outstation_addr, master_addr;
    if (!PyArg_ParseTuple(args, "II", &outstation_addr, &master_addr)) {
        return NULL;
    }

    dnp3_outstation_config_t config = create_outstation_config((uint16_t)outstation_addr, (uint16_t)master_addr);

    dnp3_outstation_config_t *config_ptr = malloc(sizeof(dnp3_outstation_config_t));
    memcpy(config_ptr, &config, sizeof(dnp3_outstation_config_t));

    // Create a capsule to hold the config
    PyObject *capsule = PyCapsule_New(config_ptr, CAPSULE_NAME_OUTSTATION_CONFIG, NULL);

    const char *name = PyCapsule_GetName(capsule);
    const char *ptr = PyCapsule_GetPointer(capsule, CAPSULE_NAME_OUTSTATION_CONFIG);
    if (!capsule) {
        return PyErr_NoMemory();
    }
    return capsule;
}

void init_database(dnp3_outstation_t *outstation) {
    dnp3_database_transaction_t startup_transaction = {
        .execute = &outstation_transaction_startup,
        .on_destroy = NULL,
        .ctx = NULL,
    };
    dnp3_outstation_transaction(outstation, startup_transaction);
}

static PyObject* dnp3_init_database(PyObject *self, PyObject *args) {
    PyObject *outstation_capsule;
    if (!PyArg_ParseTuple(args, "O", &outstation_capsule)) {
        return NULL;
    }

    dnp3_outstation_t *outstation = PyCapsule_GetPointer(outstation_capsule, CAPSULE_NAME_OUTSTATION);
    if (outstation == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid outstation capsule");
        return NULL;
    }

    init_database(outstation);
    Py_RETURN_NONE;
}

dnp3_address_filter_t* create_address_filter(const char *address_filter) {
    if (strcmp(address_filter, "any") == 0) {
        dnp3_address_filter_t *filter_any = dnp3_address_filter_any();
        return filter_any;
    }

    dnp3_address_filter_t *filter = NULL;
    dnp3_param_error_t err = dnp3_address_filter_create(address_filter, &filter);
    if (err) {
        fprintf(stderr, "Invalid address filter. Try \"any\" or a wildcard IP address. Err: %s \n", dnp3_param_error_to_string(err));
        return NULL;
    }
    return filter;
}

static PyObject* dnp3_create_address_filter(PyObject *self, PyObject *args) {
    const char *address_filter_str;
    if (!PyArg_ParseTuple(args, "s", &address_filter_str)) {
        return NULL;
    }

    dnp3_address_filter_t *filter = create_address_filter(address_filter_str);
    if (filter == NULL) {
        PyErr_SetString(DNP3Error, "Failed to create address filter. Check console output for details.");
        return NULL;
    }

    PyObject *capsule = PyCapsule_New(filter, CAPSULE_NAME_ADDRESS_FILTER, address_filter_capsule_destructor);
    if (!capsule) {
        dnp3_address_filter_destroy(filter); // Clean up on capsule creation failure
        return PyErr_NoMemory();
    }
    return capsule;
}

dnp3_outstation_t* add_outstation(dnp3_outstation_server_t *server, dnp3_address_filter_t *filter, dnp3_outstation_config_t *config) {
    dnp3_outstation_t *outstation = NULL;


    dnp3_param_error_t err = dnp3_outstation_server_add_outstation(
        server,
        *config,
        get_outstation_application(),
        get_outstation_information(),
        get_control_handler(),
        get_connection_state_listener(),
        filter,
        &outstation
    );

    if (err) {
        fprintf(stderr, "Error: %s\n", dnp3_param_error_to_string(err));
        return NULL;
    }
    return outstation;
}

static PyObject* dnp3_add_outstation(PyObject *self, PyObject *args) {
    PyObject *server_capsule, *filter_capsule, *config_capsule;
    if (!PyArg_ParseTuple(args, "OOO", &server_capsule, &filter_capsule, &config_capsule)) {
        return NULL;
    }

    dnp3_outstation_server_t *server = PyCapsule_GetPointer(server_capsule, CAPSULE_NAME_OUTSTATION_SERVER); // Assuming server capsule exists and is passed
    dnp3_address_filter_t *filter = PyCapsule_GetPointer(filter_capsule, CAPSULE_NAME_ADDRESS_FILTER);
    dnp3_outstation_config_t *config = PyCapsule_GetPointer(config_capsule, CAPSULE_NAME_OUTSTATION_CONFIG);

    if (server == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid tcp server capsule passed to add_outstation");
        return NULL;
    }
    if (filter == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid filter capsule passed to add_outstation");
        return NULL;
    }
    if (config == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid config capsule passed to add_outstation");
        return NULL;
    }

    dnp3_outstation_t *outstation = add_outstation(server, filter, config);
    if (outstation == NULL) {
        PyErr_SetString(DNP3Error, "Failed to add outstation.");
        return NULL;
    }

    PyObject *outstation_capsule_ret = PyCapsule_New(outstation, CAPSULE_NAME_OUTSTATION, outstation_capsule_destructor);
    if (!outstation_capsule_ret) {
        dnp3_outstation_destroy(outstation); // Cleanup if capsule creation fails
        return PyErr_NoMemory();
    }
    return outstation_capsule_ret;
}

static PyObject* dnp3_enable_outstation(PyObject *self, PyObject *args) {
    PyObject *outstation_capsule;
    if (!PyArg_ParseTuple(args, "O", &outstation_capsule)) {
        return NULL;
    }

    dnp3_outstation_t *outstation = PyCapsule_GetPointer(outstation_capsule, CAPSULE_NAME_OUTSTATION);
    if (outstation == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid outstation capsule");
        return NULL;
    }

    dnp3_outstation_enable(outstation);
    Py_RETURN_NONE;
}

static PyObject* dnp3_disable_outstation(PyObject *self, PyObject *args) {
    PyObject *outstation_capsule;
    if (!PyArg_ParseTuple(args, "O", &outstation_capsule)) {
        return NULL;
    }

    dnp3_outstation_t *outstation = PyCapsule_GetPointer(outstation_capsule, CAPSULE_NAME_OUTSTATION);
    if (outstation == NULL) {
        PyErr_SetString(PyExc_TypeError, "Invalid outstation capsule");
        return NULL;
    }

    dnp3_outstation_disable(outstation);
    Py_RETURN_NONE;
}


// --- Module Definition ---

static PyMethodDef methods[] = {
    {"create_outstation_config",  dnp3_create_outstation_config, METH_VARARGS, "Create an outstation configuration."},
    {"init_database", dnp3_init_database, METH_VARARGS, "Initialize the outstation database."},
    {"create_address_filter",  dnp3_create_address_filter, METH_VARARGS, "Create an address filter."},
    {"add_outstation",  dnp3_add_outstation, METH_VARARGS, "Add an outstation to a server."},
    {"enable_outstation",  dnp3_enable_outstation, METH_VARARGS, "Enable an outstation."},
    {"disable_outstation",  dnp3_disable_outstation, METH_VARARGS, "Disable an outstation."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef outstation_module = {
    PyModuleDef_HEAD_INIT,
    "dnp3_extensions",
    "DNP3 Outstation Extension Module",
    -1,
    methods
};


PyMODINIT_FUNC PyInit_outstation(void)
{
    PyObject *m = PyModule_Create(&outstation_module);
    if (m == NULL)
        return NULL;

    DNP3Error = PyErr_NewException("dnp3_extensions.DNP3Error", PyExc_RuntimeError, NULL);
    Py_XINCREF(DNP3Error);
    if (PyModule_AddObject(m, "DNP3Error", DNP3Error) < 0) {
        Py_XDECREF(DNP3Error);
        return NULL;
    }

    return m;
}
