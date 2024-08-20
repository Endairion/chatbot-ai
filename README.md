# Instructions

**Install Python 3.12.4 or above**

Steps to install python:
1. Head to https://www.python.org/downloads/ and download python installer
2. Run the python installer
3. Make sure to add python.exe to the path, tick the checkbox below
4. Use the default installation settings, or you can customizes the installation location to somewhere else
5. Once python is installed proceed to the next step

Download the zipped source code and extract all of the files.

Once Python is installed, head to command prompt `Ctrl + R` and type `cmd`. Inside the prompt, make sure Python is installed. 
> python --version

If the prompt return a python version means the python is properly installed.

First we will head to the directory of the extracted folder `chatbot-ai`. Then we will create a virtual environment for all the pip packages. Make sure you have pip installed, should be installed with python.
> pip --version

If pip is installed, we would create the virtual environment with the command below. `.venv` being the name of the directory/folder for the virtual environment.
> python -m venv .venv

Once the environment is created, you need to activate the environment
> ./.venv/Script/activate

Then we will install the pip requirements.
> pip install -r requirements.txt

This should take a few minutes to finish depends on the machine you have.

For Chromadb it would need a installation of Visual Studio Build Tools. You can download it here https://visualstudio.microsoft.com/visual-cpp-build-tools/. Select `Desktop Development with C++` then install.

Once all things is setup properly you should now be able to run the application. You have to be in `chatbot-ai/src` in order to start the application. Once you are in the directory, make sure you have activated the virtual environment, `(.venv) C:\chatbot-ai\src`, Then run the app_api_handler.py with
> py app_api_handler.py

You should see an uvicorn server started. Then head to your browser and go to http://localhost:5050/docs.

Here you would see three api endpoint, the first one is for showing purposes.
For `/submit_query`, you would need to pass in a response body. `source` being the file that you want to filter
```
Response Body:
{
    "query_text": "string"
    "filter":{
        "source": "train\\filename.txt"
    }
}
```

For `/update`, it would update the vector database if there is new entry of documents. It would take a lot of time for the vector database to update, depends on your machine.

