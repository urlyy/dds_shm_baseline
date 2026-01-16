# 一、安装
## 1. os与项目版本
ubuntu-22.04/ubuntu24.04

以下代码已在该仓库中下好，这里是下载细节。不需要执行。
```bash
git clone https://github.com/eclipse-iceoryx/iceoryx.git -b release_2.0
cd iceoryx
rm -rf .git
cd ..

git clone https://github.com/eclipse-cyclonedds/cyclonedds.git
cd cyclonedds
# 固定使用的dds版本为这次提交
git checkout ea9f8f7ba8c17b7585a2d4838ee25cd1cb2648a2
rm -rf .git
```

## 2. 环境
```bash
sudo apt install -y git build-essential cmake libssl-dev libcurl4-openssl-dev
sudo apt install -y cmake libacl1-dev libncurses5-dev pkg-config maven
```

## 3. 安装iceoryx
```bash
cd iceoryx

cmake -Bbuild -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=install -DROUDI_ENVIRONMENT=on -DBUILD_SHARED_LIBS=ON -Hiceoryx_meta

cmake --build build --config Release --target install
```

## 4. 安装开启了iceoryx的cyclonedds
```bash
cd cyclonedds

# 注意修改最后面的路径
cmake -Bbuild -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=install -DENABLE_ICEORYX=On -DBUILD_EXAMPLES=On -DCMAKE_PREFIX_PATH=/path/to/iceoryx/install/

cmake --build build --config Release --target install
```

# 二、配置文件
最基本的配置已经写在 `config` 目录里了。

建议环境变量写在文件里:
`vim ~/.bash.rc`
注意改路径。
```bash
export CYCLONEDDS_URI=/path/to/config/dds_config.xml
export LD_LIBRARY_PATH=/path/to/iceoryx/install/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/path/to/cyclonedds/install/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
```


# 三、测试
先编译例子
```bash
cd /path/to/cyclonedds/examples/helloworld
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=/path/to/cyclonedds/install .. && make
```

开三个终端。

终端1:
```bash
/path/to/iceoryx/build/iox-roudi -c /path/to/config/iox_config.toml
```

终端2:
```bash
cd /path/to/cyclonedds/examples/helloworld/build
./HelloworldPublisher
```

终端3:
```bash
cd /path/to/cyclonedds/examples/helloworld/build
./HelloworldSubscriber
```

这里也会出现`使用了共享内存`类似的日志。但其实好像还是走的socket读取。

可以试下`examples/loan`这个例子，输出略有不一样，走了共享内存读取，但是资源回收好像有问题。
最新：发现原因了，因为`message:char *`这个非固定大小的数据，共享内存好像不太支持。


# DDS大小
8021300 Bytes