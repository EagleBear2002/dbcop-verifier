build:
	cargo build --release

test: build
	#./target/release/dbcop verify -d ./excutions/antidote_all_writes/3_30_20_180/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/roachdb_general_partition_writes/3_30_20_180/hist-00001 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/galera_all_writes/12_30_20_720/hist-00024 -o ./results -c ser
	./target/release/dbcop verify -d ./excutions/galera_partition_writes/3_30_20_180/hist-00005 -o ./results -c ser # ok
	#./target/release/dbcop verify -d ./excutions/diy_excutions/5_45_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_15_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/10_45_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_100_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_200_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_300_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_400_15_1000/hist-00000 -o ./results -c ser
	#./target/release/dbcop verify -d ./excutions/diy_excutions/15_700_15_1000/hist-00000 -o ./results -c ser

	# bug here
	#./target/release/dbcop verify -d ./excutions/diy_excutions-15_45_5_1000/hist-00000 -o ./results -c ser

verify-all: build
	python3 ./script/verify-all.py

check-ans:
	python3 ./script/check-ans.py

mem-analyze-test:
	valgrind --tool=massif target/debug/dbcop verify -d ./excutions/galera_partition_writes/9_30_20_540/hist-00000 -o ./results -c ser

parse-massif:
	python3 ./script/parse-massif.py

draw-csv:
	python3 ./script/draw-csv.py