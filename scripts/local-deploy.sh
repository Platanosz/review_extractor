rm -rf dist
make ci
make docker-build
./scripts/docker-stop.sh
./scripts/docker-start.sh

curl "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{}'