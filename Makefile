build:
	cargo build --release

test: build
	#./target/release/dbcop verify -d ./excutions/antidote_all_writes/3_30_20_180/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/roachdb_general_partition_writes/3_30_20_180/hist-00001 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_15_15_1000/hist-00000 -o ./results -c ser
	./target/release/dbcop verify -d ./excutions/diy_excutions/10_45_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_100_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_200_15_1000/hist-00000 -o ./results -c ser