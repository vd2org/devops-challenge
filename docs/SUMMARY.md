# Project summary

### Step by step development log

1. I read INSTRUCTIONS.md from main repo and took time to find out how
to solve task probably.
1. I never using dynamodb before and and i needed some researches for this.
I read documentation about dynamo and see how to use this. I found python
libraries for AWS that called `boto3`.
1. I clone main repo and restructure this in the usual way.
1. After, i prepare development environment - create virtualenv and
install necessary dependencies(`pytest`, `flask`, `boto3`, etc).
1. I found and install local dynamodb installation for local
testing and experiments during coding.
1. After several attempts my code get worked with the local and production dynamo
and i got expected secret code.
1. Then i reformat code for testing and wrote tests.
1. After this i write `Dockerfile` and `docker-compose.yml` and run it for test
on my own servers.
1. I connect repo to travis-ci and wrote `.travis.yml` for run automatic tests.
It required to solve several problems. And after this everything get worked rigth.
1. I create repo on dockerhub and write script for building and publishing container
from travis.
1. I wrote documentation and this file.
1. By the final i run my code local last time and take some screenshots.
