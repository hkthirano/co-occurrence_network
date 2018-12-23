#iter_num=$1
iter_num=2
rm -rf data

for iter in `seq 1 $iter_num`
do
    for network in random sf sw
    do
        for interact in compt mix mutual pp random
        do
            for dir in A real count pred #frac
            do

                mkdir -p data/$network/$interact/iter-$iter/$dir

            done
            for method in count-pea count-spe count-ppea count-pspe flac-pea flac-spe flac-ppea flac-pspe count-mic flac-mic sparcc rebacca spiec-easi cclasso
            do
                mkdir -p data/$network/$interact/iter-$iter/pred/$method
            done
        done
    done
done
