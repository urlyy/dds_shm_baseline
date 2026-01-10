IOX_DIR=~/dds_shm/iceoryx

cd $IOX_DIR

cmake -Bbuild -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=install -DROUDI_ENVIRONMENT=on -DBUILD_SHARED_LIBS=ON -Hiceoryx_meta
cmake --build build --config Release --target install