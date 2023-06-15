faas-cli deploy -f stream-deploy.yml

# kubectl autoscale deployment -n openfaas-fn stream-net \
#   --cpu-percent=80 \
#   --min=0 \
#   --max=24



faas-cli deploy -f stream-net-wifi-deploy.yml

# kubectl autoscale deployment -n openfaas-fn stream-net-wifi \
#   --cpu-percent=80 \
#   --min=0 \
#   --max=24

faas-cli deploy -f stream-net-wired-deploy.yml

# kubectl autoscale deployment -n openfaas-fn stream-net-wired \
#   --cpu-percent=80 \
#   --min=0 \
#   --max=24