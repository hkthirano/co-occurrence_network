iter_num=50
rm -rf out-res

for iter in `seq 1 $iter_num`
do
    mkdir -p out-res/iter-$iter

    for network in random
    do
        for interact in random
        do            
            rm ../../data/$network/$interact/mode-3/iter-$iter/pred/sparcc/*
            rm ../../data/$network/$interact/mode-5/iter-$iter/pred/sparcc/*
            rm ../../data/$network/$interact/mode-6/iter-$iter/pred/sparcc/*
            rm ../../data/$network/$interact/mode-7/iter-$iter/pred/sparcc/*
        done
    done
done
