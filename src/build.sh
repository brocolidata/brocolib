directory=$1

cd $directory
rm -rf dist 
python3 setup.py sdist bdist_wheel