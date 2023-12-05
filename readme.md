<h1 align="center">
   VShoes 👟
</h1>

<p align="center">
  <img src="images/logo.png" width=400>
</p>

<hr>

## Links

> You can access this project **Document** [here](https://docs.google.com/document/d/1Gs3Hi1jrldGriVR-dZKklTssOj4GDKLoLcZajntHh8o/edit?usp=sharing).

> You can access the **Web App** repository [here](https://vshoes.vercel.app/).

> You can access the **Front End** repository [here](https://github.com/ardhanurfan/vshoes).

> You can access this project **Swagger Docs** [here](https://apivshoes.ardhanurfan.my.id/docs).

## Table of Contents

1. [General Information](#general-information)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Structure](#structure)
5. [Acknowledgements](#acknowledgements)
6. [Copyright](#copyright)

<a name="general-information">

## General Information

VShoes merupakan sebuah toko online berbasis website application yang memberikan layanan kepada pelanggan untuk melakukan personalisasi dan memilih produk sepatu melalui visual 3D. VShoes merupakan sebuah marketplace yang menjadi distributor berbagai merek sepatu. Nantinya pelanggan dapat melihat berbagai merek dan model sepatu dalam satu genggaman aplikasi.

Melalui layanan ini pengguna dapat memilih sepatu dan menyesuaikan dengan kebutuhan dan style dirinya. Dengan tampilan virtual reality diharapkan pengguna dapat dengan mudah menentukan jenis sepatu yang cocok dengan merasakan seperti melihat bentuk sepatu secara langsung.

Layanan ini terdapat tiga tabel yakni brands, shoes, dan varians yang memiliki keterkaitan satu sama lain. Terdapat tabel brands yang berisikan merek sepatu yang tersedia pada toko ini. Kemudian, setiap merek memiliki banyak jenis sepatu yang berbeda-beda. Dalam setiap sepatu juga terdapat beberapa warna model berbeda-beda yang dapat dipilih dan dilihat oleh pelanggan. Selain itu terdapat pula tabel untuk menyimpan pengguna aplikasi ini. Pengguna terbagi menjadi admin dan user yang dipisahkan pada atribut role. Setiap role tersebut dibatasi dengan fitur authorization yang telah diterapkan.

Untuk mendukung personalisasi dan membantu pengguna dalam melakukan pemilihan produk layanan ini diintegrasikan dengan layanan Sneakers Cleaner Consultation Service sehingga dapat memfasilitasi pengguna untuk memberikan rekomendasi dalam menjaga sepatu yang mereka miliki. Dengan demikian brand awareness terhadap VShoes

<a name="technologies-used"></a>

## Technologies Used

- Azure MySQL
- Azure Virtual Machine
- Python 3.12
- FastAPI
- Uvicorn
- mysql-connector-python
- requests
- python-dotenv
- etc
  > Note: The version of the libraries above is the version that we used in this project. You can use the latest version of the libraries.

<a name="installation">

## Installation

#### Instalation without Docker

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install VShoes.

```bash
pip install -r requirements.txt
```

Run the app using Uvicorn

```bash
uvicorn main:app
```

#### Instalation with Docker

First install [Docker](https://www.docker.com/) in your machine.

Let's make docker contaner using **docker-compose**

For Windows

```bash
docker compose up -d --build
```

or

For Ubuntu

Run the app using Uvicorn

```bash
docker-compose up -d --build
```

<a name="structure">

## Structure

```bash
├── .dockerignore
├── .env.example
├── .github
│  └── workflows
│    └── deploy.yaml
├── .gitignore
├── api
│  └── url.py
├── db
│  ├── connection.py
│  └── DigiCertGlobalRootCA.crt.pem
├── docker-compose.yaml
├── Dockerfile
├── main.py
├── middleware
│  └── jwt.py
├── models
│  ├── brand.py
│  ├── shoes.py
│  ├── token.py
│  ├── tokenData.py
│  ├── user.py
│  └── varian.py
├── new.tree
├── requirements.txt
└── routes
  ├── auth.py
  ├── brand.py
  ├── cleaner.py
  ├── shoes.py
  └── varian.py
```

<a name="acknowledgements">

## Acknowledgements

- Terima kasih kepada Tuhan Yang Maha Esa
- Bapak I Gusti Bagus Baskara Nugraha, S.T., M.T., Ph.D.
- Teman-teman kelas K02 Sistem dan Teknologi Informasi ITB

<a name="copyright"></a>

## Copyright

<h4 align="center">
  Copyrights @2023
</h4>

</hr>
