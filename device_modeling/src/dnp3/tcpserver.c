#include "dnp3.h"

#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

// Logger inteface
void on_log_message(dnp3_log_level_t level, const char *msg, void *arg) { printf("%s", msg); }

dnp3_logger_t get_logger()
{
    return (dnp3_logger_t){
        .on_message = &on_log_message,
        .on_destroy = NULL,
        .ctx = NULL,
    };
}

// Initialises logger and runtime
dnp3_runtime_t* init_runtime()
{
    dnp3_runtime_t *runtime = NULL;
    // initialize logging with the default configuration
    dnp3_configure_logging(dnp3_logging_config_init(), get_logger());
    
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

// Initializes the TCP server, but doesn't bind it yet
dnp3_outstation_server_t* init_server(dnp3_runtime_t *runtime, const char *socket_addr) {
    dnp3_outstation_server_t *server = NULL;
    dnp3_param_error_t err = dnp3_outstation_server_create_tcp_server(runtime, DNP3_LINK_ERROR_MODE_CLOSE, socket_addr, &server);
    if (err) {    
        printf("unable to create TCP server: %s \n", dnp3_param_error_to_string(err));
        return NULL;
    }
    return server;
}

// Only run this AFTER binding outstations
int start_server(dnp3_outstation_server_t *server) {
    dnp3_param_error_t err = dnp3_outstation_server_bind(server);
    if (err) {
        printf("unable to bind server: %s \n", dnp3_param_error_to_string(err));
        return -1;
    }
    return 0;
}

void destroy_runtime(dnp3_runtime_t *runtime) {
    dnp3_runtime_destroy(runtime);
}

void destroy_server(dnp3_outstation_server_t *server) {
    dnp3_outstation_server_destroy(server);
}

