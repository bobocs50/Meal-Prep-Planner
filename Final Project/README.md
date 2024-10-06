# YOUR PROJECT TITLE
#### Video Demo:  <URL https://youtu.be/20km7KWTtiY >
#### Description:


## Overview
- The Meal Prep Planner is a web application designed to simplify meal preparation and organization.
- It allows users to plan their meals for the week, scale recipes based on the number of servings, and generate a comprehensive grocery list.
- Whether you’re cooking for one or preparing meals for the entire family, this app provides an intuitive platform to help you streamline your cooking process.

## Features
- **Meal Input**: Easily input your favorite meals with their ingredients and instructions.
- **Recipe Scaling**: Adjust the number of servings for each recipe, and the app will automatically update ingredient quantities.
- **Grocery List Generation**: Automatically create a grocery list based on the meals you've selected for the week, ensuring you have all necessary ingredients.
- **User-Friendly Interface**: Built with Bootstrap for a clean and responsive design, making meal planning easy and accessible on any device.
- **Database Integration**: Utilizes SQLite for efficient data storage and retrieval, ensuring your meal plans and grocery lists are always at your fingertips.

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML, Bootstrap(CSS)
- **Version Control**: Git

## Getting Started
To get started with the Meal Prep Planner, follow these steps:
1. Clone the repository:
   ```bash
   git clone [repository_url]



TODO

**Page 1: Input Meals**

1. **Create a New Meal Form**:
    - Design a form where users can enter the meal name, number of servings, and ingredients.
    - Include fields for ingredient name, quantity, and unit.
    - Add functionality to dynamically add multiple ingredients to the list.
2. **Store Meal Data**:
    - When the form is submitted, capture the meal details and ingredient list.
    - Save this data in a database (e.g., SQLite) for later retrieval and processing.
- **Status:** To Do / In Progress / Done

**Page 2: Select and Scale Meals**

- **Description:** Enable users to select meals and specify portions.
- **Tasks:**
    - Fetch and display meals from the database.
    - Add checkboxes and input fields for portion scaling.
    - Handle form submission and send data to the server.
- **Status:** To Do / In Progress / Done

**Page 3: Scaled Recipes**

- **Description:** Show updated recipes with scaled ingredient quantities.
- **Tasks:**
    - Calculate scaled ingredient quantities based on user input.
    - Display scaled recipes in a user-friendly format.
- **Status:** To Do / In Progress / Done

**Page 4: Grocery List**

- **Description:** Generate and display a consolidated grocery list.
- **Tasks:**
    - Collect and consolidate scaled ingredients.
    - Display the grocery list with total quantities.
- **Status:** To Do / In Progress / Done
