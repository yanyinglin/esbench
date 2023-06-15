# rm -rf ./build
export DOCKER_CLI_EXPERIMENTAL=enabled
faas-cli publish --platforms linux/arm64 -f openfass-deep-learning.yml