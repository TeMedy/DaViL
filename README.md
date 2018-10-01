# DaViL
> Data analytics and Visualizaiton for LightTheNight. Measure and present the corporate pariticipation in the fundraising for the lightthenight.ca 

## Before you start
These instructions are aimed for Mac users. Open a terminal on your machine's linux based terminal.
1. Install Git, and clone the repo 
`git clone https://github.com/TeMedy/DaViL.git`

2. Install Docker on your machine.

## How to start
### Running locally
1. First, the Docker images need to be built. `cd` into the root folder of the project. Run `docker-compose build` to build the images. This step will pull layers from the web and install all the requirements in the image. So it might take a few minutes. 

2. Run the Docker container by `docker-compose up`. That's it!

### Running on Amazon Web Service (AWS)
#### Preparing the Docker image 
On your local machine: 
 - Run `docker login` and enter your username and password when prompted to log into the Docker hub.
 - Build the docker image `docker-compose build`.
 - Push the image to the Docker hub by running `docker-compose push`.
#### Preparing the AWS 
 - Log into your AWS
 - Spin up a machine. 
 - Connect to your machine. 
 - Install Docker on your machine, [istructions for AWS](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html#install_docker), [instructions for GCP](https://docs.docker.com/install/linux/docker-ce/debian/). 
 - Install **docker-compose** on your machine, [instructions](https://docs.docker.com/compose/install/#install-compose)
 - Looking into the `docker-compose.yml` file, you can see that a `secrets.env` file is used. Since this file includes secrets (obviously!), it is not included in this repo. Make sure you have this file and `scp` it into your instance though. 
 - Run `docker-compose up` to start the container!
