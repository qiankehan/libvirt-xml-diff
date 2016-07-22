# libvirt-xml-diff
## Dependency
xmldiff (pip install xmldiff)
python3
python3-lxml
## Usage
First, run 
```sh
./gen-tags.sh YOUR_LIBVIRT_GIT_REPO
```
Then run following to generate reports
```sh
./run.py OLD_VER_DIR NEW_VIR_DIR
```
eg.
```sh
./run.py v1.3.5 v2.0.0
```
