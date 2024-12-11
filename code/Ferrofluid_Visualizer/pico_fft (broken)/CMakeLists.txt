cmake_minimum_required(VERSION 3.13)

# Specify the linker path early in the file
#set(CMAKE_LINKER "C:/Program Files (x86)/Arm GNU Toolchain arm-none-eabi/14.2 rel1/bin/arm-none-eabi-ld.exe")

# Include the Pico SDK
set(PICO_SDK_PATH "${CMAKE_CURRENT_LIST_DIR}/pico-sdk-2.1.0")
include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "PICO")
    set(CMAKE_EXE_LINKER_FLAGS "-Wl,--major-image-version,0,--minor-image-version,0")
endif()

# Set the project name and C standard
project(fft_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the Pico SDK
pico_sdk_init()

# Add your main source file
add_executable(fft_project
    main.c
)

# Add the KISS FFT library files
target_sources(fft_project PRIVATE
    kissfft/kiss_fft.c
    kissfft/kiss_fftr.c
    # Add more files as needed
)

# Include the KISS FFT headers
target_include_directories(fft_project PRIVATE
    kissfft
)

# Link the Pico libraries
target_link_libraries(fft_project pico_stdlib hardware_gpio)

# Enable USB or UART (optional for debugging)
pico_enable_stdio_usb(fft_project 1)
pico_enable_stdio_uart(fft_project 0)

# Create a UF2 file for flashing
pico_add_extra_outputs(fft_project)