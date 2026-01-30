IOX_DIR=~/dds_shm/iceoryx
BUILD_TYPE=Release # Debug or Release

cd ~/dds_shm/cyclonedds

cmake -Bbuild -DCMAKE_BUILD_TYPE=$BUILD_TYPE -DCMAKE_INSTALL_PREFIX=install -DENABLE_ICEORYX=On -DBUILD_EXAMPLES=On -DCMAKE_PREFIX_PATH=$IOX_DIR/install
cmake --build build --config $BUILD_TYPE --target install --parallel $(nproc)