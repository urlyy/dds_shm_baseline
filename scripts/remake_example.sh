DDS_DIR=~/dds_shm/cyclonedds

cd $DDS_DIR/examples/helloworld
rm -rf build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=$DDS_DIR/install .. && make