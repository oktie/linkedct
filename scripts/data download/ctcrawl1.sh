for i in 0 1 2 3 4 5 6 7 8 9 # loop
do
for j in 0 1 2 3 4 5 6 7 8 9 # loop
do
for k in 0 1 2 3 4 5 6 7 8 9 # loop
do
for l in 0 1 2 3 4 5 6 7 8 9 # loop
do
for m in 0 1 2 3 4 5 6 7 8 9 # loop
do
for n in 0 1 2 3 4 5 6 7 8 9 # loop
do
for o in 0 1 2 3 4 5 6 7 8 9 # loop
do
 wget "http://www.clinicaltrials.gov/ct2/show/NCT0$i$j$k$l$m$n$o?displayxml=true" -nv
 mv "NCT0$i$j$k$l$m$n$o@displayxml=true" "NCT0$i$j$k$l$m$n$o.xml"
done
done
done
done
done
done
done