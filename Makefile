build:
	cargo build --release

test: build
	#./target/release/dbcop verify -d ./excutions/antidote_all_writes/3_30_20_180/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/roachdb_general_partition_writes/3_30_20_180/hist-00001 -o ./results -c ser
	./target/release/dbcop verify -d ./excutions/diy_excutions/5_45_15_1000/hist-00000 -o ./results -c ser