faas-cli deploy -f dl-deploy.yml --label com.openfaas.scale.max=3 \
--label com.openfaas.scale.target=90 \
--label com.openfaas.scale.type=cpu \
--label com.openfaas.scale.target-proportion=0.9 \
--label com.openfaas.scale.zero=true \
--label com.openfaas.scale.zero-duration=30m