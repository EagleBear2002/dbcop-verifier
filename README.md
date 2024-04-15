# DBCop

## Usage

1. Clone it.

```
git clone git@git.nju.edu.cn:EagleBear/dbcop-verifier.git
```

<!--
2. Compile and install using `cargo` and run. Make sure `~/.cargo/bin` is in your system path.

```
cd dbcop
dbcop install --path .
dbcop --help
```
-->

There are a few `docker-compose` files in `docker` directory to create docker cluster.

The workflow goes like this,

1. Generate a bunch of histories to execute on a database.
2. Execute those histories on a database using provided `traits`. (see in `examples`).
3. Verify the executed histories for `--cc`(causal consistency), `--si`(snapshot isolation), `--ser`(serialization).

## Usage on Ubuntu 22

### Build

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

### Generate History of Excutions

```sh
./target/release/dbcop generate -d ./histories -h 1 -n 3 -v 5 -t 5 -e 2
```

### Verify Histories

A demo of excutions is already in `excutions` which is used in OOPSLA'19-_On the Complexity of Checking Transactional
Consistency_.

```sh
./target/release/dbcop verify -d ./excutions/antidote_all_writes/3_30_20_180/hist-00000 -o ./results -c ser
```

### Test Performance

We provide a python script `script/test-from-excution.py` to test. You can edit it for other excutions.

```sh
python3 script/verify-all.py
```

### Code Structure

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
examples // 用于生成执行历史
├── antidotedb.rs
├── cockroachdb.rs
├── disql.rs
├── galera.rs
└── history_duration.rs
```

## 核心算法

1. 从二进制输入文件读取数据，存入 `History`
2. 调用 `Verifier.verify` 进行验证：
    1. 调用 `Verifier.transactional_history_verify` 进行验证
        1. 生成 `write_map`，维护“是哪个事务的哪个事件将这个变量 x 写成 value”
        2. 生成 `transaction_last_writes`，维护“该事务中最后修改这个变量 x 的是哪个事件”；过程中检查事务内部的冲突
        3. 生成 `transaction_infos`，维护“该事务写了哪些变量、read from 哪些事务”；生成 `root_write_info`，维护哪些事务和根节点有
           wr 和 ww 关系。
        4. 根据 `transaction_infos` 生成 `SerializableHistory`
        5. 生成 `wr` 边，并合并入 `vis`；
        6. 根据现有的 `vis` 边迭代生成 `ww` 边和 `rw` 边并将其加入 `vis`，直到不能生成新的边为止。
        7. 若有环，则不符合 `ser`；
        8. 调用 `get_linearization`：
            1. 生成 `non_det_choices`，维护“当前有哪些结点可以被扩展”，这一集合类似拓扑排序中的“没有入度的边”
            2. 生成 `active_parent`，维护“对于结点 u，有多少结点可能成为其父结点”，类似拓扑排序中的“当前入度数目”
            3. 生成 `linearization`，维护“当前已经在树中的结点”，类似拓扑排序中的“已完成排序的集合”
            4. 生成 `seen`，维护“已经搜索过的 `non_det_choices`”，用于记忆化搜索
            5. 将以上四个数据结构的引用传给 `do_dfs` 并调用，
                1. `do_dfs`：对于 `non_det_choices` 中的每个结点，如果通过了 `allow_next` 测试，将其加入`linearization`，并像拓扑排序那样将新的可扩展的结点加入 `non_det_choices`