# DBCop

## Usage

1. Clone it.

```
    git clone git@gitlab.math.univ-paris-diderot.fr:ranadeep/dbcop.git
```

2. Compile and install using `cargo` and run.
   Make sure `~/.cargo/bin` is in your system path.

```
    cd dbcop
    dbcop install --path .
    dbcop --help
```

---

There are a few `docker-compose` files in `docker` directory to create docker cluster.

The workflow goes like this,

1. Generate a bunch of histories to execute on a database.
2. Execute those histories on a database using provided `traits`. (see in `examples`).
3. Verify the executed histories for `--cc`(causal consistency), `--si`(snapshot isolation), `--ser`(serialization).

## Build on Ubuntu 22

```sh
# 0. install dependencies
sudo apt install libssl-dev libclang-dev
# cargo and rust >= 1.70.0, see https://doc.rust-lang.org/cargo/getting-started/installation.html

# 1. update Cargo.toml
# done in this repo.

# 2. build
cargo build
# generate release version for performance test
cargo build --release
```

## Generate History of Excutions

```sh
./target/debug/dbcop generate -d ./histories -h 1 -n 3 -v 5 -t 5 -e 2
```

## Verify Histories

```sh
./target/debug/dbcop verify -d ./excutions/antidote_all_writes/3_30_20_180/hist-00000 -o ./results -c ser
```

## Test Performance

```sh
python scripts/test-from-excution.py
```

## Code Structure

```
src
├── consistency // 和一致性相关
│   ├── algo.rs
│   ├── mod.rs // 声明模块和一致性
│   ├── sat.rs
│   └── util.rs
├── db // 和数据库执行相关
│   ├── cluster.rs // 似乎和分布式/并发执行有关，该项目中没有用到，已从 mod.rs 中移除
│   ├── history.rs
│   └── mod.rs // 声明模块
├── lib.rs // 声明模块和依赖
├── main.rs // 解析命令
└── verifier // 和一致性验证相关算法
    ├── mod.rs
    └── util.rs
examples // 没有用到
├── antidotedb.rs
├── cockroachdb.rs
├── disql.rs
├── galera.rs
└── history_duration.rs
```