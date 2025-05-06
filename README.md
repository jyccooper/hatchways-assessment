# Spending App Challenge

Thanks for your interest in joining our team. The purpose of this challenge is to replicate a real-world working environment and to test a diverse set of skills, to see how you would work with us on our team. The challenge itself is similar to the work you would be doing on our team.

Below is some high level detail about the project. Good luck!

## Language & Tools

- [Python](https://www.python.org/) - project tested with v3.11
- [Flask](https://flask.palletsprojects.com/en/2.2.x/) - server-side framework
- [Pip](https://pypi.org/project/pip/) - as a package manager for the server
- [NPM](https://www.npmjs.com/) - as a package manager for the client
- [React](https://reactjs.org/) - client-side framework

## Quickstart

This section contains all the information required for getting the server up and running. The application contains the following two directories:

- [server/](server/) - the server directory that contains the server code
- [client/](client/) - the client directory that contains the client code

In order to run the application, you will need to have both the server and client running in separate terminals.

### Server

- System requirements
  - Python3

1. Navigate to the server directory (in Unix that would be `cd server`)

2. Before you get started, you may want to create a virtual environment to help manage multiple versions
   of Python on your computer. This is an optional step. Here is a
   [quick tutorial](https://realpython.com/python-virtual-environments-a-primer/) on setting up virtual environments.

3. Copy the contents of the ".env.sample" file to a ".env" file. You can do this by using the following command:

   ```
   cp .env.sample .env
   ```

4. Install dependencies by using the command:

   ```
   pip install -r requirements.txt
   ```

5. Seed the database by using the command:

   ```
   python seed.py
   ```

   This will re-populate the database with data closer to-date.

6. Run the development server by using the command:

   ```
   flask run --port=8080
   ```

This command will launch the Flask server in debug mode (with hot-reloading) on port 8080.

### Client

- System requirements
  - NodeJS v18

To run the client, follow these steps:

1. Navigate to the client directory (in Unix that would be `cd client`)

2. Install dependencies

   ```bash
   npm install
   ```

   You can ignore the severity vulnerabilities, this is a [known issue](https://github.com/facebook/create-react-app/issues/11174) related to `create-react-app` and are not real vulnerabilities.

3. Start the client

   ```bash
   npm start
   ```

## Formatting Client

To format your code using [prettier](https://prettier.io/), follow these steps:

1. Navigate to the client directory (in Unix that would be `cd client`)

2. Run this command:

   ```bash
   npm run lint
   ```

   To ensure you are using the correct version of prettier, make sure to format your code after installing the dependencies (`npm install`).

## Verify That Everything Is Set Up Correctly

To verify that the frontend is working properly, go to [http://localhost:3000](http://localhost:3000). You should see the homepage that is titled "Welcome to My Spending App" and a chart as below.

![Starting Screen](https://storage.googleapis.com/m.hatchways.io/SpendingApp-screenshot.png)
