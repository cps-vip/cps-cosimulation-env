.PHONY: all
.PHONY: all-install
.PHONY: clean
.PHONY: clean-config

ifdef REPO_ROOT
else
$(error "REPO_ROOT not defined. Are you in the Nix development environment?")
endif

.DEFAULT_GOAL := all

define create-cmake-targets
.$1-cmake-setup:
	mkdir -p $2/build && \
	cmake $3 -S $2 -B $2/build

$1-all: .$1-cmake-setup
	make -j$(nproc) -C $2/build all
all:: $1-all

$1-all-install: $1-all
	make -j$(nproc) -C $2/build install
all-install:: $1-all-install

$1-clean:
	make -C $2/build clean
clean:: $1-clean

$1-clean-config:
	find $2/ -maxdepth 1 -mindepth 1 -type d -name build -exec rm -rf {} \; && \
 	rm -rf install/$2
clean-config:: $1-clean-config
endef

$(eval $(call create-cmake-targets,helics,HELICS,-DCMAKE_INSTALL_PREFIX=$(REPO_ROOT)/install/HELICS -DHELICS_BUILD_CXX_SHARED_LIB=ON -DHELICS_BUILD_EXAMPLES=ON -DHELICS_BUILD_TESTS=ON))

$(eval $(call create-cmake-targets,gridlab,gridlab-d,-DCMAKE_INSTALL_PREFIX=$(REPO_ROOT)/install/gridlab -DCMAKE_BUILD_TYPE=Debug -DGLD_USE_HELICS=ON -DGLD_HELICS_DIR=$(REPO_ROOT)/install/HELICS))
