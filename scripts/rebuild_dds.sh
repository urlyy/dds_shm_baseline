IOX_DIR=~/dds_shm/iceoryx

cd ~/dds_shm/cyclonedds

cmake -Bbuild -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=install -DENABLE_ICEORYX=On -DBUILD_EXAMPLES=On -DCMAKE_PREFIX_PATH=$IOX_DIR/install
cmake --build build --config Release --target install
