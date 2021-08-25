# Build a Blockchain & Cryptocurrency

## Activate the virtual environment

```sh
python3 -m venv blockchain-env
.\blockchain-env\Scripts\Activate
```

## Install all packages

```sh
pip3 install -r requirements.txt
```

## Run the test

Make sure to activate virtual environment.

```sh
python3 -m pytest .\backend\tests
```

## Run modules

Run the blockchain module.

```sh
python3 -m backend.blockchain.blockchain
```

Run the block module.

```sh
python3 -m backend.blockchain.block
```

Run the crypto_hash module.

```sh
python3 -m backend.util.crypto_hash
```

## Run the application and API

Make sure to activate virtual environment.

```sh
python3 -m backend.app
```

## Run the application with env variable

Make sure to activate virtual environment.

```powershell
$env:PEER = 'True'; python -m backend.app
```
