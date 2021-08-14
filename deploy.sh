#!/bin/bash

cd cloud_web

npm run build

scp -r dist/* pi:/opt/cloud/web
