Run off debian:
```
$ sudo docker build --progress=plain -t translator -f debian.Dockerfile . && sudo docker run -it translator /bin/bash
```

Run off ubuntu:
```
$ sudo docker build --progress=plain -t translator -f ubuntu.Dockerfile . && sudo docker run -it translator /bin/bash
```
