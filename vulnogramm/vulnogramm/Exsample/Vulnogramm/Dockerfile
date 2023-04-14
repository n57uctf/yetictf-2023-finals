FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build-env

WORKDIR /code
COPY . ./

RUN dotnet restore
# Build and publish a release
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:6.0

WORKDIR /app
COPY --from=build-env /code/out .
COPY Watermark ./Watermark
COPY Bebas_Neue.ttf . 

ENTRYPOINT ["dotnet", "Vulnogramm.dll"]