FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build-env

WORKDIR /code
COPY . ./

RUN dotnet restore
# Build and publish a release
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:7.0
WORKDIR /code

EXPOSE 7180
COPY --from=build-env /code/out .

ENTRYPOINT ["dotnet", "Exsample.dll"]