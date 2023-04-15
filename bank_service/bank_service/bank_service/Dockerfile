FROM maven:3.8.5-openjdk-8 as maven_build

FROM eclipse-temurin:8

EXPOSE 8080

#default command
CMD java -jar /data/app.jar

#copy hello world to docker image from builder image

COPY *.jar /data/app.jar
