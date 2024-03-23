# cid-ntrl
:)

## Setup
> python3 and rust are required so install those :P

### Windows
```sh
# clone this repo
git clone https://github.com/cybernexusteam/cid-ntrl.git

# go to it
cd cid-ntrl

# init venv
python -m venv .venv

# activate venv
.\.venv\Scripts\Activate.ps1

# install deps
pip install -r requirements.txt

### Compile Rust Library
cd av-lib

# compile lib
maturin develop

# go back
cd ..

# run application
python main.py

```

### *nix (only works on debian-like systems)
```sh
# clone this repo
git clone https://github.com/cybernexusteam/cid-ntrl.git

# go to it
cd cid-ntrl

# init venv
python -m venv .venv

# activate venv
source ./.venv/bin/activate

# install deps
pip install -r requirements.txt

### Compile Rust Library
cd av-lib

# compile lib
maturin develop

# go back
cd ..

# run application
python main.py

```
