## Michael Acevedo's solution

To run locally:

In backend directory, create a `.env` file with the following content:

```dotenv
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000
AWS_ACCESS_KEY=xxxxxx__YOUR_ACCESS_KEY__xxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxx__YOUR_SECRET_ACCESS_KEY__xxxxxxx
AWS_S3_BUCKET_NAME=xxxxxx__YOUR_S3_BUCKET_NAME__xxxxxxx
AWS_REGION=xxxxxx__YOUR_AWS_REGION__xxxxxxx
PRESIGNED_URL_EXPIRATION_DAYS=5
UNOSERVER_URL=http://unoserver:2004/request
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

```

Then run `docker compose up --build -d`

The conversion API will be available at http://localhost:8000.

In frontend directory, create a `.env.local` file with the following content:

```dotenv
NEXT_PUBLIC_API_HOST=http://localhost:8000
```

Then run `bun run build`, followed by `bun run start`.

The conversion web app will be available at http://localhost:3000.

# SlideSpeak coding challenge: Build a PowerPoint to PDF marketing tool

## The challenge!

Build a front-end implementation as well as a back-end service to convert PowerPoint documents to PDF format. This
should be done by implementing a simple **Next.js** front-end that posts a file to a **Python** server. You don’t have
to do the converting logic yourself as you can use unoconv or unoserver to do this (you can see more about this in the
acceptance criteria). The front-end is also already implemented in the /frontend folder. You only need to add the
necessary logic to switch between the steps and convert the file via the API that you're going to build.

-   Webpage for the
    tool: [https://slidespeak.co/free-tools/convert-powerpoint-to-pdf/](https://slidespeak.co/free-tools/convert-powerpoint-to-pdf/)
-   Design: [https://www.figma.com/file/CRfT0MVMqIV8rAK6HgSnKA/SlideSpeak-Coding-Challenge?type=design&t=6m2fFDaRs72CowZH-6](https://www.figma.com/file/CRfT0MVMqIV8rAK6HgSnKA/SlideSpeak-Coding-Challenge?type=design&t=6m2fFDaRs72CowZH-6)

## Acceptance criteria

### Back-end API

-   Should be implemented in Python.
-   Converting PowerPoints to PDF can be done with `unoconv` or `unoserver` via Docker if you want to be fancy 😀. You
    don’t need to implement the converting logic yourself.
    -   [Documentation on how to use unoconv and spawn a process](https://pypi.org/project/unoconv/)
        -   Note: `unoconv` is deprecated but thats ok for this challenge
    -   [How to use unoserver via docker](https://gist.github.com/kgoedecke/44955d0b0b1ed4112bcfd3e237e135c0), this will
        create an API that you can use based on [this](https://github.com/libreofficedocker/unoserver-rest-api)
        documentation.
        -   Using unoserver is nice-to-have (but the preferred way), if you find unoconv easier use it instead
-   The API should consist of one endpoint (POST /convert), which should do the following:

    1. Converts the attached file to PDF
    2. Uploads the PowerPoint and PDF file to Amazon S3
       via [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    3. Creates a presigned URL for the user to download

        [https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html)

        [https://medium.com/@aidan.hallett/securing-aws-s3-uploads-using-presigned-urls-aa821c13ae8d](https://medium.com/@aidan.hallett/securing-aws-s3-uploads-using-presigned-urls-aa821c13ae8d)

    4. Returns the presigned S3 url to the client which allows the user to download the file (by opening the url in new
       tab)

### Front-end app

-   The front-end should in terms of UX work similarly
    to [https://app.slidespeak.co/powerpoint-optimizer](https://app.slidespeak.co/powerpoint-optimizer)

## Nice to haves / tips

-   Uses unoserver to convert PowerPoint to PDF via docker compose
-   The logic of the front-end ideally should not rely on useEffect too much since it can be difficult to track what is
    happening
-   Tests
-   Use conventional commit message style: https://www.conventionalcommits.org/en/v1.0.0/
-   Lint your code
-   Keep commits clean
-   If you want to be really fancy you can add queuing with Celery
