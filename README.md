# simple_fastapi_template ⏩

This is a microservice template written in Python using the [FastAPI](https://fastapi.tiangolo.com/) framework and deployed in AWS Lambda using [Mangum](https://mangum.io).

## Introduction and Objectives ⁉
The main objective is to provide a template for repositories that can be used as a starting point for new projects. This architecture is based on the Clean Architecture, and it was based in many other projects and books, articles that were mixed by the students of Mauá Institute of Technology, from the academic group Dev. Community Mauá.
## How to use 🤔
First of all, you need to create a repo using issues from [Devmaua setup](https://github.com/Maua-Dev/devmaua_setup/), set the **project_name** as you prefer and project template as **simple_fastapi_template** and make sure it's **public** . Hit create issue and wait for the setup to finish.

After that you need to clone your new repo, create a virtual environment and install the requirements.

## Installation 👩‍💻

### Create virtual ambient in python (only first time)

###### Windows

    python -m venv venv

###### Linux

    virtualenv -p python3.9 venv

#### Activate the venv

###### Windows:

    venv\Scripts\activate

###### Linux:

    source venv/bin/activate

#### Install the requirements

    pip install -r requirements-dev.txt
    pip install -r requirements.txt

#### Run the tests

    pytest

#### Run the server local

    uvicorn src.app.main:app

#### If you want to access the FAST API interface to interact with the API, you can access the following URL:

    http://localhost:8000/docs

### Atention 🚨
In order to deploy your microservice in AWS Lambda, you need to follow some rules:
- The routes must be created using FastAPI decorators;
- Don't use complete import, only relative ones. (eg: from .move_function import move);
- ALWAYS test your code before pushing it to the repo. You can use pytest to test your code;
- Don't forget to create your own tests;
- Make sure there is a \_\_init\_\_.py file each directory, otherwise it's not a Python package;
- Every file should be inside the app folder;

### Deploy 🚀

![FastAPI DrawIO](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/d7e0f17a-b583-4594-b0f5-d7bce0a46d44)


After pushing your code to the repo, it will trigger an action to deploy your code in AWS Lambda. You can find the action in the **.github/workflows/aws_cd.yml** file.

In the first time you push your code, the action will create a new stack in AWS CloudFormation. After that, every time you push your code, the action will update the stack with the new code.

In the [Actions](https://github.com/Maua-Dev/simple_fastapi_template/actions) tab you can see the status of the deploy, and if it was successful or not. If it was successful, you can find the URL of your API in the outputs tab of the action (in the final part of the "Deploy with CDK" step).

![Action Tab](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/e7735f61-1fe5-4a6b-9e04-b5159a94f4f7)
![CD](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/9a4174b3-50c2-4114-aa57-101f8670de84)
![STEP](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/c5707f59-6e3c-44c1-8939-446c22b65fd0)

There you can find your API URL, an user and password to access the AWS Console and view the logs of the lambda function to debug it.

![Outputs](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/1ff2846c-f4f0-4547-b23f-225466e604ec)


To login in the AWS Console, click in the link name "console" on the output, and then click in "Sign in to a different account". There you need to put the account id and the user and password from the outputs tab. On your login you are required to change your password, DON'T FORGET THE NEW ONE. After that you can click in the link to lambda console, and click monitor to find the logs.

![Lambda Console](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/5851eab1-4897-4877-9b39-42012e7cb14a)
![Cloudwatch Logs](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/0350ba37-3714-4dc0-a29e-e1671a6d30eb)

After finishing your project, you can delete it from our backend using our CD.

![AwsDestroy](https://github.com/Maua-Dev/simple_fastapi_template/assets/85962841/46ea3d88-c3a7-45e6-adf7-01a0ccccbef3)

## Useful tools 🛠

- [Postman](https://www.postman.com/) - API development environment
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Python3.9](https://docs.python.org/3.9/) - Python Documentation

## Thanks 👢🍿

We hope you like and enjoy it! Thanks!

## Contributors 💰🤝💰

This project was developed to use inside Dev. Community Mauá, but feel free to help!.

- Bruno Vilardi - [Brvilardi](https://github.com/Brvilardi) 👷‍♂️
- Hector Guerrini - [hectorguerrini](https://github.com/hectorguerrini) 🧙‍♂️
- João Branco - [JoaoVitorBranco](https://github.com/JoaoVitorBranco) 😎
- Luigi Trevisan - [LuigiTrevisan](https://github.com/LuigiTrevisan) 🔙 
- Vitor Soller - [VgsStudio](https://github.com/VgsStudio) 🌞

## Contact us 📞
If you have any questions, feel free to contact us! You can find us in our [Discord](https://discord.gg/Yr2VPgAmcb) server.
