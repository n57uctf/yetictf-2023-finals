FROM maven:3.8.5-openjdk-8 as maven_build

COPY .mvn .mvn
COPY mvnw .
COPY pom.xml .
COPY src src

RUN mvn clean compile
RUN mvn -Dmaven.skip.test package

FROM eclipse-temurin:8

EXPOSE 8080

#default command
CMD java -jar /data/app.jar

#copy hello world to docker image from builder image

COPY --from=maven_build target/*.jar /data/app.jar
