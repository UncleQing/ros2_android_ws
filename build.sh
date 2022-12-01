#!/bin/bash

echo "===set env==="

#echo "source /opt/ros/galactic/setup.bash"
#source /opt/ros/galactic/setup.bash

export PYTHON3_EXEC="/usr/bin/python3"
echo "PYTHON3_EXEC=$PYTHON3_EXEC"

export ANDROID_ABI=arm64-v8a
echo "ANDROID_ABI=$ANDROID_ABI"

export ANDROID_NATIVE_API_LEVEL=android-29
echo "ANDROID_NATIVE_API_LEVEL=$ANDROID_NATIVE_API_LEVEL"

export ANDROID_TOOLCHAIN_NAME=arm-linux-androideabi-clang
echo "ANDROID_TOOLCHAIN_NAME=$ANDROID_TOOLCHAIN_NAME"

export ANDROID_STL=c++_shared
echo "ANDROID_STL=$ANDROID_STL"

export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
echo "RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"

export ANDROID_NDK=~/Android/Sdk/ndk/android-ndk-r25b-linux/android-ndk-r25b
echo "ANDROID_NDK=$ANDROID_NDK"

echo "start colcon build...."

colcon build \
  --parallel-workers 4 \
  --packages-ignore rcl_logging_log4cxx rosidl_generator_py test_msgs \
  --packages-up-to rcljava \
  --cmake-args \
  -DPYTHON_EXECUTABLE=${PYTHON3_EXEC} \
  -DPYTHON_LIBRARY=${PYTHON3_LIBRARY} \
  -DPYTHON_INCLUDE_DIR=${PYTHON3_INCLUDE_DIR} \
  -DCMAKE_TOOLCHAIN_FILE=${ANDROID_NDK}/build/cmake/android.toolchain.cmake \
  -DANDROID_FUNCTION_LEVEL_LINKING=OFF \
  -DANDROID_NATIVE_API_LEVEL=${ANDROID_NATIVE_API_LEVEL} \
  -DANDROID_TOOLCHAIN_NAME=${ANDROID_TOOLCHAIN_NAME} \
  -DANDROID_STL=${ANDROID_STL} \
  -DANDROID_ABI=${ANDROID_ABI} \
  -DANDROID_NDK=${ANDROID_NDK} \
  -DTHIRDPARTY=ON \
  -DCOMPILE_EXAMPLES=OFF \
  -DBUILD_TESTING=OFF \
  -DCMAKE_FIND_ROOT_PATH="${PWD}/install"
