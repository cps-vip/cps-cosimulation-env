cmake_minimum_required(VERSION 4.1)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

# https://scikit-build-core.readthedocs.io/en/latest/guide/cmakelists.html#finding-python
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# These next few sections relating to DNP3 come from the example CMakeLists.txt: https://github.com/stepfunc/dnp3/blob/main/ffi/bindings/c/CMakeLists.txt
# Update this version as new releases come out
set(DNP3_VERSION 1.6.0)

# Determine the architecture
if(WIN32 AND CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64|amd64|AMD64" AND CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(DNP3_RUST_TARGET "x86_64-pc-windows-msvc")
elseif(UNIX AND CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64|amd64|AMD64")
    set(DNP3_RUST_TARGET "x86_64-unknown-linux-gnu")
elseif(UNIX AND CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64")
    set(DNP3_RUST_TARGET "aarch64-unknown-linux-gnu")
else()
    message(FATAL_ERROR "target architecture not supported by this CMake file")
endif()

# Finds the Rust DNP3 package if local, otherwise downloads the release specified by DNP3_VERSION
# End result is a target named "dnp3"
if(EXISTS ${CMAKE_CURRENT_LIST_DIR}/build/_deps/dnp3-src/cmake)
    # Use the locally built library
    message("DNP3 package is local")
    find_package(dnp3 REQUIRED HINTS ${CMAKE_CURRENT_LIST_DIR}/build/_deps/dnp3-src/cmake)
else()
    # Download the library from GitHub
    message("No local DNP3, fetching remote library version ${DNP3_VERSION}")
    include(FetchContent)
    FetchContent_Declare(
        dnp3
        URL https://github.com/stepfunc/dnp3/releases/download/${DNP3_VERSION}/dnp3-${DNP3_VERSION}.zip
    )

    FetchContent_GetProperties(dnp3)
    if(NOT dnp3_POPULATED)
        FetchContent_MakeAvailable(dnp3)
        find_package(dnp3 REQUIRED HINTS ${dnp3_SOURCE_DIR})
    endif()
endif()

# Explanation: https://github.com/cps-vip/cps-cosimulation-env/wiki/Kaden-McCartney's-Notebook#1007---1013
set_property(TARGET dnp3 PROPERTY IMPORTED_NO_SONAME TRUE)

# python_add_library comes from scikit-build-core, see https://scikit-build-core.readthedocs.io/en/latest/guide/getting_started.html
python_add_library(master MODULE src/dnp3/master.c WITH_SOABI)
# Standard way to link a shared library. Note the dnp3 target comes from build/_deps/dnp3-src/cmake/dnp3-config.cmake and is configured as SHARED IMPORTED GLOBAL
target_link_libraries(master PUBLIC dnp3)
# We will be manually placing libdnp3_ffi.so into the wheel in the same directory as the master.so, so we need to tell
set_target_properties(master PROPERTIES BUILD_RPATH "$ORIGIN" INSTALL_RPATH "$ORIGIN")

python_add_library(outstation MODULE src/dnp3/outstation.c WITH_SOABI)
target_link_libraries(outstation PUBLIC dnp3)
set_target_properties(outstation PROPERTIES BUILD_RPATH "$ORIGIN" INSTALL_RPATH "$ORIGIN")

python_add_library(tcpserver MODULE src/dnp3/tcpserver.c WITH_SOABI)
target_link_libraries(tcpserver PUBLIC dnp3)
set_target_properties(tcpserver PROPERTIES BUILD_RPATH "$ORIGIN" INSTALL_RPATH "$ORIGIN")

# SKBUILD_PROJECT_NAME comes from scikit-build-core. For a full list of variables provided, see https://scikit-build-core.readthedocs.io/en/latest/guide/cmakelists.html
install(TARGETS master DESTINATION ${SKBUILD_PROJECT_NAME})
install(TARGETS outstation DESTINATION ${SKBUILD_PROJECT_NAME})
install(TARGETS tcpserver DESTINATION ${SKBUILD_PROJECT_NAME})

# Copy libdnp3_ffi.so into the wheel
install(FILES $<TARGET_FILE:dnp3> DESTINATION ${SKBUILD_PROJECT_NAME})

