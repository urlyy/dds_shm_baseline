import os
import signal
import subprocess
from multiprocessing import Process
from pathlib import Path
from time import sleep

def get_dds_size(install_path: str) -> int:
    base = os.path.expanduser(install_path)
    include = os.path.join(base, "include")
    lib = os.path.join(base, "lib")

    def get_size(path):
        total = 0
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        total += os.path.getsize(fp)
                    except:
                        pass
        return total

    # 计算大小
    s_include = get_size(include)
    s_lib = get_size(lib)
    total = s_include + s_lib
    return total

def run_command(cmd: str, stdout: bool = True):
    real_stdout = None if stdout else subprocess.DEVNULL
    subprocess.run(cmd, shell=True, check=False, stdout=real_stdout, stderr=real_stdout)

ROUDI = "~/dds_shm/iceoryx/build/iox-roudi -c ~/dds_shm/config/iox_config.toml"
SUBSCRIBER = "~/dds_shm/cyclonedds/examples/loan/build/LoanSubscriber"
PUBLISHER = "~/dds_shm/cyclonedds/examples/loan/build/LoanPublisher"

def main():
    print("dds_size:", get_dds_size("~/dds_shm/cyclonedds/install"))

    # 报错用这个killall iox-roudi
    roudi = subprocess.Popen(
        ROUDI,
        shell=True,
        preexec_fn=os.setsid,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    sleep(2)

    publisher = Process(
        target=run_command,
        args=(f"{PUBLISHER}",),
    )
    subscriber = Process(
        target=run_command,
        args=(f"{SUBSCRIBER}",),
    )
    publisher.start()
    subscriber.start()
    publisher.join()
    subscriber.join()

    try:
        os.killpg(os.getpgid(roudi.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass
    roudi.wait()


if __name__ == "__main__":
    main()