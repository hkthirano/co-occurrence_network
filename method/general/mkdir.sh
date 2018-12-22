iter_num=30
rm -rf out-res

for iter in `seq 1 $iter_num`
do
    mkdir -p out-res/iter-$iter
done