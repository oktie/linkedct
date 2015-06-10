# wget "http://www.clinicaltrials.gov/ct2/show/NCT0$i$j$k$l$m$n$o?displayxml=true" -nv
# mv "NCT0$i$j$k$l$m$n$o@displayxml=true" "NCT0$i$j$k$l$m$n$o.xml"

for ((  i = 0 ;  i <= 498;  i++  ))
do
  wget "http://clinicaltrials.gov/ct2/crawl/$i" -nv
  grep -o "/ct2/show/NCT[0-9]*" $i | sort -u > filelist.txt
  rm -f $i
  python fetchfiles.py  
done
