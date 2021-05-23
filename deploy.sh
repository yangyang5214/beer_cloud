#!/bin/bash

cd cloud_web

npm run build

cd ..

rm -rf cloud_api/src/main/resources/static/*

cp -r cloud_web/dist/* cloud_api/src/main/resources/static/

cd cloud_api

mvn clean package
