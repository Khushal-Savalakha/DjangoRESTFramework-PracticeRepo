# DjangoRESTFramework-PracticeRepo ![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.12.4-green.svg) ![Python](https://img.shields.io/badge/Python-3.8.5-blue.svg) ![License](https://img.shields.io/github/license/Khushal-Savalakha/DjangoRESTFramework-PracticeRepo.svg)

This repository contains practical examples and implementations using **Django REST Framework (DRF)**. Each example focuses on different aspects of DRF, from basic serialization to advanced session management and JWT token integration.


## 📑 Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Learning Path](#learning-path)
- [Current Focus](#current-focus)
- [Future Scope](#future-scope)
- [Related Repositories](#related-repositories)

---

## 📜 Introduction

This repository is a collection of **practice projects** aimed at mastering **Django REST Framework (DRF)**. It covers essential concepts and provides real-world examples for:
- Serialization/Deserialization
- Function-Based Views (FBVs)
- Class-Based Views (CBVs)
- API Views
- Mixins
- Session Management
- JWT Token Integration

> **Note**:  
Before diving into Django REST Framework, it is essential to have a foundational understanding of **Django**. You can refer to my [Django-Practice-Projects](https://github.com/Khushal-Savalakha/Django-Practice-Projects) repository, where basic Django concepts are covered.

For those short on time, learning up to **gs12** (Class-Based API Views) in this repository will be sufficient to build basic-level projects. Check out my project [CineView-Secure-Movie-Booking](https://github.com/Khushal-Savalakha/CineView-Secure-Movie-Booking), which integrates technologies like:
- Payment integration
- Booking history
- Real-time booking updates  
Using **Tailwind CSS**, **React**, **Django REST Framework**, **Express.js**, and **Stripe** for payment processing.

---

## ⚙️ Prerequisites

Before diving into the code, ensure you have the following installed:

| Software | Version |
|----------|---------|
| Python   | 3.8.5   |
| Django   | 3.2     |
| DRF      | 3.12.4  |
| JWT      | djangorestframework-jwt |

---

## 🚀 Project Setup

Follow these steps to set up the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Khushal-Savalakha/DjangoRESTFramework-PracticeRepo.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd DjangoRESTFramework-PracticeRepo
   ```

3. **Make migrations**:
   ```bash
   python manage.py makemigrations
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

---

## 📚 Learning Path

Below is the structured learning path covered in this repository. Each topic is introduced step-by-step with detailed examples and commit references:

| Goal Statement  | Description |
|-----------------|-------------|
| **gs1**: Add serializers and serialization examples in DRF | Learn how to use serializers for converting complex data types into JSON. |
| **gs2**: Implement deserialization and data insertion in DRF | Understand deserialization and how to insert data into models. |
| **gs3**: Create CRUD API using function-based views | Create a full CRUD API with FBVs. |
| **gs4**: Add class-based views in DRF | Introduce CBVs for more structured and reusable code. |
| **gs9**: Implement basic function-based API view | Learn the basic API view using FBVs. |
| **gs10**: Implement CRUD operations with function-based API view (Part 1) | First part of CRUD operations using FBVs. |
| **gs11**: Implement CRUD operations with function-based API view (Part 2) | Continue CRUD operations with FBVs. |
| **gs12**: Add class-based APIView | Add CBVs to streamline API development. |
| **gs13**: Implement generic API views and mixins (Part 1) | Learn how to use generic API views and mixins for DRY code. |
| **gs14**: Implement generic API views and mixins (Part 2) | Merge common operations using mixins. |
| **gs15**: Add concrete view classes | Add concrete view classes for simplicity. |

---

## 🔍 Current Focus

- **Session Management**: Explore Django’s built-in session management to handle user data across requests.
- **JWT Token**: Implement authentication using JSON Web Tokens (JWT) for secure API communication.

---

## 🔮 Future Scope

The following topics will be covered in future updates:
- Complete CRUD API implementations
- Token-based authentication using JWT
- Advanced session management with Django

---

## 🔗 Related Repositories

- [Django-Practice-Projects](https://github.com/Khushal-Savalakha/Django-Practice-Projects): Contains basic Django projects that cover essential concepts and functionality.
- [Learning_Notes](https://github.com/Khushal-Savalakha/Learning_Notes): Detailed notes and explanations of Django REST Framework and Django concepts.
- [CineView-Secure-Movie-Booking](https://github.com/Khushal-Savalakha/CineView-Secure-Movie-Booking): Example of a project that integrates Django REST Framework with payment and real-time booking updates.
