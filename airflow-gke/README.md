For a complete guide, please follow the readme on [session_04](https://github.com/wizelineacademy/Google-Africa-DEB/tree/main/session_04/exercises/airflow-gke#google-kubernetes-engine-gke-airflow-and-terraform-template)

# Google Kubernetes Engine (GKE), Airflow and Terraform template


## Prerequisites
- [Configured GCP account](https://cloud.google.com/)
- [Homebrew](https://brew.sh/) (if you're using MacOS)
- [Kubectl cli](https://kubernetes.io/docs/tasks/tools/) (choose the OS you're working with)
- [gCloud SDK](https://cloud.google.com/sdk/docs/quickstart)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) >= 0.13
- [Helm 3](https://helm.sh/docs/intro/install/)


## Step by step guide
1. Clone this repository.


2. Create a [virtual environment for your local project](https://medium.com/@dakota.lillie/an-introduction-to-virtual-environments-in-python-ce16cda92853)
and activate it:
    ```bash
    python3 -m venv .venv # create virtual environment
    source .venv/bin/activate # activate virtual environment
    deactivate # DO NOT RUN YET: deactivates virtual environment
    ```

3. Initialize gcloud SDK and authorize it to access GCP using your user account credentials:
    ```bash
    gcloud init
       
    # The next portion represents the cli settings setup
    >> [1] Re-initialize this configuration [default] with new settings # config to use
    >> [1] user@sample.com # account to perform operations for config
    >> [6] project-id # cloud project to use
    >> [8] us-central1-a # region to connect to
   
    gcloud auth application-default login # authorize access
    ```
   **DISCLAIMER:** This part will ask you to choose the Google account and the GCP project you will work with. It
will also ask you to choose a region to connect to. The information shown above in is an example of what you *can*
choose, but keep in mind that this was used for credentials that were already entered once before.  


3. For GCP to access you user account credentials for the first time, it will ask you to give it explicit permission
like so:
![Choose account for Google Cloud SDK](./imgs/google-account.png "Choose account")
![Grant access for Google Cloud SDK](./imgs/authorization.png "Grant access")


4. After choosing the Google account to work with and successfully granting permissions, you should be redirected to
    this message:
![Successful authentication message](./imgs/successful-authentication.png "Successful authentication")


5. You should also see a similar message to this in your terminal:
![Configured Google Cloud SDK](./imgs/cloud-sdk-configured.png "Configured Google Cloud SDK")


6. In the GCP Console, enable:
   - Compute Engine API
   - Kubernetes Engine API


7. In your cloned local project, copy the [terraform.tfvars.example](./terraform.tfvars.example) and paste it in the
root of the project named as *terraform.tfvars*, changing the property *project_id* to your corresponding project ID.


8. Initialize the Terraform workspace and create the resources:
    ```bash
    terraform init # initialize
    terraform init --upgrade # if you initialized once before and need to update terraform config
    terraform plan # lets us review the operations we want to perform
    terraform apply --var-file=terraform.tfvars
    >> yes # lets terraform perform actions described
    ```
    ***IMPORTANT***: This process might take around 10-15 minutes, **be patient please**.


9. Set the kubectl context:
    ```bash
    gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw location)
    ```
    _specifying it manually woked_ (gcloud container clusters get-credentials airflow-gke-data-bootcamp --region=us-east1-b) https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl


10b. and Final according to Nelson:

     ```
        gcloud container clusters create airflow-cluster \
        --machine-type n1-standard-1 \
        --num-nodes 1 \
        --zone "europe-west4"
     ```
(https://github.com/airflow-helm/charts/blob/main/charts/airflow/docs/guides/quickstart.md provides guides as listed below to install helm stable airflow chart)
14.  Create a namespace for Airflow:
    ```bash
    kubectl create ns airflow
    ```

15.  Add the chart repository:
    ```bash
    helm repo add airflow-stable https://airflow-helm.github.io/charts
    ## update your helm repo cache
    helm repo update
    ```

16.  Install the Airflow chart from the repository:
    ```bash
    helm install airflow airflow-stable/airflow  --namespace airflow  --version 8.8.0 --values airflow-values.yaml
    ```
    ***IMPORTANT***: This process might take around 5 minutes to execute, **be patient please**.


17. Verify that the pods are up and running:
    ```bash
    kubectl get pods -n airflow
    ```

18. Access the Airflow dashboard with what the Helm chart provided:
    ```bash
    Your release is named airflow.
    You can now access your dashboard(s) by executing the following command(s) and visiting the corresponding port at localhost in your browser:
    
    Airflow Webserver:     kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
    Default Webserver (Airflow UI) Login credentials:
        username: admin
        password: admin
    Default Postgres connection credentials:
        username: postgres
        password: postgres
        port: 5432
    ```
    **Note:** Sometimes there's an error when doing the kubectl portforward. If all of the pods are running, we might
    just need to keep trying.
    

19. Once in `localhost:8080`, you should see the Airflow login.
![Airflow Login](./imgs/airflow-login.png "Airflow Login")


20. After logging in with your credentials (username and password from webserver in step 18), you should see the Airflow
dashboard.
![Airflow Dashboard](./imgs/airflow-dag-dashboard.png "Airflow Dashboard")


## Don't forget to ***destroy everything*** after you're done using it!
- To destroy the cluster:
    ```bash
    terraform destroy --var-file=terraform.tfvars
    ```
- Double-check your GCP console to make sure everything was correctly destroyed.


## Troubleshooting
1. Cloud SQL instance already exists.
    > Error: Error, failed to create instance data-bootcamp: googleapi: Error 409 The Cloud SQL instance already exists. When you delete an instance, you can't reuse the name of the deleted instance until one week from the deletion date., instanceAlreadyExists
   
    ***Fix:*** In [terraform.tfvars](./terraform.tfvars), change the CloudSQL *instance_name* property to be named
differently:
    ```bash
    # CloudSQL
    instance_name = "data-bootcamp-2"
    ```

2. Root resource was present, but now absent.
    > Error: Provider produced inconsistent result after apply. When applying changes to
    > module.cloudsql.google_sql_user.users, provider "provider[\"registry.terraform.io/hashicorp/google\"]" produced an
    > unexpected new value: Root resource was present, but now absent.

    ***Fix:*** In [main.tf](./main.tf), set the terraform version to 3.77.0:
    ```bash
    terraform {
      required_providers {
        google = {
          source = "hashicorp/google"
          version = "3.77.0"
        }
      }
      required_version = ">= 0.13.0"
    }
    ```

3. Project not found.
    > ERROR: (gcloud.container.clusters.get-credentials) ResponseError: code=404, message=Not found: 
   > projects/gcp-data-eng-apprXX-XXXXXXXX/zones/us-central1-a/clusters/airflow-gke-data-apprenticeship.

    ***Fix:*** In [terraform.tfvars](./terraform.tfvars) the value of the property *project_id* might need to be changed
to match your project ID.


4. 403: Not Authorized.
    > Error: Error, failed to create instance data-bootcamp: googleapi: Error 403: The client is not authorized to make
   > this request., notAuthorized
   
    ***Fix:*** You might've skipped the `gcloud auth application-default login` command to authorize access.


5. Failed apache-airflow installation.
    > Error: INSTALLATION FAILED: failed to download "apache-airflow/airflow"
   
    This error can occur do to the `helm install airflow -f airflow-values.yaml apache-airflow/airflow --namespace airflow`
    command. ***Fix:***
    ```bash
    kubectl delete namespace airflow
    helm repo remove apache-airflow https://airflow.apache.org
    kubectl create namespace airflow
    helm repo add apache-airflow https://airflow.apache.org
    helm upgrade --install airflow -f airflow-values.yaml apache-airflow/airflow --namespace airflow
    ```
## Components not runnning?
1. Skip steps that involves NFS, that is, step 11 to 14.
2. Use the Airflow Community Chart:\
   a. Step 16:
   ```
    helm repo add airflow-stable https://airflow-helm.github.io/charts
    helm repo update
   ```
3. Edit the airflow-values.yaml file to the Community Chart values (file at the end). Remember to change the “repo” and “repoSubPath” parameters of gitSync to your own repo when you have a DAG that is ready to test, for now it’s the hello_world.py in the Google-Africa-DEB repo.
4. Before deploying the new chart, remember to remove any remaining PVC (if you deployed before the official chart of if you want a clean deploy). Replace $PVC_NAME with the name of the PVC to delete.
   
        kubectl get pvc -A
        kubectl delete pvc $PVC_NAME -n airflow

5. Deploy airflow\
    a. Step 17:

        - helm upgrade --install airflow -f airflow-values.yaml airflow-stable/airflow --namespace airflow
        - helm delete airflow -n  airflow  
        - helm upgrade --install airflow airflow-stable/airflow --namespace airflow
6. Connect to the web interface

        kubectl port-forward svc/${AIRFLOW_NAME}-web 8080:8080 --namespace $AIRFLOW_NAMESPACE
    (${AIRFLOW_NAME} and $AIRFLOW_NAMESPACE should be: **airflow**)
```
###################################
## COMPONENT | Triggerer
###################################
triggerer:
 ## if the airflow triggerer should be deployed
 ## - [WARNING] the triggerer component was added in airflow 2.2.0
 ## - [WARNING] if `airflow.legacyCommands` is `true` the triggerer will NOT be deployed
 ##
 enabled: false
###################################
## COMPONENT | Flower
###################################
flower:
 ## if the airflow flower UI should be deployed
 ##
 enabled: false
###################################
## CONFIG | Airflow Logs
###################################
logs:
 ## the airflow logs folder
 ##
 path: /usr/local/airflow/logs
 ## configs for the logs PVC
 ##
 persistence:
  ## if a persistent volume is mounted at `logs.path`
  ##
  enabled: false
###################################
## CONFIG | Airflow DAGs
###################################
dags:
 ## the airflow dags folder
 ##
 path: /usr/local/airflow/dags
 ## configs for the git-sync sidecar (https://github.com/kubernetes/git-sync)
 ##
 gitSync:
  ## if the git-sync sidecar container is enabled
  ##
  enabled: true
  ## the url of the git repo
  ##
  ## ____ EXAMPLE _______________
  ##  # https git repo
  ##  repo: https://github.com/USERNAME/REPOSITORY.git”
  ##
  ## ____ EXAMPLE _______________
  ##  # ssh git repo
  ##  repo: “git@github.com:USERNAME/REPOSITORY.git”
  ##
  repo: https://github.com/wizelineacademy/Google-Africa-DEB
  ## the sub-path within your repo where dags are located
  ## - only dags under this path within your repo will be seen by airflow,
  ##  (note, the full repo will still be cloned)
  ##
  repoSubPath: session_04/exercises/airflow-gke/dags
  ## the git branch to check out
  ##
  branch: main
###################################
## DATABASE | PgBouncer
###################################
pgbouncer:
 ## if the pgbouncer Deployment is created
 ##
 enabled: false
 ```
## Resources
1. [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
2. [Terraform GCP Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)


## Acknowledgments
This solution was based on this guide: [Provision a GKE Cluster guide](https://learn.hashicorp.com/tutorials/terraform/gke?in=terraform/kubernetes),
containing Terraform configuration files to provision an GKE cluster on GCP.
