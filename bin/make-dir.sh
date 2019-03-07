#iter_num=$1
iter_num=50
rm -rf data

for iter in `seq 1 $iter_num`
do
    for mode in 3 5 6 7
    do
        for network in random
        do
            for interact in random
            do
                for dir in A real count pred #frac
                do

                    mkdir -p data/$network/$interact/mode-$mode/iter-$iter/$dir

                done
                for method in flac-pea flac-spe flac-ppea flac-pspe count-mic flac-mic sparcc rebacca spiec-easi cclasso
                do
                    mkdir -p data/$network/$interact/mode-$mode/iter-$iter/pred/$method
                done
            done
        done
    done
done
