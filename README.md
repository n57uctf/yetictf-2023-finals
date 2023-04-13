# yetictf-2023-finals
YetiCTF 2023 Finals (School&amp;Student)

## Repo structure
```
.
├── .github/workflows
│   ├── packer.yml # # Build and Push to S3 VBox Image
│   ├── docker-service1.yml
│   └── docker-service<N>.yml
├── .vulnbox # Build VBox image w\ Vagrant/Packer
│   ├── Vagrantfile
│   └── vulnbox.pkr.hcl
├── service1
│   ├── service1
│   │   ├── <code_stuff>
│   │   ├── docker-compose.yml # Required
|   │   └── host_prepare.sh # Optional: commands to prepare Vulnbox here
│   ├── checker
│   │   ├── <code_stuff>
│   │   ├── requirements.txt
|   │   └── checker.py
│   ├── sploits
│   └── README.md
├── service<N>
│   ├── service<N>
│   ├── checker
│   ├── sploits
│   └── README.md
├── .gitignore
└── README.md
```