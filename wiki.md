# Short title

Build a Library Management System using CockroachDB

# Long title

Build a Library Management System using CockroachDB hosted on Red Hat Marketplace

# Author

* Manoj Jahgirdar <manoj.jahgirdar@in.ibm.com>
* Rahul Reddy Ravipally <raravi86@in.ibm.com>
* Srikanth Manne <srikanth.manne@in.ibm.com>

# URLs

### Github repo

* GitHub URL: <https://github.com/IBM/library-management-system-using-cockroachdb-hosted-on-rhm>

### Other URLs

<!-- * Video URL -->

# Summary

In this code pattern, we will build a Library Management System using CockroachDB hosted on Red Hat Marketplace. CockroachDB is an ultra resilient, distributed SQL that can easily scale-out serializable transactions for your apps and services. It is cloud-native, architected to simplify scale and also guarantee consistent transactions across multiple regions and multiple clouds.

# Technologies

* Databases
* Python

# Description

A Library Management System is a software that uses to maintain the record of the library. It contains work like the number of available books in the library, the number of books are issued or returning or renewing a book or late fine charge record, etc.

# Flow

![](doc/source/images/Architecture.png)

1. User performs an operation like `borrowing a book` or `returning a book`.
2. Application updates appropriate CockroachDB table accordingly.
3. Application fetches the updated data from the table.
4. Application displays the updated data that was feteched from the table. 

# Instructions

> Find the detailed steps for this pattern in the [readme file](https://github.com/IBM/library-management-system-using-cockroachdb-hosted-on-rhm/blob/master/README.md). The steps will show you how to:

1. Clone the repo
2. Setup CockroachDB Operator on OpenShift
3. Port Forward CockroachDB
4. Run the Application
5. Explore the Library Management System

# Components and services

* Red Hat OpenShift on IBM Cloud
* CockroachDB

# Runtimes

* python

# Related IBM Developer content

> List any IBM Developer resources that are closely related to this pattern, such as other patterns, blog posts, tutorials, etc..

* [Perform DML Operations with CockroachDB hosted on Red Hat Marketplace](https://github.com/IBM/dml-operations-cockroachdb-operator-rhm): In this tutorial, you will learn how to perform CRUD operations with CockroachDB hosted on Red Hat Marketplace using python runtime and Jupyter notebook.

* [Store and query unstructured JSON data from CockroachDB hosted on Red Hat Marketplace](https://github.com/IBM/store-and-query-unstructured-json-cockroachdb-operator-rhm): In this tutorial, you will learn how to get unstructured JSON data from an API, store it in CockroachDB hosted on Red Hat Marketplace, and query the unstructured JSON data from the table using python runtime and Jupyter notebook.

* [Perform CRUD operations using Crunchy PostgreSQL for Kubernetes Operator on Red Hat Marketplace](https://github.com/IBM/perform-crud-operations-using-crunchy-Postgresaql-for-kubernetes-operator-rhm): In this tutorial, you will learn how to Perform CRUD operations using Crunchy PostgreSQL for Kubernetes Operator hosted on Red Hat marketplace using python runtime and Jupyter notebook.


