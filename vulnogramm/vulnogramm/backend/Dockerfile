FROM mcr.microsoft.com/dotnet/aspnet:6.0

WORKDIR /app
COPY . .
COPY Watermark ./Watermark
COPY runtimes ./runtimes
COPY Bebas_Neue.ttf . 

ENTRYPOINT ["dotnet", "Vulnogramm.dll"]