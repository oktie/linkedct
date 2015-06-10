# wget "http://www.clinicaltrials.gov/ct2/show/NCT0$i$j$k$l$m$n$o?displayxml=true" -nv
# mv "NCT0$i$j$k$l$m$n$o@displayxml=true" "NCT0$i$j$k$l$m$n$o.xml"

#rm -f filelist.txt
cp filelist-bak1.txt filelist-bak2.txt
cp filelist.txt filelist-bak1.txt
cp filelist.txt initial-filelist.txt

for ((  i = 670 ;  i <= 770;  i++  ))
do
  wget "http://clinicaltrials.gov/ct2/crawl/$i" -nv
  grep -o "/ct2/show/NCT[0-9]*" $i | sort -u >> initial-filelist.txt
  rm -f $i
done

sort -u initial-filelist.txt > filelist.txt
