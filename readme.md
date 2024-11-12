1- creating requirements.txt 
2- creating Dockerfile
3- run: docker build -t background-magic .
4- run: docker run -d --name bg-magic-container -p 5000:5000 background-magic
5- in azure :
- Go to the Azure Portal.
- Navigate to Create a resource > Containers > Container Registry.
- Fill out the necessary fields and click Review + Create.
in cmd of own pc : 
-az login
-az acr login --name backgroundmagic
-docker tag background-magic backgroundmagic.azurecr.io/background-magic:v1
-docker push backgroundmagic.azurecr.io/background-magic:v1
Deploy the Docker Image to Azure App Service:
1- Go to the Azure Portal.
-Navigate to Create a resource > App Services > Web App.
-Fill in the necessary fields (select your subscription, resource group, and the name of the app).
-Under Publish, select Docker Container.
-For Image Source, select Azure Container Registry and enter your ACR name and image details.
-Click Review + Create.

