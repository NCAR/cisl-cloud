# TensorFlow GPU Image

## VAPOR

I am able to get VAPOR to work on this container by passing the following command during runtime

```
docker run -it --rm -p 8888:8888 --runtime=nvidia --gpus=all -e NVIDIA_DRIVER_CAPABILITIES=all <latest_image_tag> jupyter lab --ip 0.0.0.0
```

For the k8s JupyterHub we would need to provide all of these as well. The --gpus=all command I believe is the only one not provided currently