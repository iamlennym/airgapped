# README #

Script to help download and push required images for Harness SMP air-gapped installation.

### How do I use this ? ###

* Edit the pullImages.py file
* Change the *local_registry* variable to point to the local registry
* Execute
    * python3 pullImages.py 


If the script runs succesfully:
* It will pull all images listed in the *helm-charts/src/harness/images.txt* file.
* Create another file called *push2Registry.sh* which needs to be executed, once the registry is reachable (and logged into).


```
#Authenticate with Docker for Docker Registry
docker login <registry-url>

#Authenticate with Google Cloud Platform for GCR
gcloud auth login

#Authenticate with AWS for ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-
```

Reference:
[Install in Air-gapped environment](https://developer.harness.io/docs/self-managed-enterprise-edition/self-managed-helm-based-install/install-in-an-air-gapped-environment/)


