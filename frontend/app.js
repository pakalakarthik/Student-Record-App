// Backend API endpoint URL for the /students route
const API_URL = "http://127.0.0.1:5000/students";

// ----------- Fetch and show all students -----------
// Async function that fetches all student records from the backend and displays them in the table
async function loadStudents() {
    // Make a GET request to the API and wait for the response
    const response = await fetch(API_URL);
    // Parse the JSON response into a JavaScript object/array
    const data = await response.json();

    // Get reference to the HTML table element by its id
    const table = document.getElementById("studentsTable");

    // Clear the table and reset it with only the header row
    table.innerHTML = `
        <tr>
            <th>ID</th><th>Name</th><th>Age</th><th>Grade</th><th>Email</th><th>Delete</th>
        </tr>
    `;

    // Loop through each student in the response data
    data.forEach(student => {
        // Build an HTML table row as a string with student data and a Delete button
        let row = `
            <tr>
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.age}</td>
                <td>${student.grade}</td>
                <td>${student.email}</td>
                <td><button onclick="deleteStudent(${student.id})">Delete</button></td>
            </tr>
        `;
        // Add the row to the table by appending to innerHTML
        table.innerHTML += row;
    });
}

// ----------- Add a new student -----------
// Async function called when user clicks the "Add" button
async function addStudent() {
    // Create an object with values from the form input fields
    const newStudent = {
        name: document.getElementById("name").value,
        age: document.getElementById("age").value,
        grade: document.getElementById("grade").value,
        email: document.getElementById("email").value
    };

    // Send a POST request to the API with the new student data
    await fetch(API_URL, {
        method: "POST",
        // Tell the server we're sending JSON
        headers: { "Content-Type": "application/json"},
        // Convert the object to a JSON string in the request body
        body: JSON.stringify(newStudent)
    });

    // Refresh the student list to show the newly added student
    loadStudents();
}

// ----------- Delete a student -----------
// Async function called when user clicks a Delete button; id is the student's database id
async function deleteStudent(id) {
    // Send a DELETE request to the API for this specific student id
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    // Refresh the list to reflect the deletion
    loadStudents();
}

// When the page loads, immediately fetch and display all students
loadStudents();
