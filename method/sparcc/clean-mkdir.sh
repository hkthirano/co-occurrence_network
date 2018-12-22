iter_num=30
rm -rf out-res

for iter in `seq 1 $iter_num`
do
    mkdir -p out-res/iter-$iter

    for network in random sf sw
    do
        for interact in compt mix mutual pp random
        do            
            rm ../../data/$network/$interact/iter-$iter/pred/sparcc/*
        done
    done
done
