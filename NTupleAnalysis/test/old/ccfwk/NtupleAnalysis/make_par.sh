#!/bin/bash

mkdir -p lib
cd lib/

EDIR=NtupleAnalysisPAR

mkdir $EDIR

cp -r ../NtupleObjects ../inc ../src ../selectors ../makefile $EDIR

mkdir $EDIR/PROOF-INF
cd    $EDIR/PROOF-INF

cat > BUILD.sh <<EOF
#!/bin/sh
# Build libNtupleAnalysis library.

if [ "$1" = "clean" ]; then

  make clean
  exit 0
fi

make
EOF

cat > SETUP.C <<EOF
int SETUP(){

  if(gSystem->Load("libNtupleAnalysis") == -1) return -1;

  return 0;
}
EOF

chmod 755 BUILD.sh

cd ../..

tar czf $EDIR.par $EDIR

rm -rf $EDIR

cd ..

unset -v EDIR
