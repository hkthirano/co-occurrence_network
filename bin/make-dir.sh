#iter_num=$1
iter_num=5
rm -rf data

for iter in `seq 1 $iter_num`
do
    for ratio in 0 1 2 3 4 5 6 7 8 9 10
    do
        for network in random
        do
            for interact in mix2
            do
                for dir in A real count pred #frac
                do

                    mkdir -p data/$network/$interact/ratio-$ratio/iter-$iter/$dir

                done
                for method in flac-pea flac-ppea spiec-easi cclasso
                do
                    mkdir -p data/$network/$interact/ratio-$ratio/iter-$iter/pred/$method
                done
            done
        done
    done
done
