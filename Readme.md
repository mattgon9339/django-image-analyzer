# Django Project Readme

## Google Cloud CLI Installation and Authentication

1.**Install the Google Cloud CLI:** Follow the instructions [here](https://cloud.google.com/sdk/docs/install).

2.**Authenticate:**
   After installation, run the following command to authenticate:

``gcloud auth application-default login``

## Project Installation

- Clone the repository

```bash
git clone https://github.com/mattgon9339/django-image-analyzer.git
cd django-image-analyzer
```

**Install virtual environment**
`python -m venv venv`

**Activate the virtual environment**

- (On Windows)
   `venv\Scripts\activate`

- (On Unix or MacOS)
  `source venv/bin/activate`

**Install project dependencies**
`pip install -r requirements.txt`

**Apply database migrations**
`python manage.py migrate`

## Starting the Project

Run the Django development server


`python manage.py runserver`


Access the project by visiting http://127.0.0.1:8000/ in your web browser.

## Running Tests

Execute the following command to run tests


`python manage.py test`
