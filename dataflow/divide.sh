ls -1 | wc -l

PARENT=${1}
cd $PARENT 
n=0
for i in *
do
  if [ $((n+=1)) -gt $((4)) ]; then
    n=1
  fi
  todir=$PARENT/_$n
  [ -d "$todir" ] || mkdir "$todir" 
  mv "$i" "$todir" 
done

