rm -rf data/*.json

if [ -e summary.json ]; then
    cp summary.json data
else
    curl https://rsbuddy.com/exchange/summary.json > data/summary.json
fi
