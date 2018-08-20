#!/usr/bin/env bash
for a in $(ls ~/Pictures/training/images/);
 do second=${a:0:2};
 echo '~/Pictures/training/images/'"$second"'_maual.ds';
 source='../../../Pictures/training/images/'"$a"
 reference='../../../Pictures/training/1st_manual/'"$second"'_manual1.gif'

  echo 'path to source = '$source
  echo 'path to reference = '$reference
 python3 splitImage2.py $source $reference 299 299 &
done
